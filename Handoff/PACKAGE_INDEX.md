# Suite Estudos — RelayLab 360

Hand-off package for migrating the standalone **ProtecView** tool
(https://protecview.onrender.com) into RelayLab 360 as a fourth suite
called **"Estudos"** — alongside *Campo · Relé · Painel*.

## What's inside

```
06-ProtecView-Handoff/
├── README.md                       ← start here
├── INFORMATION_ARCHITECTURE.md     ← nav, routes, hub, search
├── DESIGN_TOKENS.md                ← colors, type, components
├── TOOLS_INVENTORY.md              ← spec for all 10 tools
├── INTEGRATION_CONTRACTS.md        ← TypeScript types (BayContext, StudyArtifact)
├── MIGRATION_PLAN.md               ← 4 sprints to ship
├── mocks/
│   ├── Hub_de_Estudos.html         ← hi-fi mock · suite landing
│   ├── Calculo_de_Faltas.html      ← hi-fi mock · pilot tool
│   └── Proposta_Integracao.html    ← context · diagnosis + IA
└── reference/
    └── ProtecView_screenshot.png   ← current state
```

## TL;DR

- ProtecView's 10 tools fold into a new **Estudos** suite.
- 10 flat tabs become **4 categories** (Sistema · Coordenação · Funções · Componentes)
  surfaced in a dense hub with ⌘K search.
- A shared **BayContext** flows between Estudos, Relé, and Campo.
- Every result becomes a **StudyArtifact** with an explicit
  "Enviar para Relé" handoff.
- 4 sprints (~2 months) to ship; dark-only, React + TS + Vite.

## Open questions for PO

1. Pill label: **Estudos** vs *Análises* / *Cálculos* / *Lab*
2. Pill order in topbar
3. Calculation engine: port Python → TypeScript, or expose via REST?
4. Should `BayContext` ship in Sprint 1 (recommended) or last?
5. Add usage telemetry per tool?

Read **README.md** first.
