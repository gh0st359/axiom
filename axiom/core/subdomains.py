from typing import List
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON = ["www","mail","api","dev","staging","admin","test","portal","git","vpn","m","shop","cdn","assets","static","status"]

def _check(hostname: str) -> bool:
    try:
        socket.getaddrinfo(hostname, None)
        return True
    except Exception:
        return False

def brute_subdomains(domain: str, max_workers: int = 40) -> List[str]:
    candidates = [f"{s}.{domain}" for s in COMMON]
    found = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_check, c): c for c in candidates}
        for fut in as_completed(futures):
            c = futures[fut]
            try:
                if fut.result():
                    found.append(c)
            except Exception:
                pass
    return sorted(found)
