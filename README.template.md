<!--
  ✏️ EDIT THIS FILE, NOT README.md
  README.md and everything in assets/ are rebuilt automatically by a GitHub Action
  (on every change here + once a day). Hero text, terminal lines and tags live at the
  top of .github/scripts/build_readme.py.
-->

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg" />
  <img alt="Ayush Gupta: Full-Stack Engineer and AI Systems Builder" src="assets/hero-dark.svg" width="100%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/terminal-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/terminal-light.svg" />
  <img alt="Terminal: whoami, current focus, live GitHub stats and latest commits" src="assets/terminal-dark.svg" width="100%" />
</picture>
</p>

<p align="center">
  <i>I build <b>systems that think</b>: an AI agent that patches vulnerabilities before merge, a vision pipeline that explains <b>why</b> a scene is dangerous, and a B2B platform where business rules live in the database instead of hardcoded <code>if</code> statements.</i>
</p>

---

### 🚀 Featured Projects

#### 🛡️ [CodeJanitor]({{REPO:codejanitor|code-janitor|janitor}}): Autonomous Security Agent{{DEMO_LINK:codejanitor|code-janitor|janitor}}
> *Catches vulnerabilities on commit, patches them using real call-graph context, and proves the fix in a sandbox before merge.*

```mermaid
flowchart LR
    A[GitHub Commit] -->|Webhook| B[FastAPI Agent]
    B --> C[Static Diff Analysis]
    C --> D[Graph RAG<br/>AST + ChromaDB]
    D --> E[Context-Grounded<br/>Patch Generation]
    E --> F[Docker Sandbox<br/>Red Team Exploits]
    F -->|Exploit blocked| G[✅ Safe to Merge]
    F -->|Exploit succeeds| E
```

- AST-based **Graph RAG** maps cross-file dependencies, so patches are grounded in real call graphs instead of hallucinated context
- Ephemeral **Docker sandbox** runs exploit scripts against patched code with **100% host contamination prevention** across test runs

`Python` `FastAPI` `ChromaDB` `Graph RAG` `Docker`

---

#### 💼 [DealFlow360]({{REPO:dealflow360|dealflow|deal-flow|quote-to-cash}}): Self-Governing B2B Quote-to-Cash Platform{{DEMO_LINK:dealflow360|dealflow|deal-flow|quote-to-cash}}
> *Pricing, risk scoring, and approvals driven by database-configurable rules, with real-time sync everywhere.*

- Single-write **event pipeline** powering audit logs, live dashboards, and UI sync over **Server-Sent Events**
- **RBAC across 6 roles and 20+ capabilities**, enforced on both client and server
- Multi-warehouse fulfillment splitting, hybrid subscription billing with **day-accurate proration**, and negotiation threads that auto-reroute for re-approval when terms breach policy
- One-command Docker setup · **32 automated backend tests** covering pricing, RBAC, and fulfillment edge cases

`FastAPI` `PostgreSQL` `React` `TypeScript` `Docker` `SSE`

---

#### 👁️ [AI Scene Safety Classifier]({{REPO:scene-safety|scenesafety|safety-classifier|scene|safety}}): Explainable Vision for Accessibility{{DEMO_LINK:scene-safety|scenesafety|safety-classifier|scene|safety}}
> *Classifies scenes as Safe / Caution / Danger in real time, and explains the verdict out loud.*

- Hybrid pipeline: **DeepLabV3 semantic segmentation** + **Mamdani fuzzy-logic** controller
- Left-Center-Right spatial zoning over a **1 to 12 m range**, so risk scales with proximity *and* obstacle position
- Rule-based explainability layer cut **false-safe predictions by ~20%**, with natural-language audio output

`PyTorch` `OpenCV` `DeepLabV3` `Fuzzy Logic`

---

### 🔥 Recently Active

{{LATEST_REPOS}}

---

### 💼 Experience

| Company | Role | Impact |
|---|---|---|
| **Innodatatics** · Hyderabad<br/><sub>Jun 2025 to Jul 2025</sub> | Full-Stack Developer (MERN) | Unified YouTube, Telegram, X and Meta analytics, **cutting manual reporting by 80% (~10 hrs/week)** · Role-aware JWT app for **200+ users** · Resume parser with **95% accuracy**, **5 days faster** hiring cycle |
| **Transmed** · Remote (Erasmus+)<br/><sub>Mar 2025 to Jul 2025</sub> | Full-Stack Developer (MERN) | Built and deployed a consortium platform serving **10+ global universities**, raising partner engagement **40%** · Role-based dashboards with interactive Recharts analytics |

---

### 🛠️ Tech Stack

**Languages**
<br/>
<img src="https://skillicons.dev/icons?i=cpp,py,js,ts,java,cs,html,css&theme=dark" alt="Languages" />

**Backend, Frontend & DevOps**
<br/>
<img src="https://skillicons.dev/icons?i=react,nodejs,express,fastapi,flask,mongodb,postgres,docker,git,vercel&theme=dark" alt="Frameworks and tools" />

**AI / ML & Creative**
<br/>
<img src="https://skillicons.dev/icons?i=pytorch,tensorflow,opencv,unity,blender,figma&theme=dark" alt="AI ML and creative tools" />

<sub>Also: ChromaDB · Graph RAG · DeepLabV3 · Semantic Segmentation · Fuzzy Logic · Hugging Face Spaces · XR/VR · REST APIs · Server-Sent Events</sub>

---

### 📊 Activity

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/stats-light.svg" />
  <img alt="GitHub stats" src="assets/stats-dark.svg" width="49%" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/languages-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/languages-light.svg" />
  <img alt="Top languages" src="assets/languages-dark.svg" width="49%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/snake-light.svg" />
  <img alt="Snake eating my contribution graph" src="assets/snake-dark.svg" width="100%" />
</picture>
</p>

---

### 🏆 Achievements & Leadership

| | |
|---|---|
| 🥇 **Finalist**: Odoo Hackathon 2026 (national) | 🚀 **Semi-Finalist**: Flipkart GRiD 8.0 |
| 📰 **Semi-Finalist**: Economic Times Hackathon | 🇮🇳 **Qualified**: Smart India Hackathon Internals 2024 |
| 🎤 **Student Engagement & Training Lead**: hosted 20+ events including hackathons | 📊 **Placement Committee Ambassador**: leading the Data & Email team for campus placements |

---

### 📫 Let's Connect

<p align="center">
  {{LINKEDIN_BADGE}}
  <a href="mailto:ayushgupta1075.hb@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://github.com/{{USERNAME}}?tab=repositories"><img src="https://img.shields.io/badge/All_Projects-181717?style=for-the-badge&logo=github&logoColor=white" alt="All projects" /></a>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg" />
  <img alt="Footer wave" src="assets/footer-dark.svg" width="100%" />
</picture>
<br/><sub>Auto-updated {{UPDATED}} by a GitHub Action I wrote · <a href="https://github.com/{{USERNAME}}/{{USERNAME}}/blob/main/.github/scripts/build_readme.py">see how</a></sub>
</p>
