# 🚀 Plano de Ação - ProtecView → RelayLab 360

**Data:** 2026-05-19  
**Status:** Pré-integração (Fase 1: Correções Críticas)  
**Timeline estimado:** 8-12 semanas até integração

---

## 📌 Resumo Executivo

ProtecView está **funcional mas com pendências críticas** antes de integrar em RelayLab 360:

| Item | Status | Prioridade | Effort |
|------|--------|-----------|--------|
| Bug: Módulo de Distribuição | 🔴 Crítico | ALTA | 6h |
| Consolidação CSS | ⚠️ Dívida Técnica | MÉDIA | 3h |
| Type Hints + Logging | 📋 Manutenção | MÉDIA | 7h |
| REST API (novo) | 🆕 Requerido | ALTA | 20h |
| Testes Unitários | 🆕 Requerido | ALTA | 15h |
| Documentação | 📚 Requerido | MÉDIA | 8h |
| **TOTAL** | | | **59h** |

**Equivalente a:** ~7-9 dias de trabalho focado (8h/dia)

---

## 🎯 Fase 1: CRÍTICA (Semana 1-2) - 16 HORAS

### ✅ Sprint 1.1: Corrigir Bug do Módulo de Distribuição (6h)

**O que está quebrado:**
- Módulo 8 (Proteção de Distribuição) não plota gráficos
- Fusíveis e Religadores dinâmicos não funcionam
- Callback `plot_dist_tcc_graph()` recebe listas vazias

**Plano de Ação:**

**Passo 1: Diagnosticar o mapeamento de IDs (1h)**
```python
# Em callbacks_dist_protection.py, adicionar logs:
@app.callback(...)
def plot_dist_tcc_graph(...):
    print(f"DEBUG: fuse_types_val = {fuse_types_val}")
    print(f"DEBUG: fuse_type_ids = {fuse_type_ids}")
    print(f"DEBUG: storage_json = {storage_json}")
    # Se estas listas estão vazias, o problema é o State(... ALL)
```

**Passo 2: Refatorar mapeamento (2h)**
```python
# Solução: usar ID como chave diretamente
# Em vez de: State({'type': 'fuse-type', 'index': ALL}, 'id')
# Usar: State('dist_curve_storage', 'children') e ler os valores renderizados

# Novo fluxo:
# 1. storage_json contém: [{'id': 1, 'type': 'fuse'}, ...]
# 2. render_dist_controls() cria: fuse controls com id={'type': 'fuse-type', 'index': 1}
# 3. plot_dist_tcc_graph() lê valores via State(... ALL) e faz mapeamento robusto
```

**Passo 3: Testar múltiplos dispositivos (2h)**
- Adicionar 3 fusíveis K (40A, 65A, 100A)
- Adicionar 2 religadores (Rápido + Lento)
- Validar gráfico é plotado
- Comparar com cálculos manuais

**Passo 4: Commit**
```bash
git commit -m "fix: resolve dist_protection callback data mapping issue

- Fix State(... ALL) pattern to properly map fuse/recloser values
- Add robust ID-to-value mapping for dynamic components
- Add validation and error handling
- Tested with multiple fuses and reclosers
"
```

---

### ✅ Sprint 1.2: Consolidar Styles CSS (3h)

**Ação:**
1. Mesclar `assets/style.css` + `assets/custom_styles.css` → `assets/main.css`
2. Estrutura:
   ```css
   /* 1. Variables (theme) */
   :root { --primary-color: #... }
   .light-theme { --primary-color: #... }
   .dark-theme { --primary-color: #... }
   
   /* 2. Layout & Components */
   .header-container { ... }
   .module-container { ... }
   .DashButton { ... }
   
   /* 3. Responsive */
   @media (max-width: 768px) { ... }
   ```
3. Atualizar `run.py`: remover `custom_styles.css`
4. Testar temas (claro/escuro)

---

### ✅ Sprint 1.3: Type Hints + Logging (7h)

**A. Type Hints (4h)**
```python
# Exemplo: callbacks_tcc.py
from typing import Dict, List, Tuple, Optional

def plot_tcc_graph(
    n_clicks: int,
    curve_type_vals: List[Optional[str]],
    pickup_vals: List[Optional[float]],
    ...
) -> go.Figure:
    """Plot TCC curves with multiple relays."""
    ...

# Ferramentas:
# - mypy para validação estática
# - Aplicar a todos os callbacks/utils
```

**B. Logging (3h)**
```python
# Configuração centralizada: core/logging_config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Uso em callbacks:
logger = logging.getLogger(__name__)
logger.info(f"Plotting TCC curve for relay {relay_name}")
logger.error(f"Invalid pickup value: {pickup}")
```

---

## 🎯 Fase 2: REFACTORING (Semana 3-4) - 15 HORAS

### ✅ Sprint 2.1: Refatorar Módulo 2 - Distância Dinâmica (4h)

**Template:** Copiar padrão de `callbacks_tcc.py`

```python
# Em layouts.py
layout_dist = html.Div([
    html.Button('Adicionar Zona', id='btn_add_dist_zone'),
    html.Div(id='dynamic_dist_zones'),  # Container dinâmico
    html.Button('Plotar Gráfico', id='btn_plot_dist'),
])

# Em callbacks_dist.py (novo padrão)
@app.callback(
    Output('dist_zones_storage', 'data'),
    Input('btn_add_dist_zone', 'n_clicks'),
    State('dist_zones_storage', 'data')
)
def add_zone(n_clicks, data):
    # Mesmo padrão que TCC
    ...
```

---

### ✅ Sprint 2.2: Melhorar Curva TC (3h)

**Adicionar:**
- Plotar curva de excitação senoidal (não apenas linha horizontal)
- Incluir distorção harmônica
- Referência: IEC 61869-2

---

### ✅ Sprint 2.3: Validation + Error Handling (4h)

**Padrão:**
```python
from pydantic import BaseModel, validator

class TccCurveInput(BaseModel):
    pickup: float  # A
    tds: float     # 0.05 - 10.0
    curve_type: str
    
    @validator('pickup')
    def validate_pickup(cls, v):
        if not 0.5 <= v <= 10000:
            raise ValueError('Pickup fora da faixa')
        return v

# Usar em callbacks:
try:
    data = TccCurveInput(**input_dict)
except ValueError as e:
    logger.error(f"Validation error: {e}")
    return {"error": str(e)}
```

---

### ✅ Sprint 2.4: Cleanup de Código (4h)

- Remover `_callbacks_OLD.py`
- Refatorar duplicação (factory patterns)
- Documentar com docstrings

---

## 🎯 Fase 3: INTEGRAÇÃO RelayLab 360 (Semana 5-8) - 28 HORAS

### ✅ Sprint 3.1: REST API Backend (10h)

**Estrutura:**
```python
# main.py (FastAPI ou Flask)
from fastapi import FastAPI

app = FastAPI(title="ProtecView API v1")

@app.post("/api/v1/modules/symmetric-components")
async def calc_symmetric_components(input_data: SymmetricComponentsInput):
    # Usar utils_sym.py
    ...
    return {"sequence_0": ..., "sequence_1": ..., ...}

@app.post("/api/v1/modules/tcc-curves")
async def calc_tcc_curves(input_data: TccCurvesInput):
    # Usar utils_tcc.py
    ...
    return {"times": [...], "currents": [...]}

# E assim para os 8 módulos...
```

**Tasks:**
- [ ] Setup FastAPI ou Flask-RESTful
- [ ] Criar 8 endpoints (um por módulo)
- [ ] Input validation (Pydantic)
- [ ] Error responses (HTTP 400, 422, 500)
- [ ] Documentação Swagger automática

---

### ✅ Sprint 3.2: Modelos de Dados (5h)

```python
# models.py
from sqlalchemy import Column, String, JSON, DateTime
from datetime import datetime

class ProtecViewDesign(Base):
    __tablename__ = "protecview_designs"
    
    design_id = Column(String, primary_key=True)
    user_id = Column(String)  # FK para RelayLab user
    name = Column(String)
    module = Column(String)  # 'tcc', 'distance', etc.
    configuration = Column(JSON)  # Todos os parâmetros
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # CRUD endpoints:
    # POST   /api/v1/designs
    # GET    /api/v1/designs/{design_id}
    # PUT    /api/v1/designs/{design_id}
    # DELETE /api/v1/designs/{design_id}
    # GET    /api/v1/designs?module=tcc&user_id=xxx
```

---

### ✅ Sprint 3.3: Autenticação + Segurança (5h)

```python
# core/security.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)):
    """Validar JWT token de RelayLab 360"""
    token = credentials.credentials
    # Validar assinatura com chave pública de RelayLab
    # Retornar user_id se válido
    ...

# Usar em rotas:
@app.post("/api/v1/designs")
async def create_design(design_data: dict, user=Depends(verify_token)):
    # user_id está disponível
    ...
```

**Tasks:**
- [ ] Setup JWT validation
- [ ] CORS configuration
- [ ] Rate limiting (FastAPI SlowAPI)
- [ ] Input sanitization
- [ ] HTTPS enforcement

---

### ✅ Sprint 3.4: Testes Unitários (5h)

```python
# tests/test_utils_tcc.py
import pytest
from utils.utils_tcc import get_tcc_time

def test_tcc_time_ieee_mi():
    # Teste com valores conhecidos
    t = get_tcc_time(pickup=5, current=50, tds=1.0, curve='IEEE Moderately Inverse')
    assert 0.5 < t < 2.0  # Validação de range
    
def test_tcc_time_invalid_input():
    with pytest.raises(ValueError):
        get_tcc_time(pickup=-5, ...)  # Pickup negativo
```

**Meta:** 70%+ coverage

```bash
pytest --cov=utils --cov-report=html
```

---

### ✅ Sprint 3.5: Documentação (3h)

**Gerar:**
- [ ] `docs/API.md` - Referência completa de endpoints
- [ ] `docs/INTEGRATION.md` - Como integrar com RelayLab 360
- [ ] `docs/ARCHITECTURE.md` - Diagrama e design
- [ ] OpenAPI/Swagger (automático via FastAPI)

**Exemplo para INTEGRATION.md:**
```markdown
# Integração ProtecView em RelayLab 360

## 1. Instalação
```bash
pip install -r requirements.txt
```

## 2. Autenticação
- RelayLab 360 envia JWT token no header
- ProtecView valida e associa design ao user_id

## 3. Endpoints Disponíveis
...
```

---

## 📊 Timeline Consolidado

```
SEMANA 1-2: Fase 1 (CRÍTICA) - 16h
├─ Sprint 1.1: Bug Distribuição (6h)
├─ Sprint 1.2: CSS (3h)
└─ Sprint 1.3: Type Hints + Logging (7h)

SEMANA 3-4: Fase 2 (REFACTORING) - 15h
├─ Sprint 2.1: Distância Dinâmica (4h)
├─ Sprint 2.2: TC Curva (3h)
├─ Sprint 2.3: Validation (4h)
└─ Sprint 2.4: Cleanup (4h)

SEMANA 5-8: Fase 3 (INTEGRAÇÃO) - 28h
├─ Sprint 3.1: REST API (10h)
├─ Sprint 3.2: Modelos (5h)
├─ Sprint 3.3: Segurança (5h)
├─ Sprint 3.4: Testes (5h)
└─ Sprint 3.5: Docs (3h)

TOTAL: ~59h (~7-9 dias úteis)
```

---

## ✅ Checklist de Pré-Integração

Antes de integrar com RelayLab 360, validar:

- [ ] **Código**
  - [ ] Todos os 8 módulos funcionando
  - [ ] 70%+ test coverage
  - [ ] Type hints em 100% das funções públicas
  - [ ] Pylint score 8.0+

- [ ] **Segurança**
  - [ ] OWASP Top 10 validado
  - [ ] Input validation em 100% dos endpoints
  - [ ] Rate limiting ativo
  - [ ] JWT validation funcionando

- [ ] **Performance**
  - [ ] TCC plot < 500ms
  - [ ] API responses < 200ms
  - [ ] DB queries otimizadas

- [ ] **Documentação**
  - [ ] OpenAPI/Swagger completo
  - [ ] README atualizado
  - [ ] Docstrings em 100% das funções
  - [ ] Guia de integração para RelayLab

- [ ] **Dados**
  - [ ] Modelo de banco definido
  - [ ] Migrations testadas
  - [ ] Backup/restore procedimentos

---

## 🎯 Próximas Ações Imediatas (Esta Semana)

### 👤 Você (Augusto):

1. **Revisar** `ANALISE_PROJETO.md` completo
2. **Priorizar:** Qual fase começar primeiro?
   - Opção A: Corrigir bug (recomendado) → 6h
   - Opção B: Refatorar CSS → 3h
   - Opção C: Começar API (longo prazo) → 20h

3. **Setup inicial:**
   - [ ] Criar branch: `git checkout -b improve/critical-fixes`
   - [ ] Setup venv isolado para testes
   - [ ] Documentar decision log aqui

### 📝 Documentação Gerada:

Dois arquivos estão prontos em `ProtecView/`:
- **ANALISE_PROJETO.md** - Análise detalhada com arquitetura completa
- **PLANO_ACAO.md** - Este arquivo (ação imediata + sprints)

---

## 📞 Suporte

**Dúvidas sobre a análise?**
- Email: augustocesar.mariano@gmail.com
- Próxima revisão: Após completar Fase 1

**Versão:** 1.0  
**Data:** 2026-05-19  
**Status:** Ready for Implementation
