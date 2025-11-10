# Axiom-Pro (Fixed) Architecture

- CLI entrypoint: `python3 -m axiom_pro scan --target example.com`
- scanner orchestrates: DNS -> WHOIS -> Subdomains -> Ports (threaded) -> HTTP probe
- report writer: plain text files in ./reports/
- Robust fallbacks included so missing optional libs don't crash the app
