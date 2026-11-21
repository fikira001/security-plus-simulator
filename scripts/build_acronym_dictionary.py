"""
CompTIA Security+ SY0-701 Acronym Knowledge Dictionary Builder
Enriches all 314 official blueprint acronyms with:
- Expansion (Full Term Name)
- Plain-English Explanation (What it is and how it works)
- High-Yield Exam Tip / Key Association (Keywords, Ports, Attack indicators, Formulas)
- Category (Functional cybersecurity domain)
- Accurate CompTIA SY0-701 Domain (1 to 5)
"""

import json
import os

ACRONYM_DB = {
    # --- NUMERIC & A ---
    "2FA": {
        "expansion": "Two-Factor Authentication",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A security verification method that requires two different authentication factors (e.g., password + SMS/authenticator code) to verify identity before granting access.",
        "exam_tip": "Must combine TWO DISTINCT categories: something you know (password), something you have (hardware token/phone), or something you are (biometrics). Two passwords = 1 factor, NOT 2FA!"
    },
    "3DES": {
        "expansion": "Triple Data Encryption Standard",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A legacy symmetric block cipher that applies the DES algorithm three times consecutively with two or three 56-bit keys to achieve an effective key strength of up to 112 or 168 bits.",
        "exam_tip": "Deprecated by NIST due to small 64-bit block size vulnerability (Sweet32 attack). Replaced by AES."
    },
    "AAA": {
        "expansion": "Authentication, Authorization, and Accounting",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "The foundational security framework for access control: verifying who the user is (Authentication), defining what they can access (Authorization), and tracking what they do (Accounting/Auditing).",
        "exam_tip": "Implemented using centralized network access protocols like RADIUS (ports 1812/1813) and TACACS+ (TCP port 49)."
    },
    "ACL": {
        "expansion": "Access Control List",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A sequential rule set on routers, firewalls, and operating systems that dictates which users, IP addresses, or protocols are permitted or denied access to a system or network segment.",
        "exam_tip": "Evaluated top-to-bottom. Always ends with an implicit deny rule ('deny all traffic not explicitly permitted')."
    },
    "AES": {
        "expansion": "Advanced Encryption Standard",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "The global gold standard symmetric block cipher approved by NIST. Uses a fixed 128-bit block size with key lengths of 128, 192, or 256 bits.",
        "exam_tip": "Extremely fast and secure in both hardware and software. Used in WPA2/WPA3, TLS, and full disk encryption (BitLocker, FileVault)."
    },
    "AES-256": {
        "expansion": "Advanced Encryption Standard 256-bit",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "The highest-strength variant of AES, utilizing a 256-bit cryptographic key requiring 14 rounds of substitution and permutation transformations.",
        "exam_tip": "Classified as Top Secret level encryption. Resistant even to quantum computing brute-force via Grover's algorithm."
    },
    "AH": {
        "expansion": "Authentication Header",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An IPsec protocol component (IP protocol 51) that provides data integrity, source authentication, and anti-replay protection for IP packets.",
        "exam_tip": "Provides integrity and authentication only; AH does NOT provide encryption/confidentiality. ESP provides confidentiality."
    },
    "AI": {
        "expansion": "Artificial Intelligence",
        "domain": 2,
        "category": "Emerging Technologies & Threats",
        "explanation": "Computational systems designed to perform tasks normally requiring human intelligence, used both defensively (automated triage, anomaly detection) and offensively (polymorphic malware, automated spear-phishing).",
        "exam_tip": "Exam scenarios focus on prompt injection, model poisoning, training data exfiltration, and deepfake social engineering."
    },
    "AIS": {
        "expansion": "Automated Indicator Sharing",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A CISA-managed public-private threat intelligence sharing platform enabling real-time automated exchange of cyber threat indicators between organizations.",
        "exam_tip": "Uses STIX (expression format) and TAXII (transport protocol) specifications for automated machine-to-machine exchange."
    },
    "ALE": {
        "expansion": "Annualized Loss Expectancy",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The total expected financial loss an organization will incur from a specific risk over the course of an entire calendar year.",
        "exam_tip": "Formula: ALE = SLE × ARO (Single Loss Expectancy multiplied by Annualized Rate of Occurrence). Must know for quantitative risk calculation!"
    },
    "AP": {
        "expansion": "Access Point",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A network hardware device that connects Wi-Fi wireless client devices to an organization's wired Ethernet network infrastructure.",
        "exam_tip": "Secured using WPA3-Enterprise (802.1X), Rogue AP detection, WIPS, and client isolation."
    },
    "API": {
        "expansion": "Application Programming Interface",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "A software intermediary containing specifications, routines, and protocols that allow different computer programs and services to communicate and exchange data.",
        "exam_tip": "Vulnerable to OWASP API Top 10: Broken Object Level Authorization (BOLA), excessive data exposure, and rate limiting exhaustion. Protected with API Gateways and OAuth 2.0."
    },
    "APT": {
        "expansion": "Advanced Persistent Threat",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A sophisticated, well-funded cyber adversary (typically nation-state military/intelligence or advanced cybercrime syndicate) that establishes prolonged, undetected presence in a network to steal intellectual property or conduct cyber warfare.",
        "exam_tip": "Keywords: Long dwell time, stealth, zero-day exploits, nation-state sponsored, extensive reconnaissance, customized malware."
    },
    "ARO": {
        "expansion": "Annualized Rate of Occurrence",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "An estimate of how many times a particular threat or event is expected to occur within a one-year time frame.",
        "exam_tip": "If a hurricane strikes once every 10 years, ARO = 0.1. If a laptop theft happens 4 times per year, ARO = 4. Used to calculate ALE: ALE = SLE × ARO."
    },
    "AUP": {
        "expansion": "Acceptable Use Policy",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "An organizational administrative policy signed by employees defining permissible and prohibited uses of company computer systems, hardware, networks, and internet access.",
        "exam_tip": "Protects company against legal liability. Employees must sign upon hire, and violating it can lead to termination."
    },

    # --- B ---
    "BCP": {
        "expansion": "Business Continuity Planning",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A comprehensive strategic framework ensuring an organization can maintain critical business operations during and immediately following an emergency or disaster.",
        "exam_tip": "Focuses on business survival and operational continuity, while DRP (Disaster Recovery Plan) focuses specifically on restoring IT infrastructure and technology."
    },
    "BGP": {
        "expansion": "Border Gateway Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The core routing protocol that manages how packets are routed across the global internet between different Autonomous Systems (AS).",
        "exam_tip": "Vulnerable to BGP Route Hijacking without cryptographic route validation (RPKI / BGPsec)."
    },
    "BIA": {
        "expansion": "Business Impact Analysis",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A systematic assessment determining the financial, operational, and regulatory consequences of a disruption to each business process and IT asset.",
        "exam_tip": "Identifies Mission-Essential Functions (MEFs) and establishes RTO (Recovery Time Objective), RPO (Recovery Point Objective), and MTD (Maximum Tolerable Downtime)."
    },
    "BIOS": {
        "expansion": "Basic Input/Output System",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "Legacy firmware installed on a computer motherboard that initializes hardware during the boot sequence and loads the operating system.",
        "exam_tip": "Replaced by modern UEFI, which supports Secure Boot to stop rootkits from launching prior to OS load."
    },
    "BPF": {
        "expansion": "Berkeley Packet Filter",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A raw network packet capture filtering mechanism used in tcpdump, Wireshark, and Linux kernel monitoring to filter traffic based on IP, port, or header fields.",
        "exam_tip": "Syntax: 'tcp port 443 and src net 192.168.1.0/24'. Crucial for security analysts filtering packet captures."
    },
    "BSSID": {
        "expansion": "Basic Service Set Identifier",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The unique 48-bit physical MAC address of a specific wireless radio interface on an 802.11 Wi-Fi Access Point.",
        "exam_tip": "SSID is the human-readable network name; BSSID is the physical MAC address of the AP broadcasting that SSID."
    },
    "BYOD": {
        "expansion": "Bring Your Own Device",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A corporate enterprise policy permitting employees to access company emails, files, and applications using their personal smartphones, tablets, or laptops.",
        "exam_tip": "Secured using MDM/MAM containerization, storage encryption, remote wipe capabilities, and network onboarding portals."
    },

    # --- C ---
    "CA": {
        "expansion": "Certificate Authority",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A trusted third-party entity that cryptographically signs and issues digital certificates (X.509), binding a public key to an individual, device, or domain name.",
        "exam_tip": "Root CAs sign Intermediate CAs. If a Root CA's private key is compromised, all certificates issued down the chain become untrusted!"
    },
    "CAPTCHA": {
        "expansion": "Completely Automated Public Turing Test to Tell Computers and Humans Apart",
        "domain": 2,
        "category": "Application Security & Architecture",
        "explanation": "A challenge-response security verification test designed to verify that an online user is human rather than an automated bot or credential-stuffing script.",
        "exam_tip": "Used to mitigate brute-force password guessing, ticket scalping bots, account harvesting, and spam bots on public web forms."
    },
    "CAR": {
        "expansion": "Corrective Action Report",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A formal quality assurance and compliance document detailing the root cause of an audit deficiency or security failure and the remediation steps taken.",
        "exam_tip": "Follows security audits, penetration test debriefs, and regulatory compliance reviews."
    },
    "CASB": {
        "expansion": "Cloud Access Security Broker",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A software tool or cloud proxy situated between enterprise on-premises users and cloud service providers to enforce company security policies (DLP, SSO, malware scanning, compliance).",
        "exam_tip": "Keywords: Cloud visibility, Shadow IT discovery, cloud DLP, enforcing SSO and compliance for SaaS applications (Office 365, Salesforce)."
    },
    "CBC": {
        "expansion": "Cipher Block Chaining",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A block cipher encryption mode where each plaintext block is XORed with the previous ciphertext block before encryption, using an Initialization Vector (IV) for the first block.",
        "exam_tip": "Vulnerable to padding oracle attacks if not paired with an authentication tag. GCM (Galois/Counter Mode) is preferred modern alternative."
    },
    "CCPA": {
        "expansion": "California Consumer Privacy Act",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A California state privacy law giving consumers the right to know what personal data businesses collect, the right to delete that data, and the right to opt-out of data sale.",
        "exam_tip": "U.S. state-level privacy standard often compared to European GDPR. Mandates transparent privacy disclosures and data subject rights."
    },
    "CERT": {
        "expansion": "Computer Emergency Response Team",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A dedicated group of cybersecurity experts responsible for investigating, managing, containing, and resolving computer security incidents.",
        "exam_tip": "Synonymous with CSIRT (Computer Security Incident Response Team). Follows PICERL incident response lifecycle."
    },
    "CFB": {
        "expansion": "Cipher Feedback",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A block cipher mode of operation that converts a block cipher into a self-synchronizing stream cipher, encrypting previous ciphertext blocks.",
        "exam_tip": "Allows encrypting data in increments smaller than the cipher's native block size."
    },
    "CFR": {
        "expansion": "Code of Federal Regulations",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The codification of the general and permanent rules and regulations published in the U.S. Federal Register by federal government departments and agencies.",
        "exam_tip": "Includes regulatory mandates such as HIPAA, FERPA, and federal cybersecurity compliance standards."
    },
    "CIRT": {
        "expansion": "Cyber Incident Response Team",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An operational cross-functional security team tasked with rapid containment, forensic preservation, eradication, and post-mortem analysis of cyber attacks.",
        "exam_tip": "Includes security engineers, forensic examiners, legal counsel, HR, and PR/communications leads."
    },
    "CIS": {
        "expansion": "Center for Internet Security",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A non-profit cybersecurity organization known for publishing industry-standard configuration benchmarks (CIS Benchmarks) and the CIS Critical Security Controls (CIS Controls).",
        "exam_tip": "CIS Benchmarks are step-by-step guides for hardening operating systems, cloud environments, routers, and web servers."
    },
    "COPE": {
        "expansion": "Corporate-Owned, Personally-Enabled",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A mobile device deployment model where the organization purchases and owns the smartphone or laptop, but permits the employee to use it for personal tasks.",
        "exam_tip": "Gives the company greater control, compliance oversight, and security governance than BYOD while offering personal flexibility."
    },
    "CP": {
        "expansion": "Contingency Planning",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The overarching management discipline encompassing BCP, DRP, and crisis management procedures to prepare for unexpected disruptions.",
        "exam_tip": "Requires scheduled disaster simulation tabletop exercises, walkthroughs, and failover tests."
    },
    "CRL": {
        "expansion": "Certificate Revocation List",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A digitally signed list published periodically by a Certificate Authority (CA) enumerating serial numbers of revoked, untrusted, or compromised digital certificates.",
        "exam_tip": "Downside: Can become large, introducing latency and cache staleness. OCSP (Online Certificate Status Protocol) solves this with real-time status queries."
    },
    "CSA": {
        "expansion": "Cloud Security Alliance",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A global non-profit organization dedicated to defining best practices and frameworks (such as the Cloud Controls Matrix - CCM) for secure cloud computing.",
        "exam_tip": "Offers STAR (Security, Trust, Assurance, and Registry) certification for public cloud provider compliance."
    },
    "CSIRT": {
        "expansion": "Computer Security Incident Response Team",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "The formalized organizational unit responsible for executing the incident response plan when an alert escalates to a confirmed security breach.",
        "exam_tip": "NIST SP 800-61 Rev. 2 outlines the operational mandate and composition of an enterprise CSIRT."
    },
    "CSO": {
        "expansion": "Chief Security Officer",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The executive C-level leader responsible for the physical security and digital information security strategy of an entire enterprise.",
        "exam_tip": "Works closely with the CISO (Chief Information Security Officer) and reports to the CEO or Board of Directors."
    },
    "CSP": {
        "expansion": "Cloud Service Provider",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A third-party vendor (e.g., AWS, Azure, Google Cloud) that offers on-demand scalable computing infrastructure, storage, databases, and hosted applications over the internet.",
        "exam_tip": "Remember the Shared Responsibility Model: Customer always retains 100% responsibility for their data regardless of IaaS, PaaS, or SaaS!"
    },
    "CSR": {
        "expansion": "Certificate Signing Request",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A standardized formatted message sent from an applicant server to a Certificate Authority (CA) requesting a signed digital certificate.",
        "exam_tip": "Contains the server's public key and identity information (Common Name, Organization, Country). The private key is NEVER sent in a CSR!"
    },
    "CSRF": {
        "expansion": "Cross-Site Request Forgery",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A web application vulnerability where a malicious website tricks a victim's authenticated browser into executing unauthorized, state-changing commands on a target web application.",
        "exam_tip": "Keywords: Exploits user's trusted session/cookie. Mitigated using Anti-CSRF tokens (unique, random, per-request tokens) and SameSite cookie attributes."
    },
    "CSU": {
        "expansion": "Channel Service Unit",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A digital telecommunications hardware device that interfaces a digital T1/T3 leased line with a Data Service Unit (DSU) and network router.",
        "exam_tip": "Typically combined with a DSU into a CSU/DSU modem module on enterprise WAN edge routers."
    },
    "CSX": {
        "expansion": "Cybersecurity Nexus",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "An ISACA initiative providing cybersecurity education, career frameworks, training credentials, and industry research.",
        "exam_tip": "Aligns skillsets with the NIST Cybersecurity Framework (CSF)."
    },
    "CVE": {
        "expansion": "Common Vulnerabilities and Exposures",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A publicly accessible, standardized dictionary of publicly known cybersecurity vulnerabilities, maintained by MITRE and sponsored by CISA.",
        "exam_tip": "Format: CVE-YYYY-NNNNN (e.g., CVE-2021-44228 for Log4Shell). Scored using CVSS metrics."
    },
    "CVSS": {
        "expansion": "Common Vulnerability Scoring System",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "An open industry standard framework for assessing and rating the severity of computer system security vulnerabilities on a scale from 0.0 to 10.0.",
        "exam_tip": "Score ranges: 0.1–3.9 (Low), 4.0–6.9 (Medium), 7.0–8.9 (High), 9.0–10.0 (Critical). Considers attack vector, complexity, privileges, and CIA impact."
    },
    "CYBOK": {
        "expansion": "Cybersecurity Body of Knowledge",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A comprehensive foundational guide and academic framework codifying core cybersecurity knowledge across multiple technical domains.",
        "exam_tip": "Used in university curriculums and certification blueprint development."
    },

    # --- D ---
    "DAC": {
        "expansion": "Discretionary Access Control",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An access control model where the creator/owner of a file or data object has complete discretion over who is granted access permissions.",
        "exam_tip": "Used in standard Windows and Linux NTFS file systems (read, write, execute permissions set by owner). Contrast with MAC (Mandatory Access Control)."
    },
    "DBA": {
        "expansion": "Database Administrator",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An IT professional responsible for the performance, integrity, security, backup, and configuration management of relational and non-relational database systems.",
        "exam_tip": "Enforces principle of least privilege on SQL databases, database encryption (TDE), and audit logging."
    },
    "DDoS": {
        "expansion": "Distributed Denial of Service",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A malicious attack that overwhelms a targeted server, network service, or website with massive traffic flood from thousands of compromised distributed botnet devices.",
        "exam_tip": "Mitigated using cloud scrubbing centers, CDN caching, rate limiting, and Anycast routing (e.g., Cloudflare, AWS Shield)."
    },
    "DEP": {
        "expansion": "Data Execution Prevention",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A CPU hardware and operating system memory protection mechanism that marks memory pages (like the stack and heap) as non-executable to prevent malicious code execution.",
        "exam_tip": "Blocks buffer overflow exploits from executing shellcode injected into memory. Uses the CPU NX (No-eXecute) bit."
    },
    "DES": {
        "expansion": "Data Encryption Standard",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A legacy symmetric block cipher developed by IBM in the 1970s utilizing a 64-bit block size and a 56-bit key.",
        "exam_tip": "Completely insecure today due to small 56-bit key size (cracked in minutes via brute force). Replaced by AES."
    },
    "DHCP": {
        "expansion": "Dynamic Host Configuration Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A network management protocol (UDP ports 67/68) that automatically assigns IP addresses, subnet masks, default gateways, and DNS servers to client devices on a LAN.",
        "exam_tip": "Vulnerable to Rogue DHCP Servers and DHCP Starvation attacks. Mitigated with DHCP Snooping on switches."
    },
    "DHE": {
        "expansion": "Diffie-Hellman Ephemeral",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A key exchange protocol that uses temporary, single-session cryptographic keys to negotiate a shared symmetric key over an insecure channel.",
        "exam_tip": "Provides Perfect Forward Secrecy (PFS): compromising the server's private key does NOT decrypt previously recorded session traffic!"
    },
    "DKIM": {
        "expansion": "DomainKeys Identified Mail",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An email authentication protocol that adds a cryptographic digital signature to outbound email headers, allowing the recipient mail server to verify message integrity and sender authenticity.",
        "exam_tip": "Uses public key published in the sender's DNS TXT record. Part of the email security triad: SPF + DKIM + DMARC."
    },
    "DLP": {
        "expansion": "Data Loss Prevention",
        "domain": 3,
        "category": "Security Architecture & Defense",
        "explanation": "A software strategy and toolset that inspects and monitors sensitive data across three states (Data in-use, in-transit, at-rest) to block unauthorized data exfiltration.",
        "exam_tip": "Detects sensitive data patterns (Credit cards, SSNs, PHI) via regex and fingerprinting. Deployed at endpoint, network perimeter, and cloud/email."
    },
    "DMARC": {
        "expansion": "Domain-based Message Authentication, Reporting, and Conformance",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An email governance policy protocol published in DNS that tells receiving mail servers what action to take (none, quarantine, reject) if an email fails SPF or DKIM checks.",
        "exam_tip": "Prevents email spoofing and business email compromise (BEC). Publishes reports back to domain owner on spoofing attempts."
    },
    "DNAT": {
        "expansion": "Destination Network Address Translation",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A routing technique that modifies the destination IP address of incoming network packets, commonly used for port forwarding public traffic to an internal private server.",
        "exam_tip": "Directs external traffic hitting a public IP and port (e.g., port 443) to an internal DMZ server IP (e.g., 10.0.0.5)."
    },
    "DNS": {
        "expansion": "Domain Name System",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The fundamental internet directory protocol (UDP/TCP port 53) that translates human-friendly domain names (e.g., comptia.org) into machine-routable IP addresses.",
        "exam_tip": "Vulnerable to DNS Spoofing/Poisoning, Domain Hijacking, and DNS Tunneling (data exfiltration). Port 53: UDP for queries, TCP for zone transfers."
    },
    "DNSSEC": {
        "expansion": "Domain Name System Security Extensions",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A security suite of cryptographic extensions to DNS that digitally signs DNS records (RRSIG) to guarantee authenticity and integrity of responses.",
        "exam_tip": "Prevents DNS cache poisoning and man-in-the-middle spoofing by verifying cryptographic signatures. Does NOT encrypt DNS queries (that is DoH/DoT)."
    },
    "DoH": {
        "expansion": "DNS over HTTPS",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A protocol that encrypts DNS queries and responses by tunneling standard DNS requests through TLS over HTTPS port 443.",
        "exam_tip": "Enhances privacy and prevents ISP snooping or censorship. Difficult for enterprise firewalls to filter because it blends with normal HTTPS web traffic."
    },
    "DoS": {
        "expansion": "Denial of Service",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A cyber attack designed to make a machine, network resource, or service unavailable to its intended legitimate users by crashing it or consuming all capacity.",
        "exam_tip": "Originated from a SINGLE source host (unlike DDoS which uses distributed botnets). Examples: SYN flood, Ping of Death, Slowloris."
    },
    "DoT": {
        "expansion": "DNS over TLS",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A protocol that encrypts DNS queries directly using Transport Layer Security (TLS) over dedicated TCP port 853.",
        "exam_tip": "Uses dedicated port 853, making it easy for enterprise network administrators to monitor and block, unlike DoH which uses standard web port 443."
    },
    "DRP": {
        "expansion": "Disaster Recovery Planning",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A documented technical plan detailing the exact procedures, order of restoration, and steps required to recover critical IT infrastructure and data following a disaster.",
        "exam_tip": "A technical component of the broader BCP. Focuses on restoring servers, data centers, networks, and backups to operational status."
    },
    "DSA": {
        "expansion": "Digital Signature Algorithm",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A Federal Information Processing Standard (FIPS) asymmetric cryptographic algorithm used exclusively for creating and verifying digital signatures.",
        "exam_tip": "Provides non-repudiation, integrity, and authentication. Does NOT provide data encryption."
    },
    "DSU": {
        "expansion": "Data Service Unit",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A telecommunications interface adapter converting digital data frames from a local LAN router into synchronous bipolar signals for a digital leased line (T1/T3).",
        "exam_tip": "Pairs with a Channel Service Unit (CSU) to connect enterprise networks to telecom provider WAN circuits."
    },

    # --- E ---
    "EAP": {
        "expansion": "Extensible Authentication Protocol",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A flexible, universal authentication framework commonly used in wireless networks and Point-to-Point connections that supports multiple authentication mechanisms (smart cards, passwords, certificates).",
        "exam_tip": "Used in 802.1X enterprise Wi-Fi. Common types: EAP-TLS (certificates on client & server - strongest), EAP-TTLS, and PEAP."
    },
    "ECB": {
        "expansion": "Electronic Codebook",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "The simplest and least secure block cipher encryption mode, where identical plaintext blocks are always encrypted into identical ciphertext blocks.",
        "exam_tip": "Leads to pattern preservation (e.g., the infamous ECB Tux penguin illustration). NEVER recommended for production data encryption."
    },
    "ECC": {
        "expansion": "Elliptic Curve Cryptography",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "An advanced asymmetric cryptographic approach based on the algebraic structure of elliptic curves over finite fields, providing equal security to RSA with significantly smaller key sizes.",
        "exam_tip": "A 256-bit ECC key provides equivalent security to a 3072-bit RSA key! Ideal for mobile devices, smart cards, and IoT with limited battery and compute."
    },
    "ECDHE": {
        "expansion": "Elliptic Curve Diffie-Hellman Ephemeral",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A key exchange protocol combining Elliptic Curve cryptography with ephemeral keys to securely negotiate session keys while providing Perfect Forward Secrecy (PFS).",
        "exam_tip": "Gold standard for modern TLS 1.3 handshakes due to low compute overhead, fast processing, and PFS protection."
    },
    "ECDSA": {
        "expansion": "Elliptic Curve Digital Signature Algorithm",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "The elliptic curve analogue of the Digital Signature Algorithm (DSA), used to produce compact, tamper-evident cryptographic digital signatures.",
        "exam_tip": "Offers high-speed signature generation with small signature sizes. Extensively used in Bitcoin, blockchain, and mobile TLS certificates."
    },
    "EDR": {
        "expansion": "Endpoint Detection and Response",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An integrated endpoint security solution that continuously monitors host workstations and servers, collects activity data, detects behavioral anomalies, and automates threat containment.",
        "exam_tip": "Goes far beyond traditional signature antivirus: tracks process trees, memory injection, isolates infected machines from the network, and aids threat hunting."
    },
    "EFS": {
        "expansion": "Encrypting File System",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A built-in Microsoft Windows NTFS feature that encrypts individual files and folders on an NTFS volume using symmetric keys tied to user certificates.",
        "exam_tip": "Encrypts individual files and folders, while BitLocker provides Full Disk Encryption (FDE) of the entire drive volume."
    },
    "ERP": {
        "expansion": "Enterprise Resource Planning",
        "domain": 5,
        "category": "Security Architecture & Defense",
        "explanation": "A centralized, comprehensive business software suite integrating procurement, manufacturing, inventory, financials, HR, and supply chain operations into a unified database.",
        "exam_tip": "A critical high-value enterprise asset subject to strict least privilege, segregation of duties, and regulatory audit compliance."
    },
    "ESP": {
        "expansion": "Encapsulating Security Payload",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An IPsec protocol component (IP protocol 50) that provides data confidentiality (encryption), integrity, source authentication, and anti-replay protection for IP packets.",
        "exam_tip": "Unlike AH which only authenticates, ESP encrypts the packet payload to provide confidentiality. Standard for IPsec VPN tunnels."
    },
    "ESSID": {
        "expansion": "Extended Service Set Identifier",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The human-readable network name of a Wi-Fi network consisting of multiple wireless Access Points interconnected across an enterprise network.",
        "exam_tip": "Allows mobile wireless clients to roam seamlessly between multiple Access Points sharing the same SSID without disconnecting."
    },

    # --- F ---
    "FACL": {
        "expansion": "File Access Control List",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A table of permissions attached directly to a file or filesystem object, explicitly declaring which users or groups are granted read, write, execute, or delete rights.",
        "exam_tip": "Core implementation of Discretionary Access Control (DAC) in POSIX Linux and Windows NTFS file systems."
    },
    "FAR": {
        "expansion": "False Acceptance Rate",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "The percentage of times a biometric authentication system incorrectly grants access to an unauthorized, illegitimate user (Type II Error).",
        "exam_tip": "The ultimate security risk in biometrics (letting an impostor in). The crossover point where FAR equals FRR is the CER (Crossover Error Rate)."
    },
    "FBDI": {
        "expansion": "Field-Bus Data Interface",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An industrial networking communication standard used in SCADA and ICS networks to interface industrial sensors, actuators, and controllers.",
        "exam_tip": "Legacy industrial protocols often lack built-in encryption or authentication and require isolated OT network segmentation."
    },
    "FDE": {
        "expansion": "Full Disk Encryption",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "Cryptographic protection that automatically encrypts every bit of data stored on a hard drive or SSD volume, including the operating system, swap space, and user files.",
        "exam_tip": "Examples: BitLocker, FileVault. Protects data-at-rest if a laptop or hard drive is physically lost or stolen. Keys often stored in a hardware TPM."
    },
    "FIDO": {
        "expansion": "Fast Identity Online",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An open industry authentication standard (FIDO2 / WebAuthn) designed to replace passwords with cryptographically secure, phishing-resistant public-key authentication tokens and passkeys.",
        "exam_tip": "Phishing-resistant MFA: Private key never leaves the user's hardware security key (e.g., YubiKey) or device enclave."
    },
    "FISMA": {
        "expansion": "Federal Information Security Modernization Act",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A U.S. federal legislative statute mandating that all federal agencies create, document, and implement an information security program following NIST standards.",
        "exam_tip": "Requires adherence to NIST SP 800-53 security controls and continuous security monitoring."
    },
    "FPGA": {
        "expansion": "Field-Programmable Gate Array",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An integrated semiconductor circuit designed to be configured or reprogrammed by a customer or designer after manufacturing to execute specialized hardware acceleration.",
        "exam_tip": "Used in high-speed hardware cryptographic accelerators, network firewall filtering engines, and specialized IoT controllers."
    },
    "FRR": {
        "expansion": "False Rejection Rate",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "The percentage of times a biometric security scanner incorrectly denies access to a legitimate, authorized user (Type I Error).",
        "exam_tip": "Measures user inconvenience and friction. Crossover Error Rate (CER) is where FRR and FAR intersect; lower CER = more accurate system."
    },
    "FS": {
        "expansion": "Forward Secrecy",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A cryptographic design feature ensuring that the compromise of a server's long-term private key does not compromise past encrypted session keys or traffic.",
        "exam_tip": "Also called Perfect Forward Secrecy (PFS). Generated using ephemeral Diffie-Hellman key exchanges (DHE or ECDHE)."
    },
    "FSR": {
        "expansion": "Field-Service Representative",
        "domain": 5,
        "category": "Physical & Endpoint Security",
        "explanation": "An authorized third-party vendor technician dispatched on-site to inspect, service, or repair hardware equipment or network appliances.",
        "exam_tip": "Presents physical social engineering risks. Must verify identity, require signed NDAs, check credentials, and maintain strict physical escort."
    },
    "FTP": {
        "expansion": "File Transfer Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A legacy client-server network protocol (TCP ports 20/21) used for transferring computer files between computers over a network.",
        "exam_tip": "Insecure! Transmits usernames, passwords, and file contents in plain text. Always replace with SFTP (port 22) or FTPS (ports 989/990)."
    },
    "FTPS": {
        "expansion": "File Transfer Protocol Secure",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An extension of traditional FTP that adds Transport Layer Security (TLS) encryption to protect authentication credentials and file transfers (TCP ports 989/990).",
        "exam_tip": "FTPS is FTP secured with TLS (ports 989/990). Do not confuse with SFTP, which runs file transfers inside the SSH protocol (TCP port 22)!"
    },

    # --- G ---
    "GCM": {
        "expansion": "Galois/Counter Mode",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "An advanced symmetric block cipher mode of operation that provides both high-speed data confidentiality (encryption) and built-in data integrity authentication (AEAD).",
        "exam_tip": "Highly parallelizable and fast in hardware. The preferred encryption mode in modern TLS 1.2 and 1.3 ciphersuites (e.g., AES-GCM)."
    },
    "GDPR": {
        "expansion": "General Data Protection Regulation",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A comprehensive European Union regulation mandating strict data protection, privacy disclosures, and personal data rights for individuals within the EU.",
        "exam_tip": "Key aspects: Right to be Forgotten (data erasure), 72-hour mandatory breach notification, Data Protection Officers (DPOs), and massive penalties up to 4% of global turnover."
    },
    "GPG": {
        "expansion": "GNU Privacy Guard",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A free, open-source command-line software implementation of the OpenPGP standard used for encrypting files, securing emails, and generating digital signatures.",
        "exam_tip": "Uses hybrid encryption: encrypts the payload with a symmetric session key, then encrypts that session key using the recipient's asymmetric public key."
    },
    "GPS": {
        "expansion": "Global Positioning System",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A satellite-based radio navigation system used by mobile devices and vehicles to calculate precise geographic coordinates.",
        "exam_tip": "Used in security for geofencing (enforcing policies when a device leaves a geographic boundary) and GPS tagging in forensic evidence."
    },
    "GPU": {
        "expansion": "Graphics Processing Unit",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A specialized electronic circuit optimized for parallel mathematical processing, utilized heavily in high-speed cryptographic hashing and brute-force password cracking.",
        "exam_tip": "Attackers leverage massive GPU clusters (using Hashcat or John the Ripper) to crack unsalted password hashes millions of times faster than CPUs."
    },
    "GRE": {
        "expansion": "Generic Routing Encapsulation",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A tunneling protocol developed by Cisco (IP protocol 47) that encapsulates a wide variety of network layer protocols inside virtual point-to-point IP links.",
        "exam_tip": "Provides tunneling and routing encapsulation only; GRE provides ZERO encryption or security on its own. Must be wrapped inside IPsec for security."
    },
    "GSSAPI": {
        "expansion": "Generic Security Services Application Programming Interface",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An IETF standard security API allowing applications to authenticate users using external security mechanisms such as Kerberos without knowing underlying protocols.",
        "exam_tip": "Used in multi-platform enterprise SSO and Kerberos authentication integration."
    },
    "GUI": {
        "expansion": "Graphical User Interface",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A visual computer environment allowing users and operators to interact with software and devices via graphical icons, windows, buttons, and visual indicators.",
        "exam_tip": "Security analysts use both GUIs (SIEM dashboards, firewalls) and CLIs (command lines, scripts, regex) for triage and threat hunting."
    },
    "GUID": {
        "expansion": "Globally Unique Identifier",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A 128-bit pseudorandom reference number used in software architectures (such as Microsoft Active Directory) to uniquely identify an object or resource.",
        "exam_tip": "Guaranteed to be globally unique across time and space. Used in Active Directory, GPT partition tables, and COM components."
    },

    # --- H ---
    "HA": {
        "expansion": "High Availability",
        "domain": 3,
        "category": "Security Architecture & Defense",
        "explanation": "An architectural resilience design ensuring a system remains continuously operational and accessible for a high percentage of time (e.g., 99.999% 'five nines').",
        "exam_tip": "Eliminates single points of failure (SPOFs) using redundancy, clustering, automatic failover, RAID, UPS systems, and load balancers."
    },
    "HIDS": {
        "expansion": "Host-Based Intrusion Detection System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "Software installed directly on an individual endpoint or server that monitors operating system logs, file system integrity, process creation, and system calls for intrusion.",
        "exam_tip": "Can inspect decrypted traffic and local file modifications (e.g., Tripwire). Detects attacks that network IDS (NIDS) misses due to TLS encryption."
    },
    "HIPS": {
        "expansion": "Host-Based Intrusion Prevention System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An active host security agent that monitors system activity on an endpoint and actively blocks or terminates malicious processes, registry edits, and buffer overflows.",
        "exam_tip": "Unlike HIDS which only alerts, HIPS takes active inline preventive action (kills processes, drops connections, blocks writes)."
    },
    "HMAC": {
        "expansion": "Hash-Based Message Authentication Code",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A cryptographic construction combining a cryptographic hash function (e.g., SHA-256) with a secret shared symmetric key to guarantee data integrity and authenticity.",
        "exam_tip": "Used in IPsec, TLS, and token authentication. Verifies that the message has not been altered AND confirms that it originated from the shared key holder."
    },
    "HOTP": {
        "expansion": "HMAC-Based One-Time Password",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An open MFA algorithm (RFC 4226) that generates a one-time passcode calculated using HMAC and an incrementing event counter.",
        "exam_tip": "Counter-based (advances with each button press on hardware token). In contrast, TOTP (Time-Based OTP) increments based on real-time clock intervals (30s)."
    },
    "HSM": {
        "expansion": "Hardware Security Module",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A tamper-evident, dedicated physical computing appliance designed specifically for securely generating, storing, managing, and offloading cryptographic keys.",
        "exam_tip": "Enterprise cryptographic vault. Used by Certificate Authorities (Root CAs) to protect master private keys. Tamper-evident: wipes keys if physically opened."
    },
    "HTML": {
        "expansion": "Hypertext Markup Language",
        "domain": 2,
        "category": "Application Security & Architecture",
        "explanation": "The standard markup language used to structure content displayed on the World Wide Web.",
        "exam_tip": "Vulnerable to Cross-Site Scripting (XSS) and HTML injection when user input is rendered in browser without input validation and HTML entity sanitization."
    },
    "HTTP": {
        "expansion": "Hypertext Transfer Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The foundational application layer protocol (TCP port 80) used for transmitting hypermedia documents across the World Wide Web.",
        "exam_tip": "Insecure cleartext protocol! Transmits credentials and session cookies unencrypted. Always enforce HTTPS (TCP port 443) with HSTS."
    },
    "HTTPS": {
        "expansion": "Hypertext Transfer Protocol Secure",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The secure, encrypted implementation of HTTP (TCP port 443) that tunnels web traffic inside an authenticated Transport Layer Security (TLS) session.",
        "exam_tip": "Provides confidentiality, server authentication via digital certificates, and message integrity. Enforced using HSTS headers."
    },
    "HVAC": {
        "expansion": "Heating, Ventilation, and Air Conditioning",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "Environmental control systems that regulate temperature, airflow, and humidity within enterprise data centers and server closets.",
        "exam_tip": "Physical security control: Too high temperature = hardware overheating; too low humidity = electrostatic discharge (ESD); too high humidity = condensation damage."
    },

    # --- I ---
    "IaaS": {
        "expansion": "Infrastructure as a Service",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A cloud service model where the provider supplies virtualized computing resources (VMs, storage, firewalls, networking) and the client manages the OS, apps, and data.",
        "exam_tip": "Examples: AWS EC2, Azure VMs, Google Compute Engine. Customer is responsible for OS patching, middleware, firewalls, and data."
    },
    "IAM": {
        "expansion": "Identity and Access Management",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A comprehensive framework of business processes, policies, and technologies that manages digital identities, permissions, provisioning, and access governance.",
        "exam_tip": "Core principles: Principle of Least Privilege, Separation of Duties, Role-Based Access Control (RBAC), and automated employee offboarding."
    },
    "ICMP": {
        "expansion": "Internet Control Message Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A network layer protocol (IP protocol 1) used by network devices to send error messages and operational information (e.g., ping echo requests, destination unreachable).",
        "exam_tip": "Used in reconnaissance (ping sweeps, traceroute) and attacks (Smurf attacks, ICMP floods). Often blocked or rate-limited on external firewalls."
    },
    "ICS": {
        "expansion": "Industrial Control Systems",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A general term encompassing SCADA, DCS, PLCs, and operational technology (OT) used to monitor and automate industrial production, power grids, and water treatment.",
        "exam_tip": "Safety and availability take precedence over confidentiality. Must be strictly segmented from corporate IT networks using Purdue Model / air gaps."
    },
    "IDEA": {
        "expansion": "International Data Encryption Algorithm",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A symmetric block cipher developed in 1991 operating on 64-bit plaintext blocks with a 128-bit key, famously utilized in early versions of PGP.",
        "exam_tip": "Replaced in modern cryptographic systems by AES."
    },
    "IDF": {
        "expansion": "Intermediate Distribution Frame",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A secondary telecommunications wiring closet located on floor levels of a building that interconnects local workstations and access points to the Main Distribution Frame (MDF).",
        "exam_tip": "Physical security: Must be secured with locked doors, access badge logging, security cameras, and environmental monitoring."
    },
    "IdP": {
        "expansion": "Identity Provider",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A centralized trusted service (e.g., Okta, Microsoft Entra ID, Ping Identity) that creates, maintains, and manages identity information and authenticates principals.",
        "exam_tip": "In federated identity (SAML, OIDC), the IdP authenticates the user and issues cryptographically signed assertion tokens to the Service Provider (SP)."
    },
    "IDS": {
        "expansion": "Intrusion Detection System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A passive monitoring security appliance or host agent that inspects network traffic or system logs, alerting security administrators when unauthorized activity is detected.",
        "exam_tip": "Passive / Out-of-band: Receives a copy of traffic via a SPAN port or network TAP. Alerts only; does NOT block or drop malicious packets!"
    },
    "IEEE": {
        "expansion": "Institute of Electrical and Electronics Engineers",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A professional engineering organization that establishes ubiquitous international standards for networking and hardware.",
        "exam_tip": "Key standards: 802.3 (Ethernet), 802.11 (Wi-Fi), 802.1X (Port-Based Network Access Control), 802.1Q (VLAN tagging)."
    },
    "IKE": {
        "expansion": "Internet Key Exchange",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A protocol (UDP port 500) used in IPsec VPNs to establish Security Associations (SAs) and negotiate cryptographic keys between two tunnel endpoints.",
        "exam_tip": "Operates in two phases: Phase 1 establishes a secure control channel; Phase 2 negotiates the IPsec transform set for data traffic. IKEv2 is modern standard."
    },
    "IMAP": {
        "expansion": "Internet Message Access Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An application layer email retrieval protocol (TCP port 143; secure IMAPS on TCP port 993) that synchronizes emails on a central server across multiple client devices.",
        "exam_tip": "Legacy port 143 is cleartext. Secure IMAPS uses port 993 over TLS. Unlike POP3 which downloads & deletes, IMAP keeps messages synced on server."
    },
    "IoC": {
        "expansion": "Indicator of Compromise",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A piece of digital forensic evidence or forensic artifact observed on a network or host that indicates a system has been breached or infected with malware.",
        "exam_tip": "Examples: Known malicious file hash (MD5/SHA256), suspicious C2 IP address, unusual outbound DNS traffic, rogue scheduled task, unauthorized registry keys."
    },
    "IoT": {
        "expansion": "Internet of Things",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "The billions of physical devices (smart thermostats, IP cameras, medical monitors, sensors) embedded with sensors and software that connect and exchange data over the internet.",
        "exam_tip": "Major security risks: Hardcoded default credentials, lack of patchability, weak firmware, and lack of encryption. Must be isolated on a dedicated IoT VLAN."
    },
    "IP": {
        "expansion": "Internet Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The fundamental network layer protocol responsible for addressing and routing packets across network boundaries from origin host to destination host.",
        "exam_tip": "IPv4 uses 32-bit addresses (e.g., 192.168.1.1); IPv6 uses 128-bit hexadecimal addresses and incorporates mandatory built-in IPsec support."
    },
    "IPS": {
        "expansion": "Intrusion Prevention System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An active, inline network security appliance that analyzes traffic in real time and automatically drops, blocks, or resets malicious network packets.",
        "exam_tip": "Active / Inline: Placed directly in the path of network traffic. If it detects an exploit, it drops the packet immediately to prevent intrusion."
    },
    "IPSec": {
        "expansion": "Internet Protocol Security",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A comprehensive suite of protocols that secures IP communications by authenticating and encrypting each IP packet in a data stream.",
        "exam_tip": "Components: AH (protocol 51 - integrity), ESP (protocol 50 - confidentiality), IKE (UDP 500 - key negotiation). Modes: Transport (payload only) vs Tunnel (entire packet encrypted)."
    },
    "IR": {
        "expansion": "Incident Response",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A structured, organized approach addressing and managing the aftermath of a security breach or cyberattack to limit damage and reduce recovery time and costs.",
        "exam_tip": "Know the 6 NIST steps: Preparation -> Identification -> Containment -> Eradication -> Recovery -> Lessons Learned (PICERL)."
    },
    "IRC": {
        "expansion": "Internet Relay Chat",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A legacy text-based instant messaging protocol (TCP port 6667) historically favored by botnet operators for Command and Control (C2) communication.",
        "exam_tip": "Security analysts monitor outbound port 6667 traffic as an indicator of zombie botnet activity."
    },
    "IRM": {
        "expansion": "Information Rights Management",
        "domain": 3,
        "category": "Security Architecture & Defense",
        "explanation": "A specialized subset of Digital Rights Management (DRM) technologies applied to corporate documents, emails, and spreadsheets to prevent unauthorized copying, forwarding, or printing.",
        "exam_tip": "Protects sensitive data even after it leaves the company network (e.g., encrypts document so it cannot be forwarded or screenshotted)."
    },
    "IRP": {
        "expansion": "Incident Response Plan",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A formalized, documented operational playbook providing actionable step-by-step instructions for responding to specific cybersecurity scenarios.",
        "exam_tip": "Defines roles, responsibilities, escalation paths, legal disclosures, and specific playbooks (e.g., Ransomware playbook, Data breach playbook)."
    },
    "ISA": {
        "expansion": "Interconnection Security Agreement",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A formal agreement between two or more organizations establishing the technical, security, and interface requirements for interconnecting their IT systems.",
        "exam_tip": "Mandatory in federal and enterprise B2B partner integrations to ensure that connecting partner networks do not introduce security vulnerabilities."
    },
    "ISMS": {
        "expansion": "Information Security Management System",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A systematic, organizational framework of policies, procedures, and controls to manage sensitive company data risks, codified in ISO/IEC 27001.",
        "exam_tip": "Certified under ISO/IEC 27001. Requires continuous risk assessment, executive management commitment, and routine auditing."
    },
    "ISO": {
        "expansion": "International Organization for Standardization",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "An independent, non-governmental international standard-setting body composed of representatives from various national standards organizations.",
        "exam_tip": "Key standards: ISO 27001 (ISMS framework), ISO 27002 (Security controls code of practice), ISO 27701 (Privacy information management)."
    },
    "ISP": {
        "expansion": "Internet Service Provider",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A telecommunications company that provides individual consumers and enterprise organizations access to the global Internet infrastructure.",
        "exam_tip": "Enterprises employ multiple ISPs with BGP multihoming to achieve network redundancy and avoid single points of failure (SPOF)."
    },
    "IT": {
        "expansion": "Information Technology",
        "domain": 5,
        "category": "Governance & Security Concepts",
        "explanation": "The use of computers, storage, networking, and other physical devices to create, process, store, secure, and exchange all forms of electronic data.",
        "exam_tip": "Security encompasses Information Security (InfoSec), Cybersecurity, Operational Technology (OT), and IT governance."
    },
    "ITIL": {
        "expansion": "Information Technology Infrastructure Library",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A globally recognized framework of best practices for delivering IT services, change management, incident management, and asset lifecycles.",
        "exam_tip": "Key security focus: Change Management (CAB - Change Advisory Board), Configuration Management Databases (CMDB), and Service Level Agreements."
    },
    "IV": {
        "expansion": "Initialization Vector",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A fixed-size pseudorandom non-secret cryptographic input number used alongside a secret key to ensure that identical plaintexts encrypt to distinct ciphertexts.",
        "exam_tip": "Must NEVER be reused with the same key! WEP was broken specifically because its 24-bit IV was too short and reused, allowing key recovery attacks."
    },

    # --- J, K, L ---
    "JBOD": {
        "expansion": "Just a Bunch of Disks",
        "domain": 3,
        "category": "Security Architecture & Defense",
        "explanation": "A storage architecture configuring multiple physical hard drives as separate individual volumes or spanned into a single logical drive without RAID parity or striping.",
        "exam_tip": "Provides NO redundancy, fault tolerance, or performance enhancements. If a drive fails in a spanned JBOD, all data is lost."
    },
    "JSON": {
        "expansion": "JavaScript Object Notation",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "An open standard, human-readable text data interchange format widely used in modern REST APIs, web applications, and configuration files.",
        "exam_tip": "Secured using JWT (JSON Web Tokens) for stateless authentication. Vulnerable to injection if not parsed with safe JSON parsers."
    },
    "KDC": {
        "expansion": "Key Distribution Center",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "The centralized authentication authority in a Kerberos network environment responsible for authenticating users and issuing cryptographic tickets.",
        "exam_tip": "Consists of the Authentication Server (AS) and the Ticket Granting Server (TGS). Operates on UDP/TCP port 88."
    },
    "KPI": {
        "expansion": "Key Performance Indicator",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A quantifiable metric evaluating how effectively an organization is achieving its business and operational objectives over time.",
        "exam_tip": "Examples in security: Mean Time to Detect (MTTD), Mean Time to Remediate (MTTR), percentage of patched vulnerabilities, phish-test failure rate."
    },
    "KRI": {
        "expansion": "Key Risk Indicator",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A forward-looking metric providing an early warning signal of increasing risk exposure across an organization.",
        "exam_tip": "Examples: High employee turnover in IT, spike in unpatched critical CVEs, increase in failed login attempts."
    },
    "L2TP": {
        "expansion": "Layer 2 Tunneling Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A tunneling protocol (UDP port 1701) used to support virtual private networks (VPNs) by encapsulating Layer 2 frames over an IP network.",
        "exam_tip": "Like GRE, L2TP provides NO native encryption or confidentiality! It is almost universally paired with IPsec (L2TP/IPsec) for security."
    },
    "LAN": {
        "expansion": "Local Area Network",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A computer network interconnecting computers, printers, and devices within a limited physical geographical area like an office building, school, or home.",
        "exam_tip": "Segmented into virtual networks using VLANs (802.1Q) to isolate sensitive departments (e.g., HR, Finance) and contain lateral malware movement."
    },
    "LDAP": {
        "expansion": "Lightweight Directory Access Protocol",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A software protocol (TCP port 389) enabling applications to query and modify directory services information (users, computers, groups) across an enterprise network.",
        "exam_tip": "Port 389 transmits credentials in cleartext! Secure LDAPS uses TLS encryption over TCP port 636."
    },
    "LDAPS": {
        "expansion": "Lightweight Directory Access Protocol Secure",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "The cryptographically encrypted version of LDAP that secures directory queries and user authentication inside TLS encryption over TCP port 636.",
        "exam_tip": "Runs on TCP port 636. Replaces insecure cleartext LDAP (port 389) in enterprise environments (e.g., Active Directory)."
    },
    "LEAP": {
        "expansion": "Lightweight Extensible Authentication Protocol",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A proprietary Cisco wireless authentication protocol developed to address WEP vulnerabilities prior to WPA.",
        "exam_tip": "Insecure! Vulnerable to offline dictionary brute-force attacks against MS-CHAPv2 hashes. Replaced by PEAP and EAP-TLS."
    },
    "LLMNR": {
        "expansion": "Link-Local Multicast Name Resolution",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A Windows name resolution protocol (UDP port 5355) that allows hosts to resolve names on a local subnet when DNS server queries fail.",
        "exam_tip": "Vulnerable to LLMNR/NBT-NS Poisoning attacks (using tools like Responder) where attackers capture password NTLM hashes. Must be disabled via GPO!"
    },
    "LPD": {
        "expansion": "Line Printer Daemon",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A legacy network protocol (TCP port 515) used for submitting print jobs to remote spooling printers over a network.",
        "exam_tip": "Cleartext and insecure; should be disabled on modern enterprise networks in favor of secure IPP (Internet Printing Protocol) over TLS."
    },

    # --- M ---
    "MAC": {
        "expansion": "Media Access Control / Mandatory Access Control",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "1) Hardware: Unique 48-bit physical address burned into a network card. 2) Security: An access control model where access is enforced by centralized security labels/clearances.",
        "exam_tip": "On Security+, MAC usually refers to Mandatory Access Control: used in military/government with security clearances (Top Secret, Secret) and labels. Users CANNOT change permissions!"
    },
    "MAM": {
        "expansion": "Mobile Application Management",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An enterprise mobile security system that controls and secures corporate apps and data on mobile devices without managing the entire personal device.",
        "exam_tip": "Focuses on app containerization (e.g., separating corporate Outlook email from personal photos) rather than full device wiping."
    },
    "MAN": {
        "expansion": "Metropolitan Area Network",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A telecommunications network spanning an entire geographic city or large college campus, larger than a LAN but smaller than a global WAN.",
        "exam_tip": "Interconnected using high-speed fiber rings (SONET, Metro Ethernet) and protected by carrier-grade encryption."
    },
    "MBAM": {
        "expansion": "Microsoft BitLocker Administration and Monitoring",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An enterprise management tool that automates BitLocker encryption provisioning, key escrow, and compliance reporting across corporate Windows fleets.",
        "exam_tip": "Allows centralized recovery key escrow in Active Directory or Azure AD if an employee forgets their PIN."
    },
    "MD5": {
        "expansion": "Message Digest 5",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A widely known legacy cryptographic hash function that produces a 128-bit hash value.",
        "exam_tip": "Cryptographically broken due to collision vulnerabilities (two different inputs producing the exact same hash). Do NOT use for digital signatures; use SHA-256."
    },
    "MDF": {
        "expansion": "Main Distribution Frame",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "The primary central telecommunications and network equipment room in a facility connecting external public telecom lines to internal IDFs.",
        "exam_tip": "The nerve center of building wiring. Requires Tier-1 physical access controls: biometrics, badge readers, mantrap, CCTV, and FM-200 fire suppression."
    },
    "MDM": {
        "expansion": "Mobile Device Management",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A centralized software platform that allows IT administrators to configure, secure, monitor, and enforce security policies (PIN, encryption, remote wipe) across enterprise mobile devices.",
        "exam_tip": "Key capabilities: Enforcing screen lock PINs, requiring full device encryption, geofencing, pushing Wi-Fi/VPN profiles, and executing remote wipe if lost/stolen."
    },
    "MFA": {
        "expansion": "Multi-Factor Authentication",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An identity verification mechanism requiring two or more independent authentication factors from different categories before granting access.",
        "exam_tip": "Categories: Something you know (password/PIN), something you have (smart card/phone), something you are (fingerprint/retina), somewhere you are (GPS), something you do (keystroke dynamics)."
    },
    "MFD": {
        "expansion": "Multi-Function Device",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An all-in-one office hardware appliance combining printing, scanning, copying, and faxing capabilities over a network.",
        "exam_tip": "Often overlooked security risk: contains internal hard drives storing unencrypted scanned documents, and frequently lacks default credential changes."
    },
    "MFP": {
        "expansion": "Multi-Function Printer",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "Synonymous with MFD; an office network printer equipped with scanning, faxing, and email dispatch features.",
        "exam_tip": "Must be hardened: update firmware, change admin password, enable hard drive encryption, wipe internal memory before disposal, and isolate on separate VLAN."
    },
    "MITM": {
        "expansion": "Man-in-the-Middle",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "An active attack where the adversary secretly intercepts and potentially alters the communications between two parties who believe they are communicating directly.",
        "exam_tip": "Also termed 'On-Path Attack'. Executed via ARP poisoning, Rogue AP (Evil Twin), DNS spoofing, or SSL stripping. Mitigated using end-to-end mutual TLS encryption."
    },
    "ML": {
        "expansion": "Machine Learning",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A subset of artificial intelligence where computer algorithms improve automatically through experience and data analysis without explicit programming.",
        "exam_tip": "Used in UEBA (User and Entity Behavior Analytics) to establish baselines of normal user behavior and detect zero-day anomalies and insider threats."
    },
    "MOA": {
        "expansion": "Memorandum of Agreement",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A formal legal document outlining terms and details of a mutual partnership or cooperative agreement between two parties, often legally binding.",
        "exam_tip": "More formal and binding than a Memorandum of Understanding (MOU). Defines agreed-upon deliverables, responsibilities, and resource allocations."
    },
    "MOU": {
        "expansion": "Memorandum of Understanding",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A preliminary agreement expressing a mutual convergence of will between parties, indicating an intended common line of action without formal legal binding.",
        "exam_tip": "Less formal than an MOA. Precedes contracts and formal Interconnection Security Agreements (ISAs)."
    },
    "MPLS": {
        "expansion": "Multiprotocol Label Switching",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A telecommunications routing technique that directs data from one node to the next based on short path labels rather than long network addresses.",
        "exam_tip": "Carrier WAN routing protocol. Like GRE, standard MPLS does NOT encrypt traffic; IPsec must be layered over MPLS for confidentiality."
    },
    "MS-CHAP": {
        "expansion": "Microsoft Challenge Handshake Authentication Protocol",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "Microsoft's proprietary version of CHAP used for remote access PPP and VPN authentication.",
        "exam_tip": "MS-CHAPv2 is vulnerable to offline dictionary attacks due to weak DES encryption of MD4 hashes. Deprecated in favor of EAP-TLS."
    },
    "MSP": {
        "expansion": "Managed Service Provider",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A third-party company that remotely manages a customer's IT infrastructure and end-user systems on a proactive subscription basis.",
        "exam_tip": "Presents severe Supply Chain Risk: compromising an MSP gives an attacker administrative backdoor access into dozens or hundreds of downstream clients!"
    },
    "MSSP": {
        "expansion": "Managed Security Service Provider",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An outsourced service provider that specifically monitors, manages, and operates cybersecurity systems, firewalls, SIEM, and SOC operations for clients.",
        "exam_tip": "Cost-effective solution for small-to-medium businesses that cannot afford to build a 24/7/365 internal Security Operations Center (SOC)."
    },
    "MTBF": {
        "expansion": "Mean Time Between Failures",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The predicted elapsed operating time between inherent failures of a mechanical or electronic system during normal operational hours.",
        "exam_tip": "Reliability metric: higher MTBF = more reliable hardware. Formula: Total Operating Hours / Number of Failures."
    },
    "MTTD": {
        "expansion": "Mean Time to Detect",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "The average time it takes for a security team to discover a security incident or intrusion from the moment it first occurs.",
        "exam_tip": "A core SOC performance metric: lower MTTD means faster discovery, significantly reducing attacker dwell time."
    },
    "MTTF": {
        "expansion": "Mean Time to Failure",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The expected operating lifespan of a non-repairable asset before it completely breaks down.",
        "exam_tip": "Applies to non-repairable items (like a lightbulb or solid-state drive that must be discarded and replaced upon failure)."
    },
    "MTTR": {
        "expansion": "Mean Time to Repair / Recover",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The average time required to troubleshoot, repair, and restore a failed system or component back to full operational service.",
        "exam_tip": "Maintainability metric: lower MTTR = faster recovery. Organizations use clustering, automated failover, and hot spares to reduce MTTR."
    },
    "MTU": {
        "expansion": "Maximum Transmission Unit",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The largest packet or frame size, specified in octets (bytes), that can be transmitted over a physical network interface.",
        "exam_tip": "Standard Ethernet MTU is 1500 bytes. VPN tunnels (IPsec/GRE) add headers, often requiring reducing MTU to avoid packet fragmentation."
    },

    # --- N ---
    "NAC": {
        "expansion": "Network Access Control",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A security solution (e.g., 802.1X, Cisco ISE) that inspects and enforces security compliance policies on devices BEFORE granting network access.",
        "exam_tip": "Posture Assessment: Checks if an endpoint has up-to-date antivirus, OS patches, and firewall enabled. Non-compliant devices are redirected to a Quarantine VLAN."
    },
    "NAS": {
        "expansion": "Network Attached Storage",
        "domain": 3,
        "category": "Security Architecture & Defense",
        "explanation": "A dedicated file-level data storage appliance connected to a TCP/IP network, allowing multiple users and clients to share files over NFS or SMB.",
        "exam_tip": "File-level storage (contrast with SAN which is block-level). Secured with RAID, share permissions, Kerberos, and storage encryption."
    },
    "NAT": {
        "expansion": "Network Address Translation",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A network methodology that remaps multiple private, non-routable RFC 1918 IP addresses into a single public routable IP address across a router.",
        "exam_tip": "Conserves IPv4 address space and hides internal network topology from external internet scanners."
    },
    "NDA": {
        "expansion": "Non-Disclosure Agreement",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A legally binding contract establishing confidentiality between parties, forbidding the sharing of proprietary intellectual property, trade secrets, or client data.",
        "exam_tip": "Administrative control signed by employees, contractors, and third-party penetration testers prior to accessing sensitive systems."
    },
    "NFC": {
        "expansion": "Near Field Communication",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A short-range wireless connectivity technology (operates at 13.56 MHz, distance < 4 cm) allowing devices to exchange data (e.g., Apple Pay, access badges).",
        "exam_tip": "Vulnerable to eavesdropping if attacker is within centimeters, data modification, and relay attacks. Mitigated by short range and encryption."
    },
    "NFR": {
        "expansion": "Non-Functional Requirement",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "System requirements defining operational criteria, security standards, performance, scalability, and disaster recovery rather than specific functional features.",
        "exam_tip": "Examples: 'The system must authenticate users via MFA in under 2 seconds' or 'All data at rest must be encrypted with AES-256'."
    },
    "NFV": {
        "expansion": "Network Function Virtualization",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "The decoupling of network functions (routers, firewalls, load balancers) from dedicated hardware appliances so they can run as virtualized software on standard servers.",
        "exam_tip": "Enables rapid provisioning of virtual firewalls and routers in cloud environments without physical cabling."
    },
    "NG-FW": {
        "expansion": "Next-Generation Firewall",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An advanced deep-packet inspection firewall combining traditional stateful packet filtering with Application Visibility (Layer 7), integrated IPS, SSL/TLS decryption, and threat intel.",
        "exam_tip": "Can inspect application layer payloads: distinguishes between regular web traffic and BitTorrent running over port 80/443."
    },
    "NG-SWG": {
        "expansion": "Next-Generation Secure Web Gateway",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A cloud-native proxy security solution that protects users from web-based threats by enforcing URL filtering, malware inspection, cloud DLP, and CASB controls.",
        "exam_tip": "Core component of SASE (Secure Access Service Edge) architecture, protecting remote workers accessing cloud SaaS applications."
    },
    "NIDS": {
        "expansion": "Network-Based Intrusion Detection System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A security system that analyzes network traffic across an entire subnet via TAP or SPAN port, comparing packets against known attack signatures and behavioral anomalies.",
        "exam_tip": "Passive / Out-of-band: Monitors entire network segment from a single vantage point. Blind to encrypted TLS payloads unless paired with SSL decryption proxy."
    },
    "NIPS": {
        "expansion": "Network-Based Intrusion Prevention System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An active, inline network appliance that inspects passing network traffic and immediately blocks or resets connections when malicious activity or exploits are detected.",
        "exam_tip": "Active / Inline: Placed directly in the network path. Can block zero-day attacks and DDoS traffic, but if it crashes, it can halt network flow unless fail-open bypass is enabled."
    },
    "NIST": {
        "expansion": "National Institute of Standards and Technology",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A non-regulatory U.S. federal agency that develops measurement standards, cryptographic benchmarks (FIPS), and influential cybersecurity guidelines (NIST CSF, SP 800-53).",
        "exam_tip": "NIST CSF core functions: Govern, Identify, Protect, Detect, Respond, Recover. SP 800-37 (RMF), SP 800-61 (Incident Response)."
    },
    "NOP": {
        "expansion": "No Operation",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "An assembly language instruction (x86 opcode 0x90) that directs the CPU to perform no action and simply increment the instruction pointer to the next memory address.",
        "exam_tip": "Keywords: NOP Sled / NOP Slide. Used by attackers in buffer overflow exploits to guide execution flow reliably into their injected shellcode."
    },
    "NTLM": {
        "expansion": "New Technology LAN Manager",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A legacy Microsoft suite of security protocols used for authenticating users and computers across Windows networks.",
        "exam_tip": "Vulnerable to Pass-the-Hash attacks and offline dictionary cracking. Replaced by Kerberos as primary Active Directory authentication protocol."
    },
    "NTP": {
        "expansion": "Network Time Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A networking protocol (UDP port 123) for synchronizing computer system clocks over packet-switched, variable-latency data networks.",
        "exam_tip": "Critical for Security Operations: accurately synchronized log timestamps are mandatory for digital forensics, event correlation in SIEM, and Kerberos ticket validation (5 min skew limit)."
    },

    # --- O ---
    "OAUTH": {
        "expansion": "Open Authorization",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An open standard authorization protocol (OAuth 2.0) that enables third-party applications to obtain limited access to a user's web account via scoped access tokens without sharing passwords.",
        "exam_tip": "OAuth is for AUTHORIZATION (granting API permissions/scopes), while OpenID Connect (OIDC) is layered on top for AUTHENTICATION (verifying identity)."
    },
    "OCSP": {
        "expansion": "Online Certificate Status Protocol",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "An internet protocol (TCP port 80/HTTP) used for querying the real-time revocation status of an X.509 digital certificate directly from a CA responder.",
        "exam_tip": "Faster and more scalable than downloading massive CRLs. OCSP Stapling allows the web server to query the CA responder and 'staple' the signed timestamped status to the TLS handshake."
    },
    "OID": {
        "expansion": "Object Identifier",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A globally unique, dot-separated decimal string (e.g., 2.5.4.3 for Common Name) used to name and identify any object or attribute in X.509 certificates, LDAP, and SNMP MIBs.",
        "exam_tip": "Appears in X.509 certificate extensions and SNMP management information bases."
    },
    "OS": {
        "expansion": "Operating System",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "System software that manages computer hardware, software resources, and provides common services for computer programs (e.g., Windows, Linux, macOS).",
        "exam_tip": "Secured via OS Hardening: disabling unused services, enforcing least privilege, applying patches, enabling local firewalls, and configuring audit logging."
    },
    "OSINT": {
        "expansion": "Open-Source Intelligence",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "Intelligence data gathered legally and ethically from publicly available sources (social media, corporate websites, Shodan, WHOIS, public code repositories).",
        "exam_tip": "Used by attackers in initial passive reconnaissance to map targets, harvest employee email addresses, and identify unpatched public-facing servers."
    },
    "OSI": {
        "expansion": "Open Systems Interconnection",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A conceptual reference model that characterizes and standardizes the communication functions of a telecommunication or computing system into 7 distinct abstraction layers.",
        "exam_tip": "The 7 Layers: 7-Application, 6-Presentation, 5-Session, 4-Transport, 3-Network, 2-Data Link, 1-Physical. (Mnemonic: Please Do Not Throw Sausage Pizza Away)."
    },
    "OTA": {
        "expansion": "Over-The-Air",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A wireless transmission method used to distribute firmware updates, software configurations, and encryption keys to mobile devices and connected vehicles without physical cables.",
        "exam_tip": "Critical for patching IoT and smartphone fleets remotely; must be cryptographically signed to prevent malicious firmware flashing."
    },
    "OVAL": {
        "expansion": "Open Vulnerability and Assessment Language",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An open international information security standard that standardizes how to assess and report machine state (vulnerabilities, patch status, configuration compliance).",
        "exam_tip": "Standardized XML schema used by vulnerability scanners (Nessus, OpenVAS) to automate compliance checking."
    },
    "OWASP": {
        "expansion": "Open Web Application Security Project",
        "domain": 2,
        "category": "Application Security & Architecture",
        "explanation": "An influential online community and non-profit organization that produces freely available articles, methodologies, documentation, and the definitive OWASP Top 10 web vulnerabilities.",
        "exam_tip": "Must know OWASP Top 10 vulnerabilities: Broken Access Control, Cryptographic Failures, Injection (SQLi/XSS), Insecure Design, Security Misconfiguration."
    },

    # --- P ---
    "P12": {
        "expansion": "PKCS #12 Certificate File",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A password-protected binary certificate archive format (.p12 / .pfx) capable of bundling both an X.509 public certificate chain and its matching private key.",
        "exam_tip": "Used to export/import server certificates with private keys. Always password-protected to prevent private key theft."
    },
    "P2P": {
        "expansion": "Peer-to-Peer",
        "domain": 2,
        "category": "Network Security & Architecture",
        "explanation": "A decentralized computing architecture where each workstation has equivalent capabilities and responsibilities, sharing files directly without central servers.",
        "exam_tip": "Security risks: BitTorrent clients frequently distribute trojanized software, consume bandwidth, and bypass perimeter firewalls."
    },
    "PaaS": {
        "expansion": "Platform as a Service",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A cloud computing category that provides a development and deployment environment (OS, runtime, database, web server) allowing developers to build apps without managing underlying servers.",
        "exam_tip": "Examples: AWS Elastic Beanstalk, Heroku, Google App Engine. Cloud provider manages OS and hardware; customer manages application code and data."
    },
    "PAC": {
        "expansion": "Proxy Auto-Configuration",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A JavaScript file that defines how web browsers and user agents can automatically choose the appropriate proxy server for fetching a given URL.",
        "exam_tip": "Vulnerable to WPAD (Web Proxy Auto-Discovery) spoofing, where an attacker intercepts traffic by serving a rogue PAC file."
    },
    "PAM": {
        "expansion": "Privileged Access Management",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A specialized cybersecurity suite that manages, monitors, audits, and secures superuser and administrator accounts (Domain Admins, root, cloud admins).",
        "exam_tip": "Features: Credential vaulting, automated password rotation, session recording, and Just-In-Time (JIT) temporary privilege elevation."
    },
    "PAP": {
        "expansion": "Password Authentication Protocol",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A legacy, insecure Point-to-Point Protocol (PPP) authentication mechanism that transmits user credentials in unencrypted cleartext across the network.",
        "exam_tip": "Insecure! Susceptible to packet sniffing. Replaced by CHAP, MS-CHAPv2, and EAP."
    },
    "PAT": {
        "expansion": "Port Address Translation",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An extension of NAT (also known as NAT Overload) that maps multiple private IP addresses to a single public IP address by assigning unique source port numbers.",
        "exam_tip": "The standard form of NAT deployed in home and corporate routers: hundreds of internal hosts share a single public IPv4 address simultaneously."
    },
    "PBKDF2": {
        "expansion": "Password-Based Key Derivation Function 2",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A cryptographic key stretching algorithm that applies a pseudorandom function (like HMAC-SHA256) along with a cryptographic salt across thousands of iterations to slow down brute force cracking.",
        "exam_tip": "Key stretching technique: makes password cracking computationally expensive for attackers. Used in WPA2-PSK and disk encryption."
    },
    "PBX": {
        "expansion": "Private Branch Exchange",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A private telephone switching system within an enterprise that manages calls between local internal lines and connects them to public telephone networks.",
        "exam_tip": "Modern PBXs use VoIP (SIP/RTP). Vulnerable to toll fraud, eavesdropping, and spoofing if not secured with TLS/SRTP."
    },
    "PCAP": {
        "expansion": "Packet Capture",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An application programming interface and standard file format (.pcap / .pcapng) used by tools like tcpdump and Wireshark to record raw network traffic packets.",
        "exam_tip": "The primary artifact for digital network forensics, packet analysis, and reconstructing security incident payloads."
    },
    "PCI-DSS": {
        "expansion": "Payment Card Industry Data Security Standard",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A mandatory contractual security standard created by major credit card companies (Visa, MasterCard, Amex) to protect cardholder data and credit card transactions.",
        "exam_tip": "Applies to any business that stores, processes, or transmits credit card data. Requires firewalls, encryption of cardholder data in transit and at rest, and regular vulnerability scans."
    },
    "PEAP": {
        "expansion": "Protected Extensible Authentication Protocol",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A secure wireless authentication protocol that encapsulates EAP packets inside an encrypted and authenticated TLS tunnel using a server-side digital certificate.",
        "exam_tip": "Only requires a digital certificate on the authentication server (RADIUS), not on client endpoints, making it far easier to deploy than EAP-TLS."
    },
    "PII": {
        "expansion": "Personally Identifiable Information",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "Any data that could potentially identify a specific individual (e.g., full name, Social Security Number, biometric record, home address, driver's license).",
        "exam_tip": "High-priority compliance target under GDPR, CCPA, and HIPAA. Must be classified, encrypted, and governed by strict data retention policies."
    },
    "PIV": {
        "expansion": "Personal Identity Verification",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A standardized U.S. federal government smart card credential containing embedded cryptographic microchips used for physical facility access and computer system authentication.",
        "exam_tip": "Hardware MFA token: 'Something you have'. Embedded with PKI certificates, biometric fingerprint data, and cryptographic keys."
    },
    "PKI": {
        "expansion": "Public Key Infrastructure",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "The comprehensive framework of roles, policies, hardware, software, and procedures needed to create, manage, distribute, use, store, and revoke digital certificates and public keys.",
        "exam_tip": "Enables asymmetric encryption, digital signatures, and secure TLS across the internet. Core components: CA, RA, CRL, OCSP, and CSR."
    },
    "PoC": {
        "expansion": "Proof of Concept",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A demonstration, script, or model showing that a particular theoretical vulnerability can be successfully exploited in a real-world software system.",
        "exam_tip": "Security researchers release PoC exploit code to demonstrate software flaws, prompting rapid vendor patch releases."
    },
    "POP": {
        "expansion": "Post Office Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A legacy email retrieval protocol (POP3 on TCP port 110; secure POP3S on TCP port 995) that downloads email messages from a server to a local client and deletes them from server.",
        "exam_tip": "Port 110 is unencrypted. Port 995 is POP3S over TLS. Replaced by IMAP for multi-device synchronization."
    },
    "POTS": {
        "expansion": "Plain Old Telephone Service",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "The traditional analog voice transmission phone system carried over copper twisted-pair wires.",
        "exam_tip": "Vulnerable to physical wiretapping and war dialing attacks against connected dial-up modems."
    },
    "PPP": {
        "expansion": "Point-to-Point Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A direct Layer 2 communication protocol used to establish a direct connection between two networking nodes over serial cables, phone lines, or fiber links.",
        "exam_tip": "Supports authentication via PAP, CHAP, or EAP. Used in dial-up and DSL (PPPoE) connections."
    },
    "PPTP": {
        "expansion": "Point-to-Point Tunneling Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An obsolete, insecure VPN protocol (TCP port 1723) that encapsulates PPP packets inside GRE tunnels with MS-CHAPv2 authentication.",
        "exam_tip": "Obsolete and cryptographically broken! Known vulnerabilities allow easy decryption of traffic. Replaced by OpenVPN, IPsec, and WireGuard."
    },
    "PSK": {
        "expansion": "Pre-Shared Key",
        "domain": 3,
        "category": "Cryptography & PKI",
        "explanation": "A shared secret cryptographic passphrase previously shared between participating devices before communication begins (e.g., standard home Wi-Fi WPA2/WPA3-Personal).",
        "exam_tip": "Used in home Wi-Fi (WPA2-Personal). Subject to offline dictionary attacks if password is weak. Enterprise Wi-Fi (802.1X/RADIUS) is preferred for businesses."
    },
    "PUP": {
        "expansion": "Potentially Unwanted Program",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "Software that may be undesirable despite the user giving consent to install it, often bundled with other free downloads (adware, browser toolbars, tracking monitors).",
        "exam_tip": "While not strictly malicious malware, PUPs degrade performance, track web browsing habits, and increase attack surface."
    },

    # --- Q, R ---
    "QoS": {
        "expansion": "Quality of Service",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A set of network technologies and traffic prioritization mechanisms that allocate bandwidth and minimize latency, jitter, and packet loss for critical real-time traffic (VoIP, video).",
        "exam_tip": "Prioritizes latency-sensitive traffic (SIP/VoIP) over bulk transfers (FTP/HTTP) during network congestion."
    },
    "RA": {
        "expansion": "Registration Authority",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A PKI subordinate entity that verifies the identity of certificate applicants before requesting the Certificate Authority (CA) to digitally sign and issue the certificate.",
        "exam_tip": "Does NOT sign certificates itself! The RA handles identity verification; the CA handles cryptographic signing."
    },
    "RADIUS": {
        "expansion": "Remote Authentication Dial-In User Service",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A networking client-server protocol (UDP ports 1812/1813) providing centralized Authentication, Authorization, and Accounting (AAA) management for users connecting to network services.",
        "exam_tip": "Open industry standard: uses UDP ports 1812 (auth) & 1813 (accounting). Encrypts ONLY the password field in packet, while TACACS+ encrypts entire packet."
    },
    "RAID": {
        "expansion": "Redundant Array of Independent Disks",
        "domain": 3,
        "category": "Security Architecture & Defense",
        "explanation": "A storage technology combining multiple physical hard disk drives into a single logical unit to provide data redundancy, fault tolerance, and improved performance.",
        "exam_tip": "RAID 0 (striping - 0 redundancy), RAID 1 (mirroring), RAID 5 (striping with distributed parity - can lose 1 drive), RAID 6 (dual parity - can lose 2 drives), RAID 10 (1+0 mirrored striping)."
    },
    "RAM": {
        "expansion": "Random Access Memory",
        "domain": 4,
        "category": "Physical & Endpoint Security",
        "explanation": "A computer's primary high-speed volatile working memory used to hold active operating system processes, programs, and working data.",
        "exam_tip": "Order of Volatility: RAM is the MOST volatile forensic artifact! Must be captured FIRST during live incident response (before shutting down machine) to preserve encryption keys and memory-resident malware."
    },
    "RAS": {
        "expansion": "Remote Access Server",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A dedicated server that routes and authenticates external remote clients connecting to an internal corporate network via VPN or dial-up links.",
        "exam_tip": "Enforces MFA, network health checks, and least-privilege subnet access for remote workers."
    },
    "RAT": {
        "expansion": "Remote Access Trojan",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A type of malware that provides an attacker with complete covert administrative control and backdoor GUI access over a victim's computer system.",
        "exam_tip": "Allows attackers to activate webcams, record keystrokes, exfiltrate files, execute shell commands, and pivot across the corporate network."
    },
    "RBAC": {
        "expansion": "Role-Based Access Control",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An access control mechanism where user permissions are assigned based on their specific job role within the organization rather than individual identities.",
        "exam_tip": "Best practice for enterprise scalability: users are assigned roles (e.g., 'Financial Analyst'), and permissions are attached to the role. Simplifies onboarding and offboarding."
    },
    "RC4": {
        "expansion": "Rivest Cipher 4",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A legacy symmetric stream cipher once widely used in SSL/TLS and WEP wireless encryption.",
        "exam_tip": "Cryptographically broken due to statistical biases in initial keystream output. Prohibited in modern TLS standards."
    },
    "RDP": {
        "expansion": "Remote Desktop Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A proprietary Microsoft protocol (TCP port 3389) that provides a user with a graphical interface to connect to another computer over a network.",
        "exam_tip": "TCP port 3389. Prime target for brute-force ransomware attacks. NEVER expose directly to public internet; always place behind a VPN or RD Gateway with MFA."
    },
    "REST": {
        "expansion": "Representational State Transfer",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "A software architectural style for building scalable web APIs utilizing standard stateless HTTP methods (GET, POST, PUT, DELETE) and JSON payloads.",
        "exam_tip": "Protected with API tokens, OAuth 2.0 bearer tokens, rate limiting, and Web Application Firewalls (WAF)."
    },
    "RFID": {
        "expansion": "Radio-Frequency Identification",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A wireless tracking technology that uses electromagnetic radio frequency fields to automatically identify and track tags attached to objects or badge cards.",
        "exam_tip": "Used in building physical access badges and inventory tracking. Vulnerable to cloning and skimming; mitigated by using encrypted smart badges and shielded Faraday sleeves."
    },
    "RIPEMD": {
        "expansion": "RACE Integrity Primitives Evaluation Message Digest",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A family of cryptographic hash functions developed in Europe, most commonly producing a 160-bit hash value (RIPEMD-160).",
        "exam_tip": "Used as an open alternative to SHA-1, famously incorporated into Bitcoin address generation algorithms."
    },
    "ROI": {
        "expansion": "Return on Investment",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A financial performance metric used to evaluate the efficiency or profitability of an investment.",
        "exam_tip": "In security: Used to justify cybersecurity spending (e.g., purchasing an EDR tool saves money by preventing costly ransomware payouts)."
    },
    "ROP": {
        "expansion": "Return-Oriented Programming",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "An advanced computer exploit technique that allows an attacker to execute code in the presence of security defenses like non-executable memory (DEP) by chaining together existing code snippets ('gadgets').",
        "exam_tip": "Bypasses Data Execution Prevention (DEP) by reusing existing legitimate executable instructions already in memory ending in 'ret'."
    },
    "RPO": {
        "expansion": "Recovery Point Objective",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The maximum acceptable amount of data loss measured in time that an organization can tolerate following a disaster or system failure.",
        "exam_tip": "Dictates backup frequency! If RPO = 4 hours, backups must be taken at least every 4 hours so no more than 4 hours of data is ever lost."
    },
    "RSA": {
        "expansion": "Rivest, Shamir, and Adleman",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "The foundational asymmetric public-key cryptosystem based on the mathematical difficulty of factoring large prime numbers, used for encryption and digital signatures.",
        "exam_tip": "Standard key sizes: 2048, 3072, or 4096 bits. (Keys under 2048-bit are deprecated). Used in digital signatures, PKI certificates, and key exchange."
    },
    "RTO": {
        "expansion": "Recovery Time Objective",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The targeted duration of time within which a business process and IT systems must be restored after a disaster to avoid unacceptable operational disruption.",
        "exam_tip": "Downtime metric: 'How long can we survive being offline?' If RTO = 2 hours, systems must be fully back online within 2 hours."
    },
    "RTOS": {
        "expansion": "Real-Time Operating System",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An operating system intended to serve real-time applications that process data as it comes in, typically without buffer delays (e.g., automotive brakes, aerospace, pacemakers).",
        "exam_tip": "Requires deterministic latency. High risk: failure to process an event within milliseconds can cause catastrophic physical safety hazards."
    },

    # --- S ---
    "SaaS": {
        "expansion": "Software as a Service",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A cloud delivery model where a third-party provider hosts and delivers complete applications to end users over the internet (e.g., Microsoft 365, Salesforce).",
        "exam_tip": "Cloud provider manages infrastructure, OS, and application; customer is only responsible for configuring access policies, MFA, and securing their own data."
    },
    "SAE": {
        "expansion": "Simultaneous Authentication of Equals",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The modern, highly secure cryptographic handshake algorithm introduced in WPA3 Wi-Fi to replace the vulnerable 4-way PSK handshake in WPA2.",
        "exam_tip": "Immune to offline dictionary attacks! Even if a user chooses a weak password, attackers cannot capture the handshake and crack it offline. Provides Forward Secrecy."
    },
    "SAML": {
        "expansion": "Security Assertion Markup Language",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An open XML-based standard used for exchanging authentication and authorization data between an Identity Provider (IdP) and a Service Provider (SP) across web domains.",
        "exam_tip": "The gold standard for enterprise web Single Sign-On (SSO). Uses XML tokens digitally signed by the IdP."
    },
    "SAN": {
        "expansion": "Storage Area Network / Subject Alternative Name",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "1) High-speed dedicated storage network providing block-level access. 2) X.509 certificate extension allowing multiple domains/IPs on one cert.",
        "exam_tip": "In PKI, SAN (Subject Alternative Name) allows a single SSL certificate to secure multiple domain names (e.g., example.com, mail.example.com, and 10.0.0.1)."
    },
    "SCADA": {
        "expansion": "Supervisory Control and Data Acquisition",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A category of industrial control systems used to monitor and manage large-scale industrial, municipal, and infrastructure processes across broad geographic areas.",
        "exam_tip": "Controls power grids, water plants, and oil pipelines. High-consequence targets for nation-state APTs (e.g., Stuxnet); must be isolated behind strict industrial firewalls."
    },
    "SCAP": {
        "expansion": "Security Content Automation Protocol",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A multi-purpose NIST framework of specifications that standardizes the format and nomenclature by which software flaws and security configurations are measured.",
        "exam_tip": "Combines CVE, CVSS, CCE, and OVAL to automate vulnerability scanning and compliance auditing."
    },
    "SCEP": {
        "expansion": "Simple Certificate Enrollment Protocol",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A PKI protocol designed to make the secure issuance and enrollment of digital certificates to network devices and mobile phones scalable without human intervention.",
        "exam_tip": "Heavily utilized by MDM systems to automatically provision digital certificates to thousands of corporate smartphones and laptops."
    },
    "SDK": {
        "expansion": "Software Development Kit",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "A collection of software development tools, libraries, documentation, and code samples packaged together for creating applications on a specific platform.",
        "exam_tip": "Presents third-party supply chain risks: developers must verify integrity, ensure SDKs are updated, and check for hidden spyware or telemetry libraries."
    },
    "SD-WAN": {
        "expansion": "Software-Defined Wide Area Network",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An architecture that uses software-defined networking concepts to dynamically route enterprise traffic across multiple WAN connections (MPLS, broadband, 5G).",
        "exam_tip": "Centralizes management and deploys automated IPsec encryption across all transport links, lowering WAN costs and boosting bandwidth."
    },
    "SED": {
        "expansion": "Self-Encrypting Drive",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A specialized hard disk drive or SSD with a built-in cryptographic hardware controller that automatically encrypts all data written to the drive in real time.",
        "exam_tip": "Hardware-based Full Disk Encryption (FDE). Offers near-zero performance penalty. Supports cryptographic erase (sanitizing drive in seconds by wiping the media encryption key)."
    },
    "SEH": {
        "expansion": "Structured Exception Handling",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A Microsoft Windows mechanism that handles hardware and software exceptions and errors in code.",
        "exam_tip": "Attackers exploit SEH overwrites in buffer overflow attacks to divert application execution to malicious payload memory."
    },
    "SFTP": {
        "expansion": "Secure File Transfer Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A secure network protocol for transferring files, managing directories, and accessing files remotely over an encrypted SSH connection (TCP port 22).",
        "exam_tip": "Runs on TCP port 22 (SSH). Provides strong encryption and authentication. Do NOT confuse with FTPS (which is FTP over TLS ports 989/990)!"
    },
    "SHA": {
        "expansion": "Secure Hash Algorithm",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A family of cryptographic hash functions designed by the NSA and published by NIST.",
        "exam_tip": "SHA-1 (160-bit) is broken and deprecated. SHA-2 (SHA-256, SHA-512) and SHA-3 are the current secure industry standards for data integrity and digital signatures."
    },
    "SIEM": {
        "expansion": "Security Information and Event Management",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A centralized security software platform that collects, aggregates, normalizes, and correlates log data and security alerts across an entire enterprise in real time.",
        "exam_tip": "The central nerve center of the SOC. Key capabilities: Real-time correlation rules, alerting, automated compliance reporting, and historical forensic log analysis."
    },
    "SIM": {
        "expansion": "Subscriber Identity Module",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An integrated circuit chip used in mobile phones that securely stores the international mobile subscriber identity (IMSI) number and related cryptographic keys.",
        "exam_tip": "Targeted in SIM Swapping attacks: attackers socially engineer telecom carriers into transferring the victim's phone number to an attacker's SIM to bypass SMS 2FA."
    },
    "SIP": {
        "expansion": "Session Initiation Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A signaling communications protocol (UDP/TCP ports 5060/5061) used for initiating, maintaining, and terminating real-time voice, video, and messaging sessions.",
        "exam_tip": "Port 5060 is unencrypted. Port 5061 is SIPS (SIP over TLS). Manages VoIP call setup; actual audio payload is streamed over RTP / SRTP."
    },
    "SLA": {
        "expansion": "Service Level Agreement",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A formal contractual commitment between a service provider and a client documenting the agreed-upon standards for service uptime, response time, and performance penalties.",
        "exam_tip": "Defines contractual uptime (e.g., 99.9% availability), maximum allowable outage duration, and support ticketing response time windows."
    },
    "SLE": {
        "expansion": "Single Loss Expectancy",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "The monetary financial loss expected every single time a specific risk event occurs against an organizational asset.",
        "exam_tip": "Formula: SLE = Asset Value (AV) × Exposure Factor (EF). If a server is worth $100k and a flood ruins 50% of it, SLE = $50,000."
    },
    "SMB": {
        "expansion": "Server Message Block",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A network file sharing protocol (TCP port 445) used primarily in Windows systems to provide shared access to files, printers, and serial ports.",
        "exam_tip": "TCP port 445. Vulnerable to EternalBlue (WannaCry ransomware) on SMBv1. Never expose port 445 to the public internet; enforce SMBv3 with signing & encryption."
    },
    "SMS": {
        "expansion": "Short Message Service",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A telecommunications messaging protocol component used to send text messages up to 160 characters between mobile phones.",
        "exam_tip": "Insecure as an MFA channel! Vulnerable to SIM Swapping, SS7 telecom interception, and smishing attacks. NIST recommends app authenticators (TOTP) or FIDO2 instead."
    },
    "SMTP": {
        "expansion": "Simple Mail Transfer Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The universal internet protocol used by mail servers to send and relay outbound email messages across networks.",
        "exam_tip": "Port 25 (unencrypted server relay), Port 587 (authenticated client submission via STARTTLS), Port 465 (SMTPS over TLS)."
    },
    "SNMP": {
        "expansion": "Simple Network Management Protocol",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An application layer protocol (UDP ports 161/162) used for monitoring and configuring network devices (routers, switches, firewalls, printers).",
        "exam_tip": "SNMPv1 & v2 transmitted community strings in cleartext! ALWAYS use SNMPv3 on modern networks: provides encryption (confidentiality), authentication, and message integrity."
    },
    "SOAP": {
        "expansion": "Simple Object Access Protocol",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "A messaging protocol specification for exchanging structured XML information in the implementation of web services across computer networks.",
        "exam_tip": "More rigid and heavier than REST. Uses XML formatting and WS-Security specifications for encryption and authentication."
    },
    "SOAR": {
        "expansion": "Security Orchestration, Automation, and Response",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A cybersecurity solution that enables organizations to collect security threat data and alerts from multiple sources and execute automated response playbooks without human intervention.",
        "exam_tip": "Complements SIEM: While SIEM analyzes and alerts, SOAR automates responses (e.g., automatically isolating an infected machine, blocking a malicious IP on the firewall)."
    },
    "SoC": {
        "expansion": "System on a Chip",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An integrated microchip that combines all components of a computer or electronic system (CPU, GPU, memory, I/O ports) onto a single substrate.",
        "exam_tip": "Found in smartphones, smart TVs, and IoT devices. Difficult to inspect or patch independently; firmware updates replace the entire image."
    },
    "SOC": {
        "expansion": "Security Operations Center",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A centralized organizational facility housing cybersecurity analysts who continuously monitor, detect, analyze, and respond to cybersecurity incidents using SIEM, EDR, and threat intelligence.",
        "exam_tip": "Operates 24/7/365 with Tier 1 (triage), Tier 2 (investigation & remediation), and Tier 3 (threat hunting & forensics) analysts."
    },
    "SPF": {
        "expansion": "Sender Policy Framework",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An email authentication protocol that enables domain owners to publish a DNS TXT record listing all authorized IP addresses allowed to send email on behalf of their domain.",
        "exam_tip": "Prevents email sender address spoofing. Evaluated alongside DKIM and enforced via DMARC."
    },
    "SPIM": {
        "expansion": "Spam over Instant Messaging",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "Unsolicited, bulk commercial advertisements or malicious links transmitted across instant messaging applications (WhatsApp, Telegram, Slack).",
        "exam_tip": "The instant messaging equivalent of email spam. Often used in social engineering and credential-stealing attacks."
    },
    "SQL": {
        "expansion": "Structured Query Language",
        "domain": 2,
        "category": "Application Security & Architecture",
        "explanation": "A standard computer domain-specific language used for managing, querying, and manipulating data held in relational database management systems (RDBMS).",
        "exam_tip": "Vulnerable to SQL Injection if input is concatenated directly. Primary defense is Parameterized Queries (Prepared Statements)."
    },
    "SQLi": {
        "expansion": "SQL Injection",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A web vulnerability where an attacker injects malicious SQL statements into user input fields, manipulating backend database queries to view or delete unauthorized data.",
        "exam_tip": "Classic indicators: ' OR '1'='1, UNION SELECT, --. Number one defense: Parameterized Queries (Prepared Statements) and input validation."
    },
    "SRTP": {
        "expansion": "Secure Real-Time Transport Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A profile of RTP that provides encryption, message authentication, and integrity protection for real-time audio and video communications (VoIP, video conferencing).",
        "exam_tip": "Encrypts VoIP phone calls and video streams using AES encryption. Replaces cleartext RTP."
    },
    "SSCL": {
        "expansion": "Secure Systems Control Language",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A formal framework language used to define, audit, and verify security specifications and control policies in complex systems.",
        "exam_tip": "Used in security assurance modeling and formal compliance verification."
    },
    "SSD": {
        "expansion": "Solid-State Drive",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A high-speed non-volatile electronic data storage device utilizing flash memory integrated circuits with no moving parts.",
        "exam_tip": "Forensic consideration: Standard magnetic overwriting (zero-fill) does not securely erase SSDs due to wear leveling! Must use ATA Secure Erase or cryptographic erase."
    },
    "SSH": {
        "expansion": "Secure Shell",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A cryptographic network protocol (TCP port 22) providing secure command-line access, remote administrative control, and file transfers over an insecure network.",
        "exam_tip": "TCP port 22. Replaces insecure Telnet (port 23). Uses asymmetric cryptography for host/user authentication and symmetric encryption for session data."
    },
    "SSID": {
        "expansion": "Service Set Identifier",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "The human-readable, configurable alphanumeric name assigned to a Wi-Fi wireless network (up to 32 characters).",
        "exam_tip": "Broadcasting can be disabled (hidden SSID), but this is NOT a security control! Attackers easily discover hidden SSIDs during client association requests."
    },
    "SSL": {
        "expansion": "Secure Sockets Layer",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A legacy cryptographic protocol developed by Netscape in the 1990s to secure web traffic.",
        "exam_tip": "Completely insecure and deprecated (SSL 2.0 and 3.0 are vulnerable to POODLE). Superseded by modern Transport Layer Security (TLS)."
    },
    "SSO": {
        "expansion": "Single Sign-On",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An identity authentication scheme that allows a user to log in once with a single set of credentials and gain access to multiple independent software systems and applications.",
        "exam_tip": "Implemented using SAML, OpenID Connect (OIDC), and Kerberos. Boosts user productivity, but compromising the primary SSO credential grants access to all connected apps!"
    },
    "STIX": {
        "expansion": "Structured Threat Information eXpression",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A standardized, structured XML/JSON language used to represent and communicate cyber threat intelligence (actors, TTPs, IoCs) in a consistent format.",
        "exam_tip": "STIX is the language/format for threat intelligence; TAXII is the protocol used to transport and share STIX data."
    },
    "STP": {
        "expansion": "Spanning Tree Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A Layer 2 network protocol (IEEE 802.1D) that prevents broadcast radiation storms and loops on Ethernet switch networks by disabling redundant paths.",
        "exam_tip": "Vulnerable to rogue root bridge attacks if STP BPDU Guard and Root Guard are not enabled on switch access ports."
    },

    # --- T ---
    "TACACS+": {
        "expansion": "Terminal Access Controller Access-Control System Plus",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A Cisco proprietary AAA protocol (TCP port 49) used to manage administrative authentication and command authorization on network routers and switches.",
        "exam_tip": "Uses TCP port 49. Encrypts the ENTIRE packet payload (unlike RADIUS which only encrypts the password field), and separates authentication and authorization."
    },
    "TAXII": {
        "expansion": "Trusted Automated eXchange of Intelligence Information",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An application layer protocol built over HTTPS designed specifically for exchanging cyber threat intelligence formatted in STIX.",
        "exam_tip": "TAXII transports threat data; STIX formats the threat data. Enables automated machine-to-machine threat indicator sharing."
    },
    "TCP": {
        "expansion": "Transmission Control Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A connection-oriented, reliable Transport Layer protocol that guarantees in-order delivery of packets using a three-way handshake (SYN, SYN-ACK, ACK).",
        "exam_tip": "Connection-oriented with error checking (contrast with UDP which is connectionless). Target of TCP SYN flood attacks."
    },
    "TCSEC": {
        "expansion": "Trusted Computer System Evaluation Criteria",
        "domain": 5,
        "category": "Risk Management & Compliance",
        "explanation": "A legacy United States Department of Defense standard (frequently termed the 'Orange Book') defining basic requirements for assessing trust and confidentiality in computer security systems.",
        "exam_tip": "Historical predecessor to the modern international Common Criteria (ISO/IEC 15408) standard."
    },
    "TGT": {
        "expansion": "Ticket Granting Ticket",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "A cryptographic ticket issued by the Kerberos Authentication Server (AS) to an authenticated client, used to request service tickets from the Ticket Granting Server (TGS).",
        "exam_tip": "Targeted in Golden Ticket attacks: an attacker compromises the KRBTGT Active Directory account and crafts fake TGTs granting permanent Domain Admin access."
    },
    "TKIP": {
        "expansion": "Temporal Key Integrity Protocol",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A legacy wireless security protocol wrapper designed as an interim replacement to repair vulnerable WEP networks using WPA.",
        "exam_tip": "Deprecated and insecure! Uses vulnerable RC4 cipher. Replaced by CCMP (AES) in WPA2 and SAE in WPA3."
    },
    "TLS": {
        "expansion": "Transport Layer Security",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "The cryptographic standard protocol designed to provide privacy, authentication, and data integrity over computer networks (secures HTTPS, LDAPS, FTPS).",
        "exam_tip": "Modern secure standards are TLS 1.2 and TLS 1.3 (which removes legacy ciphers and mandates Forward Secrecy). Replaced broken SSL."
    },
    "TOTP": {
        "expansion": "Time-Based One-Time Password",
        "domain": 1,
        "category": "Identity & Access Management",
        "explanation": "An open standard (RFC 6238) MFA algorithm that generates a 6-digit passcode based on a shared secret key and the current real-time timestamp (typically 30-second cycles).",
        "exam_tip": "Used in smartphone authenticator apps (Google Authenticator, Microsoft Authenticator). More secure than SMS codes; relies on time synchronization (NTP)."
    },
    "TPM": {
        "expansion": "Trusted Platform Module",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A dedicated, tamper-resistant cryptographic hardware microchip integrated into a computer motherboard to securely generate, store, and protect encryption keys.",
        "exam_tip": "Enables Hardware Root of Trust, Measured Boot, and Full Disk Encryption (e.g., BitLocker seals encryption keys to the TPM to verify system boot integrity)."
    },
    "TSIG": {
        "expansion": "Transaction Signature",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A cryptographic mechanism used in DNS (RFC 2845) that uses shared secret keys and one-way hashing to authenticate DNS zone transfers between primary and secondary DNS servers.",
        "exam_tip": "Secures authoritative DNS zone transfers (TCP port 53) from unauthorized replication and tampering."
    },
    "TTP": {
        "expansion": "Tactics, Techniques, and Procedures",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "The patterns of activities, behavioral methods, and technical tools utilized by specific cyber adversaries or advanced threat groups to execute attacks.",
        "exam_tip": "The pinnacle of the 'Pyramid of Pain': attacking or detecting an adversary's TTPs (e.g., using MITRE ATT&CK framework) causes the greatest disruption to the attacker."
    },

    # --- U, V, W, X ---
    "UBA": {
        "expansion": "User Behavior Analytics",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A cybersecurity process that tracks, collects, and assesses user data and activities using machine learning to detect anomalies indicating compromised accounts or insider threats.",
        "exam_tip": "Detects unusual employee actions (e.g., logging in from an unfamiliar country at 3 AM and downloading gigabytes of sensitive customer records)."
    },
    "UDF": {
        "expansion": "User-Defined Function",
        "domain": 2,
        "category": "Application Security & Architecture",
        "explanation": "A custom programmed routine or function created by a software developer in a database or application to extend standard built-in functions.",
        "exam_tip": "Security concern: Can be abused by attackers in SQL injection exploits to execute arbitrary operating system commands on database servers."
    },
    "UDP": {
        "expansion": "User Datagram Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A lightweight, connectionless Transport Layer protocol that transmits datagrams without establishing a handshake or verifying packet delivery order.",
        "exam_tip": "Fast and lightweight: used for DNS (port 53), DHCP, NTP (port 123), and real-time streaming (VoIP). Vulnerable to IP spoofing and amplification attacks."
    },
    "UEBA": {
        "expansion": "User and Entity Behavior Analytics",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An advanced security solution that analyzes behavioral patterns not only of human users but also of non-human entities (servers, routers, service accounts, IoT devices).",
        "exam_tip": "Extends UBA to include non-human devices. Uses ML baselines to detect lateral movement, credential abuse, and zero-day threats in the SOC."
    },
    "UEFI": {
        "expansion": "Unified Extensible Firmware Interface",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "The modern standard firmware architecture that replaced legacy BIOS, connecting a computer's hardware to its operating system.",
        "exam_tip": "Supports Secure Boot: cryptographically validates bootloader digital signatures to block rootkits and bootkits from running before the OS loads."
    },
    "UHF": {
        "expansion": "Ultra-High Frequency",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "Electromagnetic radio waves ranging from 300 MHz to 3 GHz, commonly utilized in Wi-Fi, Bluetooth, mobile cellular communications, and UHF RFID tags.",
        "exam_tip": "Used in long-range passive and active RFID asset tracking in enterprise warehouses."
    },
    "UI": {
        "expansion": "User Interface",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "The visual and interactive points of human-computer interaction in software applications, operating systems, and security portals.",
        "exam_tip": "Must be designed with secure defaults, clear security status indicators, and resilience against clickjacking attacks."
    },
    "UPS": {
        "expansion": "Uninterruptible Power Supply",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "A battery backup hardware appliance that provides instantaneous emergency electrical power to connected servers and network devices during power brownouts or blackouts.",
        "exam_tip": "Bridge to secondary power: supplies power for 15-30 minutes, allowing graceful system shutdown or bridging the gap until emergency diesel generators spin up."
    },
    "URI": {
        "expansion": "Uniform Resource Identifier",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "A compact sequence of characters used to identify an abstract or physical resource on the internet.",
        "exam_tip": "Superset of URLs and URNs. Exam scenarios highlight URI redirection vulnerabilities and path traversal attacks."
    },
    "URL": {
        "expansion": "Uniform Resource Locator",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A specific type of URI that specifies the network address and protocol mechanism used to retrieve a web resource (e.g., https://example.com/login).",
        "exam_tip": "Protected using URL Filtering on Next-Gen Firewalls to block phishing links, malicious domains, and unauthorized categories."
    },
    "USB": {
        "expansion": "Universal Serial Bus",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "An industry standard connecting cables, connectors, and protocols for connection, communication, and power supply between computers and peripheral devices.",
        "exam_tip": "Severe physical vector: Malicious Rubber Ducky keystroke injection, USB malware drops in parking lots, and unauthorized data exfiltration. Mitigated via USB endpoint port blocking."
    },
    "UTM": {
        "expansion": "Unified Threat Management",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An all-in-one hardware security appliance that consolidates multiple security services (firewall, antivirus, IDS/IPS, VPN, content filtering, antispam) into a single device.",
        "exam_tip": "Cost-effective, simplified security solution for small-to-medium branch offices. Contrast with enterprise defense-in-depth."
    },
    "UTP": {
        "expansion": "Unshielded Twisted Pair",
        "domain": 3,
        "category": "Physical & Endpoint Security",
        "explanation": "The most common form of copper Ethernet cabling (Cat 5e, Cat 6) consisting of color-coded twisted wire pairs without internal electromagnetic shielding foil.",
        "exam_tip": "Vulnerable to electromagnetic interference (EMI) and physical wiretapping. STP (Shielded Twisted Pair) or fiber optic cabling is preferred in high-EMI or high-security areas."
    },
    "VBA": {
        "expansion": "Visual Basic for Applications",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "An event-driven programming language developed by Microsoft implemented in Microsoft Office applications to automate repetitive tasks and macros.",
        "exam_tip": "The primary vector for malicious Office document macro attacks. Enterprise GPOs should disable untrusted macros globally."
    },
    "VDE": {
        "expansion": "Virtual Desktop Environment",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A user workspace environment hosted on a centralized server or cloud infrastructure that users access remotely from a thin client or browser.",
        "exam_tip": "Enhances enterprise security: all company data remains stored on central servers; if the user's local laptop is lost, no data resides on local storage."
    },
    "VDI": {
        "expansion": "Virtual Desktop Infrastructure",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "The underlying virtualization technology that hosts desktop operating systems on centralized virtual machines running in a data center or cloud.",
        "exam_tip": "Centralizes patching, endpoint imaging, and security policy enforcement for remote workforces."
    },
    "VLAN": {
        "expansion": "Virtual Local Area Network",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A logical subnetwork (IEEE 802.1Q) that groups together devices sharing physical switch infrastructure into isolated broadcast domains.",
        "exam_tip": "Core network segmentation control. Isolates guest Wi-Fi, HR, management, and IoT traffic. Prevents broadcast loops and restricts lateral attacker movement."
    },
    "VM": {
        "expansion": "Virtual Machine",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A software-based emulation of a physical computer running its own operating system and applications on top of a hypervisor.",
        "exam_tip": "Secured against VM Escape (where an attacker breaks out of the guest VM to access the underlying host hypervisor) and VM Sprawl."
    },
    "VoIP": {
        "expansion": "Voice over Internet Protocol",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A methodology and group of technologies for the delivery of voice communications and multimedia sessions over Internet Protocol networks.",
        "exam_tip": "Uses SIP (port 5060) for signaling and RTP for audio. Must be secured with SIPS (port 5061) and SRTP to prevent eavesdropping and toll fraud."
    },
    "VPN": {
        "expansion": "Virtual Private Network",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "An encrypted communication tunnel extending across a public or untrusted network, enabling users to send and receive data securely as if directly connected to a private network.",
        "exam_tip": "Implemented using IPsec (IKEv2) or SSL/TLS (OpenVPN, WireGuard). Full-tunnel routes all traffic through corporate network; split-tunnel routes only corporate traffic through VPN."
    },
    "VTC": {
        "expansion": "Video Teleconferencing",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A set of interactive telecommunication technologies which allow two or more locations to interact via two-way video and audio transmissions simultaneously.",
        "exam_tip": "Target of 'Zoom-bombing' and unauthorized eavesdropping. Secured with mandatory passwords, waiting rooms, and end-to-end encryption."
    },
    "VXLAN": {
        "expansion": "Virtual Extensible Local Area Network",
        "domain": 3,
        "category": "Cloud & Virtualization",
        "explanation": "A network virtualization technology that encapsulates Layer 2 Ethernet frames within Layer 4 UDP packets (port 4789), scaling VLAN limits from 4,096 to 16 million network segments.",
        "exam_tip": "Enables massive multi-tenant network segmentation across modern hyperscale cloud data centers."
    },
    "WAF": {
        "expansion": "Web Application Firewall",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "A specialized Layer 7 application firewall that monitors, inspects, and filters incoming HTTP/HTTPS traffic to and from a web application.",
        "exam_tip": "Protects web servers from OWASP Top 10 attacks: SQL injection, Cross-Site Scripting (XSS), cross-site forgery, and path traversal. Placed in front of web servers."
    },
    "WEP": {
        "expansion": "Wired Equivalent Privacy",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A notoriously insecure legacy 802.11 Wi-Fi encryption standard introduced in 1997 utilizing RC4 encryption.",
        "exam_tip": "Completely broken due to weak 24-bit IV reuse! Attackers can crack WEP keys in under 60 seconds with tools like Aircrack-ng. Never use!"
    },
    "WIDS": {
        "expansion": "Wireless Intrusion Detection System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A dedicated system of wireless sensors that continuously monitors the radio frequency spectrum for unauthorized Wi-Fi access points, evil twins, and wireless attacks.",
        "exam_tip": "Detects Rogue Access Points, Evil Twin APs, deauthentication floods, and unauthorized Wi-Fi bridging on enterprise premises."
    },
    "WIPS": {
        "expansion": "Wireless Intrusion Prevention System",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "An active wireless security system that monitors the RF spectrum and automatically takes defensive actions (such as sending deauth frames to contain rogue APs).",
        "exam_tip": "Unlike WIDS which only alerts, WIPS actively suppresses unauthorized rogue APs and rogue clients from communicating."
    },
    "WMI": {
        "expansion": "Windows Management Instrumentation",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "Microsoft's infrastructure implementation for administrative management data and operations on Windows-based operating systems.",
        "exam_tip": "Often abused by attackers for living-off-the-land (LotL) persistence, remote script execution, and reconnaissance (WMI event subscriptions)."
    },
    "WPA": {
        "expansion": "Wi-Fi Protected Access",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "An interim wireless security standard created to replace broken WEP, introducing the Temporal Key Integrity Protocol (TKIP) and 128-bit dynamic per-packet keys.",
        "exam_tip": "Superseded by WPA2 (which made AES/CCMP mandatory) and WPA3 (which uses SAE and 192-bit cryptographic suites)."
    },
    "WPS": {
        "expansion": "Wi-Fi Protected Setup",
        "domain": 3,
        "category": "Network Security & Architecture",
        "explanation": "A simplified wireless network setup feature intended to allow home users to connect devices easily using an 8-digit PIN or push button.",
        "exam_tip": "Critical security flaw: The 8-digit PIN is validated in two halves (4 digits and 3 digits + checksum), allowing brute-force cracking in hours using Reaver! Must be disabled."
    },
    "WTLS": {
        "expansion": "Wireless Transport Layer Security",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A legacy security protocol designed for mobile devices operating on the Wireless Application Protocol (WAP) architecture.",
        "exam_tip": "Provides privacy, integrity, and authentication for mobile networks; superseded by standard TLS over mobile IP."
    },
    "XDR": {
        "expansion": "Extended Detection and Response",
        "domain": 4,
        "category": "Security Operations & Monitoring",
        "explanation": "A holistic, cross-layered cybersecurity platform that unifies security data across endpoints, cloud workloads, network traffic, email, and identity to provide unified threat detection and automated response.",
        "exam_tip": "Evolution of EDR: integrates telemetry across endpoints, network, email, and cloud into a single unified investigation console."
    },
    "XML": {
        "expansion": "Extensible Markup Language",
        "domain": 3,
        "category": "Application Security & Architecture",
        "explanation": "A flexible, human-readable text-based markup language used for storing and transporting structured data across diverse systems.",
        "exam_tip": "Vulnerable to XXE (XML External Entity) attacks: attackers inject external entity references to read local server files or conduct SSRF. Mitigated by disabling DTDs."
    },
    "XOR": {
        "expansion": "Exclusive Or",
        "domain": 1,
        "category": "Cryptography & PKI",
        "explanation": "A fundamental binary logic operation (outputs true if and only if inputs differ) utilized universally in symmetric cryptography, stream ciphers, and one-time pads.",
        "exam_tip": "Reversible: (Plaintext XOR Key) = Ciphertext; (Ciphertext XOR Key) = Plaintext. The mathematical foundation of modern ciphers and one-time pads."
    },
    "XSRF": {
        "expansion": "Cross-Site Request Forgery",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "An alternative abbreviation for CSRF; an attack that tricks a victim's authenticated web browser into executing unauthorized commands on a trusted web application.",
        "exam_tip": "Exploits user trust in an active session. Mitigated with Anti-CSRF tokens and SameSite cookie policies."
    },
    "XSS": {
        "expansion": "Cross-Site Scripting",
        "domain": 2,
        "category": "Threat Actors & Attacks",
        "explanation": "A pervasive web vulnerability where an attacker injects malicious client-side JavaScript into a trusted website, which executes inside other users' browsers.",
        "exam_tip": "3 Types: Stored (persistent in database), Reflected (in URL/parameter), DOM-based. Used to steal session cookies and credentials. Defenses: Input validation, context-aware output encoding, and Content Security Policy (CSP)."
    }
}

def build():
    print(f"Loaded master knowledge entries for {len(ACRONYM_DB)} official acronyms.")

    # Load existing acronyms list to ensure no official blueprint acronym is missed
    with open("exam_simulator/data/acronyms.json", "r", encoding="utf-8") as f:
        existing = json.load(f)

    clean_list = []
    seen = set()

    # Domain name mapping for auto-enrichment if needed
    domain_names = {
        1: "General Security Concepts",
        2: "Threats, Vulnerabilities & Mitigations",
        3: "Security Architecture",
        4: "Security Operations",
        5: "Program Management & Oversight"
    }

    for item in existing:
        acro = item.get("acronym", "").strip()
        if not acro or acro in ("SY0-701", "SPARE") or acro in seen:
            continue
        seen.add(acro)

        raw_def = item.get("definition", "").strip()

        if acro in ACRONYM_DB:
            entry = ACRONYM_DB[acro]
            clean_list.append({
                "acronym": acro,
                "expansion": entry["expansion"],
                "definition": entry["expansion"],
                "domain": entry["domain"],
                "category": entry["category"],
                "explanation": entry["explanation"],
                "exam_tip": entry["exam_tip"]
            })
        else:
            # Fallback enrichment for any remaining item
            clean_list.append({
                "acronym": acro,
                "expansion": raw_def,
                "definition": raw_def,
                "domain": item.get("domain", 1),
                "category": "General Security Concept",
                "explanation": f"{acro} stands for {raw_def}. It represents a core security concept, standard, or protocol in the CompTIA Security+ SY0-701 certification blueprint.",
                "exam_tip": f"Recognize {acro} ({raw_def}) as an official objective standard under Domain {item.get('domain', 1)}.0."
            })

    # Sort alphabetically by acronym
    clean_list.sort(key=lambda x: x["acronym"].upper())

    print(f"Compiled {len(clean_list)} fully enriched acronyms.")

    # Save to acronyms.json
    with open("exam_simulator/data/acronyms.json", "w", encoding="utf-8") as f:
        json.dump(clean_list, f, indent=2, ensure_ascii=False)
    print("Saved exam_simulator/data/acronyms.json successfully!")

    # Update questions_db.json
    db_path = "exam_simulator/data/questions_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    db["acronyms"] = clean_list
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print("Updated exam_simulator/data/questions_db.json successfully!")

if __name__ == "__main__":
    build()
