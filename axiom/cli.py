import argparse, sys
from typing import Set
from .core.scanner import scan_target
from .core.report import write_text_report
from .utils.common import parse_ports, TOP_100_PORTS
from .utils.logger import get_logger

BANNER = """
╔═══════════════════════════════════════════════════════╗
║  AXIOM — Infrastructure Intelligence CLI v2.0         ║
║  Sleek. Local-first. No paid APIs.                    ║
╚═══════════════════════════════════════════════════════╝
"""

def resolve_ports(spec: str) -> Set[int]:
    if spec.lower() in ('top', 'top100'):
        return set(TOP_100_PORTS)
    return parse_ports(spec)

def main(argv=None):
    parser = argparse.ArgumentParser(prog='axiom', description='Axiom CLI — Professional Infrastructure Intelligence Tool')
    parser.add_argument('-t', '--target', help='Domain or IP target')
    parser.add_argument('-p', '--ports', default='top100', help='Ports (80,443,22-25 or top100)')
    parser.add_argument('-T', '--threads', type=int, default=100, help='Thread count')
    parser.add_argument('--timeout', type=float, default=1.0, help='Connection timeout')
    parser.add_argument('--no-subdomains', action='store_true', help='Disable subdomain scan')
    parser.add_argument('-f', '--file', help='Scan multiple targets from file')
    args = parser.parse_args(argv)
    logger = get_logger()
    print(BANNER)

    ports = resolve_ports(args.ports)

    targets = []
    if args.file:
        try:
            with open(args.file) as fh:
                targets = [x.strip() for x in fh if x.strip()]
        except Exception as e:
            logger.error('File read error: %s', e)
            sys.exit(1)
    elif args.target:
        targets = [args.target]
    else:
        parser.print_help()
        sys.exit(0)

    for t in targets:
        logger.info('Scanning %s', t)
        res = scan_target(t, ports=ports, threads=args.threads, timeout=args.timeout, include_subdomains=not args.no_subdomains)
        report_path = write_text_report(t, res, out_dir='reports')
        logger.info('Report: %s', report_path)

if __name__ == '__main__':
    main()
