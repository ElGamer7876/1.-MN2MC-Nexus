"""Global 1.7.15 authentication extension point; fails closed by default.

No verified Global password endpoint exists in project documentation.
Never send passwords to guessed or Chinese account servers.
"""
from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from getpass import getpass

class GlobalAuthUnavailable(RuntimeError):
    pass

class InvalidPassword(Exception):
    pass

class TemporaryAuthFailure(Exception):
    pass

@dataclass(frozen=True)
class GlobalIdentity:
    uid: int
    region: str

class Authenticator:
    available = False

    def login(self, uid: int, password: str, region: str) -> GlobalIdentity:
        raise GlobalAuthUnavailable("Global 1.7.15 password login is not implemented.")

def login_with_retries(authenticator: Authenticator, uid: int, region: str, *,
                       ask_password: Callable[[str], str] = getpass,
                       notify: Callable[[str], None] = print,
                       max_attempts: int = 3) -> GlobalIdentity:
    """Retry only server-confirmed wrong passwords; stop on rate limits."""
    if not authenticator.available:
        raise GlobalAuthUnavailable("No verified Global login provider. Password NOT requested.")
    if type(uid) is not int or uid <= 0:
        raise ValueError("Invalid UID")
    if region not in {"overseas", "usz", "hkz", "jpz"}:
        raise ValueError("Unknown region")
    if not 1 <= max_attempts <= 5:
        raise ValueError("Invalid maximum attempts")
    for attempt in range(1, max_attempts + 1):
        password = ask_password(f"Global password ({attempt}/{max_attempts}): ")
        if not password:
            notify("Empty password, retry.")
            continue
        try:
            result = authenticator.login(uid, password, region)
        except InvalidPassword:
            notify("Incorrect password; retry." if attempt < max_attempts else "Attempts exhausted.")
            continue
        finally:
            password = ""  # Python strings cannot be reliably zeroed.
        if not isinstance(result, GlobalIdentity) or (result.uid, result.region) != (uid, region):
            raise GlobalAuthUnavailable("Authentication result mismatch")
        return result
    raise InvalidPassword("No successful login after the bounded retry limit")
