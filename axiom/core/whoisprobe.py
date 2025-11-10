from typing import Dict, Any
try:
    import whois as _whois
except Exception:
    _whois = None

def whois_lookup(name: str) -> Dict[str, Any]:
    if _whois is None:
        return {'error': 'python-whois not installed; whois lookup unavailable'}
    try:
        w = _whois.whois(name)
        return {
            'domain_name': str(w.domain_name) if getattr(w,'domain_name',None) else None,
            'registrar': getattr(w,'registrar',None),
            'creation_date': str(getattr(w,'creation_date',None)),
            'expiration_date': str(getattr(w,'expiration_date',None)),
            'name_servers': w.name_servers if isinstance(w.name_servers, list) else [w.name_servers] if w.name_servers else [],
            'emails': w.emails if isinstance(w.emails, list) else [w.emails] if w.emails else []
        }
    except Exception as e:
        return {'error': str(e)}
