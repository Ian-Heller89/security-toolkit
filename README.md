# 🛡️ Enterprise Security Toolkit

A multi-disciplinary, high-performance security simulation and auditing platform featuring production-ready tooling written in **Python**, **Go**, and **Rust**. This repository serves as a centralized operational hub showcasing modular implementations across offensive engineering (**Red Team**), telemetry detection diagnostics (**Blue Team**), and collaborative emulation harnesses (**Purple Team**).

## 🗂️ Repository Architecture

```text
security-toolkit/
├── red-team/
│   ├── 01_port_scanner/   # Multi-threaded concurrent network recon scanner
│   ├── lockpick/          # Cross-platform payload factory & raw TCP command listener
│   └── quitemouse/        # Host-agnostic post-exploitation audit engine & memory stager
├── blue-team/             # Telemetry log analysis, network monitoring, and signature detection
├── purple-team/           # Emulation harnesses mapped to the MITRE ATT&CK framework
└── notes/                 # Sanitized architectural research, protocols, and study logs
```

---

## 🚀 Active Production Tooling (Red Team Index)

### 1. Concurrency Network Port Scanner
*   **Core Utility:** Executes high-speed asynchronous port discovery and target-facing banner grabbing across open boundaries to identify exposed network footprints.
*   **Technical Implementation:** Written using multi-threaded execution pools to optimize transmission socket throughput without exhausting local descriptor pipelines.

### 2. Lock Pick: Payload Factory & Interceptor
*   **Core Utility:** Automates the construction of native, dependency-free reverse shell payloads while hosting a resilient, multi-platform local TCP listener.
*   **Technical Implementation:** Employs Base64 obfuscated PowerShell pipelines, native Zsh socket modules, and strict `0.0.0.0` attack-box interface binding to eliminate address collision loops.

### 3. Quiet Mouse: Post-Exploitation Audit Suite
*   **Core Utility:** Performs automated local system risk enumeration (SUID flags, Unquoted Service Paths, Active Directory domains, registry credential stores) on compromised hosts.
*   **Technical Implementation:** Features native Linux diagnostic loops combined with an on-demand background HTTP stager that delivers memory-only, fileless execution wrappers to Windows and macOS endpoints.

---

## 🛠️ Operational Engineering Roadmap

*   **Blue Team Folder (Phase 1):** Deploying an asynchronous SSH brute-force log parser and real-time network anomaly detector.
*   **Purple Team Folder (Phase 2):** Developing continuous attack/detection harnesses dynamically mapped to automated MITRE ATT&CK testing pathways.
*   **Cloud Infrastructure Auditing:** Building an automated multi-tenant AWS S3 bucket misconfiguration and IAM policy drift analyzer.

## ⚖️ Legal & Ethical Compliance Policy

All artifacts, tools, and execution stagers contained within this repository are engineered exclusively for authorized security research, educational simulation vectors, and legitimate white-hat testing boundaries. Execution is strictly restricted to sandboxed lab architecture, local virtual machine hypervisors, authorized platform playgrounds (e.g., Hack The Box, TryHackMe), or host systems where explicit, written administrative authorization and Rules of Engagement (RoE) have been formalized. 

Unauthorized deployment against third-party network properties is strictly prohibited and violates statutory regulations.
