# 🛡️ Enterprise Security Toolkit

A multi-disciplinary, high-performance security simulation, operational auditing, and real-time defense validation platform featuring production-ready tooling written in **Python 3** and native **Windows PowerShell**. This repository serves as a centralized operational hub showcasing modular implementations across offensive engineering (**Red Team**), telemetry detection forensics (**Blue Team**), and collaborative testing automation (**Purple Team**).

## 🗂️ Repository Architecture

```text
security-toolkit/
├── red-team/
│   ├── flyby/             # Multi-threaded concurrent network recon scanner
│   ├── lockpick/          # Cross-platform payload factory & raw TCP command listener
│   ├── quitemouse/        # Host-agnostic post-exploitation audit engine & memory stager
│   └── shadow_haul/       # Zero-interaction multi-OS data discovery & hardened AES-256 packer
├── blue-team/
│   ├── log_grip/          # Asynchronous Linux auth monitor & active firewall blocker
│   ├── sentry_check/      # Multi-sector cryptographic file integrity monitor (FIM)
│   ├── ghost_watch/       # Windows native memory process anomaly detection engine
│   └── deep_trace/        # Windows native incident response forensic triage harvester
├── purple-team/
│   └── harness_core/
│       ├── linux/         # Python 3 MITRE ATT&CK emulation & log validation engine
│       └── windows/       # PowerShell MITRE ATT&CK emulation & kernel validation engine
└── notes/                 # Sanitized architectural research, protocols, and study logs
```

---

## 🚀 Active Production Tooling Index

### 🔴 Offensive Security Engineering (Red Team)

1. **FlyBy: Concurrency Network Port Scanner**
   *   *Utility:* Executes high-speed asynchronous port discovery and target-facing banner grabbing across open boundaries to identify exposed network footprints.
   *   *Implementation:* Written using multi-threaded execution pools to optimize transmission socket throughput without exhausting local descriptor pipelines.

2. **Lock Pick: Payload Factory & Interceptor**
   *   *Utility:* Automates the construction of native, dependency-free reverse shell payloads while hosting a resilient, multi-platform local TCP listener.
   *   *Implementation:* Employs Base64 obfuscated PowerShell pipelines, native Zsh socket modules, and strict `0.0.0.0` attack-box interface binding to eliminate address collision loops.

3. **Quiet Mouse: Post-Exploitation Audit Suite**
   *   *Utility:* Performs automated local system risk enumeration (SUID flags, Unquoted Service Paths, Active Directory domains, registry credential stores) on compromised hosts.
   *   *Implementation:* Features native Linux diagnostic loops combined with an on-demand background HTTP stager that delivers memory-only, fileless execution wrappers to Windows and macOS endpoints.

4. **Shadow Haul: High-Value Asset Cryptographic Staging Suite**
   *   *Utility:* Automatically identifies and harvests critical corporate documents, private keys, and database configurations using a strict 26-extension whitelist, packing them into encrypted structures.
   *   *Implementation:* Enforces zero-interaction path expansion and military-grade **AES-256 Symmetric Encryption** [11] (utilizing native Windows .NET and Mac OpenSSL libraries). Features volatile RAM memory scrubbing, silent input console history evasion, privilege-safe fallback error-trapping, and file timestamp metadata timestomping.

### 🔵 Defensive Operations & Incident Response (Blue Team)

1. **LogGrip: Asynchronous Auth Monitor & Automated Firewall Blocker**
   *   *Utility:* Monitors live Linux server authentication logs asynchronously to flag ongoing brute-force sweeps and malicious access attempts.
   *   *Implementation:* Deploys an expanded double-filter regular expression engine to track authentication failure patterns within strict rolling time windows, communicating directly with **`iptables`** or **`ufw`** to drop attacking IP addresses instantly at the kernel layer.

2. **SentryCheck: Cryptographic File Integrity Monitor (FIM)**
   *   *Utility:* Establishes an authoritative security snapshot baseline across core system account files, shell configurations, driver modules, and scheduling directories to catch unauthorized persistence hooks.
   *   *Implementation:* Runs a directory-aware recursive file crawler that generates deterministic **SHA-256 hash baselines** (`sentry_baseline.json`), cross-referencing files in real time to isolate modified records, deleted parameters, or rogue file injections.

3. **GhostWatch: Windows Process Anomaly Memory Scanner**
   *   *Utility:* Scans active Windows system memory spaces natively to hunt for stealthy process hollowing, fileless malware injections, and credential spoofing.
   *   *Implementation:* Written in pure, dependency-free **Windows PowerShell**. Queries the Windows kernel via native **WMI/CIM pipelines (`Win32_Process`)** to validate core system processes, catch null executable image paths, verify strict PID 4 system boundaries, and flag browser-spawned command shells.

4. **DeepTrace: Windows Native Incident Response Triage Harvester**
   *   *Utility:* Automates rapid, volatile evidence acquisition and host data carving during active compromise scenarios to capture forensic indicators before they vanish from memory.
   *   *Implementation:* Native PowerShell script that harvests outbound/listening network sockets, carves cleartext console history caches (`ConsoleHost_history.txt`), extracts memory-resident DNS client lookups, and captures active terminal user sessions. All extracted datasets are programmatically compiled into a standalone, human-readable **HTML Investigator Dashboard Report** for immediate tactical evaluation.

### 🟣 Coordinated Continuous Validation (Purple Team)

1. **HarnessCore: Cross-Platform MITRE ATT&CK Testing Suite**
   *   *Utility:* Combines offensive tactical execution and defensive validation tracking into an automated, single-command system posture checking loop.
   *   *Implementation:* Split into separate, specialized cross-platform automation scripts to evaluate environments completely natively:
       *   **Linux Component (`.py`):** Coordinates safe local simulations for command interpreter execution (**T1059.004**), unauthorized infrastructure file modifications (**T1485**), and credential account persistence indicators (**T1136.001**), cross-checking disk and log arrays for tracking visibility.
       *   **Windows Component (`.ps1`):** Leverages native PowerShell to trigger hidden scripting execution (**T1059.001**), hidden file attribute injections (**T1564.001**), and core system binary masquerading (**T1036.005**), programmatically querying the **CIM process tables** and Win32 file handles to detect security blind spots.

---

## 🛠️ Operational Engineering Roadmap

*   **Cloud Infrastructure Auditing:** Building an automated multi-tenant AWS S3 bucket misconfiguration and IAM policy drift analyzer.
*   **Active Directory Posture Hardening:** Engineering an automated Kerberoasting and AS-REP roasting tracking baseline validation script.

## ⚖️ Legal & Ethical Compliance Policy

All artifacts, tools, and execution stagers contained within this repository are engineered exclusively for authorized security research, educational simulation vectors, and legitimate white-hat testing boundaries. Execution is strictly restricted to sandboxed lab architecture, local virtual machine hypervisors, authorized platform playgrounds (e.g., Hack The Box, TryHackMe), or host systems where explicit, written administrative authorization and Rules of Engagement (RoE) have been formalized. 

Unauthorized deployment against third-party network properties is strictly prohibited and violates statutory regulations.
