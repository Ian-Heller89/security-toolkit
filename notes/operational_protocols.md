# 📓 Operational Protocols & Security Engineering Reference Logs
**Classification:** Internal Research Baseline / Portfolio Reference Log

This document houses the core architectural research, cryptographic mechanics, and host-level telemetry detection signatures mapped during the development of the multi-disciplinary enterprise security toolkit.

---

## 🔴 Section 1: Offensive Cryptodynamics & Forensics Evasion

### 1.1 The Vulnerability of Symmetric XOR Headers (Magic Bytes)
Standard network boundary detection filters and Endpoint Detection and Response (EDR) agents utilize signature-based heuristics to classify file formats by inspecting their leading byte constraints, commonly referred to as **Magic Bytes**. 

*   *Example:* A standard ZIP compressed archive always initializes with the specific hex signature string `50 4B 03 04` (ASCII: `PK`).
*   *The XOR Flaw (Known-Plaintext Attack):* Implementing a repeating bitwise XOR logic gate ($P \oplus K = C$) across an asset package offers insufficient protection against an analytical blue team classmate. If an investigator captures the output file stream and guesses or knows a single block of the underlying plaintext (such as the standard `PK` file header), they can mathematically extract your repeating key instantly by reversing the logical gate: $C \oplus P = K$.

### 1.2 Upgrading to Natively Sourced AES-256-CBC Protection
To enforce mathematical unbreakability that prevents packet-capturing tools (e.g., Wireshark) or disk analysts from decoding exfiltrated files, the toolkit transitions to **AES-256-CBC (Advanced Encryption Standard with Cipher Block Chaining)**. 

To maintain a zero-dependency footprint that evades suspicion from local defense scripts, the tool invokes pre-installed, trusted operating system abstractions directly in memory:
*   **Windows Subsystem:** Leverages the native Windows .NET cryptographic namespace API: `System.Security.Cryptography.AesManaged`.
*   **Unix Subsystem (Linux/macOS):** Spawns local pipeline streams directly through the built-in system core binaries: `openssl enc -aes-256-cbc -pbkdf2`.

### 1.3 Linux and Windows Host History Evasion Mechanics
Every keystroke entered into a standard command shell is recorded to plain-text local history caches on disk to assist administrators, creating a significant forensic trace file for incident responders.
*   *The Windows Risk:* PowerShell natively logs commands to `%userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`.
*   *The Unix Risk:* Linux and macOS write input command strings directly to hidden home file buffers (`~/.bash_history` or `~/.zsh_history`).
*   *The Containment Fix:* By calling native, non-echoing console input strings—PowerShell's `-AsSecureString` parameter or the Unix terminal `read -s` hidden stream flag—the passphrase string bypasses the terminal rendering display entirely. This prevents the operational data from ever being committed to local history log files on disk.
---

## 🔵 Section 2: Defensive Telemetry Analysis & Telemetry Hunting

### 2.1 Parsing Asynchronous Authentication Anomalies
Automated credential attacks generate a distinct forensic trail inside the operating system's localized text buffers. Threat hunters scan for elevated failure counts mapped from individual IP identifiers across a narrow time frame to isolate automated scans from normal user errors.

*   *Linux Telemetry Target:* `/var/log/auth.log` (Debian/Ubuntu) or `/var/log/secure` (RHEL/CentOS) [^21].
*   *Hardened Double-Filter Regular Expression Matching:* 
    `(?:Failed password for invalid user .* from|Failed password for .* from) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})` [^21]
*   *Mitigation Action:* Upon detecting an threshold breach (e.g., 5 failures in 10 seconds), the tool issues a synchronous sub-process rule injection command communicating directly with the network filter tables: `sudo iptables -A INPUT -s <IP> -j DROP` [^2].

### 2.2 Windows Process Masquerading & Memory Validation
Attackers attempt to evade detection by renaming their custom payload binaries to match trusted Windows core applications (e.g., naming an executable `svchost.exe` or `lsass.exe`) [^2]. Defensive tools interrogate the active process environment blocks natively via CIM pipelines (`Win32_Process`) [^2] to parse key structural red flags:

| Target Process Name | True Authoritative Image Path Location | Behavioral Anomaly Signal |
| :--- | :--- | :--- |
| `System` | None (Kernel Space Architecture) | Running with a Process ID (PID) other than **PID 4** |
| `lsass.exe` | `C:\Windows\System32\lsass.exe` | Loading out of user-writable directories (e.g., `Downloads\`) |
| `svchost.exe` | `C:\Windows\System32\svchost.exe` | Running without being spawned natively by `services.exe` |
| `cmd.exe` / `powershell.exe` | `C:\Windows\System32\` | Process parent identity matches an internet browser or user app |

---

## 🟣 Section 3: Purple Team Collaborative Continuous Validation

### 3.1 Establishing Closed-Loop Security Posture Metrics
Purple Teaming automates the synchronization between offensive tactical simulation and defensive rule verification. Rather than relying on static or unverified defensive assumptions, the **HarnessCore** framework automates an interactive engineering pipeline that executes a structured three-step lifecycle loop entirely in memory:

```text
  [1. RED EMULATION]         [2. BLUE VALIDATION]          [3. METRICS LOGGING]
Trigger a benign, localized  -> Interrogate host file structures -> Serialize the outcome to
MITRE ATT&CK technique         and kernel event arrays to       a centralized audit trail
(e.g., T1485 File Tampering)    verify visibility signatures     (purple_validation_report.json)
```

By keeping all generated file adjustments, mock audit entries, and variable arrays strictly contained within the tool's active directory, the validation test cycle remains completely non-destructive. This architecture guarantees a 100% stable execution footprint that evaluates telemetry rules flawlessly on both Linux (`.py`) and Windows (`.ps1`) nodes without requiring administrative privilege overrides or altering critical baseline root environments.
