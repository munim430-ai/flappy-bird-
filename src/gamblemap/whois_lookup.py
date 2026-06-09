"""
Module 1 — whois_lookup

Queries public WHOIS registries for a domain and returns a structured dict.
Uses python-whois. No contact with the target domain's infrastructure.
"""

import time
import json
import argparse
from pathlib import Path
from datetime import datetime, date

import whois

from .cache import load, save

RATE_DELAY = 1.5  # seconds between WHOIS queries


def _normalise_dates(val):
    """Flatten lists and serialise date/datetime objects to ISO strings."""
    if isinstance(val, list):
        val = val[0] if val else None
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    return val


def lookup(domain: str) -> dict:
    """
    Return WHOIS data for *domain*.

    Fields returned (all may be None if privacy-masked or unavailable):
      registrar, creation_date, expiry_date, updated_date,
      nameservers, registrant_name, registrant_org,
      registrant_country, registrant_email, status, raw_text
    """
    cached = load("whois", domain)
    if cached is not None:
        return cached

    try:
        w = whois.whois(domain)
    except Exception as exc:
        result = {"domain": domain, "error": str(exc)}
        save("whois", domain, result)
        return result

    nameservers = w.name_servers
    if isinstance(nameservers, list):
        nameservers = sorted({ns.lower().rstrip(".") for ns in nameservers if ns})
    elif isinstance(nameservers, str):
        nameservers = [nameservers.lower().rstrip(".")]
    else:
        nameservers = []

    result = {
        "domain": domain,
        "registrar": w.registrar,
        "creation_date": _normalise_dates(w.creation_date),
        "expiry_date": _normalise_dates(w.expiration_date),
        "updated_date": _normalise_dates(w.updated_date),
        "nameservers": nameservers,
        "registrant_name": w.get("name"),
        "registrant_org": w.org,
        "registrant_country": w.country,
        "registrant_email": w.get("emails"),
        "status": (
            w.status if isinstance(w.status, list) else
            [w.status] if w.status else []
        ),
        "raw_text": w.text,
    }

    save("whois", domain, result)
    return result


def _print_result(r: dict) -> None:
    raw = r.pop("raw_text", None)
    print(json.dumps(r, indent=2, default=str))
    r["raw_text"] = raw  # restore for callers


def run_file(path: str) -> list[dict]:
    results = []
    domains = [
        line.strip()
        for line in Path(path).read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    for i, domain in enumerate(domains):
        print(f"[whois] {domain} ({i+1}/{len(domains)})")
        r = lookup(domain)
        _print_result(r)
        results.append(r)
        if i < len(domains) - 1:
            time.sleep(RATE_DELAY)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Module 1: passive WHOIS lookup (public registries only)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--domain", help="Single domain to look up")
    group.add_argument("--input", help="Path to a file with one domain per line")
    parser.add_argument(
        "--output", help="Write results as JSON to this file (optional)"
    )
    args = parser.parse_args()

    if args.domain:
        results = [lookup(args.domain)]
        for r in results:
            _print_result(r)
    else:
        results = run_file(args.input)

    if args.output:
        Path(args.output).write_text(
            json.dumps(results, indent=2, default=str)
        )
        print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()
