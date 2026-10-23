# 🧬 HarnessCore: Automated Linux MITRE ATT&CK Emulation & Validation Harness

A professional, high-fidelity security validation utility written in **Python 3**. This tool functions as a closed-loop purple team coordination framework, programmatically triggering safe, non-destructive offensive tactical actions mapped directly to the **MITRE ATT&CK Matrix** and immediately executing forensic telemetry audits to verify host defensive logging posture.

## ⚙️ Core Operational Advantages

Security operations controls and logging policies require validation to guarantee visibility parameters are active across threat boundaries. Passive security engineering solutions often assume data ingestion rules function correctly without verifying telemetry end-to-end. `HarnessCore` addresses this engineering gap through automated testing automation loops:

1. **Deterministic Technique Emulation:** Safely triggers low-overhead system adjustments mimicking critical adversary tactics, including process command interpreter manipulation (**T1059.004**), unauthorized infrastructure file modifications (**T1485**), and credential log persistence tracking (**T1136.001**).
2. **Automated Defensive Verification:** Inspects local active data sectors, log files, and size metrics milliseconds after the offensive trigger to programmatically confirm if local security configurations successfully captured the infraction footprint.
3. **Structured Posture Reporting:** Consolidates testing metrics entirely within an automated local data index (`purple_validation_report.json`), generating formal metrics summaries separating validated execution chains from baseline defensive blind spots.

## 🚀 Key Technical Features Illustrated

*   **Standardized Interactive Navigation Console:** Employs uniform layout criteria, matching alphanumeric choice mappings, and standard graceful teardown flags (`999`).
*   **Volatile Environment Self-Cleaning:** Integrates strict file tracking teardowns to purge mock configuration traces and scratch logs safely upon tool exit.
*   **Privilege-Safe Logic Traps:** Features comprehensive exception handling bounds to preserve smooth tool operations across unprivileged system user constraints without experiencing process lockups.
