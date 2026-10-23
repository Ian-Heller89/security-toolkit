#!/usr/bin/env python3
import os
import sys
import hashlib
import json
import time
import platform

# Central configuration file mapping for the database storage footprint
BASELINE_DB = "sentry_baseline.json"

def print_banner():
    print("=" * 80)
    print(" " * 33 + "SENTRY CHECK")
    print(" " * 22 + "CRYPTOGRAPHIC FILE INTEGRITY MONITOR")
    print("=" * 80 + "\n")

def get_critical_files():
    """Defines a highly comprehensive, enterprise whitelist of high-value system assets to monitor."""
    # Explicit high-value single system files
    critical_files = [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/sudoers",
        "/etc/crontab",
        "/etc/hosts",
        "/etc/resolv.conf",
        "/etc/profile",
        "/etc/bash.bashrc",
        "/etc/environment",
        "/etc/modules",
        "/etc/rc.local",
        "/etc/nsswitch.conf",
        "/etc/ssh/sshd_config"
    ]
    
    # Critical security folders targeted by Red Teams for script injection/persistence
    critical_directories = [
        "/etc/cron.d",
        "/etc/cron.daily",
        "/etc/cron.hourly",
        "/etc/cron.weekly",
        "/etc/cron.monthly"
    ]
    
    active_targets = []
    
    # Ingest individual file paths if they exist natively on the target host environment
    for f in critical_files:
        if os.path.exists(f) and os.path.isfile(f):
            active_targets.append(f)
            
    # Advanced Directory Sweep: Crawl folders recursively to map all nested script files
    for d in critical_directories:
        if os.path.exists(d) and os.path.isdir(d):
            for root, _, files in os.walk(d):
                for file in files:
                    full_path = os.path.join(root, file)
                    active_targets.append(full_path)
                    
    return active_targets

def calculate_sha256(file_path):
    """Generates an explicit SHA-256 checksum signature for a designated file location."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def create_system_baseline():
    """Generates a brand new cryptographic snapshot baseline and writes it to disk database storage."""
    print("\n[*] Initializing comprehensive multi-sector system baseline crawl...")
    target_files = get_critical_files()
    baseline_data = {}
    
    for file_path in target_files:
        file_hash = calculate_sha256(file_path)
        if file_hash:
            baseline_data[file_path] = file_hash
            print(f"    [+] Signed signature baseline for: {file_path}")
            
    try:
        with open(BASELINE_DB, "w") as f:
            json.dump(baseline_data, f, indent=4)
        print(f"\n[+] SUCCESS: Cryptographic baseline database completely written to: {BASELINE_DB}")
        print(f"[*] Secure baseline established tracking {len(baseline_data)} critical host assets.")
    except Exception as e:
        print(f"[-] Failed to serialize cryptographic file database: {e}")
def execute_system_audit():
    """Compares active system file hashes against the database baseline to isolate tampering anomalies."""
    print("\n[*] Initializing cryptographic integrity verification sweep...")
    
    if not os.path.exists(BASELINE_DB):
        print(f"[-] Audit Aborted: No existing baseline profile discovered. Run Option [1] first.")
        return

    try:
        with open(BASELINE_DB, "r") as f:
            baseline_data = json.load(f)
    except Exception as e:
        print(f"[-] Critical Error: Failed to parse baseline signature registry database: {e}")
        return

    tampered_count = 0
    missing_count = 0
    clean_count = 0
    
    print("-" * 80)
    print(f"{'MONITORED SYSTEM TARGET FILE':<45} | {'INTEGRITY POSTURE REPORT':<30}")
    print("-" * 80)

    # Cross-reference the active file footprint states with the frozen database snapshot entries
    for file_path, original_hash in baseline_data.items():
        if not os.path.exists(file_path):
            print(f"{file_path:<45} | [!!!] CRITICAL: FILE DELETED/MISSING")
            missing_count += 1
            continue
            
        current_hash = calculate_sha256(file_path)
        
        if current_hash is None:
            print(f"{file_path:<45} | [-] ERROR: READ ACCESS PERMISSION DENIED")
            continue
            
        if current_hash != original_hash:
            print(f"{file_path:<45} | [!!!] WARNING: TAMPERED / MODIFIED")
            tampered_count += 1
        else:
            print(f"{file_path:<45} | [+] VERIFIED CLEAN")
            clean_count += 1

    # Check for unauthorized new file files dropped into monitored automation task folders
    current_targets = get_critical_files()
    new_files_count = 0
    for path in current_targets:
        if path not in baseline_data:
            print(f"{path:<45} | [!!!] UNKNOWN: NEW FILE INJECTED")
            new_files_count += 1

    print("-" * 80)
    print(f"\n[=] INTEGRITY AUDIT METRICS SUMMARY:")
    print(f"    -> Verified Intact: {clean_count}")
    print(f"    -> Malicious Modifications: {tampered_count}")
    print(f"    -> Missing/Deleted Files: {missing_count}")
    print(f"    -> Rogue File Injections: {new_files_count}")
    
    if tampered_count > 0 or missing_count > 0 or new_files_count > 0:
        print("\n[!!!] DETECTION ALERT: Critical host anomalies identified! Immediate containment required.")
    else:
        print("\n[+] System posture secure. All critical configurations match the certified baseline database.")
    print("=" * 80)

def main():
    while True:
        print_banner()
        print(f"[+] Active Host Baseline: {platform.system()} | Signature Store: {BASELINE_DB}")
        print("\n--- Linux Core Host File Integrity Configuration ---")
        print(" [1] Initialize/Generate Cryptographic File System Baseline")
        print(" [2] Run Active System Integrity Audit (Scan for Tampering)")
        print(" [999] Exit Defensive Suite Entirely")
        
        choice = input("\n[?] Select Operational Mode (1-2 / 999): ").strip()
        
        if choice == '999':
            print("[*] Shutting down SentryCheck Security Engine.")
            break
        elif choice == '1':
            create_system_baseline()
            input("\n[*] Press Enter to return to menu...")
        elif choice == '2':
            execute_system_audit()
            input("\n[*] Press Enter to return to menu...")
        else:
            print("[-] Choice index not recognized.")
            time.sleep(1)

if __name__ == "__main__":
    main()
