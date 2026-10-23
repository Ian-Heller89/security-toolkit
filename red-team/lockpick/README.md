# 🔑 Lock Pick: Cross-Platform Payload Generator & Listener

A modular, cross-platform interactive command-line interface (CLI) toolkit written in **Python 3**. This tool automates the construction of native, dependency-free reverse shell payloads across **Windows**, **Linux**, and **macOS** environments, while concurrently hosting a resilient network architecture listener.

## ⚙️ Architecture Design Overview

In real-world red teaming operations, targeted endpoints frequently operate in varied, restricted, or mixed network ecosystems (e.g., Windows baselines lack default Python installations). To address this limitation, `Lock Pick` separates payload construction from the listener stack:

1. **Payload Generation (Target Side):** Leverages living-off-the-land (LotL) binaries and native scripting features (such as Base64 encoded PowerShell pipelines, netcat configurations, and native shell abstractions) to ensure payload execution without demanding secondary framework runtimes.
2. **Local Socket Listener (Attacker Side):** Employs pure `socket` structures to establish a robust raw TCP interceptor bound locally across all interfaces (`0.0.0.0`), bypassing interface binding loops.

## 🚀 Technical Features Illustrated

*   **Multi-Platform Payload Indexing:** Seamlessly switches target environments across Windows, Linux, and macOS.
*   **Living-Off-The-Land Implementation:** Automates utility variations like `certutil.exe` structures or Netcat fifo pipelines to slide past standard operating bounds.
*   **Asynchronous UX Routing:** Implements standard numerical error-trapping inputs (`999`) to provide step-back menu navigation and graceful session terminations.
*   **Zero External Dependencies:** Built using strictly default Python 3 standard modules (`socket`, `sys`, `base64`), eliminating setup friction during fast deployment.
