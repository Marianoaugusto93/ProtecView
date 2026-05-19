# 🎯 Plano de Execução em Fases - ProtecView

**Preparado em:** 2026-05-19  
**Executor:** Claude Code (via Claude Code CLI)  
**Deployment:** onRender (sem mudanças de infraestrutura)  
**Timeline Total:** 4-5 semanas  

---

## 📌 Overview

```
FASE 0 (1 dia)        FASE 1 (2-3 dias)     FASE 2 (3-4 dias)     FASE 3 (5-7 dias)
Setup & Planning      Crítica              Refactoring           Integração RelayLab
    ↓                    ↓                      ↓                       ↓
   Done              ✅ Funcional         Production-Ready      REST API Ready
                    7/8 módulos          Código limpo           Testes 70%+
```

---

## 🎬 FASE 0: Setup & Planning (1 dia)

**Objetivo:** Preparar ambiente e validar acesso

### Task 0.1: Validar Ambiente (30 min)
**Status:** Ready
**Por:** Claude Code
**Ação:**
```bash
# 1. Clone/pull repo
cd C:\Users\augus\Documentos\claude\ProtecView
git status
git log --oneline -5

# 2. Setup venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 3. Validar app roda
python run.py
# Abrir http://127.0.0.1:8050 → testar 2 módulos

# 4. Confirmar
# ✅ Venv funciona
# ✅ Dependências instaladas
# ✅ App inicia sem erros
# ✅ Navegador carrega home
```

**Saída Esperada:**
```
✅ Venv ativo
✅ requirements.txt OK
✅ App rodando em 8050
✅ 7/8 módulos testados (Distribuição quebrada, esperado)
```

**Merge:** Direto em master (nenhuma mudança de código)

---

### Task 0.2: Criar Branch Estrutura (30 min)
**Status:** Ready
**Por:** Claude Code
**Ação:**
```bash
# Criar branches para cada fase
git checkout master
git pull origin master

# Branches de trabalho
git checkout -b phase-1-critical-fixes
git checkout master && git checkout -b phase-2-refactoring
git checkout master && git checkout -b phase-3-relaylab-integration

# Voltar para Phase 1
git checkout phase-1-critical-fixes

# Verificar
git branch -a
```

**Saída Esperada:**
```
✅ 3 branches criados
✅ Master limpo (sem mudanças)
✅ Phase 1 branch pronto
```

**Merge:** Nenhum (só estrutura)

---

## 🔴 FASE 1: Crítica (Correções de Bugs) - 2-3 DIAS

**Objetivo:** Corrigir bugs + code quality básica  
**Critério de Sucesso:** 7/8 módulos funcionando + código limpo

---

### Sprint 1.1: Corrigir Bug Módulo 8 (Proteção Distribuição)

**Branch:** `phase-1-critical-fixes`  
**Tempo:** 6-8 horas

#### Task 1.1.1: Diagnosticar Bug (1 hora)
**Por:** Claude Code

**Ação:**
```python
# Em callbacks/callbacks_dist_protection.py
# Linhas 136-165: função plot_dist_tcc_graph

# Adicionar logs para debug:
import logging
logger = logging.getLogger(__name__)

@app.callback(...)
def plot_dist_tcc_graph(...):
    logger.info(f"[DEBUG] n_clicks: {n_clicks}")
    logger.info(f"[DEBUG] fuse_types_val: {fuse_types_val}")
    logger.info(f"[DEBUG] fuse_type_ids: {fuse_type_ids}")
    logger.info(f"[DEBUG] storage_json: {storage_json}")
    
    # Se estas listas vazias → problema é State(... ALL) não retornando valores
```

**Teste Manual:**
1. Rodar app: `python run.py`
2. Ir para aba "Proteção de Distribuição"
3. Clicar "Adicionar Dispositivo" → tipo "Fusível"
4. Clicar "Plotar Gráfico"
5. Ver logs no terminal → identificar onde falha

**Saída Esperada:**
```
[DEBUG] storage_json: [{'id': 1, 'type': 'fuse'}]  ✅ OK
[DEBUG] fuse_types_val: []  ❌ PROBLEMA
[DEBUG] fuse_type_ids: []   ❌ PROBLEMA
```

**Arquivo:** `callbacks/callbacks_dist_protection.py`  
**Linhas modificadas:** Adicionar ~20 linhas de logging

---

#### Task 1.1.2: Implementar Fix (3-4 horas)
**Por:** Claude Code

**Problema Diagnosticado:**
```
State({'type': 'fuse-type', 'index': ALL}, 'value')
      retorna [] quando controles foram renderizados dinamicamente
```

**Solução:**
Refatorar callback para usar padrão mais robusto:

```python
# Novo padrão (baseado em TCC que funciona):

@app.callback(
    Output('dist_tcc_graph', 'figure'),
    Input('btn_plot_dist_curves', 'n_clicks'),
    [
        State('dist_curve_storage', 'children'),  # JSON storage
        State({'type': 'fuse-type', 'index': ALL}, 'value'),
        State({'type': 'fuse-rating', 'index': ALL}, 'value'),
        # ... outros estados
    ],
    prevent_initial_call=True
)
def plot_dist_tcc_graph(n_clicks, storage_json, *args):
    # NOVO: Parsing robusto do storage JSON
    try:
        curves = json.loads(storage_json) if storage_json else []
    except:
        curves = []
    
    # Para cada curve no storage:
    # 1. Identificar seu ID
    # 2. Procurar valores correspondentes nos args
    # 3. Montar dicionário com dados
    
    fig = go.Figure(...)
    
    for curve in curves:
        curve_id = curve['id']
        curve_type = curve['type']
        
        if curve_type == 'fuse':
            # Procurar valores deste fusível específico
            # Usar mapping robusto: ID → valor
            f_type = find_value_by_id('fuse-type', curve_id, ...)
            f_rating = find_value_by_id('fuse-rating', curve_id, ...)
            
            if f_type and f_rating:
                # Calcular e plotar
                ...
    
    return fig
```

**Código a Modificar:**
- `callbacks/callbacks_dist_protection.py`: Função `plot_dist_tcc_graph` (~40 linhas)

**Testes:**
1. Adicionar 1 fusível K 40A → plotar → gráfico aparece ✅
2. Adicionar 2 fusíveis (diferentes ratings) → plotar → ambas curvas ✅
3. Adicionar religador → plotar → 2 curvas (rápida + lenta) ✅
4. Remover fusível → plotar → gráfico atualiza ✅
5. Limpar tudo → plotar → figura vazia com mensagem ✅

**Saída Esperada:**
```
✅ Gráfico TCC plotado corretamente
✅ Múltiplos dispositivos suportados
✅ Adicionar/remover funciona
✅ Sem erros no console
```

---

#### Task 1.1.3: Commit (30 min)
**Por:** Claude Code

```bash
git add callbacks/callbacks_dist_protection.py

git commit -m "fix: resolve dist_protection callback data mapping issue

- Refactor State(... ALL) pattern to use robust ID-to-value mapping
- Fix issue where fuse/recloser values were not being read by callback
- Add validation for empty storage and missing values
- Tested with multiple fuses and reclosers configurations
- All dynamic controls now properly synchronized with plot
"

git log --oneline -3  # Verificar
```

**Saída Esperada:**
```
✅ Commit criado com mensagem descritiva
✅ Mudança é atômica e reversível
✅ Git history limpo
```

---

### Sprint 1.2: Consolidar CSS (3 horas)

**Branch:** `phase-1-critical-fixes`  
**Tempo:** 3 horas

#### Task 1.2.1: Mesclar style.css + custom_styles.css (2 horas)
**Por:** Claude Code

**Ação:**
1. Ler `assets/style.css` e `assets/custom_styles.css`
2. Mesclar em `assets/main.css` com estrutura:
```css
/* 1. CSS Variables (Theme) */
:root {
  --primary-color: ...
  --secondary-color: ...
  --text-color: ...
  --bg-color: ...
}

.light-theme {
  --primary-color: ...
  /* light colors */
}

.dark-theme {
  --primary-color: ...
  /* dark colors */
}

/* 2. Base Layout */
* { ... }
body { ... }

/* 3. Components */
.header-container { ... }
.module-container { ... }
.DashButton { ... }
.DashInput { ... }
.DashDropdown { ... }

/* 4. Responsive */
@media (max-width: 768px) { ... }
```

3. Verificar que todos os seletores foram inclusos
4. Remover duplicatas

**Arquivos:**
- `assets/style.css` → DELETE
- `assets/custom_styles.css` → DELETE
- `assets/main.css` → CREATE (novo)

**Testes:**
1. Rodar app
2. Testar tema claro → cores corretas ✅
3. Testar tema escuro → cores corretas ✅
4. Testar responsivo (F12 → device toolbar)
5. Testar em mobile size (375px) ✅

**Saída Esperada:**
```
✅ CSS consolidado em 1 arquivo
✅ Sem conflito de estilos
✅ Temas funcionam (claro/escuro)
✅ Responsivo OK
```

---

#### Task 1.2.2: Atualizar Referências em run.py (30 min)
**Por:** Claude Code

**Ação:**
```python
# Em app.py, verificar que assets são carregados automaticamente
# Dash carrega tudo em assets/ automaticamente
# Nada a fazer se houver apenas main.css

# Se houver problema, adicionar em app.py:
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap'
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    assets_folder='assets',  # main.css será carregado automaticamente
    suppress_callback_exceptions=True,
    meta_tags=[...]
)
```

**Testes:**
1. Rodar app
2. F12 → Network → procurar main.css
3. Verificar CSS carregado corretamente

**Saída Esperada:**
```
✅ main.css carregado
✅ Sem erros 404
✅ Estilos aplicados
```

---

#### Task 1.2.3: Commit CSS (30 min)
**Por:** Claude Code

```bash
git add assets/main.css
git rm assets/style.css assets/custom_styles.css

git commit -m "refactor: consolidate CSS files into single main.css

- Merge style.css and custom_styles.css into assets/main.css
- Organize CSS: variables, base, components, responsive sections
- Remove duplicate styles and selectors
- Validate light/dark theme switching
- Tested on mobile responsive sizes
"

git log --oneline -3
```

---

### Sprint 1.3: Type Hints + Logging (7 horas)

**Branch:** `phase-1-critical-fixes`  
**Tempo:** 7 horas

#### Task 1.3.1: Setup Logging (2 horas)
**Por:** Claude Code

**Criar:** `core/logging_config.py`
```python
import logging
import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'protecview.log'
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
```

**Atualizar:** `app.py`
```python
from core.logging_config import setup_logging
setup_logging()

logger = logging.getLogger(__name__)
logger.info("ProtecView started")
```

**Arquivos a Modificar:**
- `app.py` (adicionar 2 linhas)
- `run.py` (adicionar 2 linhas)
- `core/logging_config.py` (CREATE - novo arquivo)

---

#### Task 1.3.2: Adicionar Type Hints (4 horas)
**Por:** Claude Code

**Arquivos Priority:**
1. `run.py` - Entry point
2. `callbacks/callbacks_tcc.py` - Mais complexo
3. `callbacks/callbacks_dist_protection.py` - Já modificado
4. `utils/utils_common.py` - Base utils

**Exemplo de conversão:**
```python
# ANTES
def plot_tcc_graph(n_clicks, curve_types, pickups, tds):
    fig = go.Figure()
    ...
    return fig

# DEPOIS
from typing import List, Optional, Dict, Any
import plotly.graph_objects as go

def plot_tcc_graph(
    n_clicks: int,
    curve_types: List[Optional[str]],
    pickups: List[Optional[float]],
    tds: List[Optional[float]],
) -> go.Figure:
    """Plot TCC curves with multiple relays."""
    fig = go.Figure()
    ...
    return fig
```

**Adicionar imports em cada arquivo:**
```python
from typing import Dict, List, Optional, Tuple, Any, Union
import logging

logger = logging.getLogger(__name__)
```

**Validar com mypy:**
```bash
pip install mypy
mypy callbacks/ utils/ --ignore-missing-imports
```

**Saída Esperada:**
```
Success: no issues found in 8 files
```

---

#### Task 1.3.3: Adicionar Logging em Callbacks Críticos (1 hora)
**Por:** Claude Code

**Callbacks para Instrumentar:**
- `callbacks_sym.py` - Componentes simétricos
- `callbacks_tcc.py` - Curvas TCC
- `callbacks_dist_protection.py` - Distribuição (já tem debug)
- `callbacks_fault.py` - Cálculo de faltas

**Padrão:**
```python
logger = logging.getLogger(__name__)

@app.callback(...)
def plot_tcc_graph(...):
    logger.info(f"Plotting TCC with {len(pickups)} relays")
    try:
        # ... cálculos ...
        logger.info("TCC plot successful")
        return fig
    except Exception as e:
        logger.error(f"TCC plot failed: {e}", exc_info=True)
        return empty_figure()
```

---

#### Task 1.3.4: Commit Type Hints (30 min)
**Por:** Claude Code

```bash
git add core/logging_config.py callbacks/ utils/ app.py run.py

git commit -m "feat: add type hints and structured logging

- Add Python type hints to all public functions
- Implement structured logging configuration
- Add logging to critical callback functions
- Validate with mypy: no issues found
- Improve debuggability and type safety
"

# Verificar
mypy callbacks/ utils/ --ignore-missing-imports
```

---

### Sprint 1.4: Validação e Deploy Fase 1 (2 horas)

**Branch:** `phase-1-critical-fixes`

#### Task 1.4.1: Testes Manuais Completos (1 hora)
**Por:** Claude Code

**Checklist:**
- [ ] App inicia sem erros
- [ ] Home page carrega
- [ ] Módulo 1 (Simétricos): calcula e gráfico aparece ✅
- [ ] Módulo 2 (Distância): zonas aparecem ✅
- [ ] Módulo 3 (Faltas): calcula ✅
- [ ] Módulo 4 (TCC): múltiplos relés funcionam ✅
- [ ] Módulo 5 (Ampacidade): calcula ✅
- [ ] Módulo 6 (TC): saturação aparece ✅
- [ ] Módulo 7 (Diferencial): curva aparece ✅
- [ ] Módulo 8 (Distribuição): **AGORA FUNCIONA** ✅ (era quebrado)
- [ ] Tema claro/escuro funciona ✅
- [ ] Responsive em mobile ✅
- [ ] Console sem erros JavaScript ✅
- [ ] Logs aparecem no terminal ✅

**Rodar:**
```bash
python run.py
# Testar cada módulo
# F12 console → sem erros
# Terminal → logs aparecem
```

---

#### Task 1.4.2: Merge para Master (30 min)
**Por:** Claude Code

```bash
# Verificar tudo funciona
git status  # Limpo
git log --oneline -5  # Mostra 3 commits

# Merge
git checkout master
git pull origin master
git merge phase-1-critical-fixes

# Verificar
git log --oneline -3
# Mostrar: fix dist_protection, refactor CSS, feat type hints

# Tag release
git tag -a v1.1.0 -m "Phase 1: Critical fixes and code quality"

# Push
git push origin master --tags
```

**Saída Esperada:**
```
✅ Fase 1 merged em master
✅ 3 commits adicionados
✅ Nenhum conflito
✅ v1.1.0 tagged
```

---

#### Task 1.4.3: Deploy em onRender (30 min)
**Por:** Claude Code (monitorar)

**onRender faz deploy automático quando código é pushed!**

```bash
# Apenas monitorar:
# 1. Ir para dashboard onRender
# 2. Ver "Deployments" → novo deploy em progresso
# 3. Aguardar "Build succeeded"
# 4. Testar em produção:
#    https://protecview.onrender.com (seu URL)
# 5. Validar Módulo 8 funciona em produção ✅
```

**Checklist:**
- [ ] onRender detectou push
- [ ] Build iniciado
- [ ] Build completed (5-10 min)
- [ ] App online
- [ ] Teste Módulo 8 em produção
- [ ] Logs em onRender mostram sucesso

---

### 🎯 Saída Final Fase 1

**Commits:**
```
fix: resolve dist_protection callback data mapping issue
refactor: consolidate CSS files into single main.css
feat: add type hints and structured logging
```

**Benefícios:**
- ✅ Módulo 8 (Distribuição) **agora funciona**
- ✅ CSS consolidado (menos dívida técnica)
- ✅ Type hints adicionados (melhor IDE support)
- ✅ Logging implementado (melhor debug)
- ✅ Code quality aumentada
- ✅ Em produção (onRender atualizado)

**Tempo Total Fase 1:** ~16 horas (2-3 dias)

**Status após Fase 1:**
```
✅ 8/8 módulos funcionando
✅ Código mais limpo
✅ Pronto para Fase 2
```

---

## 🟡 FASE 2: Refactoring (3-4 DIAS)

**Objetivo:** Melhorar código, adicionar testes básicos  
**Branch:** `phase-2-refactoring`  
**Tempo:** ~15 horas

---

### Sprint 2.1: Refatorar Módulo 2 - Distância Dinâmica (4 horas)

**Por:** Claude Code

**Objetivo:** Transformar Módulo 2 (Zonas Distância) em UI dinâmica

**Template:** Copiar padrão de `callbacks_tcc.py` que já é dinâmico

**Arquivos a Modificar:**
- `layouts.py` - UI (Adicionar/Remover Zonas)
- `callbacks/callbacks_dist.py` - Novo padrão dinâmico

**Saída Esperada:**
```
✅ Adicionar zona button funciona
✅ Múltiplas zonas aparecem
✅ Remover zona funciona
✅ Gráfico R-X atualiza dinamicamente
✅ Dados persistem no storage JSON
```

---

### Sprint 2.2: Melhorar Curva TC (3 horas)

**Por:** Claude Code

**Objetivo:** Plotar curva de excitação senoidal (não apenas linha)

**Arquivos a Modificar:**
- `callbacks/callbacks_ct.py`
- `utils/utils_ct.py`

**Saída Esperada:**
```
✅ Curva de excitação realista
✅ Distorção harmônica incluída
✅ Kneepoint marcado corretamente
```

---

### Sprint 2.3: Validation + Error Handling (4 horas)

**Por:** Claude Code

**Objetivo:** Validar inputs, tratrar erros gracefully

**Usar Pydantic:**
```bash
pip install pydantic
```

**Arquivos:**
- `core/validators.py` - CREATE (novo)

**Padrão:**
```python
from pydantic import BaseModel, validator, ValidationError

class TccCurveInput(BaseModel):
    pickup: float
    tds: float
    curve_type: str
    
    @validator('pickup')
    def validate_pickup(cls, v):
        if not 0.5 <= v <= 10000:
            raise ValueError('Pickup deve estar entre 0.5 e 10000')
        return v
```

**Saída Esperada:**
```
✅ Inputs validados
✅ Mensagens de erro claras
✅ App não quebra com dados ruins
```

---

### Sprint 2.4: Code Cleanup (4 horas)

**Por:** Claude Code

**Ações:**
1. Remover `_callbacks_OLD.py`
2. Refatorar duplicação (factory patterns)
3. Documentar com docstrings
4. Limpar arquivos não usados

**Saída Esperada:**
```
✅ Sem arquivos antigos
✅ Código DRY (Don't Repeat Yourself)
✅ Docstrings em 100% funções públicas
```

---

### 🎯 Saída Final Fase 2

**Status após Fase 2:**
```
✅ Código refatorado
✅ Testes básicos (se implemente)
✅ Pronto para Fase 3
```

**Tempo Total Fase 2:** ~15 horas (3-4 dias)

---

## 🔵 FASE 3: Integração RelayLab 360 (5-7 DIAS)

**Objetivo:** Criar REST API + prepare integração  
**Branch:** `phase-3-relaylab-integration`  
**Tempo:** ~28 horas

---

### Sprint 3.1: REST API Backend (10 horas)

**Por:** Claude Code

**Setup FastAPI:**
```bash
pip install fastapi uvicorn pydantic
```

**Arquivos:**
- `main.py` - FastAPI app (novo)
- `api/routes/` - Endpoints por módulo (novos)
- `core/config.py` - Configuração (novo)

**8 Endpoints REST:**
```
POST /api/v1/modules/symmetric-components
POST /api/v1/modules/tcc-curves
POST /api/v1/modules/distance-zones
POST /api/v1/modules/fault-calculation
POST /api/v1/modules/ampacity
POST /api/v1/modules/ct-saturation
POST /api/v1/modules/differential
POST /api/v1/modules/distribution
```

**Saída Esperada:**
```
✅ FastAPI app roda em :8000
✅ Swagger docs em /docs
✅ 8 endpoints funcionam
✅ Input validation via Pydantic
✅ Error handling (HTTP 400, 422, 500)
```

---

### Sprint 3.2: Modelos de Dados (5 horas)

**Por:** Claude Code

**Setup SQLAlchemy:**
```bash
pip install sqlalchemy
```

**Criar:**
- `core/database.py` - Conexão DB
- `models/protecview.py` - Modelos

**Modelo ProtecViewDesign:**
```python
class ProtecViewDesign(Base):
    design_id: str (PK)
    user_id: str  # FK para RelayLab user
    name: str
    module: str  # 'tcc', 'distance', etc
    configuration: JSON
    created_at: datetime
    updated_at: datetime
```

**CRUD Endpoints:**
- `POST /api/v1/designs`
- `GET /api/v1/designs/{design_id}`
- `PUT /api/v1/designs/{design_id}`
- `DELETE /api/v1/designs/{design_id}`

**Saída Esperada:**
```
✅ DB schema criado
✅ CRUD endpoints funcionam
✅ Dados persistem
```

---

### Sprint 3.3: Autenticação + Segurança (5 horas)

**Por:** Claude Code

**Setup FastAPI Security:**
```bash
pip install python-jose[cryptography] passlib
```

**Implementar:**
- JWT token validation
- CORS configuration
- Rate limiting
- Input sanitization

**Saída Esperada:**
```
✅ JWT validation funciona
✅ CORS habilitado para RelayLab
✅ Rate limiting em lugar
✅ Inputs sanitizados
```

---

### Sprint 3.4: Testes Unitários (5 horas)

**Por:** Claude Code

**Setup Pytest:**
```bash
pip install pytest pytest-cov
```

**Estrutura:**
```
tests/
├─ test_api/
│  ├─ test_symmetric_components.py
│  └─ test_tcc_curves.py
├─ test_utils/
│  ├─ test_utils_sym.py
│  └─ test_utils_tcc.py
└─ conftest.py  # Fixtures
```

**Meta:** 70%+ coverage

```bash
pytest tests/ --cov=api --cov=utils --cov-report=html
```

**Saída Esperada:**
```
✅ 70%+ coverage alcançado
✅ Testes passam (verde)
✅ CI-ready
```

---

### Sprint 3.5: Documentação (3 horas)

**Por:** Claude Code

**Gerar:**
1. OpenAPI/Swagger (automático FastAPI)
2. `docs/API.md` - Referência endpoints
3. `docs/INTEGRATION.md` - Como integrar RelayLab
4. Update README.md

**Saída Esperada:**
```
✅ Swagger UI em /docs
✅ API documentation completa
✅ Guia integração escrito
```

---

### 🎯 Saída Final Fase 3

**Status após Fase 3:**
```
✅ REST API implementada
✅ 8 módulos expostos via API
✅ Autenticação implementada
✅ Testes 70%+
✅ Documentação completa
✅ Pronto para RelayLab 360
```

**Tempo Total Fase 3:** ~28 horas (5-7 dias)

---

## 📊 Timeline Consolidado

```
SEMANA 1
├─ Dia 1: Fase 0 (Setup) - 1 dia ✓
├─ Dia 2-3: Sprint 1.1-1.3 (7-8 horas cada) - 2-3 dias
└─ Dia 3-4: Sprint 1.4 + Deploy - 2 horas

SEMANA 2
├─ Dia 1-2: Sprint 2.1-2.4 (Refactoring) - 3-4 dias
└─ Deploy intermediário (branch phase-2-refactoring)

SEMANA 3-4
├─ Sprint 3.1: REST API (10 horas) - 2-3 dias
├─ Sprint 3.2: DB Models (5 horas) - 1 dia
├─ Sprint 3.3: Auth (5 horas) - 1 dia
├─ Sprint 3.4: Testes (5 horas) - 1 dia
└─ Sprint 3.5: Docs (3 horas) - 1 dia

TOTAL: 4-5 semanas (~60-70 horas desenvolvimento)
```

---

## ✅ Critérios de Aceitação por Fase

### Fase 1 COMPLETA quando:
- [ ] Módulo 8 funciona (gráfico TCC plotado)
- [ ] CSS consolidado (1 arquivo)
- [ ] Type hints adicionados
- [ ] Logging implementado
- [ ] Testes manuais passam (8/8 módulos)
- [ ] Deploy em onRender bem-sucedido
- [ ] Master branch atualizado com v1.1.0 tag

### Fase 2 COMPLETA quando:
- [ ] Módulo 2 é dinâmico (Adicionar/Remover zonas)
- [ ] Curva TC melhorada
- [ ] Validation + error handling implementado
- [ ] Code cleanup concluído
- [ ] Refatoração passa em testes manuais
- [ ] Deploy intermediário bem-sucedido

### Fase 3 COMPLETA quando:
- [ ] FastAPI app funciona
- [ ] 8 endpoints REST implementados
- [ ] DB schema criado
- [ ] JWT authentication funciona
- [ ] 70%+ test coverage
- [ ] Documentação OpenAPI/Swagger completa
- [ ] Pronto para integração RelayLab 360

---

## 🚀 Como Executar (Para o Usuário)

### Iniciar Fase 1:
```bash
# 1. Clonar repo (já está feito)
cd C:\Users\augus\Documentos\claude\ProtecView

# 2. Pedir ao Claude Code:
# "Executar FASE 1 do plano de execução em fases"
# (Claude Code lerá este documento + executará sprints)

# 3. Monitorar progresso:
git log --oneline  # Ver commits sendo adicionados
git branch -a      # Ver branches

# 4. Quando Fase 1 estiver pronta:
git checkout master
# Verificar em onRender que v1.1.0 está online
```

### Iniciar Fase 2:
```bash
# Após conclusão Fase 1:
# "Executar FASE 2 do plano de execução em fases"

# Monitorar
git checkout phase-2-refactoring
git log --oneline
```

### Iniciar Fase 3:
```bash
# Após conclusão Fase 2:
# "Executar FASE 3 do plano de execução em fases"

# Monitorar + testar API
curl http://localhost:8000/docs  # Swagger UI
```

---

## 📈 Métricas de Sucesso

### Final Fase 1:
```
Módulos funcionais:  8/8 ✅ (antes: 7/8)
Code quality score:  7/10 (antes: 5/10)
Type coverage:       40% (antes: 0%)
Logging:            Implementado ✅
```

### Final Fase 2:
```
Type coverage:       80%+ ✅
Refactoring:        Completo ✅
Code quality score:  8/10
Documentation:      Básica
```

### Final Fase 3:
```
Type coverage:       100% ✅
REST API:           Pronto ✅
Test coverage:      70%+ ✅
Documentation:      Completa ✅
RelayLab ready:     SIM ✅
```

---

## 🎯 Dependências Entre Fases

```
FASE 0 (Setup)
    ↓
FASE 1 (Critical Fixes)  ← BLOCKER: Fase 2 depende de Fase 1 pronta
    ↓
FASE 2 (Refactoring)     ← BLOCKER: Fase 3 depende de Fase 2 pronta
    ↓
FASE 3 (RelayLab API)    ← Pode começar quando Fase 2 ~80% pronta
```

**OBS:** Fases são sequenciais (não parallelizáveis com segurança)

---

## 📞 Comandos Úteis para Monitorar

```bash
# Ver status de branches
git branch -a

# Ver commits recentes
git log --oneline -10

# Ver próximo commit antes de merge
git log phase-1-critical-fixes ^master

# Testar aplicação
python run.py

# Validar type hints
mypy callbacks/ utils/ --ignore-missing-imports

# Testar API (depois da Fase 3)
curl http://localhost:8000/api/v1/symmetric-components \
  -X POST -H "Content-Type: application/json" \
  -d '{"direction": "phase-to-sym", ...}'
```

---

## 🎬 Começar Agora!

**Para Iniciar Fase 1:**

```
1. Você: "Claude Code, execute FASE 1 conforme PLANO_EXECUCAO_FASES.md"

2. Claude Code:
   - Lerá este documento
   - Executará Sprint 1.1 (diagnóstico + fix bug)
   - Executará Sprint 1.2 (CSS)
   - Executará Sprint 1.3 (type hints + logging)
   - Executará Sprint 1.4 (validação + deploy)
   - Fará commits e merge para master
   - Reportará status

3. Você:
   - Monitora progresso em git
   - Aguarda deploy em onRender
   - Testa em produção
```

---

**Status:** ✅ Plano pronto para execução  
**Data:** 2026-05-19  
**Próximo Passo:** Solicitar execução de Fase 1 ao Claude Code  
**Tempo Total:** 4-5 semanas para completar tudo
