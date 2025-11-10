# Axiom v2.0 — Professional Infrastructure Intelligence Tool

Most reconnaissance tools collect surface-level data — ports, hosts, and subdomains — but rarely organize it into meaningful intelligence. Axiom is built to change that. While it currently performs familiar discovery and enrichment tasks, its architecture is designed for deeper contextual analysis and scalable, local-first intelligence generation. It structures findings into linked entities, preparing them for correlation, automation, and analyst-driven exploration. The goal: to move from raw scan output to operational understanding — privately, efficiently, and without external dependencies.

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

# Example Output
```bash
[INFO] Scanning example.com
[INFO] Starting reconnaissance for example.com
[DNS] 6 record(s) found
[WHOIS] RESERVED-Internet Assigned Numbers Authority (N/A)
[INFO] Discovering subdomains...
[+] 1 subdomain(s) found
[INFO] Scanning ports...
[+] Port 443 open (unknown)
[+] Port 80 open (unknown)
[+] Port 53 open (unknown)
[INFO] Probing HTTP/HTTPS...
[INFO] Recon complete for example.com in 12.61s

[INFO] Report: reports/example.com_1234.txt
```

Reports are stored under ./reports/
