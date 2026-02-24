#!/usr/bin/env python3
"""
Network Scanner - A fast, multi-threaded port and service scanner.
Author: GitHub Portfolio Project
"""

import socket
import argparse
import threading
import ipaddress
import sys
import json
from datetime import datetime
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed

class Colors:
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB", 5900: "VNC",
}

def grab_banner(host, port, timeout=2.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            return banner[:100] if banner else ""
    except Exception:
        return ""

def scan_port(host, port, timeout, grab):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                service = COMMON_SERVICES.get(port, "Unknown")
                try:
                    service = socket.getservbyport(port)
                except Exception:
                    pass
                banner = grab_banner(host, port, timeout) if grab else ""
                return {"port": port, "state": "open", "service": service, "banner": banner}
    except socket.error:
        pass
    return None

def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        print(f"{Colors.RED}[ERROR] Cannot resolve host: {host}{Colors.RESET}")
        sys.exit(1)

def run_scan(host, ports, timeout, threads, grab, output):
    ip = resolve_host(host)
    open_ports = []
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═'*55}")
    print(f"  🔍  Network Scanner")
    print(f"{'═'*55}{Colors.RESET}")
    print(f"  Target   : {Colors.YELLOW}{host}{Colors.RESET} ({ip})")
    print(f"  Ports    : {ports[0]}-{ports[-1]} ({len(ports)} total)")
    print(f"  Threads  : {threads}")
    print(f"  Timeout  : {timeout}s")
    print(f"  Banners  : {'Yes' if grab else 'No'}")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.CYAN}{'═'*55}{Colors.RESET}\n")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, p, timeout, grab): p for p in ports}
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            if result:
                open_ports.append(result)
                port = result["port"]
                service = result["service"]
                banner = result["banner"]
                print(f"  {Colors.GREEN}[OPEN]{Colors.RESET}  {Colors.BOLD}{port:>5}/tcp{Colors.RESET}  {Colors.YELLOW}{service:<15}{Colors.RESET}", end="")
                if banner:
                    print(f"  -> {Colors.CYAN}{banner.split(chr(10))[0][:50]}{Colors.RESET}", end="")
                print()
            pct = int((completed / len(ports)) * 40)
            print(f"\r  [{'#'*pct}{'.'*(40-pct)}] {completed}/{len(ports)}", end="", flush=True)
    print(f"\n\n{Colors.CYAN}{'═'*55}{Colors.RESET}")
    print(f"  Scan complete. {Colors.GREEN}{len(open_ports)} open port(s){Colors.RESET} found.")
    print(f"  Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.CYAN}{'═'*55}{Colors.RESET}\n")
    if output:
        report = {"target": host, "ip": ip, "scanned_ports": len(ports), "open_ports": open_ports, "timestamp": datetime.now().isoformat()}
        with open(output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"  {Colors.YELLOW}[+] Report saved -> {output}{Colors.RESET}\n")

def parse_ports(port_str):
    ports = set()
    for part in port_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def main():
    parser = argparse.ArgumentParser(description="🔍 Network Scanner - fast multi-threaded port scanner")
    parser.add_argument("host", help="Target host or IP")
    parser.add_argument("--ports", "-p", default="1-1024", help="Port range (default: 1-1024)")
    parser.add_argument("--timeout", "-t", type=float, default=1.0)
    parser.add_argument("--threads", "-T", type=int, default=200)
    parser.add_argument("--banner", "-b", action="store_true")
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()
    run_scan(args.host, parse_ports(args.ports), args.timeout, args.threads, args.banner, args.output)

if __name__ == "__main__":
    main()
