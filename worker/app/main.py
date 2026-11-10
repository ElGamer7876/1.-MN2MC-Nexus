"""Standalone MySQL-backed room status service (not a Mini World login proxy).

Public endpoint: GET /health, GET /regions, GET /rooms.
Admin endpoint: PUT /rooms/{region}/{room_id}; requires NEXUS_API_TOKEN.
No actual game-room creation occurs here.
"""
from __future__ import annotations

import asyncio
import hmac
import os
from contextlib import asynccontextmanager
from typing import Literal

import aiomysql
from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

REGION_CODES = frozenset(("overseas", "usz", "hkz", "jpz"))
INDEPENDENT_AREAS = ("russia", "brazil", "europe_except_spain")
CREATE_SCHEMA_NOTICE = "Apply worker/schema.sql before starting the API."

class RoomUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    account_alias: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.-]+$")
    players: int = Field(ge=0, le=40)
    capacity: int = Field(default=40, ge=1, le=40)
    status: Literal["open", "full", "offline"] = "open"

class RoomView(RoomUpdate):
    region: str
    room_id: str

def require_admin(authorization: str | None = Header(default=None)) -> None:
    token = os.environ.get("NEXUS_API_TOKEN", "")
    if not token or len(token) < 32:
        raise HTTPException(503, "Admin API disabled: configure a strong token")
    submitted = (authorization or "").removeprefix("Bearer ").strip()
    if not hmac.compare_digest(token, submitted):
        raise HTTPException(401, "Invalid bearer token")

def validate_region(region: str) -> str:
    region = region.lower()
    if region not in REGION_CODES:
        raise HTTPException(404, "Region is unsupported or not yet verified")
    return region

def get_pool(app: FastAPI):
    if app.state.pool is None:
        raise HTTPException(503, "Database not configured")
    return app.state.pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = None
    try:
        required = ("MYSQL_HOST", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD")
        if all(os.getenv(k) for k in required):
            app.state.pool = await aiomysql.create_pool(
                host=os.environ["MYSQL_HOST"],
                port=int(os.getenv("MYSQL_PORT", "3306")),
                db=os.environ["MYSQL_DATABASE"],
                user=os.environ["MYSQL_USER"],
                password=os.environ["MYSQL_PASSWORD"],
                autocommit=False,
                minsize=1,
                maxsize=3,
                connect_timeout=5,
                charset="utf8mb4",
            )
        yield
    finally:
        if app.state.pool is not None:
            app.state.pool.close()
            await app.state.pool.wait_closed()

app = FastAPI(
    title="MN2MC-Nexus Worker",
    description="Region-aware, authenticated room status API; no account login or actual game room creation",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/health")
async def health():
    return {"status": "ok", "database_configured": app.state.pool is not None}

@app.get("/regions")
async def regions():
    return {
        "candidates": ["overseas", "usz", "hkz", "jpz"],
        "independent_unverified": list(INDEPENDENT_AREAS),
        "note": "These regions are candidate configurations; routing/login is not validated.",
    }

@app.get("/rooms")
async def rooms(region: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=500)):
    if region is not None:
        region = validate_region(region)
    pool = get_pool(app)
    query = ("SELECT region, room_id, account_alias, players, capacity, status "
             "FROM rooms")
    params = []
    if region is not None:
        query += " WHERE region=%s"
        params.append(region)
    query += " ORDER BY region, room_id LIMIT %s"
    params.append(limit)
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query, tuple(params))
            return {"rooms": await cur.fetchall()}

@app.put("/rooms/{region}/{room_id}", dependencies=[Depends(require_admin)])
async def upsert_room(region: str, room_id: str, update: RoomUpdate):
    region = validate_region(region)
    if not 1 <= len(room_id) <= 128 or any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-" for c in room_id):
        raise HTTPException(422, "Invalid room ID")
    if update.players > update.capacity:
        raise HTTPException(422, "Players exceed capacity")
    if update.status == "full" and update.players != update.capacity:
        raise HTTPException(422, "Full status requires full occupancy")
    if update.status == "open" and update.players == update.capacity:
        raise HTTPException(422, "Full room must have status full")
    pool = get_pool(app)
    async with pool.acquire() as conn:
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO rooms (region, room_id, account_alias, players, capacity, status) "
                    "VALUES (%s,%s,%s,%s,%s,%s) "
                    "ON DUPLICATE KEY UPDATE account_alias=VALUES(account_alias), "
                    "players=VALUES(players), capacity=VALUES(capacity), status=VALUES(status)",
                    (region, room_id, update.account_alias, update.players, update.capacity, update.status),
                )
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise
    return {"region": region, "room_id": room_id, **update.model_dump()}
