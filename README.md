# ⚡ ProtecView: Ferramentas de Análise de Sistemas Elétricos

**ProtecView** é uma aplicação web interativa, construída em Python e Dash, que fornece um conjunto de ferramentas essenciais para engenheiros eletricistas e estudantes de sistemas de potência.

Esta aplicação permite a visualização e cálculo de fenómenos complexos de proteção e análise de sistemas elétricos diretamente no seu navegador.

---

## ⚠️ Disclaimer

Esta ferramenta foi desenvolvida por um engenheiro eletricista com o auxílio de inteligência artificial (Gemini) para fins educacionais e de demonstração. Os cálculos são baseados em fórmulas e tabelas padrão da indústria (IEC/IEEE), mas não devem ser usados para projetos de engenharia reais sem a validação de um profissional qualificado.

Caso seja identificado algum bug ou inconsistência, por favor, informe pelo email: [protecview@eletrogrid.com.br](mailto:protecview@eletrogrid.com.br).

---

## ✨ Funcionalidades

O ProtecView está agora organizado em sete módulos principais:

### 1. Calculador de Componentes Simétricos
Converte fasores de tensão ou corrente entre os domínios de Fase (A, B, C) e de Sequência (0, 1, 2).
* **Conversão Bi-direcional:** Permite a escolha do sentido (Fase $\rightarrow$ Simétrico ou Simétrico $\rightarrow$ Fase).
* **Visualização Dupla:** Plota gráficos polares interativos para os fasores de entrada e de saída.

### 2. Visualizador de Zonas de Proteção de Distância
Plota e visualiza as zonas de operação para relés de distância (ANSI 21) num diagrama R-X (Resistência vs. Reatância).
* **Múltiplos Tipos de Zona:** Suporta a plotagem de círculos **Mho** e zonas **Quadrilaterais**.
* **Configuração de Múltiplas Zonas:** Permite a configuração de duas zonas fixas (Zona 1 e Zona 2).

### 3. Calculadora de Curto-Circuito
Calcula as correntes de falta (em p.u.) num ponto do sistema, com base nas suas impedâncias de sequência.
* **Entradas de Impedância:** Permite a entrada das impedâncias Z1 (Positiva), Z2 (Negativa) e Z0 (Zero).
* **Cálculo de Faltas Assimétricas:** Calcula as magnitudes das correntes de falta Trifásica (3PH), Fase-Terra (LG) e Fase-Fase (LL).

### 4. Plotter de Curvas TCC (Tempo-Corrente)
Plota e analisa a coordenação entre dois relés de sobrecorrente (ANSI 50/51) num gráfico log-log.
* **Vasta Biblioteca de Curvas:** Permite a seleção de múltiplas curvas padrão **IEC** e **IEEE C37.112**.
* **Cálculo de CTI:** Calcula automaticamente o **Intervalo de Tempo de Coordenação (CTI)** para uma corrente de falta específica.

### 5. Calculadora de Ampacidade de Cabos
Calcula a capacidade de condução de corrente de um cabo com base em fatores de correção de normas (ex: IEC 60364-5-52).
* **Entradas:** Corrente nominal base, Tipo de isolamento (PVC/XLPE), Temperatura ambiente e Método de instalação (Agrupamento).
* **Saídas:** Fatores de correção e a ampacidade final corrigida.

### 6. Calculadora de Saturação de TC
Analisa se um Transformador de Corrente (TC) irá saturar durante uma falta, com base na fórmula ANSI/IEEE.
* **Entradas:** Corrente de falta (do Módulo 4), Relação X/R, Rácio do TC, Classe de Saturação (ex: C400) e Burden (Rct + Rb).
* **Análise Gráfica:** Plota a curva de capacidade do TC (Tensão de Kneepoint) e o ponto de operação requerido, mostrando visualmente se o TC satura.

### 7. Visualizador de Proteção Diferencial (87)
Plota a curva de restrição (slope) de um relé diferencial de transformador e permite a análise de pontos de operação.
* **Curva Multi-Slope:** Permite a definição de uma curva de 3 estágios (Pickup, Slope 1, Breakpoint, Slope 2, Pickup Não Restrito).
* **Análise de Pontos de Teste:** O utilizador pode inserir um ponto (Iop, Ir) para simular uma falta ou *inrush*, e a ferramenta indica se o ponto está na zona de "OPERAR" ou "BLOQUEAR".

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
    (O Gunicorn é para o *deploy* em servidores Linux. Para executar localmente, use o servidor de desenvolvimento do Dash)
    ```bash
    python run.py
    ```

5.  **Abra o seu navegador** e visite `http://127.0.0.1:8050`.

---

## 🔮 Próximas Funções (Roadmap)

Temos um plano robusto para adicionar novas funcionalidades e melhorias ao ProtecView:

#### 1. Módulos de Proteção de Distribuição (Média Tensão)
* **Coordenação de Fusíveis e Religadores:** Um novo módulo TCC focado em distribuição, permitindo ao utilizador adicionar curvas de fusíveis (Tipo K, T) e sequências de religadores (ex: 2 rápidas + 2 lentas) para coordenar a proteção de alimentadores.

#### 2. Módulos de Análise de Equipamentos
* **Análise de Partida de Motor:** Plotar a curva de corrente e suportabilidade térmica de um motor no gráfico TCC para coordenar a sua proteção (sobrecarga e curto-circuito).
* **Cálculo de Corrente de *Inrush***: Calcular a corrente de magnetização de transformadores e plotá-la como um ponto de teste no módulo Diferencial (87).
* **Dimensionamento Completo de Cabos (VD e $I^2t$):** Expandir o módulo de Ampacidade para incluir cálculos de Queda de Tensão ($V_d$) e Suportabilidade Térmica ($I^2t$) a curto-circuito, usando dados dos módulos de Faltas e TCC.

#### 3. Melhorias nos Módulos Existentes
* **Interface Dinâmica (Adicionar/Remover):** Refatorar os módulos de TCC e Zonas de Distância para permitir que o utilizador adicione um número ilimitado de curvas ou zonas dinamicamente.
* **Análise de Curto-Circuito Assimétrico:** Calcular a corrente de pico assimétrica ($i_p$) e a componente DC, com base na relação X/R, para uma análise de saturação de TC mais precisa.
* **Curva de Saturação de TC (Senoidal):** Substituir a linha de *kneepoint* por uma plotagem da curva de excitação (senoidal) completa do TC.

#### 4. Módulos Educacionais
* **Visualizador de Lógica de Proteção:** Uma ferramenta para construir esquemas lógicos (Portas E/OU, Temporizadores) para simular a lógica de trip de um relé.