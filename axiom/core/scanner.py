
from typing import Dict, Any, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
from colorama import Fore, Style
import time

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


def scan_target(
    target: str,
    ports: Iterable[int],
    threads: int = 100,
    timeout: float = 1.0,
    include_subdomains: bool = True,
    silent: bool = False,
) -> Dict[str, Any]:
    """
    Perform infrastructure intelligence gathering on a target.
    Outputs findings in real time unless 'silent=True'.
    """
    result: Dict[str, Any] = {"target": target}
    if not silent:
        print(Fore.CYAN + f"[INFO] Starting reconnaissance for {target}" + Style.RESET_ALL)
        start = time.time()

    # DNS
    try:
        dns_info = resolve_dns(target)
        result["dns"] = dns_info
        if not silent:
            print(Fore.BLUE + f"[DNS] {len(dns_info)} record(s) found" + Style.RESET_ALL)
    except Exception as e:
        result["dns"] = {"error": str(e)}
        if not silent:
            print(Fore.YELLOW + f"[WARN] DNS lookup failed: {e}" + Style.RESET_ALL)

    # WHOIS
    if not _is_ip(target):
        try:
            whois_info = whois_lookup(target)
            result["whois"] = whois_info
            if not silent:
                org = whois_info.get("org") or whois_info.get("registrar") or "Unknown"
                country = whois_info.get("country") or "N/A"
                print(Fore.MAGENTA + f"[WHOIS] {org} ({country})" + Style.RESET_ALL)
        except Exception as e:
            result["whois"] = {"error": str(e)}
            if not silent:
                print(Fore.YELLOW + f"[WARN] WHOIS lookup failed: {e}" + Style.RESET_ALL)
    else:
        result["whois"] = {"info": "WHOIS skipped for IP"}

    # Subdomains
    result["subdomains"] = []
    if include_subdomains and not _is_ip(target):
        if not silent:
            print(Fore.CYAN + "[INFO] Discovering subdomains..." + Style.RESET_ALL)
        try:
            subs = brute_subdomains(target, max_workers=min(threads, 50))
            result["subdomains"] = subs
            if not silent:
                print(Fore.GREEN + f"[+] {len(subs)} subdomain(s) found" + Style.RESET_ALL)
        except Exception as e:
            if not silent:
                print(Fore.YELLOW + f"[WARN] Subdomain discovery failed: {e}" + Style.RESET_ALL)
            result["subdomains"] = {"error": str(e)}

    # Ports
    result["ports"] = []
    if not silent:
        print(Fore.CYAN + "[INFO] Scanning ports..." + Style.RESET_ALL)
    with ThreadPoolExecutor(max_workers=min(threads, 200)) as ex:
        futures = {ex.submit(scan_port, target, p, timeout): p for p in ports}
        total = len(futures)
        completed = 0
        for fut in as_completed(futures):
            data = fut.result()
            completed += 1
            if data:
                result["ports"].append(data)
                if not silent:
                    print(Fore.GREEN + f"[+] Port {data['port']} open ({data.get('service', 'unknown')})" + Style.RESET_ALL)
            else:
                if not silent and completed % 25 == 0:
                    print(Fore.LIGHTBLACK_EX + f"[...]{completed}/{total} ports scanned" + Style.RESET_ALL)

    # HTTP probe
    if not silent:
        print(Fore.CYAN + "[INFO] Probing HTTP/HTTPS..." + Style.RESET_ALL)
    try:
        http = http_headers(target, use_https=True, timeout=2.0)
        if http.get("error"):
            http = http_headers(target, use_https=False, timeout=2.0)
        result["http"] = http
        if not silent:
            if http.get("server"):
                print(Fore.BLUE + f"[HTTP] Server: {http['server']}" + Style.RESET_ALL)
            elif http.get("error"):
                print(Fore.YELLOW + f"[WARN] HTTP probe failed: {http['error']}" + Style.RESET_ALL)
    except Exception as e:
        result["http"] = {"error": str(e)}
        if not silent:
            print(Fore.YELLOW + f"[WARN] HTTP probe error: {e}" + Style.RESET_ALL)

    # Wrap-up
    if not silent:
        elapsed = time.time() - start
        print(Fore.CYAN + f"[INFO] Recon complete for {target} in {elapsed:.2f}s" + Style.RESET_ALL)
        print(Style.RESET_ALL)

    return result
