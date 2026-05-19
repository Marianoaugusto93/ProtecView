# Inventário das 10 ferramentas

Ficha por ferramenta. Cada uma especifica: **categoria**, **rota**, **inputs**
(do bay e específicos), **outputs**, **fórmula/norma**, **dependências de
visualização**, **continuidade** (para onde os dados podem fluir), **status
do design** e **complexidade estimada**.

Legenda de complexidade: ★ trivial · ★★ média · ★★★ alta.

---

## 1. Componentes Simétricos

- **Categoria:** Sistema
- **Rota:** `/estudos/simetricos`
- **Função ANSI relacionada:** 46, 47, 59N (sequências)
- **Status do design:** especificação · sem mock dedicado (deriva da piloto)
- **Complexidade:** ★

### Inputs
| Campo | Tipo | Unidade |
|---|---|---|
| Vₐ, Vᵦ, V꜀ | complex (mag ∠ ang) | V ou pu |
| Iₐ, Iᵦ, I꜀ | complex (mag ∠ ang) | A ou pu |
| Base de referência | enum | sec / pri / pu |

### Outputs
- V₁, V₂, V₀ (sequências positiva, negativa, zero)
- I₁, I₂, I₀
- Fator de desequilíbrio (Δ = I₂/I₁ × 100%)
- Diagrama fasorial das 6 grandezas

### Fórmula
Transformação de Fortescue:
```
[X₀]       1   [1 1  1 ][Xₐ]
[X₁] = ─── ·[1 a  a²][Xᵦ]
[X₂]   3   [1 a² a ][X꜀]    com a = e^(j120°)
```

### Visualizações
- `<PhasorDiagram>` em 2 cópias (V e I)
- Tabela de magnitudes/ângulos por sequência
- Indicador grande de % de desequilíbrio (verde < 2% / amarelo 2–5% / vermelho > 5%)

### Continuidade
- → **Cálculo de Faltas:** sequências usadas em faltas assimétricas
- → **Relé:** valida que I₂/I₁ não dispara a função 46

---

## 2. Cálculo de Faltas

- **Categoria:** Sistema
- **Rota:** `/estudos/faltas`
- **Função ANSI:** 50/51, 50N/51N, 67, 87
- **Status do design:** 🟢 **mock hi-fi pronto** (`mocks/Calculo_de_Faltas.html`)
- **Complexidade:** ★★

### Inputs (do bay)
- Vₙ, Sₛc da fonte, X/R, frequência, conexão (YN/Δ/etc.)

### Inputs específicos
| Campo | Tipo | Unidade |
|---|---|---|
| Tipo de falta | enum | 3φ / 2φ / 2φ-T / 1φ-T |
| Z₁, Z₂, Z₀ (linha) | complex | Ω |
| Zf (resistência de falta) | real | Ω |
| Localização | real | km ou % do trecho |

### Outputs
| Output | Para | Unidade |
|---|---|---|
| Iₛc simétrico | cada fase | A primário / A sec / pu |
| Iₛc assimétrico (pico) | falta como um todo | kA pico |
| Tempo de decaimento DC | até 50% e 90% | ms |
| I₁, I₂, I₀ na falta | sequências | A |
| Tensão residual durante falta | 3 fases | V |

### Fórmulas
- 3φ:    `I = E / (Z₁ + Zf)`
- 2φ:    `I = E·√3 / (Z₁ + Z₂ + Zf)`
- 1φ-T:  `I = 3·E / (Z₁ + Z₂ + Z₀ + 3·Zf)`
- Assimetria pico: `Ip = Iₛc·√2 · (1 + e^(−R/(ωL)·t))` com `t` no primeiro pico

### Visualizações
- Cards de resultado grandes em laranja (3 cells: simétrico, assimétrico, tempo DC)
- Forma de onda das 3 correntes ao longo do tempo (8 ciclos)
- `<PhasorDiagram>` das correntes
- Tabela de sequências

### Continuidade
- **→ Relé:** envia `Iₛc` como pickup do estágio 50 (CTA primária)
- **→ Saturação de TC:** envia X/R e Iₛc para verificar saturação
- **→ Curvas TCC:** sobrepõe pickup calculado na curva

---

## 3. Curvas TCC (Tempo-Corrente)

- **Categoria:** Coordenação
- **Rota:** `/estudos/tcc`
- **Função ANSI:** 50/51, 50N/51N
- **Status do design:** especificação
- **Complexidade:** ★★★ (layout diferente: workspace 60%)

### Inputs
- Lista de curvas a plotar, cada uma com:
  - Nome, cor
  - Tipo (IEC: SI/VI/EI/LTI; IEEE: MI/VI/EI; ANSI; Definite Time; User)
  - Pickup (A primário)
  - Time dial
  - Instantâneo (50) opcional: pickup + time delay
  - Reset characteristic

### Outputs
- Gráfico log-log tempo × corrente
- Tabela de tempos de atuação para correntes notáveis (1.5×, 2×, 5×, 10× pickup)
- Margem de coordenação entre pares (CTI) — alerta se < 0.2 s

### Fórmulas (família IEC 60255-151)
```
SI (Standard Inverse):    t = TD · 0.14 / ((I/Ip)^0.02 - 1)
VI (Very Inverse):        t = TD · 13.5 / ((I/Ip) - 1)
EI (Extremely Inverse):   t = TD · 80  / ((I/Ip)^2 - 1)
```
+ família IEEE C37.112 (MI/VI/EI), Definite Time, Curva customizada por pontos.

### Visualizações
- Recharts log-log com até 8 curvas simultâneas
- Cursor cruzado que mostra (I, t) ao mover mouse
- Painel lateral com lista de curvas, cor, toggle de visibilidade

### Continuidade
- **← Relé:** importa pickup/TD do estágio 51 configurado
- **← Faltas:** sobrepõe pontos de operação Iₛc 3φ/2φ/1φ-T
- **→ Relé:** envia curva ajustada como preset

---

## 4. Proteção de Distribuição

- **Categoria:** Coordenação
- **Rota:** `/estudos/distribuicao`
- **Função ANSI:** 50/51, 79, fusível K/T
- **Status do design:** especificação
- **Complexidade:** ★★★

### Inputs
- Topologia do alimentador (subestação → tronco → ramal → cliente)
- Por nó: tipo de dispositivo (relé · religador · fusível), ajustes
- Por trecho: impedância, comprimento, demanda

### Outputs
- TCC sobreposta dos N dispositivos em série
- Verificação de coordenação (cada dispositivo a jusante deve operar antes
  do montante para falta no fim do seu trecho)
- Relatório por falta de coordenação

### Visualizações
- TCC compartilhada com `<TccChart>`
- Diagrama unifilar simplificado (uma fileira horizontal de devices)
- Cards de alerta para cada coordenação violada

### Continuidade
- ↔ **TCC:** mesma engine
- → **Relé:** envia ajuste do dispositivo selecionado

---

## 5. Proteção de Distância (21)

- **Categoria:** Funções de Proteção
- **Rota:** `/estudos/distancia`
- **Função ANSI:** 21, 21N
- **Status do design:** especificação
- **Complexidade:** ★★★ (R-X custom)

### Inputs
- Impedância de linha por km (R₁ + jX₁, R₀ + jX₀)
- Comprimento da linha (km)
- Característica desejada (Mho / Quadrilateral / Mho com blinder)
- Zonas a configurar (Z1, Z2, Z3) com alcance % e atraso

### Outputs
- Plano R-X com zonas plotadas
- Pickup de impedância de cada zona (ohms secundários)
- Tempo de atuação por zona
- Verificação de sobreposição entre zonas

### Visualizações
- `<RXPlane>` 400×400, ohm/div ajustável
- Cursor móvel mostrando impedância de falta hipotética
- Painel de configuração de zona em accordion

### Continuidade
- **← Faltas:** sobrepõe ponto de impedância da falta calculada
- **→ Relé:** envia ajustes de zona como preset 21

---

## 6. Proteção Diferencial (87)

- **Categoria:** Funções de Proteção
- **Rota:** `/estudos/diferencial`
- **Função ANSI:** 87T (trafo), 87L (linha), 87B (barra)
- **Status do design:** especificação
- **Complexidade:** ★★

### Inputs
- Tipo (87T / 87L / 87B)
- Para 87T: relação de tap, conexão (YNd1, Dyn11…), grupo vetorial
- TCs envolvidos (relação, classe, polaridade)
- Slope 1 (%), Slope 2 (%), breakpoint
- Pickup mínimo

### Outputs
- Curva de operação Iop × Irest
- Verificação de mismatch de tap
- Compensação de defasagem (matriz de correção)

### Visualizações
- Gráfico cartesiano Iop × Irest com curva (Slope 1 antes do breakpoint,
  Slope 2 depois) — região de operação acima da curva
- Marcador do ponto de operação atual (alimentado por live do Relé quando disponível)
- Tabela TC + tap mismatch

### Continuidade
- **← Faltas:** ponto Iop/Irest da falta interna/externa
- **→ Relé:** preset de 87T

---

## 7. Cálculo de Inrush

- **Categoria:** Funções de Proteção
- **Rota:** `/estudos/inrush`
- **Função ANSI:** 87 (2ª harmônica), 50/51 bloqueio
- **Status do design:** especificação
- **Complexidade:** ★★

### Inputs
- Potência do trafo (MVA)
- Tensão (kV)
- Impedância de curto (%)
- Característica magnética: Bsat, Br (remanência), tipo de núcleo
- Ponto da onda de fechamento (ângulo θ)

### Outputs
- Forma de onda da corrente de inrush por fase (5–10 ciclos)
- Pico estimado (× corrente nominal)
- Espectro harmônico (1ª, 2ª, 3ª, 5ª)
- Recomendação de bloqueio por 2ª harmônica

### Visualizações
- Forma de onda 3φ no tempo (Recharts ou SVG custom)
- Barras do espectro harmônico
- Indicador do %2ª harmônica vs threshold típico (15–18%)

### Continuidade
- **→ Relé:** ajusta % de bloqueio 2H da função 87T
- ↔ **Diferencial:** mesma engine de espectro

---

## 8. Ampacidade de Cabos

- **Categoria:** Componentes
- **Rota:** `/estudos/cabos`
- **Status do design:** especificação
- **Complexidade:** ★★

### Inputs
- Secção (mm²), isolação (EPR/XLPE/PVC), tensão (kV)
- Modo de instalação (eletroduto enterrado / aéreo / bandeja perfurada / …)
- Quantidade de cabos no agrupamento
- Temperatura ambiente, temperatura do solo, resistividade térmica do solo
- Fator de carga

### Outputs
- Corrente admissível (A) em regime permanente
- Corrente de curta duração (1 s) sem dano
- Temperatura interna estimada na carga nominal
- Tabela de fatores aplicados (FC)

### Fórmula
IEC 60287-1-1 (cálculo analítico) ou consulta a tabelas IEC 60364 conforme
modo de instalação.

### Visualizações
- Card grande com valor final em A
- Lista de fatores corretivos aplicados (visão tipo cascata)
- Corte transversal do agrupamento (SVG)

### Continuidade
- **→ Faltas:** define Iₙ máximo do circuito (referência para % de Iₛc)

---

## 9. Saturação de TC

- **Categoria:** Componentes
- **Rota:** `/estudos/tc`
- **Status do design:** especificação · marcado como **NEW** no hub
- **Complexidade:** ★★★

### Inputs (parte herdada do bay)
- Iₛc, X/R do sistema
### Inputs específicos
- TC: relação (ex. 600/5), classe (5P20, 10P20, C400…)
- Resistência do enrolamento secundário (Rct)
- Resistência do burden (relé + cabos) (Rb)
- Tensão de joelho (Vk)

### Outputs
- Tempo até saturação (ms)
- Verificação ANSI/IEEE: `Vs ≥ Iₛc/n · (Rct + Rb) · (1 + X/R)`
- Curva de excitação B-H
- Forma de onda do secundário sob falta (mostra "achatamento" se saturar)

### Visualizações
- B-H plot (SVG)
- Forma de onda do secundário (com e sem saturação sobrepostas)
- Indicador grande VERDE/AMARELO/VERMELHO conforme margem de Vs

### Continuidade
- **← Faltas:** Iₛc e X/R alimentam direto
- **→ Relé:** alerta se a TC saturar antes do tempo de atuação programado

---

## 10. (Espaço para futuro)

- **Categoria:** Componentes (placeholder)
- **Rota:** card vazio no hub, sem rota ativa
- **Status:** futuro · pelo menos 3 candidatos:

| Candidato | Função ANSI | Norma de referência |
|---|---|---|
| **Arco-Elétrico** | — | IEEE 1584-2018 (incident energy) |
| **Aterramento de Subestação** | — | IEEE 80 (passo e toque) |
| **Trafo — perdas e regime** | — | IEC 60076 |
| **TP — saturação e ferrorressonância** | — | IEC 61869-3 |

Decidir prioridade em planejamento pós-migração.

---

## Resumo executivo

| # | Ferramenta | Categoria | Complexidade | Mock pronto |
|---|---|---|---|---|
| 1 | Componentes Simétricos | Sistema | ★ | — |
| 2 | Cálculo de Faltas | Sistema | ★★ | 🟢 |
| 3 | Curvas TCC | Coordenação | ★★★ | — |
| 4 | Prot. de Distribuição | Coordenação | ★★★ | — |
| 5 | Prot. de Distância | Funções | ★★★ | — |
| 6 | Prot. Diferencial | Funções | ★★ | — |
| 7 | Cálculo de Inrush | Funções | ★★ | — |
| 8 | Ampacidade de Cabos | Componentes | ★★ | — |
| 9 | Saturação de TC | Componentes | ★★★ | — |

**Esforço total estimado:** ~22 pontos de complexidade. Veja
`MIGRATION_PLAN.md` para a distribuição em sprints.
