"""One already-authorized account per room, 40 players maximum.

A separate audited provider must be supplied for actual room creation.
"""
import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from mn2mc.nexus.regions import REGIONS, Region

@dataclass
class Room:
    region: str
    account_alias: str
    room_id: str
    players: int = 0
    capacity: int = 40

RoomCreator = Callable[[Region, str, int], Awaitable[str]]

class RoomPool:
    def __init__(
        self,
        accounts: dict[str, list[str]],
        *,
        capacity: int = 40,
        auto_expand: bool = False,
        create_room: RoomCreator | None = None,
    ) -> None:
        if type(capacity) is not int or not 1 <= capacity <= 40:
            raise ValueError("Capacity must be 1..40")
        if any(region not in REGIONS for region in accounts):
            raise ValueError("Unknown/independent region requires verified integration")
        for aliases in accounts.values():
            if any(not isinstance(alias, str) or not alias.strip() for alias in aliases):
                raise ValueError("Account aliases must not be empty")
            if len(aliases) != len(set(aliases)):
                raise ValueError("Duplicate account in region")
        self.accounts = {region: tuple(aliases) for region, aliases in accounts.items()}
        self.capacity = capacity
        self.auto_expand = auto_expand
        self.create_room = create_room
        self.rooms: dict[str, Room] = {}
        self._locks = {region: asyncio.Lock() for region in accounts}

    def attach_room(self, region: str, account_alias: str, room_id: str, players: int = 0) -> Room:
        if region not in self.accounts or account_alias not in self.accounts[region]:
            raise ValueError("No account in selected region")
        if not room_id or room_id in self.rooms:
            raise ValueError("Room ID missing or in use")
        if any(r.region == region and r.account_alias == account_alias for r in self.rooms.values()):
            raise ValueError("An account can host only one room per region")
        if type(players) is not int or not 0 <= players <= self.capacity:
            raise ValueError("Invalid occupancy")
        room = Room(region, account_alias, room_id, players, self.capacity)
        self.rooms[room_id] = room
        return room

    def max_rooms(self, region: str) -> int:
        return len(self.accounts[region])

    def max_capacity(self, region: str) -> int:
        return self.max_rooms(region) * self.capacity

    async def update_occupancy(self, room_id: str, players: int) -> Room | None:
        if type(players) is not int or not 0 <= players <= self.capacity:
            raise ValueError("Invalid occupancy")
        room = self.rooms[room_id]
        async with self._locks[room.region]:
            room.players = players
            if players < room.capacity or not self.auto_expand or self.create_room is None:
                return None
            used = {r.account_alias for r in self.rooms.values() if r.region == room.region}
            next_alias = next((a for a in self.accounts[room.region] if a not in used), None)
            if next_alias is None:
                return None
            new_id = await self.create_room(REGIONS[room.region], next_alias, self.capacity)
            if not isinstance(new_id, str) or not new_id.strip():
                raise ValueError("Room creator did not supply a room ID")
            return self.attach_room(room.region, next_alias, new_id)
