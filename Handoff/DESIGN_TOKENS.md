# Design Tokens — Suíte Estudos

Os tokens abaixo são **herdados** do RelayLab 360. Não há tokens novos
introduzidos pela suíte Estudos — todos os componentes da migração reusam
o sistema existente. Esta página serve de referência rápida + componentes
que ainda não existem no codebase atual.

## 1. CSS variables (copiar para `tokens.css`)

```css
:root{
  /* ───────────── Backgrounds ───────────── */
  --bg:        #0E1015;   /* page background */
  --card:      #181B22;   /* primary card */
  --card2:     #1E2129;   /* nested / hover */
  --card3:     #252830;   /* input / segmented */
  --card4:     #2C2F38;   /* deepest */

  /* ───────────── Borders ───────────── */
  --bdr:       rgba(255,255,255,.06);
  --bdr2:      rgba(255,255,255,.10);

  /* ───────────── Brand ───────────── */
  --orange:    #F97316;   /* primary CTA · pílula ativa · acentos */
  --orange-d:  #c2410c;
  --orange-dim:rgba(249,115,22,.12);

  /* ───────────── Domain ───────────── */
  --cyan:      #0EA5E9;   /* análise · estudos · medidas live */
  --cyan-dim:  rgba(14,165,233,.10);
  --green:     #4ADE80;   /* status OK · energizado · injetar */
  --green-dim: rgba(74,222,128,.10);
  --red:       #F87171;   /* erro · alarme · parar */
  --red-dim:   rgba(248,113,113,.10);
  --amber:     #FBBF24;   /* atenção · preset */
  --violet:    #A78BFA;   /* secundário · religador */

  /* ───────────── Phase colors (compartilhado c/ Campo) ─────── */
  --pa:        #FFE033;   /* fase A · amarelo */
  --pb:        #E53935;   /* fase B · vermelho */
  --pc:        #9E9E9E;   /* fase C · cinza/branco */
  --pg:        #43A047;   /* terra · verde */

  /* ───────────── Text ───────────── */
  --tx:        #F3F4F6;   /* primário */
  --tx2:       #9CA3B0;   /* secundário */
  --tx3:       #5C6370;   /* terciário · labels */
  --tx4:       #3F4651;   /* placeholder · disabled */

  /* ───────────── Type families ───────────── */
  --fm:        'JetBrains Mono', ui-monospace, monospace;
  --fh:        'Rajdhani', system-ui, sans-serif;
}
```

## 2. Tipografia

| Uso | Família | Tamanho | Peso | Letter-spacing |
|---|---|---|---|---|
| H1 página | Rajdhani | 22–34 px | 600 | 0.3px |
| Título de card | Rajdhani | 14–17 px | 600 | 0.2px |
| Body | Rajdhani | 12–13 px | 400–500 | 0 |
| Label uppercase | JetBrains Mono | 9–10.5 px | 700 | 1.0–1.5 px |
| Valor numérico (resultado) | JetBrains Mono | 14–24 px | 700 | 0 |
| Tag/chip | JetBrains Mono | 8.5–10 px | 700 | 0.6–0.8 px |
| Breadcrumb | JetBrains Mono | 10 px | 700 | 0.7 px |
| Código / unidade | JetBrains Mono | 9–11 px | 600 | 0.3 px |

> Toda label uppercase usa **JetBrains Mono 700**, jamais Rajdhani.
> Todo número usa **JetBrains Mono**. Rajdhani só para textos legíveis.

## 3. Spacing e radii

- **Radius:** 3 px (tag), 5–6 px (button/input), 7–8 px (chip/card pequeno),
  10–12 px (card), 14 px (viewport).
- **Padding card body:** 10–14 px.
- **Padding ph (header de card):** `9 px 14 px`.
- **Gap entre cards:** 8 px (denso, ferramenta) / 10–14 px (hub) / 16 px (página).
- **Sub-nav height:** 40 px. Topbar height: 54 px.

## 4. Componentes compartilhados — checklist de implementação

A suíte Estudos depende destes componentes. Os marcados com **(novo)** ainda
não existem no codebase e devem ser construídos na Sprint 1.

### `.topbar` (existe)
Já implementado em Campo/Relé/Painel. Adicionar pílula `Estudos` com badge
`NEW` por 60 dias.

### `.nav-pills`, `.np`, `.np.on` (existe)
Reusar sem mudanças. Acrescentar `.np.new` com badge:
```css
.np.new::after{
  content:'NEW';
  position:absolute;top:-6px;right:-6px;
  background:var(--cyan);color:#0E1015;
  font-size:7.5px;font-family:var(--fm);font-weight:800;
  padding:1px 4px;border-radius:3px;letter-spacing:.4px;
}
```

### `.card` + `.ph` (existe)
Padrão de card com header colorido por domínio. **Não criar variante nova**
— usar `.ph .bar.c` (ciano) para todos os headers de Estudos por padrão;
laranja `.ph .bar` para CTAs / estados ativos.

### `<SubNav>` **(novo)**
Breadcrumb + ações secundárias da ferramenta.
```jsx
<SubNav
  trail={['Estudos','Sistema','Cálculo de Faltas']}
  context={{ bay:'BAY-01', vn:'13.8 kV' }}
  actions={[
    { label:'↓ Importar', onClick:... },
    { label:'↑ Exportar', onClick:... },
    { label:'→ Enviar p/ Relé', primary:true, onClick:... },
  ]}
/>
```
Altura 40 px, JetBrains Mono 10 px, separadores `/` em `--tx4`.

### `<SearchPalette>` **(novo)**
Modal de busca global ⌘K. Backdrop blur, input grande, lista de até
10 resultados com ícone + nome + categoria + atalho de navegação.

### `<ToolCard>` **(novo)**
Card do hub. Props: `icon`, `name`, `description`, `tags[]`, `featured`,
`href`. Veja `mocks/Hub_de_Estudos.html` para o markup canônico.

### `<BayContext>` **(novo, compartilhado entre Estudos e Relé)**
Componente sticky lateral. Renderiza/edita os parâmetros do bay
(`BayContext` tipo em `INTEGRATION_CONTRACTS.md`). Persistido em Zustand.

### `<PhasorDiagram>` **(novo)**
SVG 260×260 com eixos cartesianos, círculos de magnitude (60% e 100%),
3 vetores rotuláveis (Iₐ Iᵦ I꜀ ou Vₐ Vᵦ V꜀) e legenda numérica embaixo.
Cores das fases via `--pa --pb --pc --pg`.

### `<TccChart>` **(novo)**
Recharts log-log para curvas tempo-corrente. Compartilhado entre TCC,
Distribuição, Diferencial. Eixos `t (s)` × `I/Ipk`, suporta múltiplas
curvas sobrepostas.

### `<FaultMatrix>` **(novo)**
Tabela 4×N (3φ, 2φ, 2φ-T, 1φ-T) com Iₛc simétrico, assimétrico, tempo de
decaimento DC. Reuso em Faltas e Distância.

### `<RXPlane>` **(novo, específico de Distância)**
Plano R-X com zonas Mho/Quad selecionáveis.

### `<SegmentedControl>` (existe — `.seg`)
Reusar sem mudanças.

### `<Toggle>` (existe — `.tog`)
Reusar sem mudanças.

## 5. SVG icons da suíte Estudos

Os 10 ícones de ferramenta são SVG inline, viewBox `0 0 24 24`, stroke 1.8,
`fill="none"`, cor `currentColor` (herda do `.tool .ic`). Marcação canônica
em `mocks/Hub_de_Estudos.html` na grid. Resumo:

| Ferramenta | Glifo |
|---|---|
| Componentes Simétricos | círculo com agulha de relógio (eixos) |
| Cálculo de Faltas | onda de pulso de curto |
| Curvas TCC | degraus descendentes (tempo × corrente) |
| Prot. de Distribuição | barras crescentes (alimentador) |
| Prot. de Distância | círculo bipartido + raio diagonal (zona Mho) |
| Prot. Diferencial | duas ondas convergindo (entrada/saída) |
| Cálculo de Inrush | curva exponencial decrescente |
| Ampacidade de Cabos | anel concêntrico (corte do cabo) |
| Saturação de TC | curva BH com joelho |
| Futuro (placeholder) | `+` em moldura tracejada |

## 6. Animações e microinterações

- **Pílula nav:** transição de cor 120 ms `ease-out`.
- **Card de ferramenta hover:** `background: var(--card)` → `--card2`,
  150 ms; `.go` muda para `--orange`.
- **Resultado numérico ao recalcular:** flash sutil — `background-color`
  vai a `--orange-dim` por 300 ms e volta.
- **Enviar para Relé:** botão pulsa verde uma vez, toast "Preset enviado
  para Relé · BAY-01" aparece por 3 s no canto inferior direito.
- **Modal de busca:** fade + scale 0.96 → 1 em 120 ms.

## 7. Modo claro

O RelayLab 360 atual é **dark-only**. A suíte Estudos não introduz modo
claro — o toggle "Modo Claro/Escuro" do ProtecView original é removido na
migração (item de débito técnico anotado, sem prioridade).

## 8. Don'ts (proibições explícitas)

- ❌ Não usar emoji em ícones — só SVG inline.
- ❌ Não usar Inter, Roboto, Arial, Open Sans — apenas Rajdhani e JetBrains Mono.
- ❌ Não inventar nova cor de domínio — usar `--cyan` para tudo que for
  análise. Laranja só para acentos primários e CTA.
- ❌ Não usar gradientes em backgrounds de página ou card. Permitido apenas
  no `::before` da topbar (única exceção) e em metais skeumórficos do Campo.
- ❌ Não criar variante "compact" ou "comfortable" — densidade é fixa.
