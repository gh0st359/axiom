from typing import Dict, List
import socket
def _socket_resolve(name:str) -> Dict[str,List[str]]:
    out = {'A':[], 'AAAA':[], 'MX':[], 'NS':[], 'TXT':[], 'CNAME':[]}
    try:
        infos = socket.getaddrinfo(name, None)
        for fam,_,_,_,sock in infos:
            ip = sock[0]
            if ':' in ip:
                out['AAAA'].append(ip)
            else:
                out['A'].append(ip)
    except Exception:
        pass
    return out

try:
    import dns.resolver
    def resolve_dns(name: str) -> Dict[str, List[str]]:
        r = dns.resolver.Resolver()
        r.timeout = 2.0
        r.lifetime = 2.5
        res = {}
        for t in ('A','AAAA','MX','NS','TXT','CNAME'):
            try:
                ans = r.resolve(name, t, raise_on_no_answer=False)
                res[t] = [a.to_text() for a in ans] if getattr(ans, 'rrset', None) else []
            except Exception:
                res[t] = []
        return res
except Exception:
    # fallback implementation using socket only for A/AAAA
    def resolve_dns(name: str) -> Dict[str, List[str]]:
        return _socket_resolve(name)
