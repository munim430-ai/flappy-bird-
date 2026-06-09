# GambleMap — Passive OSINT Network Mapper

> **Jurisdiction & purpose**: Built exclusively for submission to the Bangladesh CID Cyber Police Centre and investigative journalists. This tool maps networks of illegal online-gambling sites targeting Bangladeshi users.

---

## Strict Passive / Public-Records-Only Policy

**This tool NEVER:**
- Probes, port-scans, or actively fingerprints any target system
- Brute-forces, enumerates, or fuzzes any endpoint
- Logs into or authenticates against any target system
- Sends anything to a target's infrastructure beyond a **single ordinary HTTP GET of its public homepage** (identical to what any browser does)
- Stores or transmits personal data beyond what appears in public registries

**This tool ONLY reads:**
- Public WHOIS registries (via python-whois)
- Public Certificate Transparency logs (crt.sh JSON API)
- Public passive-DNS / DNS records (SecurityTrails API or plain DNS resolution)
- Public homepage HTML (one GET per domain, normal User-Agent)
- Public urlscan.io scan results (their API, no new scans initiated)

If a step would require touching a target in a way a browser wouldn't, the code refuses and explains why.

---

## Modules

| Module | Source | What it finds |
|---|---|---|
| `whois_lookup` | Public WHOIS registries | Registrar, dates, nameservers, registrant |
| `cert_transparency` | crt.sh JSON API | Subdomains, sibling domains via SAN/CN |
| `passive_dns` | SecurityTrails API / dnspython fallback | Hosting IPs, shared infrastructure |
| `tracker_extract` | Target homepage HTML (1 GET) | GA/GA4 IDs, AdSense IDs, Facebook Pixel IDs, platform strings |
| `urlscan_client` | urlscan.io public API | Existing screenshots, linked resources |
| `correlate` | All module outputs | Link chart; clusters domains sharing fingerprints |
| `report` | Correlation output | CSV + Markdown dossier for investigators |

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env — add your API keys (SecurityTrails, urlscan.io)
```

## Usage

```bash
# Run a single module against a seed list
python -m gamblemap.whois_lookup --input config/seed_domains.txt

# Run the full pipeline
python -m gamblemap.pipeline --input config/seed_domains.txt --output-dir output/
```

## Rate Limits & Caching

All external API calls enforce a **1–2 second inter-request delay**. Responses are cached in `cache/` as JSON files keyed by domain + module name, so re-runs never re-query already-seen data.

## Output

- `output/<run_id>/report.csv` — machine-readable dossier
- `output/<run_id>/report.md` — human-readable Markdown summary
- `cache/` — raw API responses per domain

---

## Legal & Ethics

Use of this tool is restricted to:
1. Passive collection of publicly available records
2. Submission to authorized law enforcement (Bangladesh CID Cyber Police Centre)
3. Publication by credentialed investigative journalists in the public interest

Do not use this tool to harass, extort, or target individuals. The maintainers accept no liability for misuse.
