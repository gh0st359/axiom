# Axiom v2.0 — Professional Infrastructure Intelligence Tool

Sleek CLI like nmap. No paid APIs. Built for speed and insight.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e .
```

## Usage

```bash
axiom -t example.com
axiom -t 1.1.1.1 -p 22,80,443 -T 200
axiom -f targets.txt --no-subdomains
```

Reports are stored under ./reports/
