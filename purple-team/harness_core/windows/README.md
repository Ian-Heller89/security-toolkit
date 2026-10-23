# 🧬 HarnessCore: Automated Windows MITRE ATT&CK Emulation & Validation Harness

A professional, high-fidelity security validation utility written in pure **Windows PowerShell (.ps1)**. This tool functions as a native, closed-loop purple team coordination framework, programmatically triggering safe, non-destructive offensive tactical actions mapped directly to the **MITRE ATT&CK Matrix** and immediately executing kernel-level telemetry audits to verify Windows defensive monitoring visibility.

## ⚙️ Core Operational Advantages

Security operations controls and logging policies require validation to guarantee visibility parameters are active across threat boundaries. Passive security engineering solutions often assume data ingestion rules function correctly without verifying telemetry end-to-end. `HarnessCore` addresses this engineering gap through automated testing automation loops:

1. **Deterministic Technique Emulation:** Safely triggers low-overhead system adjustments mimicking critical adversary tactics on Windows, including process shell scripting execution (**T1059.001**), hidden filesystem attribute injection (**T1564.001**), and system binary identity masquerading (**T1036.005**).
2. **Kernel-Level Defensive Verification:** Bypasses third-party dependencies by querying the Windows OS subsystem directly via native **WMI/CIM pipeline interfaces (`Win32_Process`)** and interrogating object attribute metadata to programmatically confirm if local security configurations successfully captured the infraction footprint.
3. **Structured Posture Reporting:** Consolidates testing metrics entirely within an automated local data index (`purple_validation_report.json`), generating formal metrics summaries separating validated execution chains from baseline defensive blind spots.

## 🚀 Key Technical Features Illustrated

*   **Production-Ready PowerShell Compliance:** Requires zero external modules or binary installations, allowing rapid deployment across enterprise workstations.
*   **Standardized Interactive Navigation Console:** Employs uniform layout criteria, matching alphanumeric choice mappings, and standard graceful teardown flags (`999`).
*   **Volatile Environment Self-Cleaning:** Integrates strict file tracking teardowns to purge mock configuration traces and temporary folder layouts safely upon tool exit.
