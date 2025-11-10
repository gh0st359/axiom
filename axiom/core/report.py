import os
from datetime import datetime
from typing import Dict, Any, List

def write_text_report(target: str, data: Dict[str, Any], out_dir: str = 'reports') -> str:
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    safe = target.replace('/', '_').replace(':','_')
    path = os.path.join(out_dir, f"{safe}_{ts}.txt")
    lines: List[str] = []
    lines.append('AXIOM-PRO REPORT')
    lines.append(f"Target: {target}")
    lines.append(f"Generated: {datetime.utcnow().isoformat()} UTC")
    lines.append('='*60)
    # DNS
    lines.append('\n[DNS]')
    dns = data.get('dns', {})
    for k,v in dns.items():
        if v:
            lines.append(f"{k}: {', '.join(v)}")
    # WHOIS
    lines.append('\n[WHOIS]')
    who = data.get('whois', {})
    if who.get('error'):
        lines.append('WHOIS error: ' + who.get('error'))
    else:
        for k in ('domain_name','registrar','creation_date','expiration_date'):
            if who.get(k):
                lines.append(f"{k}: {who.get(k)}")
    # Subdomains
    lines.append('\n[SUBDOMAINS]')
    subs = data.get('subdomains', [])
    if subs:
        for s in subs:
            lines.append('- ' + s)
    else:
        lines.append('None (fast wordlist)')
    # Ports
    lines.append('\n[PORTS]')
    ports = data.get('ports', [])
    if ports:
        lines.append(f"{'PORT':<8}{'STATE':<8}BANNER")
        lines.append('-'*60)
        for p in sorted(ports, key=lambda x: x['port']):
            lines.append(f"{p['port']:<8}{p['state']:<8}{(p.get('banner') or '')[:120]}")
    else:
        lines.append('No open ports found')
    # HTTP
    lines.append('\n[HTTP]')
    http = data.get('http', {})
    if http.get('error'):
        lines.append('HTTP probe error: ' + http.get('error'))
    else:
        if http.get('status') is not None:
            lines.append(f"Status: {http.get('status')} {http.get('reason')}")
            for k in ('server','x-powered-by','content-type','strict-transport-security','content-security-policy','x-frame-options'):
                if k in http.get('headers',{}):
                    lines.append(f"  {k}: {http['headers'][k]}")
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    return path
