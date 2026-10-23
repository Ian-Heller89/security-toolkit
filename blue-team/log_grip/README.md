# 🛡️ LogGrip: Asynchronous Authentication Monitor & Active Kernel Firewall Response Engine

A professional, high-performance defensive security utility written in **Python 3**. This tool provides real-time monitoring and active defense lines for enterprise Linux infrastructure, scanning system authentication logs asynchronously, isolating threat vectors via regular expression pattern analytics, and dynamically modifying network filters to isolate attackers instantly.

## ⚙️ Core Defensive Advantages

Automated brute-force attacks and network sweeps create massive validation strain on local authentication structures. Standard log checkers often parse historical entries passively, introducing significant latency before alert propagation. `LogGrip` is engineered to resolve these visibility gaps through active kernel-level response rules:

1. **Double-Filter Signature Scanners:** Features a multi-tiered regular expression matching engine optimized to catch sophisticated adversaries who try to disguise their brute-force scripts by rotating invalid accounts, system users, or standard usernames.
2. **Zero-Latency Stream Trailing:** Leverages low-overhead file stream pointer manipulation to catch new anomalies as they occur, ensuring attacks are flagged milliseconds after transmission rather than during post-incident analysis.
3. **Automated Active Kernel Mitigation:** Communicates directly with native Linux networking controls—**Uncomplicated Firewall (UFW)** and **`iptables` kernel filters**—to drop malicious source IP addresses automatically at the network layer.

## 🚀 Key Technical Features Illustrated

*   **Interactive Operational Console:** Implements a unified text menu mapping framework featuring structured numerical controls and standard graceful exit hooks (`999`).
*   **Kernel Block Verification Auditing:** Integrates direct sub-process hooks (`iptables -L`) to allow system administrators to view an active, live list of exactly which IP paths are currently blocked at the perimeter.
*   **Dynamic Network Flushing Reset:** Features an automated rule-clearing function (`iptables -F`) that cleanses temporary block pools, allowing an analyst to easily restore the original network baseline configuration on demand.
