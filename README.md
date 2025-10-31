# ⚡ ProtecView: Ferramentas de Análise de Sistemas Elétricos

**ProtecView** é uma aplicação web interativa, construída em Python e Dash, que fornece um conjunto de ferramentas essenciais para engenheiros eletricistas e estudantes de sistemas de potência.

Esta aplicação permite a visualização e cálculo de fenómenos complexos de proteção e análise de sistemas elétricos diretamente no seu navegador.

---

## ✨ Funcionalidades

O ProtecView está organizado em quatro módulos principais:

### 1. Calculador de Componentes Simétricos
Converte fasores de tensão ou corrente entre os domínios de Fase (A, B, C) e de Sequência (0, 1, 2).
* **Conversão Bi-direcional:** Permite a escolha do sentido (Fase $\rightarrow$ Simétrico ou Simétrico $\rightarrow$ Fase).
* **Visualização Dupla:** Plota gráficos polares interativos para os fasores de entrada e de saída.

### 2. Visualizador de Zonas de Proteção de Distância
Plota e visualiza as zonas de operação para relés de distância (ANSI 21) num diagrama R-X (Resistência vs. Reatância).
* **Múltiplos Tipos de Zona:** Suporta a plotagem de círculos **Mho** (definidos por Magnitude/Ângulo) e zonas **Quadrilaterais** (definidas por Alcance X/R).
* **Configuração de Múltiplas Zonas:** Permite a configuração de duas zonas fixas (Zona 1 e Zona 2) para análise de sobreposição e alcance.

### 3. Calculadora de Curto-Circuito
Calcula as correntes de falta (em p.u.) num determinado ponto do sistema, com base nas suas impedâncias de sequência.
* **Entradas de Impedância:** Permite a entrada das impedâncias de sequência Positiva (Z1), Negativa (Z2) e Zero (Z0) em formato polar.
* **Cálculo de Faltas Assimétricas:** Calcula as magnitudes das correntes de falta Trifásica (3PH), Fase-Terra (LG) e Fase-Fase (LL).

### 4. Plotter de Curvas TCC (Tempo-Corrente)
Plota e analisa a coordenação entre dois relés de sobrecorrente (ANSI 50/51) num gráfico log-log.
* **Vasta Biblioteca de Curvas:** Permite a seleção de múltiplas curvas padrão **IEC** (Standard Inverse, Very Inverse, Extremely Inverse) e **IEEE C37.112** (Moderately Inverse, Very Inverse, Extremely Inverse).
* **Cálculo de CTI:** Calcula automaticamente o **Intervalo de Tempo de Coordenação (CTI)** entre os dois dispositivos para uma corrente de falta específica.

---

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal.
* **Dash (by Plotly):** O framework web para construir a interface e os callbacks.
* **Plotly:** Usado para criar todos os gráficos interativos (polares, cartesianos e log-log).
* **Numpy:** Utilizado para todos os cálculos matemáticos e de números complexos.
* **Gunicorn:** O servidor web WSGI para executar a aplicação em produção.

---

## 🚀 Como Executar Localmente

Para executar este projeto na sua própria máquina, siga estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/TEU_UTILIZADOR/ProtecView.git](https://github.com/TEU_UTILIZADOR/ProtecView.git)
    cd ProtecView
    ```

2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    ```
    *No Windows:*
    ```bash
    .\venv\Scripts\activate
    ```
    *No macOS/Linux:*
    ```bash
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    (O Gunicorn é para o *deploy* em servidores Linux. Para executar localmente no Windows ou macOS, use o servidor de desenvolvimento do Dash)
    ```bash
    python run.py
    ```

5.  Abra o seu navegador e visite `http://127.0.0.1:8050`.

---

## 🔮 Próximas Funções (Roadmap)

Temos um plano robusto para adicionar novas funcionalidades e tornar o ProtecView ainda mais completo:

* **Curvas TCC Dinâmicas (Adicionar/Remover Curva):**
    Permitir que o utilizador plote um número ilimitado de curvas (Relé 1, Relé 2, Fusível, Relé 3...) no mesmo gráfico para uma coordenação complexa.

* **Zonas de Distância Dinâmicas (Adicionar/Remover Zona):**
    Permitir que o utilizador adicione e remova um número ilimitado de zonas (Z1, Z2, Z3, Z4, Reversa) no mesmo diagrama R-X.

* **Calculadora de Saturação de TC (Transformador de Corrente):**
    Um novo módulo para analisar a saturação de TCs (ANSI C57.13). O utilizador inseriria os dados do TC (Rácio, Classe, Burden) e a corrente de falta (do Módulo 4!), e a ferramenta calcularia se o TC irá saturar e distorcer a medição.

* **Módulo de Proteção Diferencial (ANSI 87):**
    Uma ferramenta para visualizar a proteção diferencial de transformadores, incluindo a plotagem da curva de restrição (slope) e a análise de operação vs. restrição para faltas internas e externas.

* **Dimensionamento de Cabos (Ampacidade):**
    Um utilitário para calcular a ampacidade (capacidade de corrente) de cabos com base no tipo de isolamento, método de instalação e temperatura, seguindo normas (IEC ou NBR).