#!/usr/bin/env python3
"""
Port Scanner - Educational Network Security Tool

This tool demonstrates basic network scanning concepts for learning
about network security and understanding how port scanning works.

EDUCATIONAL PURPOSE ONLY - Only scan hosts you own or have permission to test.
Author: Educational Security Project
"""

import socket
import argparse
import sys
import concurrent.futures
import time
from typing import List, Tuple, Optional
from datetime import datetime

# ==============================================================================
# Configuration
# ==============================================================================

# Common port definitions for educational reference
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}

# Well-known port ranges
PORT_RANGES = {
    "well-known": (1, 1023),
    "registered": (1024, 49151),
    "dynamic": (49152, 65535),
}


# ==============================================================================
# Port Scanning Functions
# ==============================================================================

def scan_port(host: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str]:
    """
    Scan a single port on a host.

    Args:
        host: Target hostname or IP address
        port: Port number to scan
        timeout: Connection timeout in seconds

    Returns:
        Tuple of (port, is_open, service_name)
    """
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Attempt connection
        result = sock.connect_ex((host, port))

        sock.close()

        # Result 0 means connection successful (port is open)
        is_open = result == 0

        # Get service name
        service = COMMON_PORTS.get(port, "Unknown")

        return (port, is_open, service)

    except socket.timeout:
        return (port, False, COMMON_PORTS.get(port, "Unknown"))
    except socket.gaierror:
        raise ValueError(f"Could not resolve hostname: {host}")
    except Exception:
        return (port, False, COMMON_PORTS.get(port, "Unknown"))


def scan_ports_tcp(
    host: str,
    ports: List[int],
    timeout: float = 1.0,
    max_workers: int = 50
) -> List[Tuple[int, bool, str]]:
    """
    Scan multiple ports using TCP connections.

    Args:
        host: Target hostname or IP address
        ports: List of port numbers to scan
        timeout: Connection timeout per port
        max_workers: Maximum concurrent connections

    Returns:
        List of (port, is_open, service) tuples
    """
    results = []

    print(f"[*] Scanning {host} for {len(ports)} ports...")

    # Use ThreadPoolExecutor for concurrent scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all scan tasks
        future_to_port = {
            executor.submit(scan_port, host, port, timeout): port
            for port in ports
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_port):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"[!] Error scanning port: {e}")

    return results


def generate_port_list(
    start: Optional[int] = None,
    end: Optional[int] = None,
    scan_common: bool = True,
    scan_all: bool = False
) -> List[int]:
    """
    Generate a list of ports to scan.

    Args:
        start: Start port (inclusive)
        end: End port (inclusive)
        scan_common: Include common ports
        scan_all: Scan all ports (1-65535)

    Returns:
        Sorted list of unique port numbers
    """
    ports = set()

    if scan_all:
        # Full port range
        ports.update(range(1, 65536))
    else:
        if scan_common:
            # Add well-known common ports
            ports.update(COMMON_PORTS.keys())

        if start is not None and end is not None:
            # Add specified range
            ports.update(range(start, end + 1))

    return sorted(list(ports))


def resolve_host(host: str) -> str:
    """
    Resolve hostname to IP address.

    Args:
        host: Hostname or IP address

    Returns:
        IP address string
    """
    try:
        # Check if it's already an IP
        socket.inet_aton(host)
        return host
    except socket.error:
        pass

    # Resolve hostname
    try:
        ip = socket.gethostbyname(host)
        print(f"[*] Resolved {host} to {ip}")
        return ip
    except socket.gaierror as e:
        raise ValueError(f"Could not resolve {host}: {e}")


# ==============================================================================
# Network Discovery
# ==============================================================================

def discover_local_network() -> List[str]:
    """
    Discover devices on the local network (basic implementation).

    This is a simplified educational example. Real network discovery
    uses protocols like ARP, mDNS, SSDP, etc.

    Returns:
        List of local IP addresses
    """
    devices = []

    try:
        # Get local hostname and IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print(f"[*] Local hostname: {hostname}")
        print(f"[*] Local IP: {local_ip}")

        # Extract network prefix (last octet set to 0)
        parts = local_ip.split('.')
        if len(parts) == 4:
            network_prefix = '.'.join(parts[:3])
            print(f"[*] Network prefix: {network_prefix}.0/24")

            # Quick scan common ports on potential devices
            print(f"[*] Scanning local network for active hosts...")

            for i in range(1, 255):
                ip = f"{network_prefix}.{i}"
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    if sock.connect_ex((ip, 80)) == 0:
                        devices.append(ip)
                        print(f"    [+] Found device: {ip}")
                    sock.close()
                except:
                    pass

    except Exception as e:
        print(f"[!] Error discovering network: {e}")

    return devices


def scan_localhost() -> List[Tuple[int, bool, str]]:
    """
    Quick scan of common ports on localhost.

    Returns:
        List of open ports on localhost
    """
    print("[*] Scanning localhost (127.0.0.1)...")
    print("[*] This shows which services are running on YOUR machine")

    return scan_ports_tcp("127.0.0.1", list(COMMON_PORTS.keys()))


# ==============================================================================
# Output Formatting
# ==============================================================================

def print_results(results: List[Tuple[int, bool, str]], verbose: bool = True):
    """
    Print scan results in a formatted table.

    Args:
        results: List of (port, is_open, service) tuples
        verbose: Show closed ports too
    """
    open_ports = [r for r in results if r[1]]

    print("\n" + "=" * 60)
    print("                    SCAN RESULTS")
    print("=" * 60)

    if open_ports:
        print(f"\n{'PORT':<8} {'STATE':<10} {'SERVICE':<15}")
        print("-" * 40)

        for port, is_open, service in sorted(open_ports):
            status = "OPEN"
            print(f"{port:<8} {status:<10} {service:<15}")

        print("-" * 40)
        print(f"Total open ports: {len(open_ports)}")
    else:
        print("\nNo open ports found in the scanned range.")

    if verbose:
        closed_count = len([r for r in results if not r[1]])
        print(f"\nScanned ports: {len(results)}")
        print(f"Open: {len(open_ports)}, Closed/Filtered: {closed_count}")


def print_security_advice():
    """Print educational security advice based on scan results."""
    print("\n" + "=" * 60)
    print("                 SECURITY EDUCATION")
    print("=" * 60)

    advice = """
    WHY PORT SCANNING MATTERS:

    1. NETWORK MAPPING
       - Attackers scan networks to find entry points
       - Know your attack surface by scanning YOUR network

    2. COMMON VULNERABILITIES
       - Port 22 (SSH): Brute force attacks common
       - Port 3389 (RDP): Target for ransomware
       - Port 445 (SMB): EternalBlue vulnerability
       - Port 3306/5432/27017: Database exposure

    3. BEST PRACTICES
       - Close unused ports
       - Use firewalls to restrict access
       - Enable logging on open ports
       - Run services on non-standard ports when possible
       - Use strong authentication on all services

    4. DEFENSE IN DEPTH
       - Don't rely on "security through obscurity"
       - Multiple layers of security (firewall + auth + monitoring)

    LEGAL NOTICE:
       Only scan networks and hosts you own or have explicit
       written permission to test. Unauthorized scanning is
       illegal in many jurisdictions.
    """

    print(advice)


# ==============================================================================
# CLI Interface
# ==============================================================================

def print_banner():
    """Display educational banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║              EDUCATIONAL PORT SCANNER - LEARN SECURITY       ║
║                                                              ║
║  This tool demonstrates network scanning for EDUCATION.      ║
║  Understanding port scanning helps you DEFEND networks.      ║
║                                                              ║
║  ⚠️  EDUCATIONAL PURPOSE ONLY - ONLY SCAN HOSTS YOU OWN       ║
║     OR HAVE WRITTEN PERMISSION TO TEST                       ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Educational Port Scanner - Learn Network Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s localhost                      # Scan common ports on localhost
  %(prog)s 192.168.1.1                   # Scan common ports on IP
  %(prog)s localhost -p 1-1000            # Scan ports 1-1000
  %(prog)s localhost --all                # Scan all 65535 ports (slow!)
  %(prog)s localhost -t 0.5 --verbose    # Faster scan with verbose output
  %(prog)s --discover                     # Discover local network devices

Disclaimer: Only scan hosts you own or have permission to test.
        """
    )

    parser.add_argument(
        "host",
        nargs="?",
        help="Target host (IP or hostname)"
    )

    parser.add_argument(
        "-p", "--ports",
        help="Port range (e.g., '1-1000' or '80,443,8080')"
    )

    parser.add_argument(
        "-c", "--common",
        action="store_true",
        help="Scan common ports only (default)"
    )

    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Scan all ports (1-65535) - WARNING: Slow!"
    )

    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=1.0,
        help="Connection timeout in seconds (default: 1.0)"
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=50,
        help="Concurrent workers (default: 50)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover devices on local network"
    )

    parser.add_argument(
        "--localhost",
        action="store_true",
        help="Quick scan of localhost common ports"
    )

    args = parser.parse_args()

    print_banner()

    start_time = time.time()

    try:
        # Network discovery mode
        if args.discover:
            print("[*] Network Discovery Mode")
            print("=" * 60)
            discover_local_network()
            return 0

        # Localhost quick scan
        if args.localhost or (not args.host):
            host = "127.0.0.1"
            ports = list(COMMON_PORTS.keys())
            print(f"[*] Quick scan of localhost")

        else:
            host = args.host

            # Parse port range
            if args.ports:
                try:
                    if '-' in args.ports:
                        start_port, end_port = args.ports.split('-')
                        ports = generate_port_list(
                            start=int(start_port),
                            end=int(end_port),
                            scan_common=False
                        )
                    elif ',' in args.ports:
                        ports = [int(p.strip()) for p in args.ports.split(',')]
                    else:
                        ports = [int(args.ports)]
                except ValueError:
                    print("[!] Invalid port format. Use '1-1000' or '80,443,8080'")
                    return 1
            else:
                ports = generate_port_list(scan_common=not args.all, scan_all=args.all)

        # Resolve hostname
        ip = resolve_host(host)

        print(f"[*] Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Timeout: {args.timeout}s, Workers: {args.workers}")
        print()

        # Perform scan
        results = scan_ports_tcp(
            ip,
            ports,
            timeout=args.timeout,
            max_workers=args.workers
        )

        # Print results
        print_results(results, verbose=args.verbose)

        # Security advice
        print_security_advice()

        elapsed = time.time() - start_time
        print(f"\n[*] Scan completed in {elapsed:.2f} seconds")

        return 0

    except ValueError as e:
        print(f"[!] Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user.")
        return 130
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
