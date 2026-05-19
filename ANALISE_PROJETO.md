# 📊 Análise Completa - ProtecView v1.0

**Data:** 2026-05-19  
**Versão:** 1.0 (Post-Merge da Feature Dynamic UI)  
**Objetivo:** Análise técnica e roadmap para integração futura em RelayLab 360

---

## 📋 Sumário Executivo

**ProtecView** é uma aplicação web interativa construída em Python + Dash que fornece 8 ferramentas de análise de sistemas elétricos de potência. O projeto está em estágio **funcional com bugs conhecidos** e necessita de refatoração e padronização antes da integração em RelayLab 360.

### Status Atual
- ✅ **8 módulos funcionais** implementados
- ⚠️ **1 bug crítico** documentado (dist_protection)
- ⚠️ **3 itens de dívida técnica** identificados
- 🔄 **UI dinâmica** recentemente implementada (TCC, Distance)
- 📱 **Responsivo** para dispositivos móveis

---

## 🏗️ Arquitetura do Projeto

### Estrutura de Diretórios

```
ProtecView/
├── app.py                      # Inicialização Dash (externos stylesheets)
├── run.py                      # Entry point + Layout principal
├── layouts.py                  # Definições de layout das 8 abas
├── requirements.txt            # Dependências (Dash 3.2.0, Plotly 6.3.1, etc)
├── Procfile                    # Deploy em Heroku/produção
├── assets/                     # CSS, imagens, logo
│   ├── style.css              # Tema claro/escuro (variáveis CSS)
│   ├── custom_styles.css      # Estilos customizados (DUPLICADO)
│   └── logo_protecview.png    # Logo marca
├── callbacks/                  # Callbacks Dash por módulo
│   ├── callbacks_sym.py        # Componentes Simétricos
│   ├── callbacks_dist.py       # Proteção de Distância
│   ├── callbacks_tcc.py        # Curvas TCC (dinâmico)
│   ├── callbacks_fault.py      # Cálculo de Faltas
│   ├── callbacks_amp.py        # Ampacidade de Cabos
│   ├── callbacks_ct.py         # Saturação de TC
│   ├── callbacks_diff.py       # Proteção Diferencial
│   ├── callbacks_inrush.py     # Cálculo de Inrush
│   └── callbacks_dist_protection.py  # Proteção de Distribuição (BUGGY)
├── utils/                      # Funções utilitárias/cálculos
│   ├── utils_common.py         # Funções comuns (polar_to_complex)
│   ├── utils_sym.py            # Cálculos de componentes simétricos
│   ├── utils_dist.py           # Cálculos de distância
│   ├── utils_tcc.py            # Curvas TCC + tabelas IEC/IEEE
│   ├── utils_fault.py          # Cálculos de faltas assimétricas
│   ├── utils_amp.py            # Cálculos de ampacidade (NBR/IEC)
│   ├── utils_ct.py             # Saturação de TC
│   ├── utils_diff.py           # Curva diferencial (slope)
│   ├── utils_inrush.py         # Inrush de motor
│   └── utils_dist_protection.py # Fusíveis/Religadores
└── _callbacks_OLD.py           # Versão antiga (deprecated)
```

### Stack Tecnológico

| Componente | Versão | Propósito |
|-----------|--------|----------|
| **Python** | 3.x | Linguagem principal |
| **Dash** | 3.2.0 | Framework web + UI callbacks |
| **Plotly** | 6.3.1 | Gráficos interativos |
| **Flask** | 3.1.2 | Backend WSGI (via Dash) |
| **NumPy** | 2.3.4 | Cálculos matemáticos/complexos |
| **Gunicorn** | 23.0.0 | Servidor WSGI produção |
| **Requests** | 2.32.5 | HTTP requests (futuro: integração APIs) |

---

## 🔧 Os 8 Módulos

### 1. **Calculador de Componentes Simétricos** (Módulo 1)
- **Status:** ✅ Funcional, UI dinâmica
- **Arquivo principal:** `callbacks_sym.py`
- **Funcionalidade:**
  - Conversão bidirecional: Fase ↔ Sequência (0,1,2)
  - Visualização polar interativa de fasores
  - Entrada: Magnitude + Ângulo (graus)
  - Saída: Sequência 0, 1, 2 (complexos)
- **Dependências:** utils_sym.py, utils_common.py
- **Fórmulas:** Transformação de Clarke (matriz 3x3)

### 2. **Visualizador de Zonas de Distância** (Módulo 2)
- **Status:** ⚠️ Funcional, mas **estático** (2 zonas fixas)
- **Arquivo principal:** `callbacks_dist.py`
- **Funcionalidade:**
  - Plotagem de círculos Mho ou zonas Quadrilaterais
  - Diagrama R-X (impedância)
  - Zona 1 e Zona 2 configuráveis
  - **BACKLOG:** Refatorar para interface dinâmica (Adicionar/Remover zonas)
- **Padrão:** ANSI 21 (Distance Relay)

### 3. **Calculadora de Curto-Circuito** (Módulo 3)
- **Status:** ✅ Funcional
- **Arquivo principal:** `callbacks_fault.py`
- **Funcionalidade:**
  - Cálculo de faltas assimétricas (3PH, LG, LL)
  - Base: Impedâncias de sequência (Z0, Z1, Z2)
  - Saída: Correntes em p.u.
- **Método:** Componentes simétricos + superposição

### 4. **Plotter de Curvas TCC** (Módulo 4)
- **Status:** ⚠️ Funcional com UI dinâmica (recentemente implementado)
- **Arquivo principal:** `callbacks_tcc.py`
- **Funcionalidade:**
  - Múltiplos relés dinâmicos (Adicionar/Remover)
  - Curvas IEC + IEEE standard
  - Análise de partida de motor
  - Cálculo de CTI (Coordination Time Interval)
  - **BACKLOG:** Validação de entrada numérica, erro handling
- **Curvas suportadas:** 6 tipos padrão IEC/IEEE

### 5. **Ampacidade de Cabos** (Módulo 5)
- **Status:** ✅ Funcional
- **Arquivo principal:** `callbacks_amp.py`
- **Funcionalidade:**
  - Capacidade térmica (NBR/IEC)
  - Queda de tensão (VD%)
  - Suportabilidade de curto-circuito (I²t)
  - Correções: Temperatura, agrupamento, solo, etc.
- **Referência:** NBR 5410, IEC 60364

### 6. **Saturação de TC** (Módulo 6)
- **Status:** ⚠️ Funcional, mas aproximado
- **Arquivo principal:** `callbacks_ct.py`
- **Funcionalidade:**
  - Análise de saturação do Transformador de Corrente
  - Plotagem: Tensão de Kneepoint vs. Ponto de operação
  - **BACKLOG:** Curva de excitação senoidal completa (atualmente linha horizontal)

### 7. **Proteção Diferencial (ANSI 87)** (Módulo 7)
- **Status:** ✅ Funcional
- **Arquivo principal:** `callbacks_diff.py`
- **Funcionalidade:**
  - Curva de restrição (slope) multi-estágio
  - 3 estágios: Pickup, 2 Slopes, 2 Breakpoints
  - Plotagem: Zonas "Operar" (vermelho) e "Bloquear" (azul)
  - Interface estática (não dinâmica)

### 8. **Proteção de Distribuição (Fusíveis/Religadores)** (Módulo 8)
- **Status:** 🔴 **BUG CRÍTICO - Não plota gráfico**
- **Arquivo principal:** `callbacks_dist_protection.py`
- **Funcionalidade Esperada:**
  - Interface dinâmica para múltiplos fusíveis/religadores
  - Curvas Tipo K e Tipo T
  - Sequências Rápida/Lenta (religadores)
  - Coordenação TCC em distribuição
- **Problema:**
  - O callback `plot_dist_tcc_graph` não consegue ler dados dos componentes dinâmicos
  - Padrão de mapeamento entre IDs de formulário e storage falha
  - **Raiz provável:** Desincronização entre `dist_curve_storage` e o rendering dos controles
- **Impacto:** Módulo 8 não funciona (gráfico em branco)

---

## 🐛 Bugs Identificados

### 🔴 BUG CRÍTICO - Módulo de Proteção de Distribuição

**Prioridade:** ALTA  
**Severidade:** Crítica (feature não funciona)

**Sintomas:**
- Gráfico não é plotado (figura vazia)
- Botão "Plotar Gráfico" não gera visualização
- Controles dinâmicos (fusíveis/religadores) são criados mas não lidos

**Diagnóstico:**
```python
# Em callbacks_dist_protection.py, linha 158-165
# O callback espera que os IDs dos controles correspondam aos IDs no storage
# MAS os controles são renderizados dinamicamente em render_dist_controls()

# O problema é que:
# 1. add_dist_curve() armazena curve_id no storage
# 2. render_dist_controls() cria controles com esse curve_id
# 3. plot_dist_tcc_graph() tenta recuperar valores usando State(... ALL)
# 4. MAS os State(... ALL) retornam listas vazias se os controles não existem ainda

# Resultado: fuse_types_val, fuse_ratings_val, etc. estão vazios
```

**Solução Recomendada:**
1. Refatorar o callback para usar `dcc.Store` com JSON estruturado
2. Validar que os controles foram renderizados antes de plotar
3. Usar padrão de mapeamento robusto (ID → valor)
4. Adicionar logs de debug para validar os dados

**Tempo estimado:** 4-6 horas

---

### ⚠️ DÍVIDA TÉCNICA - Duplicação de CSS

**Prioridade:** MÉDIA  
**Severidade:** Manutenção

**Problema:**
- `assets/style.css` (tema claro/escuro com variáveis CSS)
- `assets/custom_styles.css` (estilos customizados)
- Ambos carregados, possível conflito

**Solução:**
- Mesclar em um único `assets/main.css`
- Manter organização clara (variáveis, layout, componentes, tema)
- Otimizar seletores CSS

**Tempo estimado:** 2-3 horas

---

### ⚠️ BACKLOG - Refatoração de Interfaces Estáticas

**Prioridade:** BAIXA  
**Severidade:** Feature enhancement

**Módulos afetados:**
- **Módulo 2 (Distância):** 2 zonas fixas → Dinâmicas (Adicionar/Remover)
- **Módulo 4 (TCC):** Já foi feito! Usar como template

**Benefício:**
- Consistência (todos dinâmicos)
- Flexibilidade para usuários

**Tempo estimado:** 3-4 horas por módulo

---

### ⚠️ BACKLOG - Curva de Saturação de TC Incompleta

**Prioridade:** BAIXA  
**Severidade:** Precisão matemática

**Atual:**
- Plotagem como linha horizontal (aproximação)

**Esperado:**
- Curva de excitação senoidal completa
- Plotar perdas e distorção harmônica

**Tempo estimado:** 3 horas

---

## 📊 Análise de Código

### Padrões Utilizados

#### ✅ Boas Práticas
1. **Separação de Responsabilidades**
   - `layouts.py` → Estrutura HTML
   - `callbacks/` → Lógica UI
   - `utils/` → Lógicos matemáticos

2. **Callbacks Dash bem estruturados**
   - Uso de `State()` para valores não-reativos
   - Padrão `Input/Output` claro
   - Tratamento básico de exceções

3. **Tema Dinâmico**
   - CSS variables para claro/escuro
   - Toggle switch funcional
   - Responsivo em mobile

#### ⚠️ Oportunidades de Melhoria

1. **Type Hints**
   - Faltam em callbacks e utils
   - Recomendado para futuro: Adicionar type hints

2. **Logging**
   - Sem logs estruturados
   - Recomendado: Python `logging` module

3. **Validação de Entrada**
   - Inputs numéricos sem validação rigorosa
   - Risco: valores inválidos podem gerar exceções não tratadas

4. **Reutilização**
   - `create_fuse_controls()` e `create_recloser_controls()` poderiam usar factory pattern
   - Callbacks TCC vs Dist_Protection têm lógica duplicada

5. **Performance**
   - Gráficos com muitos pontos podem ser lentos (Plotly é OK para escalas atuais)
   - Sem caching (futuro: Redis para operações pesadas)

---

## 🎯 Roadmap de Correções e Ajustes

### **Fase 1: Crítica (Semana 1-2)**

#### 1.1 - Corrigir Bug do Módulo de Distribuição
- [ ] Debug do callback `plot_dist_tcc_graph()`
- [ ] Refatorar mapeamento de IDs
- [ ] Testar com múltiplos fusíveis/religadores
- [ ] **Tempo:** 6h
- **Status:** Not Started

#### 1.2 - Consolidar Styles CSS
- [ ] Mesclar `style.css` + `custom_styles.css`
- [ ] Testar temas claro/escuro
- [ ] Validar responsividade
- [ ] **Tempo:** 3h
- **Status:** Not Started

### **Fase 2: Refactoring (Semana 3-4)**

#### 2.1 - Adicionar Type Hints
- [ ] Annotate callbacks (Callable types)
- [ ] Annotate utils (param types + return)
- [ ] Validar com `mypy`
- [ ] **Tempo:** 4h
- **Status:** Not Started

#### 2.2 - Implementar Logging
- [ ] Configurar `logging.config`
- [ ] Adicionar logs em callbacks críticos
- [ ] Logs em utils (erros matemáticos)
- [ ] **Tempo:** 3h
- **Status:** Not Started

#### 2.3 - Refatoração de Distância (Módulo 2)
- [ ] Implementar UI dinâmica (usar TCC como template)
- [ ] Testar adicionar/remover zonas
- [ ] Validar cálculos
- [ ] **Tempo:** 4h
- **Status:** Not Started

### **Fase 3: Preparação para RelayLab 360 (Semana 5-8)**

#### 3.1 - Criar Arquivo de Configuração
- [ ] `config.py` com constantes globais
- [ ] URLs de API (futuro)
- [ ] Parâmetros de ambiente
- [ ] **Tempo:** 2h

#### 3.2 - Documentação de API (REST)
- [ ] Expor cálculos via endpoints REST
- [ ] Flask routes para cada módulo
- [ ] Input validation + error codes
- [ ] **Tempo:** 8h

#### 3.3 - Sistema de Templates
- [ ] Template manager para RelayLab 360
- [ ] Serialização de configurações (JSON)
- [ ] Import/Export de designs
- [ ] **Tempo:** 6h

#### 3.4 - Autenticação e Segurança
- [ ] CORS configuration
- [ ] API key management
- [ ] Rate limiting
- [ ] **Tempo:** 4h

#### 3.5 - Testes Unitários
- [ ] Unit tests para utils/ (fixtures de dados)
- [ ] Integration tests para callbacks
- [ ] Coverage mínimo: 70%
- [ ] **Tempo:** 10h

#### 3.6 - Documentação Técnica
- [ ] README.md atualizado (arquitetura)
- [ ] Docstrings em todas as funções
- [ ] Guia de integração para RelayLab 360
- [ ] **Tempo:** 5h

---

## 🔌 Plano de Integração com RelayLab 360

### Visão Geral

ProtecView será integrado como um **módulo de análise** dentro de RelayLab 360, permitindo que usuários executem cálculos de proteção sem sair da plataforma.

### Arquitetura Proposta

```
RelayLab 360
    ├── ProtecView Module (backend)
    │   ├── API REST endpoints
    │   ├── Cálculos (utils/)
    │   └── Templates de design
    │
    └── UI Integrada
        ├── Dashboard unificado
        ├── Salvar designs em banco
        └── Exportar relatórios
```

### Fases de Integração

#### **FASE I: Backend Preparation (2-3 semanas)**

**Objetivos:**
1. Expor funcionalidades como REST API
2. Criar camada de autenticação
3. Implementar persistência

**Tasks:**
```python
# 1. Criar routes Flask para cada módulo
from flask import Blueprint, request, jsonify

@app.route('/api/v1/symmetric-components', methods=['POST'])
def api_symmetric_components():
    """
    POST: Calcular componentes simétricos
    Body: {"direction": "phase-to-sym", "phase_a": {...}, ...}
    Response: {"sequence_0": {...}, "sequence_1": {...}, ...}
    """

@app.route('/api/v1/tcc-curve', methods=['POST'])
def api_tcc_curve():
    """POST: Plotar curva TCC"""

# ... e assim por diante para outros 7 módulos
```

**2. Criar modelo de dados**
```python
# models.py
class ProtecViewDesign:
    design_id: str
    name: str
    module: str  # 'tcc', 'distance', 'fault', etc.
    configuration: dict  # JSON com todos os parâmetros
    created_at: datetime
    updated_at: datetime
    user_id: str  # Referência ao usuário RelayLab
```

**3. Integração com banco de dados RelayLab**
- Usar ORM da RelayLab 360 (SQLAlchemy?)
- Endpoints CRUD para designs salvos

#### **FASE II: Frontend Integration (2-3 semanas)**

**Objetivos:**
1. Integrar UI de ProtecView em RelayLab 360
2. Single Sign-On (SSO)
3. Dashboard de designs salvos

**Tasks:**
1. **Embed ProtecView como iframe ou webcomponent**
   - Ou reimplementar UI em frameworks RelayLab (React/Vue?)
   - Manter lógica de cálculos (backend-agnostic)

2. **Dashboard de designs**
   ```
   ┌─ Meus Designs (ProtecView)
   │  ├─ TCC Coordination - Subestação A
   │  ├─ Distance Protection - Linha 100
   │  └─ Fuse Coordination - Distribuição
   ```

3. **Exportar relatórios**
   - PDF com gráficos + configurações
   - CSV com dados dos cálculos

#### **FASE III: Advanced Features (4+ semanas)**

**Objetivos:**
1. Machine Learning para recomendações
2. Colaboração em tempo real
3. Histórico de versões

**Exemplos:**
- "Baseado em suas faltas calculadas, recomendamos..."
- Merge de designs de múltiplos usuários
- Git-like version control para configurações

---

## 🎨 Novo Template para RelayLab 360

### Estrutura Proposta

```
ProtecView-RelayLab/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── symmetric_components.py
│   │   │   ├── tcc.py
│   │   │   ├── distance.py
│   │   │   ├── fault.py
│   │   │   ├── ampacity.py
│   │   │   ├── ct.py
│   │   │   ├── differential.py
│   │   │   └── distribution.py
│   │   ├── models.py          # Design models
│   │   ├── schemas.py         # Pydantic validation
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py          # Settings
│   │   ├── security.py        # Auth
│   │   └── __init__.py
│   ├── utils/                 # Cálculos (refatorados de ProtecView)
│   │   └── ... (todos os utils_*.py)
│   ├── tests/
│   │   ├── test_api/
│   │   ├── test_utils/
│   │   └── conftest.py
│   ├── requirements.txt
│   └── main.py               # FastAPI ou Flask main
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Componentes Dash/React
│   │   ├── pages/
│   │   │   ├── dashboard.py
│   │   │   ├── editor.py
│   │   │   └── designs_list.py
│   │   └── ...
│   └── package.json
│
├── docs/
│   ├── API.md                 # Documentação REST API
│   ├── INTEGRATION.md         # Como integrar com RelayLab
│   ├── ARCHITECTURE.md        # Visão técnica
│   └── USER_GUIDE.md          # Guia do usuário
│
└── docker-compose.yml         # Containerização (opcional)
```

### API REST - Especificação de Entrada/Saída

#### Exemplo 1: Componentes Simétricos
```json
// POST /api/v1/modules/symmetric-components
{
  "direction": "phase-to-sym",
  "input": {
    "phase_a": {"magnitude": 2.5, "angle_deg": 0},
    "phase_b": {"magnitude": 3.5, "angle_deg": -150},
    "phase_c": {"magnitude": 5.0, "angle_deg": -177}
  }
}

// RESPONSE 200 OK
{
  "success": true,
  "output": {
    "sequence_0": {"magnitude": 1.85, "angle_deg": 45.2},
    "sequence_1": {"magnitude": 3.2, "angle_deg": -2.5},
    "sequence_2": {"magnitude": 0.95, "angle_deg": 178.3}
  }
}
```

#### Exemplo 2: Cálculo de Faltas
```json
// POST /api/v1/modules/fault-calculation
{
  "z0_ohm": 15.0,
  "z1_ohm": 5.0,
  "z2_ohm": 5.0,
  "v_base_kv": 138.0,
  "kva_base": 100000
}

// RESPONSE 200 OK
{
  "success": true,
  "faults": {
    "3ph_pu": 2.5,
    "lg_pu": 1.8,
    "ll_pu": 2.1
  }
}
```

#### Exemplo 3: Salvar Design
```json
// POST /api/v1/designs
{
  "name": "Coordenação TCC - Subestação A",
  "module": "tcc",
  "configuration": {
    "relays": [
      {"name": "Relé 1", "curve": "IEEE Moderately Inverse", "pickup": 5, "tds": 1.0},
      {"name": "Relé 2", "curve": "IEEE Very Inverse", "pickup": 10, "tds": 0.5}
    ],
    "motor": {...}
  }
}

// RESPONSE 201 Created
{
  "design_id": "uuid-xxx",
  "created_at": "2026-05-19T10:30:00Z"
}
```

---

## 📈 Métricas e KPIs

### Qualidade de Código
- [ ] Type coverage: 80%+
- [ ] Test coverage: 70%+
- [ ] Pylint score: 8.0+
- [ ] Docstring coverage: 100% funções públicas

### Performance
- [ ] TCC plot: < 500ms
- [ ] API response: < 200ms (sem plot)
- [ ] Dashboard load: < 2s

### Segurança
- [ ] OWASP Top 10 remediation
- [ ] Input validation em 100% dos endpoints
- [ ] Rate limiting implementado

---

## 📚 Recomendações Finais

### Curto Prazo (1 mês)
1. **CRÍTICO:** Corrigir bug do módulo de distribuição
2. **IMPORTANTE:** Consolidar CSS
3. Adicionar type hints + logging

### Médio Prazo (2-3 meses)
1. Refatorar Módulo 2 (distância) para UI dinâmica
2. Melhorar curva TC
3. Iniciar testes unitários (70% coverage)

### Longo Prazo (4-6 meses)
1. Implementar REST API completa
2. Documentação REST (OpenAPI/Swagger)
3. Integração RelayLab 360
4. Dashboard de designs salvos

### Antes de Integração em RelayLab 360
- ✅ Todos os bugs corrigidos
- ✅ Testes automatizados (70%+ coverage)
- ✅ Documentação técnica completa
- ✅ API REST estável (v1 finalizada)
- ✅ Modelo de dados para persistência definido
- ✅ Segurança validada (OWASP, input validation)

---

## 📞 Contatos e Referências

**Email de Bugs:** protecview@eletrogrid.com.br  
**Desenvolvido com:** Python + Dash + Plotly + Numpy  
**Referências normativas:** IEC 60255, IEEE C37.112, NBR 5410

---

**Documentação gerada em:** 2026-05-19  
**Versão:** 1.0 (Post-Merge Feature Dynamic UI)  
**Próxima revisão:** Após correção do bug crítico
