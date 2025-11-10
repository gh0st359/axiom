from typing import Dict, Any, Iterable, List, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

from .dnsprobe import resolve_dns
from .whoisprobe import whois_lookup
from .ports import scan_port
from .http_probe import http_headers
from .subdomains import brute_subdomains

def _is_ip(host: str) -> bool:
    try:
        socket.inet_aton(host)
        return True
    except Exception:
        pass
    try:
        socket.inet_pton(socket.AF_INET6, host)
        return True
    except Exception:
        return False

def scan_target(target: str, ports: Iterable[int], threads: int = 100, timeout: float = 1.0, include_subdomains: bool = True) -> Dict[str, Any]:
    result: Dict[str, Any] = {'target': target}
    # DNS
    result['dns'] = resolve_dns(target)
    # WHOIS
    if not _is_ip(target):
        result['whois'] = whois_lookup(target)
    else:
        result['whois'] = {'error': 'WHOIS skipped for IP'}
    # Subdomains
    if include_subdomains and not _is_ip(target):
        result['subdomains'] = brute_subdomains(target, max_workers=min(threads,50))
    else:
        result['subdomains'] = []
    # Ports
    result['ports'] = []
    with ThreadPoolExecutor(max_workers=min(threads,200)) as ex:
        futures = {ex.submit(scan_port, target, p, timeout): p for p in ports}
        for fut in as_completed(futures):
            data = fut.result()
            if data:
                result['ports'].append(data)
    # HTTP probe (try https then http if https fails)
    if not _is_ip(target):
        http = http_headers(target, use_https=True, timeout=2.0)
        if http.get('error'):
            http = http_headers(target, use_https=False, timeout=2.0)
        result['http'] = http
    else:
        result['http'] = http_headers(target, use_https=True, timeout=2.0)
    return result
