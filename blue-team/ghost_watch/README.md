# 🪟 GhostWatch: Windows Native Process Anomaly Detection Engine

A professional, zero-dependency host defensive security module written in pure **Windows PowerShell (.ps1)**. This tool interfaces directly with the native Windows kernel architecture via the Common Information Model (CIM) to map active system memory spaces, parse parent-child relationship loops, and isolate stealthy memory masquerading, process hollowing, and living-off-the-land execution techniques.

## ⚙️ Core Defensive Advantages

Advanced adversaries and modern red team payloads frequently run completely fileless or hide process execution traces directly within volatile RAM. By masquerading malicious payloads under legitimate operating system binary identities (such as `svchost.exe`), hollowing process memory structures, or leveraging built-in administrative tools, they easily bypass standard filesystem security scanners. `GhostWatch` eliminates these visibility blind spots natively:

1. **Kernel-Level Object Triage:** Avoids the third-party dependency trap by querying the Windows OS subsystem directly via native **WMI/CIM pipeline interfaces (`Win32_Process`)**, guaranteeing high-fidelity forensics on unhardened target machines.
2. **Process Hollowing & Injection Detection:** Inspects active task blocks for empty or null executable path variables. If a running process has stripped its image pathway within the kernel tables, it isolates it instantly as a high-risk hidden memory injection signature.
3. **Masquerade Directory & PID Validation:** Cross-references active binary names against true physical disk load locations and static system properties, catching rogue binaries masquerading outside `System32` or mimicking the core system process ID structure (PID 4 validation).
4. **Living-off-the-Land (LotL) Analysis:** Monitors high-risk dual-use administrative binaries (e.g., `certutil.exe`, `bitsadmin.exe`, `vssadmin.exe`) spawned unexpectedly by unprivileged client applications, web browsers, or basic script interpreters.

## 🚀 Key Technical Features Illustrated

*   **Production-Ready PowerShell Compliance:** Written in native, administrative shell script parameters to guarantee execution out of standard incident response toolkits without forcing dependencies onto targets.
*   **Structured Interactive Navigation Layout:** Implements uniform option arrays and standard step-back parameters (`999`) matching professional repository engineering metrics.
*   **Context-Aware Posture Summary Matrix:** Generates clean, real-time telemetry console dumps highlighting active target metrics, PID references, and exact behavioral warning flags.
