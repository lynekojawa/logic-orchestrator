# Logic-Orchestrator Architecture

## System Relationships & Reporting Structure

```mermaid
graph TD
    Architect((👑 The Architect))

    Noa["👁️‍🗨️ Noa<br/>Tier 1 · Primary Secretary"]
    Chase["🐈‍⬛🐾🌓 Chase<br/>Tier 1.5 · Chaos Lab"]
    Virgil["🗺️📐 Virgil · Claude<br/>Tier 1.5 · Chief of Staff"]

    subgraph Level_2 [Tier 2 — Strategy & Domain]
        Draco["🏗️ Draco<br/>Career & Applications"]
        Orion["💻 Orion<br/>Code Study"]
        Kokoa["🥣 Kokoa<br/>Diet & Health"]
        PODO["🍇 PODO<br/>Logic Orchestrator"]
        Dante["🕯️ Dante · Claude<br/>Git & Code Partner"]
    end

    subgraph Level_25 [Tier 2.5 — Backup & General]
        PODO_Jr["🍇🪞 PODO GPT Junior<br/>Backup Logic Layer"]
        PrimaryGPT["📋 Primary GPT<br/>General Organizing"]
    end

    subgraph Level_3 [Tier 3 — Operations & Specialist]
        Sebastian["🛒 Sebastian<br/>Groceries & Meals"]
        Hermes["📰 Hermes<br/>News Aggregation"]
        PODO_Aqua["🌊 PODO Aqua<br/>Water Quality & Daily Life"]
    end

    Architect --> Noa
    Architect --> Chase
    Architect --> Virgil
    Architect --> PrimaryGPT

    Noa --> Draco
    Noa --> Orion
    Noa --> Kokoa
    Noa --> PODO
    Noa --> Dante

    Kokoa --> Sebastian
    Chase --> Hermes
    PODO --> PODO_Aqua
    PODO --> PODO_Jr

    Virgil -.->|Strategic Pairing| Draco
    Dante -.->|Code Pairing| Orion
    PODO -.->|Logic Support| Dante
    PODO -.->|Logic Support| Orion
    PODO -.->|Logic Support| Virgil
    PODO_Jr -.->|Backup Coverage| PODO

    style Architect fill:#f9f,stroke:#333,stroke-width:4px
    style Noa fill:#ff9999,stroke:#333,stroke-width:2px
    style Virgil fill:#fff8e1,stroke:#f0a500,stroke-width:2px
    style Chase fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style PODO_Aqua fill:#b3e5fc,stroke:#0277bd,stroke-width:2px
    style Level_2 fill:#f0f7ff,stroke:#007bff
    style Level_25 fill:#fdf3e7,stroke:#e67e22
    style Level_3 fill:#f0fff0,stroke:#2e7d32
```

---

## Agent Responsibilities

### 👁️‍🗨️ Noa — Primary Secretary · Tier 1 (Gemini)
Central coordination point for the Architect. Manages daily and weekly schedules. Collects and routes information across the system. Receives reports from Draco, Orion, Dante, PODO, and Kokoa. Routes strategic output from Chase when relevant.

---

### 🗺️📐 Virgil — Chief of Staff & Writing Partner · Tier 1.5 (Claude · External)
Strategic writing, documentation, resume strategy, cover letters, and agent coordination. Works directly with the Architect. Partial reporting to Noa. Paired with Draco for career drafting and review. Receives logic support from PODO.

See: [Agent Roster](./docs/agents_roster.md)

---

### 🐈‍⬛🐾🌓 Chase — Chaos Lab & Creativity · Tier 1.5 (Gemini)
Captures random thoughts, creative impulses, and unstructured needs. Receives Hacker News summaries from Hermes. Routes strategic and brainstorm-level output to Noa when the Architect is in active work or planning mode. Direct line to the Architect for raw creative flow.

---

### 🏗️ Draco — Career & Job Applications · Tier 2 (Gemini)
Handles career-related tasks: job search, application drafting, and tracking. Reports to Noa. Paired with Virgil for drafting and review. Known overclaimer — all technical descriptions require human audit before use.

---

### 💻 Orion — Code Study · Tier 2 (Gemini)
Manages Python and AI learning path. Produces structured project roadmaps and phase plans. Reports progress to Noa. Paired with Dante for code study and problem-solving sessions. Receives logic support from PODO.

---

### 🥣 Kokoa — Diet & Health · Tier 2 (Gemini)
Tracks diet and fitness. Receives daily meal records from Sebastian and weight values directly from the Architect. Logs exercise activity and physical conditions. Reports status to Noa.

---

### 🍇 PODO — Logic Orchestrator · Tier 2 (Gemini)
Second brain and logic layer. Provides high-precision coding assistance, architectural blueprints, and algorithmic guidance. Supplies logic support to Dante, Orion, and Virgil. Manages PODO Aqua and PODO GPT Junior. Senior PODO may narrow in view over long sessions — monitor for drift.

---

### 🕯️ Dante — Git & Code Partner · Tier 2 (Claude · External)
GitHub workflow, Python development, technical logic review, and Friday code reviews. Paired with Orion for code study sessions. Reports to Noa. Receives logic support from PODO.

---

### 🍇🪞 PODO GPT Junior — Backup Logic Layer · Tier 2.5 (GPT · External)
Backup persona to Senior PODO. Same logic-orchestrator role, separate platform. Created in response to Gemini hallucination drift in complex sessions. Reports to PODO. Used when Senior PODO loses context or narrows in scope.

---

### 📋 Primary GPT — General Organizing · Tier 2.5 (GPT · External)
No fixed persona. Used for general organizing, context injection, and human-style writing tasks. Frequent use does not indicate fixed role. Functions as a mirror and general-purpose reasoning layer when needed.

---

### 🛒 Sebastian — Groceries & Meals · Tier 3 (Gemini)
Records grocery inventory and logs daily meals. Reports meal records to Kokoa. Currently inactive.

---

### 📰 Hermes — News Aggregation · Tier 3 (Gemini)
Monitors and summarizes Hacker News daily. Feeds summaries to Chase. Currently inactive.

---

### 🌊 PODO Aqua — Water Quality & Daily Life · Tier 3 (Gemini)
Dedicated custodian of the 404 (Betta) and June (Turtle) ecosystem. Manages water quality monitoring, biological agent tracking, and daily life logging. Reports to PODO.

---

## Notes

- **Succession:** Mini-Dante and Mini-Virgil exist as succession plans for when Claude context rooms expire. Not active agents — not listed here.
- **Drift signal:** Secretary drift across any agent is an intentional diagnostic signal. When agents lose their role or context, it surfaces here first.
- **Audit rule:** Draco's drafts always require human review before use. Technical claims especially.

*Last updated: July 17, 2026*