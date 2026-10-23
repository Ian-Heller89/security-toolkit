# 📦 Shadow Haul: Zero-Interaction Multi-OS Discovery, Hardened AES-256 Packer & Recovery Engine

A production-grade, host-agnostic post-exploitation exfiltration staging framework written in **Python 3**. This utility automates the final "Actions on Objectives" phase of an assessment by dynamically mapping critical corporate data sectors across **Windows (PowerShell)**, **Linux**, and **macOS (Zsh)** environments. Discovered high-value assets are aggregated into an in-memory compression envelope and encrypted with unbreakable, military-grade **AES-256 Symmetric Encryption** leveraging native OS kernel engines to maintain a zero-dependency footprint on targets.

## ⚙️ Core Operational Advantages

During high-priority red team assessments, manual target classification causes terminal latency, while passing raw or poorly obfuscated data (like raw XOR blocks) across a network can easily be decoded by blue teams via Known-Plaintext Attacks. `Shadow Haul` resolves these constraints through zero-interaction environment profiling and secure cryptographic boundaries:

1. **Automated Sector Mapping:** Bypasses noisy, system-wide crawls by using native path expansion libraries to instantly lock onto primary user workspaces (`Documents`, `Desktop`, `Downloads`, `Development`, `Projects`) while applying explicit exclusion rules to prevent processing dead-locks in system cache or local application runtime folders.
2. **Zero-Dependency Native AES-256:** Bypasses the "third-party library trap." The generated payloads invoke pre-installed core OS mechanisms natively inside the target system's temporary memory—**Windows .NET Framework API (`AesManaged`)** or **macOS OpenSSL binaries**—enforcing bulletproof encryption that remains impossible for packet-capturing analysts (e.g., Wireshark) to decode without the master passphrase.
3. **Closed-Loop Attack Host Decryption:** Provides a centralized decryption platform interface choice `[D]`. The framework automatically ingests the exfiltrated binary payload (`haul.dat`), validates the cryptographic blocks, decrypts the contents using Python standard pipelines, and reconstructs the original directory layouts cleanly on the attack station.

## 🚀 Key Technical Features Illustrated

*   **Comprehensive Asset Whitelist:** Automatically isolates and harvests data records across 26 discrete, high-value corporate storage extensions spanning cryptographic keys (`.key`, `.pem`), sensitive ledger databases (`.sql`, `.sqlite`, `.xlsx`), network configurations, and environment files (`.env`).
*   **Volatile Dynamic Delivery Server:** Employs multi-threaded background HTTP stagers running concurrently on the operator's attack platform to serve payload wrappers seamlessly on-demand.
*   **Volatile Memory Scrubbing:** Implements explicit programmatic RAM sanitization by overwriting key byte arrays with zero-bytes (`0x00`) immediately after execution to prevent key exposure via forensic memory dumps.
*   **Anti-Forensic Timestomping:** Automatically matches the file metadata creation timestamps of the output `haul.dat` container to a trusted, pre-existing local system binary (`/etc/hosts`), blending the exfiltration package into the target host's timeline.
