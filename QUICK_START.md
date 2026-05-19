# ⚡ Quick Start - ProtecView Development

**Preparado em:** 2026-05-19  
**Para:** Começar desenvolvimento imediatamente  
**Tempo estimado:** 30 minutos até primeira execução

---

## 🚀 Setup Ambiente (5 minutos)

### 1. Clonar e Entrar no Diretório
```bash
cd C:\Users\augus\Documentos\claude\ProtecView
```

### 2. Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt

# Verificar instalação
pip list | findstr "dash plotly numpy"
```

### 4. Executar Aplicação
```bash
python run.py
```

**Resultado esperado:**
```
Dash is running on http://127.0.0.1:8050/
```

Abra seu navegador: **http://127.0.0.1:8050**

---

## 📊 Validar Instalação

### Testes Rápidos (5 minutos)

```bash
# 1. Verificar Python
python --version
# Expected: Python 3.x

# 2. Verificar dependências críticas
python -c "import dash; import plotly; import numpy; print('✅ All OK')"

# 3. Verificar estrutura do projeto
python -c "from app import app; from layouts import *; print('✅ Imports OK')"
```

### Teste Manual da Aplicação (10 minutos)

No navegador (http://127.0.0.1:8050):

- [ ] Home tab carrega
- [ ] Logo aparece no topo
- [ ] Theme toggle funciona (claro/escuro)
- [ ] Abrir aba "Componentes Simétricos" → calcular → gráfico aparecer
- [ ] Abrir aba "Proteção de Distribuição" → **esperado:** NÃO funciona (bug conhecido)

---

## 🔧 Git Setup para Desenvolvimento

### 1. Criar Branch de Desenvolvimento
```bash
# Criar branch para Fase 1
git checkout -b improve/phase-1-critical-fixes

# Verificar status
git status
```

### 2. Commit Padrão (Semantic Commit)
```bash
# Template para commits
git commit -m "fix: description of what was fixed

- Detailed explanation of the fix
- Why this was necessary
- Testing done
"

# Exemplo real:
git commit -m "fix: resolve dist_protection callback data mapping

- Refactor State(... ALL) pattern to properly map fuse/recloser IDs
- Add robust ID-to-value mapping for dynamic components
- Add validation and error handling for missing values
- Tested with 3 fuses and 2 reclosers
"
```

### 3. Ver Histórico
```bash
git log --oneline -10
git log --graph --oneline --all
```

---

## 🐛 Debug & Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'dash'"

**Solução:**
```bash
# Verificar venv ativado
pip list | findstr dash
# Se vazio, instalar:
pip install -r requirements.txt
```

### Problema: "Port 8050 already in use"

**Solução:**
```bash
# Opção 1: Matar processo na porta 8050
# Windows
netstat -ano | findstr :8050
taskkill /PID <PID> /F

# Option 2: Usar porta diferente em run.py
# Mudar app.run(debug=False) para:
app.run(debug=False, port=8051)
```

### Problema: "Graphs not displaying"

**Solução:**
```bash
# Verificar assets foram carregados
# No navegador: F12 → Console
# Procurar por erros de CSS

# Limpar cache
# CTRL+SHIFT+R (hard refresh)
```

### Problema: "CSS looks weird (colors wrong)"

**Solução:**
```bash
# Check if both CSS files carregados (style.css + custom_styles.css)
# Solução: consolidar em um único CSS
# Ver PLANO_ACAO.md Sprint 1.2
```

---

## 🧪 Testes Básicos (Para Depois)

### Rodar Tests (quando implementado)
```bash
# Instalar pytest
pip install pytest pytest-cov

# Rodar testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=utils --cov-report=html
# Abrir htmlcov/index.html no navegador
```

---

## 📝 Estrutura de Pastas Importante

```
ProtecView/
├── app.py                          # Inicialização (não mexer)
├── run.py                          # Entry point
├── layouts.py                      # Estrutura HTML das 8 abas
├── callbacks/                      # Lógica de cada módulo
│   ├── callbacks_sym.py
│   ├── callbacks_dist.py
│   ├── callbacks_tcc.py
│   ├── callbacks_fault.py
│   ├── callbacks_amp.py
│   ├── callbacks_ct.py
│   ├── callbacks_diff.py
│   ├── callbacks_inrush.py
│   └── callbacks_dist_protection.py    # ⚠️ AQUI ESTÁ O BUG
├── utils/                          # Cálculos matemáticos
│   ├── utils_common.py
│   ├── utils_sym.py
│   ├── utils_tcc.py
│   ├── utils_dist_protection.py    # Fusíveis/Religadores
│   └── ...
├── assets/                         # CSS, imagens
│   ├── style.css                   # Theme claro/escuro
│   ├── custom_styles.css           # Estilos customizados
│   └── logo_protecview.png
└── requirements.txt                # Dependências
```

---

## 🎯 Próximos Passos por Fase

### Se Começando Fase 1 (Sprint 1.1 - Bug Distribuição)

```bash
# 1. Branch criado ✓
git checkout improve/phase-1-critical-fixes

# 2. Abrir arquivo com bug
# Arquivo: callbacks/callbacks_dist_protection.py

# 3. Navegar para o callback problem:
# Função: plot_dist_tcc_graph (linha ~158)

# 4. Adicionar debug logs:
# print(f"DEBUG: fuse_types_val = {fuse_types_val}")
# print(f"DEBUG: storage_json = {storage_json}")

# 5. Testar:
python run.py
# → Adicionar fusível no UI
# → Ver logs no terminal
# → Identificar onde listas estão vazias

# 6. Implementar fix:
# Ver PLANO_ACAO.md "Passo 2: Refatorar mapeamento"

# 7. Commit:
git commit -m "fix: resolve dist_protection..."

# 8. Próxima sprint:
git checkout -b improve/phase-1-css-consolidation
```

### Se Apenas Lendo Código

```bash
# Explorar callbacks de um módulo OK
vim callbacks/callbacks_tcc.py

# Comparar com módulo bugado
vim callbacks/callbacks_dist_protection.py

# Ver diferenças
git diff callbacks/callbacks_tcc.py callbacks/callbacks_dist_protection.py
```

---

## 🔍 Inspect Rápido do Código

### Ver Imports de um Callback
```bash
# Exemplo: Simétricos
grep -n "^import\|^from" callbacks/callbacks_sym.py
```

### Ver Estrutura de um Arquivo
```bash
# Ver todas as funções
grep -n "^def\|^class" callbacks/callbacks_tcc.py
```

### Procurar por TODO/FIXME
```bash
grep -r "TODO\|FIXME\|BUG\|XXX" .
```

---

## 📊 Verificar Status do Projeto

### Check Rápido de Saúde
```bash
# 1. Listar arquivos Python
find . -name "*.py" | wc -l
# Expected: ~15-20 arquivos

# 2. Contar linhas de código
wc -l **/*.py
# Expected: ~3000-4000 linhas

# 3. Ver estrutura de módulos
ls -la callbacks/
ls -la utils/
```

### Ver Estado do Git
```bash
git status
git log --oneline -5
git branch -a
```

---

## 💡 Dicas de Desenvolvimento

### Debug no Navegador (F12 Console)

```javascript
// Verificar se Dash carregou
console.log(window._dash_is_loading)

// Verificar erros de CSS
document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
  console.log(`CSS: ${link.href}`)
})

// Chamar callbacks manualmente (teste)
// Depende da estrutura Dash
```

### Debug no VS Code

Arquivo `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Dash",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/run.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

Depois: F5 para debug com breakpoints

---

## 🔗 Links Úteis

### Documentação Oficial
- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Python Graphs](https://plotly.com/python/)
- [NumPy Docs](https://numpy.org/doc/)

### Este Projeto
- [LEIA_PRIMEIRO.md](./LEIA_PRIMEIRO.md) - Guia de documentação
- [RESUMO_EXECUTIVO.md](./RESUMO_EXECUTIVO.md) - Status visual
- [PLANO_ACAO.md](./PLANO_ACAO.md) - Plano de sprints
- [ANALISE_PROJETO.md](./ANALISE_PROJETO.md) - Deep dive técnico

---

## 📋 Checklist Setup

- [ ] Clone do repositório (`git clone` ou já está?)
- [ ] Venv criado (`python -m venv venv`)
- [ ] Venv ativado (`. venv/Scripts/activate` no Windows)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Aplicação rodando (`python run.py`)
- [ ] Navegador aberto (`http://127.0.0.1:8050`)
- [ ] Home page carrega
- [ ] Um módulo testado (ex: Simétricos)
- [ ] Branch criado (`git checkout -b improve/...`)
- [ ] Pronto para começar!

---

## ⚡ Comando Único para Começar

### Windows PowerShell
```powershell
# Setup completo em um comando
python -m venv venv; `
.\venv\Scripts\activate; `
pip install -r requirements.txt; `
python run.py
```

### Linux/Mac
```bash
# Setup completo em um comando
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python run.py
```

---

## 🆘 Suporte

Se ficar preso:

1. **Verificar este arquivo:** Seção "Debug & Troubleshooting"
2. **Verificar LEIA_PRIMEIRO.md:** Qual documentação ler
3. **Verificar ANALISE_PROJETO.md:** Seção "Arquitetura"
4. **Google:** "Dash Plotly [seu erro]"
5. **Stack Overflow:** Tag `plotly-dash`

---

## 📞 Contato

**Email:** augustocesar.mariano@gmail.com  
**Projeto:** ProtecView (ProtecView)  
**Status:** Ready for Development

---

## 🎬 Comece Agora!

```bash
# 1. Ativar venv
.\venv\Scripts\activate

# 2. Rodar app
python run.py

# 3. Abrir navegador
# http://127.0.0.1:8050

# 4. Testar módulo OK (Simétricos)
# → Entrar na aba "Componentes Simétricos"
# → Clicar "Calcular Componentes"
# → Ver gráfico aparecer ✅

# 5. Confirmar bug (Distribuição)
# → Entrar na aba "Proteção de Distribuição"
# → Clicar "Plotar Gráfico"
# → Nada acontece ❌ (esperado)

# 6. Ler documentação
# → LEIA_PRIMEIRO.md
# → PLANO_ACAO.md

# 7. Começar Fase 1
# → git checkout -b improve/phase-1-critical-fixes
# → Implementar fix em callbacks_dist_protection.py
```

---

**Versão:** 1.0  
**Status:** ✅ Ready  
**Próxima etapa:** python run.py

Boa sorte! 🚀
