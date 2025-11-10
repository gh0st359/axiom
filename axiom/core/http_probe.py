from typing import Dict
import http.client, ssl

def http_headers(host: str, use_https: bool = True, timeout: float = 2.0) -> Dict:
    conn = None
    try:
        if use_https:
            ctx = ssl.create_default_context()
            conn = http.client.HTTPSConnection(host, 443, timeout=timeout, context=ctx)
        else:
            conn = http.client.HTTPConnection(host, 80, timeout=timeout)
        conn.request('GET', '/', headers={'Host': host, 'User-Agent': 'axiom-pro/0.1'})
        resp = conn.getresponse()
        headers = {k.lower(): v for k,v in resp.getheaders()}
        sample = resp.read(512).decode(errors='ignore')
        return {'status': resp.status, 'reason': resp.reason, 'headers': headers, 'body_sample': sample}
    except Exception as e:
        return {'error': str(e)}
    finally:
        try:
            if conn: conn.close()
        except Exception:
            pass
