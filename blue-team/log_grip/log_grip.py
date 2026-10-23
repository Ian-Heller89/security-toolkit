#!/usr/bin/env python3
import os
import sys
import re
import time
import subprocess
import platform

def print_banner():
    print("=" * 80)
    print(" " * 34 + "LOG GRIP")
    print(" " * 18 + "ASYNCHRONOUS AUTHENTICATION MONITOR & RESPONSE ENGINE")
    print("=" * 80 + "\n")

def get_default_log_path():
    """Identifies the standard authentication log track location based on active host OS."""
    current_os = platform.system()
    if current_os == "Linux":
        # Standard Debian/Ubuntu authentication log footprint
        if os.path.exists("/var/log/auth.log"): return "/var/log/auth.log"
        # RedHat/CentOS footprint alternative configuration tracking
        elif os.path.exists("/var/log/secure"): return "/var/log/secure"
    elif current_os == "Darwin": # macOS footprint trace
        if os.path.exists("/var/log/system.log"): return "/var/log/system.log"
    return "test_auth.log" # Fallback local mock workspace file for testing

def monitor_log_stream(log_path, threshold, window):
    """Trails the target log file dynamically and tracks failures per IP context."""
    print(f"\n[*] Initializing real-time file stream tracking on target: {log_path}")
    print(f"[*] Configuration parameters: Threshold = {threshold} failed attempts within {window} seconds.")
    
    failure_tracker = {}
    blocked_ips = set()
    
    # HARDENED DEFENSE: Double-filter regex to catch standard bad passwords AND invalid/fake username sweeps
    fail_regex = re.compile(
        r'(?:Failed password for invalid user .* from|Failed password for .* from|Invalid user .* from) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    )

    if not os.path.exists(log_path):
        with open(log_path, "w") as f: f.write("")

    try:
        with open(log_path, "r") as f:
            # Jump straight to the end of the file to process live attacks, avoiding historical noise
            f.seek(0, 2)
            print("[+] Active listener synchronized! Press Ctrl+C to return to main menu.")
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1) # Aggressive high-speed sampling for class lab testing
                    continue
                    
                match = fail_regex.search(line)
                if match:
                    attacker_ip = match.group(1)
                    current_time = time.time()
                    print(f"[!] Warning: Detected authentication failure footprint from IP: {attacker_ip}")
                    
                    if attacker_ip in blocked_ips:
                        continue
                        
                    if attacker_ip not in failure_tracker:
                        failure_tracker[attacker_ip] = []
                        
                    failure_tracker[attacker_ip].append(current_time)
                    
                    # Keep track only of infractions happening within our tight sliding window
                    failure_tracker[attacker_ip] = [t for t in failure_tracker[attacker_ip] if current_time - t <= window]
                    
                    if len(failure_tracker[attacker_ip]) >= threshold:
                        print(f"\n[!!!] ALERT: Threshold breached! IP {attacker_ip} triggered attack profile!")
                        trigger_firewall_mitigation(attacker_ip)
                        blocked_ips.add(attacker_ip)
                        
    except PermissionError:
        print("[-] Error: Insufficient privileges to read system authentication logs. Run via 'sudo'.")
    except KeyboardInterrupt:
        print("\n[*] Stopping log stream listener. Returning to menu.")
def trigger_firewall_mitigation(attacker_ip):
    """Dynamically applies active firewall block rules via native Linux security tools."""
    current_os = platform.system()
    if current_os != "Linux":
        print(f"[*] Simulated block enforced on non-Linux platform for target IP: {attacker_ip}")
        return

    print(f"[*] Communicating with Linux network kernel to isolate threat: {attacker_ip}")
    
    # Strategy A: Attempt to utilize the universal Uncomplicated Firewall (UFW)
    try:
        cmd = f"sudo ufw deny from {attacker_ip} to any"
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[+] SUCCESS: Automated UFW rule created. Packets dropped from {attacker_ip}.")
        return
    except subprocess.CalledProcessError:
        pass # Fall back to raw iptables if UFW is not active on the distribution
        
    # Strategy B: Core iptables kernel routing injection
    try:
        cmd = f"sudo iptables -A INPUT -s {attacker_ip} -j DROP"
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[+] SUCCESS: Automated iptables rule injected. {attacker_ip} is now dropped at kernel boundary.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Firewall Injection Blocked: Ensure script is running with elevated 'sudo' rights. Details: {e}")

def audit_firewall_rules():
    """Queries the Linux kernel to view all actively enforced firewall block rules."""
    print("\n" + "="*80)
    print("                ACTIVE KERNEL FIREWALL BLOCK RULES AUDIT")
    print("="*80)
    if platform.system() != "Linux":
        print("[-] Audit failed: Active host machine is not running a Linux kernel.")
        return

    try:
        print("[*] Retrieving active iptables block configurations...")
        cmd = "sudo iptables -L INPUT -v -n"
        res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = res.stdout.decode('utf-8', errors='ignore').strip()
        if output:
            print(output)
        else:
            print("[*] No active blocks found in the primary iptables input chain.")
    except subprocess.CalledProcessError:
        try:
            print("[*] iptables restricted. Querying Uncomplicated Firewall (UFW) status...")
            cmd = "sudo ufw status verbose"
            res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(res.stdout.decode('utf-8', errors='ignore').strip())
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed to query system firewall state: {e}")

def flush_firewall_rules():
    """Cleanses all temporary security block rules to restore network baseline connectivity."""
    print("\n[*] Initializing global firewall rule flush sequence...")
    if platform.system() != "Linux":
        print("[-] Operation aborted: Non-Linux host detected.")
        return

    try:
        print("[*] Flushing iptables INPUT chain rules...")
        subprocess.run("sudo iptables -F INPUT", shell=True, check=True)
        print("[+] SUCCESS: iptables rules cleared.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to flush iptables chain: {e}")

def main():
    target_log = get_default_log_path()
    failed_threshold = 5   # Maximum failed attempts allowed before triggering remediation
    time_window = 10       # Time threshold envelope tracked in seconds

    while True:
        print_banner()
        print(f"[+] Active Host Baseline: {platform.system()} | Monitored Log File: {target_log}")
        print("\n--- Linux Authentication Bruteforce Protection Configuration ---")
        print(" [1] Launch Real-Time Asynchronous Authentication Stream Monitor")
        print(" [2] Audit Active Kernel Firewall Block Rules (View Blocked IPs)")
        print(" [3] Flush All Enforced Firewall Rules (Reset Network Baseline)")
        print(" [999] Exit Defensive Suite Entirely")
        
        choice = input("\n[?] Select Operational Mode (1-3 / 999): ").strip()
        
        if choice == '999':
            print("[*] Shutting down LogGrip Protection Suite. Maintaining active blocks.")
            break
        elif choice == '1':
            monitor_log_stream(target_log, failed_threshold, time_window)
        elif choice == '2':
            audit_firewall_rules()
            input("\n[*] Press Enter to return to menu...")
        elif choice == '3':
            confirm = input("[!] WARNING: This will unblock all previously isolated IPs. Proceed? (y/N): ").strip().lower()
            if confirm == 'y':
                flush_firewall_rules()
            input("\n[*] Press Enter to return to menu...")
        else:
            print("[-] Choice index not recognized.")
            time.sleep(1)

if __name__ == "__main__":
    main()
