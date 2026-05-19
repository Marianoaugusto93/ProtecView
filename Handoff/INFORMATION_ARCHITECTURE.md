# Arquitetura de Informação — Suíte Estudos

## 1. Topbar — antes e depois

### Antes (atual)
```
[RL]  RelayLab 360       [Campo] [Relé] [Painel]                ⓘ
```

### Depois
```
[RL]  RelayLab 360       [Estudos] [Campo] [Relé] [Painel]      ⓘ
                          └ NEW
```

- A pílula nova fica **à esquerda** porque o fluxo cronológico de um projeto
  começa em análise (Estudos), passa por parametrização (Relé) e termina em
  comissionamento (Campo) — Painel é transversal.
- Mantém-se badge `NEW` (cor ciano `#0EA5E9`) por 60 dias após o release.
- Pílula ativa usa fundo laranja `#F97316`, idêntico às outras três.

## 2. Mapa de rotas

```
/estudos                                    Hub (10 cards + busca + filtros)
/estudos?cat=sistema                        Hub filtrado por categoria
/estudos?q=faltas                           Hub com query de busca aplicada

/estudos/simetricos                         Sistema · Componentes Simétricos
/estudos/faltas                             Sistema · Cálculo de Faltas
/estudos/tcc                                Coordenação · Curvas TCC
/estudos/distribuicao                       Coordenação · Proteção de Distribuição
/estudos/distancia                          Funções · Proteção de Distância (21)
/estudos/diferencial                        Funções · Proteção Diferencial (87)
/estudos/inrush                             Funções · Cálculo de Inrush
/estudos/cabos                              Componentes · Ampacidade de Cabos
/estudos/tc                                 Componentes · Saturação de TC

/estudos/*?bay=<id>                         Carrega bay de contexto persistido
/estudos/*?from=<rota>                      Indica origem (breadcrumb + back)

# Compatibilidade — domínio antigo
https://protecview.onrender.com/<qualquer>  → 301 → relaylab360.com/estudos
```

## 3. Hierarquia visual da suíte

```
TOPBAR (54 px)
├── Logo · Nome · Subtítulo
├── Nav pills (4)
└── Status · Lang · Help

SUB-NAV / BREADCRUMB (40 px, só em ferramentas)
├── Estudos / Categoria / Ferramenta
└── Estudo: BAY-01 · 13.8 kV · [Importar] [Exportar] [→ Relé]

PÁGINA
├── HUB: title row · filtros · grid 4-col
└── FERRAMENTA: 3 colunas (parâmetros · workspace · resultados/insights)
```

## 4. Hub — anatomia

```
┌──────────────────────────────────────────────────────────────────┐
│ Estudos de Sistema e Proteção                                    │
│ 10 ferramentas · análise pré-projeto e validação de ajustes      │
│                                  ┌─────────────────┐ ┌────────┐  │
│                                  │ ⌕  Buscar  ⌘K   │ │+ Novo  │  │
│                                  └─────────────────┘ └────────┘  │
├──────────────────────────────────────────────────────────────────┤
│ [Todas 10] [Sistema 2] [Coord. 2] [Funções 3] [Comp. 2] · ★Rec.  │
├──────────────────────────────────────────────────────────────────┤
│ ┌──Card──┐ ┌──Card──┐ ┌──Card──┐ ┌──Card──┐                     │
│ │ ic     │ │ ic     │ │ ic     │ │ ic     │                     │
│ │ nome   │ │ nome   │ │ nome   │ │ nome   │                     │
│ │ descr. │ │ descr. │ │ descr. │ │ descr. │                     │
│ │ [tag]  │ │ [tag]  │ │ [tag]  │ │ [tag]  │                     │
│ └────────┘ └────────┘ └────────┘ └────────┘                     │
│ (4 cards × 3 linhas = 10 + 1 placeholder + 1 vazio)              │
└──────────────────────────────────────────────────────────────────┘
```

### Filtros — comportamento
- **Mutuamente exclusivos** entre as 4 categorias (radio).
- **★ Recentes** é toggle independente — quando ativo, reordena os cards
  da categoria visível por `lastUsedAt` desc.
- Estado do filtro persistido em `searchParams` (`?cat=sistema`).

### Busca — comportamento
- Atalho global `⌘K` / `Ctrl+K` em qualquer página da suíte abre overlay
  modal com input focado.
- Match em: nome, descrição, função ANSI (50/51/87/21/2nd…), tags.
- Resultados em tempo real (debounce 80 ms).
- `Enter` navega para a ferramenta; `Esc` fecha; `↑/↓` move seleção.

### Card de ferramenta — campos obrigatórios
1. **Ícone** (SVG 20×20, stroke 1.8, monocromático ciano ou laranja se featured)
2. **Nome** (Rajdhani 14 px / 600)
3. **Descrição** em 1 linha (JetBrains Mono 10 px / `--tx3`)
4. **Tags** (≤ 3): categoria + função ANSI + opcional (`NEW`, `BETA`, etc.)
5. **Indicador de "ir"** (`↗`) no canto inferior direito
6. **Top-stripe colorido** — laranja se featured, ciano caso contrário

## 5. Ferramenta — anatomia padrão

Layout em **3 colunas**, replicando o padrão de `Relé`:

```
┌─ 300 px ──┬─────────── flex ──────────────┬─ 280 px ──┐
│           │                               │           │
│  COLUNA   │      COLUNA CENTRAL           │  COLUNA   │
│ ESQUERDA  │                               │  DIREITA  │
│           │  workspace principal:         │           │
│  Inputs   │  - tipo de cálculo            │ Resultado │
│  do bay   │  - controles                  │ visual    │
│  (params) │  - viewport (curva, fasor)    │ + listas  │
│           │  - tabela / dataset           │ + ações   │
│           │  - footer com ações           │           │
└───────────┴───────────────────────────────┴───────────┘
```

- **Coluna esquerda:** sempre o **Bay de Contexto** (ver
  `INTEGRATION_CONTRACTS.md`) + filtros específicos.
- **Coluna central:** o cálculo em si. Card único com `.ph` "azul/laranja" no
  topo, segmented controls quando necessário, viewport SVG mínima de 160 px
  de altura, footer com 3–4 ações (Reset / Copiar / Exportar / **Enviar para Relé**).
- **Coluna direita:** saídas secundárias (fasor, sequências, próximos passos,
  alertas). Cards múltiplos empilhados.

> **Exceção: TCC e Distância** — workspace ocupa 60% da viewport, parâmetros
> ficam à esquerda em accordions. Veja `TOOLS_INVENTORY.md`.

## 6. Atalhos de teclado

| Atalho | Ação |
|---|---|
| `⌘K` / `Ctrl+K` | Abrir busca global |
| `g` `e` | Ir para Estudos (hub) |
| `g` `c` | Ir para Campo |
| `g` `r` | Ir para Relé |
| `g` `p` | Ir para Painel |
| `?` | Painel de atalhos |
| `Esc` | Fechar modal / busca / overlay |
| dentro de ferramenta: `r` | Reset |
| dentro de ferramenta: `e` | Exportar |
| dentro de ferramenta: `⏎` `r` | Enviar para Relé |

## 7. Estados vazios e de erro

- **Hub sem resultados de busca:** card único central com sugestão de termos
  populares ("Tente: 87, faltas, distância, TCC").
- **Ferramenta com bay vazio:** prompt "Defina o bay de contexto à esquerda
  para começar" + botão "Usar bay de exemplo (13,8 kV)".
- **Erro de cálculo:** banner `--red` no topo do card central com a fórmula
  que falhou + link para "Ver no console".

## 8. Acessibilidade — mínimo necessário

- Contraste WCAG AA em todos os pares texto/fundo.
- Cores das fases (amarelo/vermelho/branco) **sempre** acompanhadas de label
  textual no SVG (`Iₐ`, `Iᵦ`, `I꜀`) e linha tracejada/sólida diferente onde
  faz sentido.
- Tab order: nav → search → filtros → primeiro card → demais cards.
- ARIA: `role="tab"`/`role="tabpanel"` nos filtros do hub; `aria-current="page"`
  na pílula ativa da topbar.

## 9. Telemetria sugerida

Eventos a emitir (Mixpanel/Amplitude compatível):
- `estudos.hub_opened`
- `estudos.search_used` (props: `query`, `result_count`)
- `estudos.tool_opened` (props: `tool_id`)
- `estudos.bay_imported` (props: `source` = manual/relé/painel)
- `estudos.preset_sent_to_rele` (props: `tool_id`, `preset_type`)
- `estudos.export` (props: `tool_id`, `format` = json/csv/pdf)

Estes dados validam quais ferramentas têm uso real e qual é a taxa de
continuidade Estudos → Relé.
