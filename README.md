# ⚡ ProtecView: Ferramentas de Análise de Sistemas Elétricos

**ProtecView** é uma aplicação web interativa, construída em Python e Dash, que fornece um conjunto de ferramentas essenciais para engenheiros eletricistas e estudantes de sistemas de potência.

Esta aplicação permite a visualização e cálculo de fenómenos complexos de proteção e análise de sistemas elétricos diretamente no seu navegador.

---

## ⚠️ Disclaimer

Esta ferramenta foi desenvolvida por um engenheiro eletricista com o auxílio de inteligência artificial (Gemini). Os cálculos são baseados em fórmulas e tabelas padrão da indústria (IEC/IEEE), mas não devem ser usados para projetos de engenharia reais sem a validação de um profissional qualificado.

Caso seja identificado algum bug ou inconsistência, por favor, informe pelo email: [protecview@eletrogrid.com.br](mailto:protecview@eletrogrid.com.br).

---

## ✨ Funcionalidades

O ProtecView está agora organizado em oito módulos principais:

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
* **Cálculo de Faltas Assimétricas:** Calcula as magnitudes das correntes de falta Trifásica (3PH), Fase-Terra (LG) e Fase-Fase (LL).

### 4. Plotter de Curvas TCC (Sobrecorrente)
Plota e analisa a coordenação entre dois relés de sobrecorrente (ANSI 50/51) e inclui a análise de partida de motor.
* **Vasta Biblioteca de Curvas:** Permite a seleção de múltiplas curvas padrão **IEC** e **IEEE C37.112**.
* **Cálculo de CTI:** Calcula automaticamente o **Intervalo de Tempo de Coordenação (CTI)** para uma corrente de falta específica.
* **Análise de Partida de Motor:** Plota a curva de partida (Ip vs. ts) e a curva de suportabilidade térmica (I²t) de um motor no mesmo gráfico.

### 5. Dimensionamento Completo de Cabos
Verifica o dimensionamento de um cabo com base em três critérios essenciais.
* **Ampacidade:** Calcula a capacidade de corrente corrigida (temperatura, agrupamento).
* **Queda de Tensão (VD):** Calcula a queda de tensão percentual e em Volts.
* **Suportabilidade de Curto-Circuito (I²t):** Verifica se o cabo suporta a energia da falta.

### 6. Calculadora de Saturação de TC
Analisa se um Transformador de Corrente (TC) irá saturar durante uma falta, com base na fórmula ANSI/IEEE.
* **Análise Gráfica:** Plota a curva de capacidade do TC (Tensão de Kneepoint) e o ponto de operação requerido, mostrando visualmente se o TC satura.

### 7. Visualizador de Proteção Diferencial (87)
Plota a curva de restrição (slope) de um relé diferencial de transformador e permite a análise de pontos de teste.
* **Curva Multi-Slope:** Permite a definição de uma curva de 3 estágios (Pickup, Slope 1, Breakpoint, Slope 2, Pickup Não Restrito).
* **Análise de Pontos de Teste:** O utilizador pode inserir um ponto (Iop, Ir) para simular uma falta ou *inrush*, e a ferramenta indica se o ponto está na zona de "OPERAR" ou "BLOQUEAR".

### 8. Proteção de Distribuição (Fusíveis/Religadores)
Um módulo TCC focado em distribuição para coordenar dispositivos de média tensão.
* **Interface Dinâmica:** Permite ao utilizador adicionar/remover curvas de múltiplos dispositivos (Fusíveis e Religadores) no mesmo gráfico.
* **Curvas de Fusíveis:** Inclui as fórmulas para fusíveis padrão Tipo **K** e **T**.
* **Curvas de Religadores:** Permite a plotagem de sequências Rápida e Lenta usando as curvas IEC/IEEE.

---

## 🐞 Bugs Conhecidos e Próximas Atividades

* **Bug no Módulo de Distribuição:** O *callback* de plotagem do módulo "Proteção de Distribuição" (`callbacks_dist_protection.py` ) não está a conseguir ler os dados dos componentes dinâmicos (Fusível/Religador), fazendo com que o gráfico não seja plotado. **Esta é a nossa próxima prioridade a ser corrigida.**
* **Melhoria na Curva de Saturação de TC:** A plotagem da capacidade do TC no Módulo 6 é uma aproximação (linha horizontal). Um item futuro é plotar a curva de excitação senoidal completa.
* **Refatoração de Interfaces Dinâmicas:** Os módulos TCC (Módulo 4) e Zonas de Distância (Módulo 2) ainda usam interfaces estáticas (2 relés, 2 zonas). Um item futuro é refatorá-los para usar a mesma lógica dinâmica "Adicionar/Remover" que usámos no Módulo 8.

---

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal.
* **Dash (by Plotly):** O framework web para construir a interface e os callbacks.
* **Plotly:** Usado para criar todos os gráficos interativos.
* **Numpy:** Utilizado para todos os cálculos matemáticos e de números complexos.
* **Gunicorn:** O servidor web WSGI para executar a aplicação em produção.

---

## 🚀 Como Executar Localmente

(Instruções do teu `README.md` original)

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/TEU_UTILIZADOR/ProtecView.git](https://github.com/TEU_UTILIZADOR/ProtecView.git)
    cd ProtecView
    ```

2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python run.py
    ```

5.  Abra o seu navegador e visite `http://127.0.0.1:8050`.