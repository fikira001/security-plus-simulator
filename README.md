# OpenSecPlus — SY0-701 Security+ Exam Simulation Suite

**An open-source, browser-based exam preparation platform for the CompTIA Security+ (SY0-701) certification.**

> This project is not affiliated with or endorsed by CompTIA, Inc. "CompTIA" and "Security+" are trademarks of CompTIA, Inc.

---

## Features

- **5 Full-Length Timed Exams** modeled on the official Pearson VUE testing format (90-minute countdown, review screen, scaled scoring 100–900)
- **Domain Drills** — targeted practice sessions per domain with instant feedback and explanations
- **15 Performance-Based Question (PBQ) Simulations** — firewall ACLs, incident response, PKI configuration, and more
- **Adaptive Randomized Exam Generator** — generates fresh exams weighted by official blueprint percentages
- **Global Search** — search across acronyms, domain objectives, PBQs, and question content in one keystroke
- **Domain Study Guides** — structured notes covering all 5 SY0-701 domains with accordion objectives
- **316 Official Acronym Flashcards** — flip mode, 4-option recall quiz, and searchable glossary table
- **Quick Reference Cheat Sheets** — ports, cryptography, incident response, risk formulas, security controls matrix
- **Missed Questions Bank** — automatically tracks incorrect answers across sessions for targeted remediation
- **Light and Dark Theme** — crisp modern UI with full keyboard navigation support
- **100% Offline** — no external dependencies at runtime; runs from a simple Python HTTP server

---

## Project Structure

```
opensecplus/
├── exam_simulator/
│   ├── index.html          # Main application shell (single-page app)
│   ├── app.js              # Application logic (exam engine, navigation, search)
│   ├── style.css           # Styling (light/dark themes, SaaS dashboard layout)
│   ├── server.py           # Local HTTP server for the exam_simulator directory
│   └── data/
│       ├── questions_db.json         # Question database (MCQs, PBQs, Acronyms)
│       ├── domain_study_guides.json  # Structured study notes per domain
│       └── acronyms.json             # Standalone acronym glossary
├── scripts/
│   └── verify_database.py    # Data integrity verification utility
├── server.py                 # Root-level launcher (serves exam_simulator/)
├── Start-Exam-Simulator.bat  # One-click Windows launcher
├── FAST_PASS_STUDY_GUIDE.md  # Condensed exam strategy and high-yield reference
└── LICENSE                   # MIT License with educational disclaimer
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A modern web browser (Chrome, Edge, Firefox)

### Launch (Windows)

```
Double-click: Start-Exam-Simulator.bat
```

### Launch (Any OS)

```bash
python server.py
```

Then open `http://localhost:8000` in your browser.

---

## Exam Blueprint Coverage

| Domain | Official Weight | Focus |
|--------|:--------------:|-------|
| 1.0 General Security Concepts | 12% | CIA triad, AAA, cryptography, certificates |
| 2.0 Threats, Vulnerabilities & Mitigations | 22% | Attack types, threat actors, hardening |
| 3.0 Security Architecture | 18% | Cloud, segmentation, Zero Trust, firewalls |
| 4.0 Security Operations | 28% | SIEM, incident response, forensics, IAM |
| 5.0 Security Program Management | 20% | Governance, risk formulas, compliance |

---

## Legal & Disclaimer

This project is an independent community study tool. No proprietary exam questions or third-party copyrighted content are distributed here. All content is independently authored or paraphrased from publicly available certification objective outlines. See [LICENSE](./LICENSE) for full terms.

---

## Contributing

Pull requests and issue reports are welcome. Please do not submit proprietary exam content, verbatim commercial question dumps, or any third-party copyrighted materials.

---

## Star This Project

If this helped you study, give it a star and share it with others preparing for their certification journey!
