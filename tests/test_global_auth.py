"""Offline tests; no real accounts, passwords, or network requests."""
import pytest
from mn2mc.nexus.global_auth import (
    Authenticator, GlobalAuthUnavailable, GlobalIdentity,
    InvalidPassword, TemporaryAuthFailure, login_with_retries,
)
from scripts.setup_global import ask_uid, ask_region, ask_mode
from scripts.install_paper import select_build

def test_unavailable_login_never_prompts():
    with pytest.raises(GlobalAuthUnavailable):
        login_with_retries(Authenticator(), 12345, "usz",
                           ask_password=lambda _: (_ for _ in ()).throw(AssertionError("prompted")))

def test_retry_explicit_bad_password_then_success():
    class Provider(Authenticator):
        available = True
        attempts = 0
        def login(self, uid, password, region):
            self.attempts += 1
            if password != "correct":
                raise InvalidPassword()
            return GlobalIdentity(uid, region)
    provider = Provider()
    passwords = iter(["wrong", "correct"])
    result = login_with_retries(provider, 12345, "usz",
                                ask_password=lambda _: next(passwords), notify=lambda _: None)
    assert result.uid == 12345
    assert provider.attempts == 2

def test_stops_after_three_password_failures():
    class Provider(Authenticator):
        available = True
        attempts = 0
        def login(self, uid, password, region):
            self.attempts += 1
            raise InvalidPassword()
    provider = Provider()
    with pytest.raises(InvalidPassword):
        login_with_retries(provider, 12345, "usz",
                           ask_password=lambda _: "bad", notify=lambda _: None)
    assert provider.attempts == 3

def test_transient_failure_is_not_bad_password():
    class Provider(Authenticator):
        available = True
        def login(self, uid, password, region):
            raise TemporaryAuthFailure("rate limited")
    with pytest.raises(TemporaryAuthFailure):
        login_with_retries(Provider(), 12345, "usz",
                           ask_password=lambda _: "somepass", notify=lambda _: None)

def test_interactive_validation_and_paper_stable():
    items = iter(["abc", "12345"])
    assert ask_uid(lambda _: next(items)) == 12345
    items = iter(["invalid", "hkz"])
    assert ask_region(lambda _: next(items)) == "hkz"
    assert ask_mode(lambda _: "y") == "both"
    assert ask_mode(lambda _: "") == "china"
    response = [{"channel": "STABLE", "downloads": {"server:default": {"url": "https://fill-data.papermc.io/test.jar"}}}]
    assert select_build(response)[0].endswith("test.jar")
    with pytest.raises(RuntimeError):
        select_build([])
