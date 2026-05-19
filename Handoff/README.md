# Handoff — Integração ProtecView → RelayLab 360 (suíte "Estudos")

## 1. Visão geral

Este pacote contém **o plano e o design** para migrar a ferramenta avulsa
**ProtecView** (Dash · https://protecview.onrender.com) para dentro do
**RelayLab 360**, como uma **4ª suíte** chamada **"Estudos"** — ao lado de
*Campo · Relé · Painel*.

```
┌──────────────────────────────────────────────────────────────────┐
│  Topbar RelayLab 360                                              │
│  [RL]  RelayLab 360       [Estudos] [Campo] [Relé] [Painel]   ⓘ │
└──────────────────────────────────────────────────────────────────┘
                ↑
                └─ pílula nova (esta entrega)
```

Dentro de **Estudos**, as 10 ferramentas atuais do ProtecView são
re-agrupadas em **4 categorias por intenção de uso**:

| Categoria | Ferramentas |
|---|---|
| **Sistema** | Componentes Simétricos · Cálculo de Faltas |
| **Coordenação** | Curvas TCC · Proteção de Distribuição |
| **Funções de Proteção** | Distância (21) · Diferencial (87) · Inrush |
| **Componentes** | Ampacidade de Cabos · Saturação de TC |

> **Status do design:** alta fidelidade para **Hub de Estudos** e
> **Cálculo de Faltas** (ferramenta-piloto). Demais 8 ferramentas têm
> especificação funcional + tokens definidos — a aparência deriva
> diretamente do sistema mostrado na piloto.

## 2. O que muda em relação ao ProtecView atual

A migração **não é um reskin**. Cinco coisas mudam:

1. **Identidade** — adota o sistema visual do RelayLab 360 (Rajdhani +
   JetBrains Mono, paleta laranja `#F97316` / ciano `#0EA5E9`, cards `.ph`).
2. **Topbar** — substituída pela topbar canônica do RelayLab. O nome
   "ProtecView" desaparece da chrome; vira o **rótulo da suíte** ("Estudos").
3. **Hub de entrada** — a "Home" apologética (*"Bem-vindo ao ProtecView…"*) é
   substituída por um **hub denso** com busca ⌘K, filtros por categoria,
   recentes e cards de ferramenta.
4. **Bay de contexto** — parâmetros do sistema (Vₙ, Sₛc, X/R, Iₙ, TC, TP)
   passam a viver num **componente compartilhado** que percorre todas as
   ferramentas de Estudos e flui também para Relé e Campo.
5. **Continuidade Estudos → Relé** — toda ferramenta que produz um
   ajuste (pickup, time dial, slope, zona) ganha o CTA **"Enviar como preset
   para Relé"**, materializando a integração de dados via `StudyArtifact`
   (veja `INTEGRATION_CONTRACTS.md`).

## 3. Arquivos deste pacote

| Arquivo | Para quê serve |
|---|---|
| `README.md` | Este documento — visão geral + escopo |
| `INFORMATION_ARCHITECTURE.md` | Nav, rotas, hierarquia, busca, atalhos |
| `DESIGN_TOKENS.md` | Cores, tipografia, componentes compartilhados |
| `TOOLS_INVENTORY.md` | Fichas das 10 ferramentas (inputs, outputs, fórmulas, status) |
| `INTEGRATION_CONTRACTS.md` | Tipos TypeScript do `BayContext` e `StudyArtifact` |
| `MIGRATION_PLAN.md` | Plano em 4 sprints + critérios de aceite |
| `mocks/Hub_de_Estudos.html` | Mock hi-fi · tela inicial da suíte |
| `mocks/Calculo_de_Faltas.html` | Mock hi-fi · ferramenta-piloto |
| `mocks/Proposta_Integracao.html` | Diagnóstico + IA + comparativo (apresentação) |
| `reference/ProtecView_screenshot.png` | Estado atual (captura) |

## 4. Stack-alvo (recomendação)

A entrega anterior do RelayLab usou **React + TypeScript + Vite**. Mantemos
essa stack:

- **Framework:** React 18 + TypeScript
- **Build:** Vite
- **Roteamento:** React Router (`/estudos/*`)
- **Estado:** Zustand para `BayContext` (compartilhado); estado local por
  ferramenta com `useState`/`useReducer`
- **Gráficos:** Recharts para TCC e curvas dinâmicas; SVG inline para
  fasores e R-X
- **Fonts:** Google Fonts (Rajdhani + JetBrains Mono — já carregadas)
- **i18n:** pt-BR (atual); estrutura preparada para en/es

> Se o motor de cálculo atual do ProtecView é Python (Dash), recomenda-se
> **portar a lógica para TypeScript** (sem servidor) — todas as ferramentas
> são computacionalmente leves (matriz 6×6 no pior caso). Alternativa: expor
> o backend Python como microsserviço REST e consumir via fetch — funciona,
> mas adiciona latência e infra.

## 5. Ordem de leitura sugerida

1. **Este README** (5 min) — entender o quê
2. **INFORMATION_ARCHITECTURE.md** (10 min) — entender o onde
3. **mocks/Hub_de_Estudos.html** + **mocks/Calculo_de_Faltas.html** (15 min) —
   ver o como
4. **DESIGN_TOKENS.md** (15 min) — componentes a construir
5. **INTEGRATION_CONTRACTS.md** (10 min) — tipos e fluxo de dados
6. **TOOLS_INVENTORY.md** (referência) — abrir conforme migra cada ferramenta
7. **MIGRATION_PLAN.md** (5 min) — planejar as sprints

## 6. Definição de pronto (DoD da integração inteira)

- [ ] Pílula **Estudos** visível e funcional na topbar do RelayLab 360
- [ ] As 10 ferramentas do ProtecView acessíveis em `/estudos/*` com paridade
      funcional (cálculo idêntico, ±0,1% de tolerância)
- [ ] Hub com busca ⌘K, filtros e cards densos
- [ ] `BayContext` implementado e persistente por sessão
- [ ] Pelo menos 3 fluxos de continuidade funcionando:
      Faltas → Relé (preset), Faltas → Saturação de TC, Faltas → TCC
- [ ] `protecview.onrender.com` configurado para redirect 301 →
      `relaylab360.com/estudos` com banner explicativo nos 6 primeiros meses
- [ ] Documentação de usuário em pt-BR atualizada referindo "Estudos" no
      lugar de "ProtecView"

## 7. Fora de escopo (não-objetivos)

- Novas ferramentas além das 10 atuais (Arco-Elétrico IEEE 1584, Aterramento,
  Trafo etc. são propostas em `TOOLS_INVENTORY.md` como **futuro**)
- Re-escrita do motor de cálculo do Relé ou Campo
- Multi-tenant / autenticação (já existe no RelayLab e não é tocado)
- Migração de dados de usuários do ProtecView (cada uso era sessão-only;
  não havia persistência server-side a migrar)

## 8. Pontos abertos para alinhamento

Itens que precisam de decisão do PO antes de começar:

1. **Nome da pílula** — confirmar "Estudos" vs *Análises* / *Cálculos* / *Lab*
2. **Ordem na topbar** — Estudos primeiro (cronologia do projeto) ou último (último a chegar)
3. **Motor de cálculo** — portar Python → TS, ou expor Python como API?
4. **Bay de contexto** — entra na Sprint 1 (compartilhado desde o início)
   ou na Sprint 4 (depois das ferramentas migradas)?
5. **Telemetria** — adicionar tracking de uso por ferramenta para validar
   relevância das 10?
