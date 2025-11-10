from typing import Set
def parse_ports(spec: str) -> Set[int]:
    ports = set()
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a,b = part.split('-',1)
            ports.update(range(int(a), int(b)+1))
        else:
            ports.add(int(part))
    return {p for p in ports if 1 <= p <= 65535}

TOP_100_PORTS = [80,443,22,21,25,110,143,53,123,3306,1433,3389,8080,8443,6379,27017,5432,5900,8000,5000,9200,27015,2375,2376]
