#!/usr/bin/env python3
"""FlyBy - menu-driven recon tool. For authorized testing only."""

import asyncio
import platform
import socket
import subprocess
import time

BACK = "999"

LOGO = r"""
                 __________________________________
                /                                 /|
               /   ____________________________  / |
              /   /                           / /  |
             /   /   R A D I O   F L Y E R   / /   |
            /   /___________________________/ /    |
           /_________________________________/     |
     O    |                                 |      /
      \   |                                 |     /
       \  |                                 |    /
        \_|_________________________________|___/
           \_______/               \_______/
           /   _   \               /   _   \

          |   / \   |             |   / \   |
          |  | O |  |             |  | O |  |
          |   \_/   |             |   \_/   |
           \_______/               \_______/
"""

TITLE = "F L Y B Y   |   recon toolkit"
WARNING = "Authorized targets only: your own lab, HTB, or written permission."

# Preset port groups for the scan menu
PRESETS = {
    "1": ("Web (80, 443, 8080, 8443)", [80, 443, 8080, 8443]),
    "2": ("Remote access (22, 23, 3389, 5900)", [22, 23, 3389, 5900]),
    "3": ("Common services (top ~25)", [
        21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993,
        995, 1723, 3306, 3389, 5432, 5900, 6379, 8000, 8080, 8443, 27017]),
}

SERVICE_NAMES = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns", 80: "http",
    110: "pop3", 111: "rpcbind", 135: "msrpc", 139: "netbios", 143: "imap",
    443: "https", 445: "smb", 993: "imaps", 995: "pop3s", 1723: "pptp",
    3306: "mysql", 3389: "rdp", 5432: "postgresql", 5900: "vnc",
    6379: "redis", 8000: "http-alt", 8080: "http-proxy", 8443: "https-alt",
    27017: "mongodb",
}


# ---------- helpers ----------

def banner() -> None:
    print(LOGO)
    print(f"  {TITLE}")
    print(f"  {WARNING}\n")


def ask(prompt: str) -> str:
    """Input wrapper: Ctrl+C / Ctrl+D act like 'back'."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return BACK


def get_target(prompt: str = "  Target IP or hostname (999 = back): ") -> str | None:
    """Ask for a target and make sure it resolves. None means go back."""
    while True:
        target = ask(prompt)
        if target == BACK:
            return None
        if not target:
            continue
        try:
            socket.gethostbyname(target)
            return target
        except socket.gaierror:
            print("  Could not resolve that host. Try again.")


def parse_ports(spec: str) -> list[int]:
    """Turn '22,80,443' or '1-1024' (or a mix) into a sorted list of ints."""
    ports: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        elif part:
            ports.add(int(part))
    return sorted(p for p in ports if 1 <= p <= 65535)


# ---------- port scanning ----------

async def check_port(host: str, port: int, timeout: float,
                     sem: asyncio.Semaphore) -> int | None:
    async with sem:
        try:
            conn = asyncio.open_connection(host, port)
            _, writer = await asyncio.wait_for(conn, timeout=timeout)
            writer.close()
            await writer.wait_closed()
            return port
        except (asyncio.TimeoutError, OSError):
            return None


async def scan(host: str, ports: list[int], timeout: float,
               concurrency: int) -> list[int]:
    sem = asyncio.Semaphore(concurrency)
    results = await asyncio.gather(
        *(check_port(host, p, timeout, sem) for p in ports))
    return [p for p in results if p is not None]


def run_scan(host: str, ports: list[int], label: str) -> None:
    print(f"\n  Scanning {host} - {label} ({len(ports)} ports)...")
    start = time.time()
    # keep concurrency under the default 1024 open-file limit
    timeout = 0.6 if len(ports) > 1000 else 1.0
    open_ports = asyncio.run(scan(host, ports, timeout, 500))
    elapsed = time.time() - start

    if open_ports:
        print("\n  PORT      STATE   SERVICE")
        for p in open_ports:
            print(f"  {str(p) + '/tcp':<9} open    {SERVICE_NAMES.get(p, '-')}")
    else:
        print("  No open ports found (or the host is filtering/blocking).")
    print(f"\n  Done in {elapsed:.1f}s")
    ask("  Press Enter to continue...")


def scan_menu() -> None:
    host = get_target()
    if host is None:
        return
    while True:
        print(f"\n  === Scan Ports: {host} ===")
        for key, (name, _) in PRESETS.items():
            print(f"  {key}) {name}")
        print("  4) Custom ports")
        print("  5) All ports (1-65535)")
        print("  999) Back")
        choice = ask("\n  FlyBy/scan > ")

        if choice == BACK:
            return
        if choice in PRESETS:
            name, ports = PRESETS[choice]
            run_scan(host, ports, name)
        elif choice == "4":
            spec = ask("  Ports (e.g. 22,80,443 or 1-1024, 999 = back): ")
            if spec == BACK:
                continue
            try:
                ports = parse_ports(spec)
            except ValueError:
                print("  Invalid format. Use numbers, commas, and ranges.")
                continue
            if not ports:
                print("  No valid ports (must be 1-65535).")
                continue
            run_scan(host, ports, "custom")
        elif choice == "5":
            print("  Full scan can take a minute or two.")
            run_scan(host, list(range(1, 65536)), "all ports")
        else:
            print("  Invalid option.")


# ---------- host alive check ----------

def ping_host(host: str) -> bool:
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", flag, "1", "-W", "2", host],
                                capture_output=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def tcp_probe(host: str) -> list[int]:
    """Fallback: many hosts block ping, so see if any common port answers."""
    probe_ports = [80, 443, 22, 445, 3389, 8080]
    return asyncio.run(scan(host, probe_ports, 1.5, 10))


def alive_menu() -> None:
    while True:
        print("\n  === Host Alive Check ===")
        host = get_target()
        if host is None:
            return
        ip = socket.gethostbyname(host)
        print(f"\n  Checking {host} ({ip})...")

        ping_ok = ping_host(host)
        print(f"  [{'+' if ping_ok else '-'}] ICMP ping: "
              f"{'reply received' if ping_ok else 'no reply'}")

        answered = tcp_probe(host)
        if answered:
            names = ", ".join(f"{p}/{SERVICE_NAMES.get(p, '?')}" for p in answered)
            print(f"  [+] TCP probe: responded on {names}")
        else:
            print("  [-] TCP probe: no response on common ports")

        if ping_ok or answered:
            print("\n  Result: HOST IS UP")
        else:
            print("\n  Result: no response. Host may be down, or it is "
                  "blocking ping and probes.")
        ask("  Press Enter to continue...")


# ---------- banner grab ----------

def banner_grab(host: str, port: int) -> str:
    try:
        with socket.create_connection((host, port), timeout=3) as s:
            s.settimeout(3)
            if port in (80, 8000, 8080):
                s.sendall(f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
            data = s.recv(1024)
            return data.decode(errors="replace").strip() or "(connected, no banner)"
    except (socket.timeout, OSError) as exc:
        return f"(failed: {exc})"


def banner_menu() -> None:
    while True:
        print("\n  === Banner Grab ===")
        host = get_target()
        if host is None:
            return
        port_s = ask("  Port (999 = back): ")
        if port_s == BACK:
            continue
        if not port_s.isdigit() or not 1 <= int(port_s) <= 65535:
            print("  Enter a port number between 1 and 65535.")
            continue
        print(f"\n  Connecting to {host}:{port_s}...\n")
        for line in banner_grab(host, int(port_s)).splitlines()[:10]:
            print(f"  {line}")
        ask("\n  Press Enter to continue...")


# ---------- DNS lookup ----------

def dns_menu() -> None:
    while True:
        print("\n  === DNS Lookup ===")
        name = ask("  Hostname or IP (999 = back): ")
        if name == BACK:
            return
        if not name:
            continue
        try:
            host, aliases, addrs = socket.gethostbyname_ex(name)
            print(f"\n  Name:      {host}")
            print(f"  Addresses: {', '.join(addrs)}")
            if aliases:
                print(f"  Aliases:   {', '.join(aliases)}")
        except socket.gaierror:
            print("  Could not resolve that name.")
        try:
            rev = socket.gethostbyaddr(socket.gethostbyname(name))[0]
            print(f"  Reverse:   {rev}")
        except (socket.herror, socket.gaierror):
            print("  Reverse:   (no PTR record)")
        ask("\n  Press Enter to continue...")


# ---------- main menu ----------

def main() -> None:
    actions = {"1": scan_menu, "2": alive_menu, "3": banner_menu, "4": dns_menu}
    while True:
        banner()
        print("  1) Scan ports")
        print("  2) Check if a host is alive")
        print("  3) Grab a service banner")
        print("  4) DNS lookup")
        print("  0) Exit")
        choice = ask("\n  FlyBy > ")

        if choice in ("0", BACK):
            print("\n  Safe travels.\n")
            return
        action = actions.get(choice)
        if action:
            action()
        else:
            print("  Invalid option.")
            time.sleep(1)


if __name__ == "__main__":
    main()
