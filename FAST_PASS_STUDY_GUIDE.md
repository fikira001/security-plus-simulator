# CompTIA Security+ (SY0-701) Fast-Pass Strategy & Master Guide

> **Target Score:** 750 / 900 (Approx. 83.3%)  
> **Exam Duration:** 90 Minutes  
> **Total Questions:** Up to 90 (Includes Performance-Based Questions + Multiple Choice)

---

## 🚀 1. The 5 Exam Domains & Where to Focus

| Domain | Exam Weight | Key Focus Areas | Priority |
| :--- | :---: | :--- | :---: |
| **Domain 4.0: Security Operations** | **28%** | SIEM, SOAR, incident response playbooks, digital forensics, log analysis, vulnerability scanning | **HIGHEST** |
| **Domain 2.0: Threats, Vulnerabilities & Mitigations** | **22%** | Threat actors, attack types (XSS, SQLi, CSRF, DDoS), social engineering, malware types | **HIGHEST** |
| **Domain 5.0: Security Program Management & Oversight** | **20%** | Governance, risk management formulas (ALE/SLE), privacy (GDPR/HIPAA), compliance & audits | **HIGH** |
| **Domain 3.0: Security Architecture** | **18%** | Cloud models, Zero Trust architecture, network segmentation, firewalls, proxies, VPNs | **MEDIUM** |
| **Domain 1.0: General Security Concepts** | **12%** | CIA triad, AAA, control categories (technical/operational/managerial), cryptography basics | **FOUNDATION** |

> 💡 **Golden Rule:** **Domain 4 + Domain 2 make up 50% of your entire exam score!** If you master log analysis, incident response, threat actors, and attack vectors, you are already halfway to passing.

---

## 🎯 2. Real Exam Strategy & Time Management

1. **The PBQ Trap (First 1–5 Questions):**
   - On the real Pearson VUE exam, **Performance-Based Questions (PBQs)** appear *first*.
   - **Do NOT get stuck on PBQs!** They can consume 20+ minutes if you are not careful.
   - **Strategy:** Flag the PBQs immediately, skip straight to Question 6 (Multiple Choice), answer all multiple-choice questions in ~50 minutes, and return to the PBQs with 35–40 minutes remaining.

2. **Multi-Select Question Mastery:**
   - Pay close attention to questions requiring multiple answers (`Select TWO` or `Select THREE`).
   - The simulator dynamically informs you of how many options are required (e.g. `1 of 2 selected`).
   - In multi-select questions, look for distinct layers of defense (e.g., one technical control and one administrative control, or prevention plus detection).

3. **Log & Packet Capture Analysis:**
   - Stems featuring firewall logs, IPS alerts, and packet dumps are rendered in dedicated terminal boxes.
   - Look for:
     - **Source & Destination IPs / Ports** (e.g., port 80/443 = Web, port 22 = SSH, port 1433 = SQL Server).
     - **HTTP Methods & Payloads** (e.g., `' OR '1'='1` indicates SQLi; `<script>` indicates XSS).
     - **Action Results** (e.g., `blocked`, `dropped`, `permitted`).

---

## 🧠 3. High-Yield Acronyms & Formulas You MUST Know

### Quantitative Risk Formulas:
- $\text{SLE} = \text{AV} \times \text{EF}$ (Single Loss Expectancy = Asset Value $\times$ Exposure Factor)
- $\text{ALE} = \text{SLE} \times \text{ARO}$ (Annualized Loss Expectancy = Single Loss Expectancy $\times$ Annualized Rate of Occurrence)
- **MTBF** (Mean Time Between Failures): Operational uptime before breakdown.
- **MTTR** (Mean Time To Repair): Time required to restore service.
- **RTO** (Recovery Time Objective): Maximum acceptable downtime.
- **RPO** (Recovery Point Objective): Maximum acceptable data loss duration.

### Essential Ports & Protocols:
- `22`: **SSH / SFTP / SCP** (Encrypted remote terminal & file transfer)
- `53`: **DNS** (Domain Name System)
- `88`: **Kerberos** (Authentication service)
- `123`: **NTP** (Network Time Protocol — critical for log sync)
- `389 / 636`: **LDAP / LDAPS** (Directory service cleartext vs TLS)
- `443`: **HTTPS** (Web traffic encrypted over TLS)
- `445`: **SMB** (Windows file sharing)
- `1812 / 1813`: **RADIUS** (Authentication / Accounting)
- `3389`: **RDP** (Remote Desktop Protocol)

### NIST Incident Response Lifecycle (PICERL):
1. **Preparation**: Hardware kits, playbooks, communication channels.
2. **Identification (Detection & Analysis)**: Alert triage, verifying IoCs, scoping impact.
3. **Containment**: Isolating infected systems from the network.
4. **Eradication**: Removing malware, revoking compromised credentials, patching.
5. **Recovery**: Restoring systems from verified backups, monitoring.
6. **Lessons Learned**: Post-mortem review within 2 weeks.

---

## 🖥️ 4. How to Use the Built-in Study Suite

1. **Launch:** Double-click **`Start-Exam-Simulator.bat`** (or run `python server.py`).
2. **Read the Domain Guides:** Head to **Domain Guides** in the top navigation bar to read comprehensive notes for each domain with live search.
3. **Drill Weak Spots:** Use **Domain Drills** in Study Mode for instant answer explanations.
4. **Practice PBQs:** Master the 15 authentic PBQ simulations in the **PBQ Lab**.
5. **Run Full Mocks:** Take Exams A, B, C, and Dynamic Randomizer exams.
6. **Detailed Review:** After every exam, use the **Question Navigator Jump Grid** to review full option breakdowns and explanations for any question you missed.
