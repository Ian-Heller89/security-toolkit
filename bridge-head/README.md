# ⚡ BridgeHead: Automated Perimeter Tunneling & External Network Mapper

A zero-dependency, root-level network architecture utility written in **Python 3**. `BridgeHead` automates remote port forwarding and WAN edge tracking for security operators testing software or staging listeners behind separate routers, firewalls, or carrier-grade NAT (CGNAT) environments. It establishes a live, internet-routable ingress gateway without requiring manual port forwarding or external API token configurations.

## ⚙️ Core Operational Advantages

During red team assessments, threat emulation, or lab testing across separate networks, private IP addresses (e.g., `192.168.x.x` or `10.x.x.x`) are unreachable by target assets located behind different routers. Traditional port forwarding is rarely an option on enterprise networks or university campuses due to administrative restrictions. `BridgeHead` addresses this routing hurdle natively:

1. **Automated Layer-3 Mapping:** Instantly queries private network interfaces and correlates them against public outbound WAN gateways using built-in Python network sockets, establishing an immediate baseline of active routing paths.
2. **Zero-Setup SSH Reverse Proxying:** Avoids the third-party dependency trap (eliminating the need for custom binary installations, account creation, or API keys). The tool spawns a background, keyless SSH reverse tunnel (`localhost.run`), directing public servers to forward external internet traffic straight to the operator's designated local ingress port.
3. **Frictionless Edge Routing Pipeline:** Generates a secure, unique, and public internet domain name (e.g., `example.lhr.life`). This allows remote payloads or reverse stagers executing on external, isolated networks to resolve and route traffic over standard web ports (Port 80) straight back to the local attack box.

## 🚀 Key Technical Features Illustrated

*   **Zero-Dependency Portability:** Written entirely in standard, native Python 3 standard libraries to guarantee immediate execution across any default Kali Linux or standard terminal environment.
*   **Background Tunnel Subprocess Control:** Spawns and manages the underlying SSH routing infrastructure as a non-blocking background thread, preserving terminal focus while dynamically parsing incoming domain string variables.
*   **Volatile Session Collapse Handler:** Implements tight keyboard interrupt monitoring (`Ctrl+C`). Upon termination, the utility forces an explicit teardown sequence to close active background sockets and restore strict local system isolation instantly.
