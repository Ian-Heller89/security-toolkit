# 🔍 DeepTrace: Windows Native Incident Response (IR) Forensic Triage Harvester

A production-grade, zero-dependency host forensic acquisition utility written in pure **Windows PowerShell (.ps1)**. This application automates the rapid capture of critical, volatile system artifacts during live security incidents, compiling data structures natively and formatting evidence logs into an interactive, human-readable HTML investigator report dashboard.

## ⚙️ Core Defensive Advantages

When an enterprise endpoint is compromised, volatile forensic indicators sitting in temporary memory spaces vanish completely upon host reboot or connection loss. Manual incident triage across discrete command-line interfaces slows response boundaries and creates log clutter. `DeepTrace` handles these investigative bottlenecks natively through standardized rapid data carving:

1. **Volatile Network Mapping Retention:** Sweeps the OS network stack directly to grab active sockets, listing ports, and process IDs (`Get-NetTCPConnection`), instantly exposing external reverse shell C2 destinations.
2. **Plain-Text Console History Carving:** Locates, sanitizes, and carves hidden terminal profiles (`ConsoleHost_history.txt`), retrieving the full string logs of instructions executed by attackers while evading output character injection risks via structural HTML encoding.
3. **Memory DNS Cache Extraction:** Queries internal memory resolution databases (`Get-DnsClientCache`) to pull recent web domain resolutions, highlighting hidden beacons or suspicious download channels used by malware.
4. **Active Session Token Auditing:** Logs active concurrent connections and interactive profiles natively (`query user`), letting an investigator immediately identify lateral movement vectors or live session theft.

## 🚀 Key Technical Features Illustrated

*   **Integrated HTML Dashboard Compilation:** Programmatically parses, structures, and compiles all raw telemetry dumps into a clean, standalone interactive HTML investigator file (`Triage_Report.html`) for rapid management analysis.
*   **Production-Ready PowerShell Compliance:** Requires zero external modules or binary installations, allowing execution straight out of security response thumb-drives.
*   **Structured Interactive Navigation Layout:** Adheres to uniform layout conventions featuring distinct alphanumeric menu navigation arrays and standard step-back parameters (`999`).
