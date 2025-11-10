from typing import Optional, Dict
import socket, ssl

def scan_port(host: str, port: int, timeout: float = 1.0) -> Optional[Dict]:
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            banner = ''
            if port in (443,8443,9443):
                try:
                    ctx = ssl.create_default_context()
                    with ctx.wrap_socket(s, server_hostname=host) as tls:
                        cert = tls.getpeercert()
                        banner = f"TLS {tls.version()} | subject={cert.get('subject') if cert else ''}"
                except Exception:
                    banner = 'TLS handshake failed'
            else:
                try:
                    s.sendall(b"\r\n")
                    data = s.recv(512)
                    banner = data.decode(errors='ignore').strip()
                except Exception:
                    banner = ''
            return {'port': port, 'state': 'open', 'banner': banner}
    except Exception:
        return None
