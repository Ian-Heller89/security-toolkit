# 🐭 Quiet Mouse: Host-Agnostic Post-Exploitation Auditing Engine & Web Stager

A professional, modular local post-exploitation auditing toolkit written in **Python 3**. This tool provides hybrid operational deployment workflows: it can conduct native, low-footprint internal security audits on **Linux** hosts natively, while doubling as a multi-threaded **Windows** (PowerShell) and **macOS** (Zsh) memory-only payload generator and stager.

## ⚙️ Core Architectural Advantages

Standard post-exploitation automation tools often rely heavily on complex binary configurations or dropping massive scripts directly onto a victim's filesystem. `Quiet Mouse` is engineered to address target restrictions and security baseline variables through a split-execution architecture:

1. **Native Linux Diagnostics Mode:** Operates immediately and locally inside any default Unix terminal room with zero network overhead, checking for environmental misconfigurations, permissive task schedules, and privilege parameters.
2. **On-Demand Cross-Platform Web Staging:** When targeting Windows or macOS endpoints, the attacker's master platform launches an on-demand, multi-threaded background HTTP server framework. Rather than compiling heavy executables or forcing Python onto targets, it builds a native, lightweight one-liner command stream.

## 🚀 Key Technical Features Illustrated

*   **Fileless Memory Execution:** Generates custom PowerShell `IEX` and Zsh `curl` stagers that pull full auditing modules straight into the target system's temporary memory (RAM), avoiding common static disk footprint analysis flags.
*   **Comprehensive Privilege Risk Enumeration:** Audits critical privilege vectors including **Unquoted Service Paths**, Active Directory logon domain mappings, local credential store registries, SUID permissions, and shadow configurations.
*   **Asynchronous Interface Routing:** Leverages clean numerical menu input mapping loops and unified step-back controls (`999`) to provide robust console navigation.
*   **Graceful Auto-Teardown Framework:** Implements strict environment cleanup procedures on termination, closing listening network card ports instantly and deleting staging files to leave zero traces on the master system.
