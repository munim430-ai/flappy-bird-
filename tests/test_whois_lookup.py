"""Tests for whois_lookup — use a well-known domain so the test is deterministic."""

import sys
import types
from pathlib import Path

# Allow imports from src/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def _make_mock_whois(monkeypatch):
    """Replace whois.whois with a stub that returns predictable data."""
    from gamblemap import whois_lookup

    class FakeWhois:
        registrar = "Test Registrar, Inc."
        creation_date = None
        expiration_date = None
        updated_date = None
        name_servers = ["ns1.example.com", "ns2.example.com"]
        org = "Example Org"
        country = "BD"
        text = "raw whois text"
        status = ["clientTransferProhibited"]

        def get(self, key):
            return {"name": "John Doe", "emails": "admin@example.com"}.get(key)

    monkeypatch.setattr(whois_lookup.whois, "whois", lambda domain: FakeWhois())
    return whois_lookup


def test_lookup_returns_expected_fields(monkeypatch, tmp_path):
    # Point cache at a temp dir so tests don't pollute real cache
    import gamblemap.cache as cache_mod
    cache_mod._CACHE_ROOT = tmp_path / "cache"

    wl = _make_mock_whois(monkeypatch)
    result = wl.lookup("example.com")

    assert result["domain"] == "example.com"
    assert result["registrar"] == "Test Registrar, Inc."
    assert "ns1.example.com" in result["nameservers"]
    assert result["registrant_org"] == "Example Org"
    assert result["registrant_country"] == "BD"
    assert isinstance(result["status"], list)
    assert "error" not in result


def test_lookup_handles_whois_exception(monkeypatch, tmp_path):
    import gamblemap.cache as cache_mod
    import gamblemap.whois_lookup as wl

    cache_mod._CACHE_ROOT = tmp_path / "cache"
    monkeypatch.setattr(wl.whois, "whois", lambda d: (_ for _ in ()).throw(
        Exception("WHOIS server unavailable")
    ))

    result = wl.lookup("broken-domain.test")
    assert "error" in result
    assert result["domain"] == "broken-domain.test"


def test_cache_prevents_second_call(monkeypatch, tmp_path):
    import gamblemap.cache as cache_mod
    import gamblemap.whois_lookup as wl

    cache_mod._CACHE_ROOT = tmp_path / "cache"
    call_count = {"n": 0}

    class FakeWhois:
        registrar = "Cached Registrar"
        creation_date = expiration_date = updated_date = None
        name_servers = []
        org = country = text = None
        status = []

        def get(self, key):
            return None

    def counting_whois(domain):
        call_count["n"] += 1
        return FakeWhois()

    monkeypatch.setattr(wl.whois, "whois", counting_whois)

    wl.lookup("cached-domain.com")
    wl.lookup("cached-domain.com")  # should hit cache

    assert call_count["n"] == 1
