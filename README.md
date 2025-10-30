# ⚡ ProtecView: Ferramentas de Análise de Sistemas Elétricos

**ProtecView** é uma aplicação web interativa, construída em Python e Dash, que fornece um conjunto de ferramentas essenciais para engenheiros eletricistas e estudantes de sistemas de potência.

Esta aplicação permite a visualização e cálculo de fenómenos complexos de proteção e análise de sistemas elétricos diretamente no seu navegador.

---

## ✨ Funcionalidades

O ProtecView está organizado em três módulos principais:

### 1. Calculador de Componentes Simétricos
Converte fasores de fase (A, B, C) desequilibrados nos seus componentes simétricos (Sequência Zero, Positiva e Negativa).
* Entrada de magnitude e ângulo para as Fases A, B e C.
* Cálculo imediato dos componentes de sequência 0, 1 e 2.
* Visualização dupla de fasores: um gráfico polar para os componentes de fase e outro para os componentes simétricos.

### 2. Visualizador de Zonas de Proteção de Distância
Plota círculos Mho para zonas de proteção de distância (ANSI 21) num diagrama R-X (Resistência vs. Reatância).
* Entrada de impedância e ângulo para a linha.
* Definição da magnitude e ângulo para múltiplas zonas de proteção (ex: Zona 1, Zona 2).
* Visualização clara da linha e das zonas de operação no plano de impedância.

### 3. Plotter de Curvas TCC (Tempo-Corrente)
Plota e analisa a coordenação entre dois relés de sobrecorrente (ANSI 50/51).
* Configuração de dois relés (Montante e Jusante).
* Seleção do tipo de curva (ex: IEC Standard Inverse, Very Inverse).
* Definição de Pickup (Partida) e Time Dial (TDS) para cada relé.
* Cálculo do **Intervalo de Tempo de Coordenação (CTI)** para uma corrente de falta específica.

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
    git clone [https://github.com/marianoaugusto93/ProtecView.git](https://github.com/marianoaugusto93/ProtecView.git)
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

4.  **Execute a aplicação com o Gunicorn:**
    ```bash
    gunicorn run:server
    ```

5.  Abra o seu navegador e visite `http://127.0.0.1:8000`.