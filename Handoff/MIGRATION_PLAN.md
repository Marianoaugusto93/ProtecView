# Plano de migração

Migração executada em **4 sprints de 2 semanas** (~2 meses calendário).
Cada sprint termina com release entregável e medível.

## Visão geral

```
S1 │ Fundação    │ Pílula + Hub + BayContext + 2 ferramentas-âncora
S2 │ Coordenação │ Curvas TCC + Proteção de Distribuição
S3 │ Funções     │ Distância · Diferencial · Inrush
S4 │ Componentes │ Cabos + Saturação de TC + cutover de domínio
```

---

## Sprint 1 — Fundação · "A pílula Estudos existe"

**Duração:** 2 semanas
**Equipe sugerida:** 1 dev sr · 1 dev pl · 1 designer (½) · 1 PO (¼)

### Entregas
1. **Nova rota** `/estudos` ativa no RelayLab 360
2. **Pílula `Estudos`** com badge `NEW` na topbar
3. **Hub** funcional:
   - Grid de 10 cards (Sprint 1 ativa só 2; demais navegam para placeholder)
   - Busca ⌘K com índice estático local
   - Filtros por categoria com persistência em URL
   - Atalhos `g e`, `g c`, `g r`, `g p`
4. **`BayContext` store** (Zustand + persist localStorage)
   - Editor lateral
   - Bay de exemplo pré-carregado
5. **`SubNav` component** (breadcrumb + ações)
6. **Ferramentas-âncora** (paridade funcional com ProtecView):
   - **Componentes Simétricos** (`/estudos/simetricos`)
   - **Cálculo de Faltas** (`/estudos/faltas`)
7. **`ProtectionPreset` artifact bus** + CTA "Enviar para Relé" em Faltas
8. **Redirect placeholder** em `protecview.onrender.com` → banner
   "Em breve em RelayLab 360 → continue aqui ou abra a nova versão"

### Critérios de aceite
- [ ] Pílula visível em 100% das telas
- [ ] ⌘K abre busca em < 100 ms
- [ ] Faltas 3φ retorna mesmo valor que ProtecView (± 0,1%) para 5 cenários de teste
- [ ] Cenário canônico Faltas → Relé (toast) funciona ponta a ponta
- [ ] Zero erros no console em CI

### Riscos / mitigações
- **Risco:** lógica Python do ProtecView pode ter dependências obscuras
  ao ser portada. **Mitigação:** Sprint 0 (3 dias) só para análise.
- **Risco:** decisão sobre motor Python vs TS atrasa. **Mitigação:** começar
  já em TS para Componentes Simétricos (trivial) e validar.

---

## Sprint 2 — Coordenação · "TCC vive em Estudos"

**Duração:** 2 semanas

### Entregas
1. **`TccChart` component** (Recharts log-log reutilizável)
2. **`/estudos/tcc`** completo:
   - Adicionar/remover curvas (família IEC + IEEE + Definite Time)
   - Cursor cruzado
   - Margem CTI entre pares
3. **`/estudos/distribuicao`** completo (reusa `TccChart`)
4. **Continuidade Faltas → TCC** (botão "Abrir em Curvas TCC" no Cálculo de Faltas)
5. **Continuidade Relé → TCC** (atalho na tela de Relé para abrir a curva atual)
6. **Recentes** do hub funcionais

### Critérios de aceite
- [ ] 8 curvas plotadas simultaneamente sem lag perceptível (60fps)
- [ ] Coordenação detecta CTI < 0,2 s e gera alerta
- [ ] Importar curva de Relé volta com mesmos parâmetros

---

## Sprint 3 — Funções de Proteção

**Duração:** 2 semanas

### Entregas
1. **`/estudos/distancia`** (21)
   - `<RXPlane>` component
   - Configuração de Z1/Z2/Z3 (Mho/Quad)
   - Sobrepor ponto de falta vindo de `/estudos/faltas`
2. **`/estudos/diferencial`** (87)
   - Curva Slope 1/2 com breakpoint
   - Verificação de tap mismatch
   - Compensação de defasagem (matriz YNd1, Dy11…)
3. **`/estudos/inrush`** (2nd harmônica)
   - Forma de onda 5–10 ciclos
   - Espectro harmônico
4. Continuidades:
   - Distância ↔ Faltas (ponto R-X)
   - Inrush → Diferencial (sugestão de %2H)
   - Todas → Relé (presets)

### Critérios de aceite
- [ ] Característica Mho 87% e Quadrilateral renderizam corretamente
- [ ] 87T com YNd1 calcula matriz de compensação correta
- [ ] Inrush gera espectro com 1ª harmônica > 100% e 2ª harmônica 15–40%

---

## Sprint 4 — Componentes + Cutover

**Duração:** 2 semanas

### Entregas
1. **`/estudos/cabos`** (IEC 60287 + tabelas IEC 60364)
2. **`/estudos/tc`** com badge `NEW`
   - Curva B-H
   - Verificação ANSI/IEEE
   - Forma de onda do secundário sob falta
3. **Continuidade Cabos → Faltas** (limite Iₙ)
4. **Continuidade Faltas → TC** (X/R + Iₛc)
5. **Cutover do domínio:**
   - `protecview.onrender.com/*` → 301 redirect → `relaylab360.com/estudos`
   - Banner explicativo sobreposto por 30 dias mostrando "Esta ferramenta
     agora se chama Estudos. Saiba mais."
   - E-mail para base de usuários
6. **Documentação de usuário** atualizada (FAQ, vídeo curto, tour interativo)
7. **Remoção do badge NEW** da pílula Estudos

### Critérios de aceite
- [ ] 100% das URLs antigas redirecionam corretamente
- [ ] Lighthouse score > 90 em `/estudos` e nas 10 ferramentas
- [ ] Telemetria mostra que 80% dos usuários ativos do ProtecView passaram
      pela suíte Estudos em até 7 dias após o cutover

---

## Quality gates por sprint

A cada fim de sprint:

1. **Visual regression:** snapshot de cada tela em 1280×800, 1440×900, 1920×1080.
   Falha > 0,5% de diff aciona review.
2. **Paridade de cálculo:** suite de 50+ casos de teste comparando saída
   da suíte Estudos vs ProtecView. Tolerância ± 0,1%.
3. **Acessibilidade:** axe-core sem violations sérias.
4. **Performance:** Lighthouse > 90 em todas as 4 categorias.
5. **Demo:** sessão de 30 min com PO + 2 engenheiros eletricistas usuários.

## Equipe ideal

| Papel | Sprints | %FTE |
|---|---|---|
| Tech Lead (full-stack TS) | S1–S4 | 100% |
| Dev pleno (frontend/SVG/charts) | S1–S4 | 100% |
| Dev pleno (motor de cálculo) | S1–S4 | 100% |
| Designer | S1–S2 | 50% |
| PO/Eng. elétrico (validador) | S1–S4 | 25% |

## Pós-migração — 30 dias de observação

- Monitor de erros (Sentry)
- Telemetria de uso por ferramenta
- Survey NPS específico da nova suíte
- Backlog de melhorias priorizado pelos dados acima
