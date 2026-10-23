# 📦 Shadow Haul: Automated Multi-OS High-Value Asset Discovery & Anti-Forensic Staging Suite

A production-grade, host-agnostic post-exploitation exfiltration staging framework written in **Python 3**. This tool automates the "Actions on Objectives" phase of an assessment by dynamically mapping critical corporate data sectors across **Windows (PowerShell)**, **Linux**, and **macOS (Zsh)** environments, grouping high-value files inside a lossless compressed package, and masking structural file headers via symmetric cryptography.

## ⚙️ Core Operational Advantages

During red team operations, manual target triage creates massive terminal latency, while passing raw or unencrypted data blocks across a network immediately triggers Data Loss Prevention (DLP) and Network Intrusion Detection Systems (NIDS). `Shadow Haul` is engineered to solve these challenges through zero-interaction environment profiling and programmatic anti-forensics:

1. **Automated Sector Mapping:** Bypasses noisy, system-wide sweeps by using native system path expansion libraries to instantly lock onto primary user workspaces (`Documents`, `Desktop`, `Downloads`, `Development`, `Projects`) while applying explicit exclusion filters to prevent lockouts in system cache or application directories.
2. **Fileless Memory Staging:** Generates lightweight, dependency-free native stagers delivered entirely via RAM execution streams. When called, the target agent packages assets natively and routes the final payload directly to clear user destination zones (such as the Windows Desktop or macOS Home folder).
3. **Cryptographic Signatures Evasion:** Applies a byte-level symmetric XOR transformation using a custom passphrase to alter the container's structural Magic Bytes. This process renders the final package (**`haul.dat`**) completely unclassifiable to network firewall heuristics.

## 🚀 Key Technical Features Illustrated

*   **Comprehensive Asset Whitelist:** Targets 26 critical data extensions covering cryptographic private keys (`.key`, `.pem`), security credentials, enterprise databases (`.sql`, `.sqlite`, `.xlsx`), network configurations, and local environment files (`.env`).
*   **Volatile Dynamic Delivery Server:** Employs multi-threaded background HTTP stagers running concurrently on the operator's attack platform to serve payload wrappers seamlessly on-demand.
*   **Volatile Memory Scrubbing:** Implements explicit programmatic RAM sanitization by overwriting key byte arrays with zeros (`0x00`) immediately after execution to prevent key exposure via forensic memory dumps.
*   **Anti-Forensic Timestomping:** Automatically copies the exact Creation, Last Write, and Last Access metadata timestamps from a trusted local system binary (e.g., `hosts`), blending the output `haul.dat` container into the target host's timeline.
*   **Zero-Footprint Self-Cleaning:** Clears all temporary flat directories, cleartext staging archives, and socket variables instantly on completion to minimize environmental footprints.
