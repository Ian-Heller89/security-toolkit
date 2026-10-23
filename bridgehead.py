#!/usr/bin/env python3
# BridgeHead: Automated Perimeter Tunneling & External Network Mapper
# Path: bridge_head.py
# Language: Python 3 (.py) - Zero Dependencies Required

import sys
import os
import socket
import subprocess
import time
import urllib.request
import json

def print_banner():
    print("=" * 80)
    print(" " * 33 + "BRIDGE HEAD")
    print(" " * 19 + "AUTOMATED PERIMETER TUNNELING & WAN MATRIX")
    print("=" * 80 + "\n")

def get_internal_ip():
    """Extracts the active local private IP configuration of the system adapter."""
    try:
        # Create a temporary socket connection to resolve the primary outbound interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        internal_ip = s.getsockname()[0]
        s.close()
        return internal_ip
    except Exception:
        return "127.0.0.1"

def get_external_wan_ip():
    """Queries public metadata endpoints to identify the current external WAN gateway."""
    try:
        # Utilizing standard python built-in web request streams to avoid library dependencies
        req = urllib.request.Request("https://ipify.org", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            return data.get("ip", "Unknown WAN")
    except Exception:
        return "Offline / Interrupted Interface"

def allocate_native_ssh_tunnel(local_port):
    """Establishes a zero-dependency remote SSH reverse tunnel to generate an internet-routable endpoint."""
    print(f"\n[*] Requesting secure perimeter mapping tunnel for local port: {local_port}...")
    
    # Using localhost.run as a zero-setup, keyless SSH reverse proxy tunnel endpoint
    ssh_cmd = f"ssh -R 80:localhost:{local_port} nokey@localhost.run"
    
    print("[*] Spawning native background tunnel subsystem channel...")
    try:
        # Open the SSH tunnel in a non-blocking background process
        process = subprocess.Popen(
            ssh_cmd, shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            text=True, bufsize=1
        )
        
        print("[*] Synchronizing network sockets and parsing public domain tokens (Please wait)...")
        time.sleep(4) # Allow connection handshake to finalize
        
        public_url = None
        # Read the output from the SSH server to grab our assigned public URL
        for _ in range(10):
            line = process.stdout.readline()
            if "tunneled to" in line or "lhr.life" in line or "localhost.run" in line:
                parts = line.split()
                for part in parts:
                    if "localhost.run" in part or "lhr.life" in part:
                        public_url = part.replace("https://", "").replace("http://", "").strip()
                        break
            if public_url: break
            
        if public_url:
            return public_url, process
        else:
            process.terminate()
            return None, None
    except Exception as e:
        print(f"[-] Tunnel runtime initialization exception: {e}")
        return None, None
def main():
    print_banner()
    
    # 1. Automate internal and external asset mapping variables
    internal_ip = get_internal_ip()
    external_ip = get_external_wan_ip()
    
    print("--- System Network Interface Baseline ---")
    print(f"[+] Private Adapter IP (LAN): {internal_ip}")
    print(f"[+] Public Gateway IP (WAN):  {external_ip}\n")
    
    # 2. Demand target port configuration property allocation
    port_input = input("[?] Enter local ingress port to allocate for external routing (e.g., 8080): ").strip()
    if not port_input.isdigit():
        print("[-] Error: Local port configuration attributes must be an integer sequence.")
        return
        
    local_port = int(port_input)
    
    # 3. Spawn background routing infrastructure channel
    public_dns, tunnel_proc = allocate_native_ssh_tunnel(local_port)
    
    if public_dns and tunnel_proc:
        print("\n" + "="*80)
        print("🎉 SUCCESS: INTERNET ROUTABLE TUNNEL ESTABLISHED LIVE")
        print("="*80)
        print(f"[+] Target Ingress Port (Local Host): {local_port}")
        print(f"[+] Assigned Public Endpoint Address: {public_dns}")
        print(f"[+] Operational Listen Interface:     Port 80 (Standard HTTP Web Link)")
        print("="*80 + "\n")
        print("[*] Active Tunnel established in background. Traffic is routing live!")
        print("[*] Press Ctrl+C at any time to collapse the tunnel and restore local isolation...\n")
        
        try:
            # Sit passively and keep the background process running until user hits Ctrl+C
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[*] Keyboard signal intercepted. Collapsing background tunnel channels...")
            tunnel_proc.terminate()
            print("[+] Network isolation restored. Workspace clean. Safe tracking complete.")
    else:
        print("\n[!!!] TUNNEL ALLOCATION FAILURE: Unable to negotiate automated SSH reverse proxy parameters.")
        print("[*] Check local internet connectivity or verify outbound SSH ports are unrestricted.")

if __name__ == "__main__":
    main()
