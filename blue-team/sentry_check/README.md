# 🛡️ SentryCheck: Multi-Sector Cryptographic File Integrity Monitor (FIM)

A production-grade, enterprise host security defensive module written in **Python 3**. This utility establishes an authoritative cryptographic baseline across critical operating system files, shell configuration initializations, core module drivers, and system scheduling directories to catch unauthorized persistence hooks and file manipulation tactics.

## ⚙️ Core Defensive Advantages

Once an adversary gains initial execution boundaries on an enterprise Linux node, they immediately focus on establishing continuous **Persistence** or privilege persistence vectors. This is frequently achieved by injecting rogue strings or backdoor keys into hidden startup configurations or scheduled cron directories. `SentryCheck` addresses this risk through strict verification tracking:

1. **Recursive Multi-Sector Traversal:** Extends beyond basic account files to monitor 14 key infrastructure documents and dynamically traverses 5 critical system-scheduling folders (`/etc/cron.*`) to map all sub-nested operational task profiles.
2. **Cryptographic Fingerprint Baseline:** Generates a secure, deterministic **SHA-256 hash snapshot database** (`sentry_baseline.json`) tracking precise file state baselines. Even a minor manipulation (single byte adjustment or added space) completely shifts the signature variance.
3. **Context-Aware Injection Analytics:** Compares active operational filesystem states to the snapshot index. It isolates modified files or missing records while dynamically highlighting unmapped file additions left behind in secure directories by automated red team tools.

## 🚀 Key Technical Features Illustrated

*   **Standardized Interactive Navigation Console:** Employs a crisp typographic input wrapper matching professional portfolio interface conventions and step-back mechanisms (`999`).
*   **Volatile Access Error Containment:** Implements safe read-handling controls to slide smoothly past permission variables or file system exceptions without experiencing engine lockups or freezing.
*   **Authoritative Posture Summary Matrix:** Features a clean data table layout generating detailed status logs tracking Intact, Modified, Missing, and Rogue asset files explicitly.
