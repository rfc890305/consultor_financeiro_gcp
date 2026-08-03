# Quantum Finance - Multi-Agent Financial Advisor

Sistema multiagente inteligente construído com o **Google Agent Development Kit (ADK)** e **Gemini**, projetado para atuar como um consultor financeiro automatizado, fornecendo desde conceitos educacionais até recomendações de alocação de carteira baseadas em dados reais da B3 via integração com a **BolsaAI**.

## 🏗️ Arquitetura e Hierarquia dos Agentes

O sistema opera sob uma estrutura hierárquica baseada em um Agente Raiz e subagentes especializados:

1. **`atendimento_quantum` (Root Agent)**
   - **Função:** Ponto de contato exclusivo com o usuário final. Gerencia o gatilho de inicialização (`PROMPT_INICIAL_SISTEMA`) e decide o roteamento inicial.
   - **Ferramentas (`tools`):** Possui a `ferramenta_pesquisador` (`AgentTool` encapsulando o `agente_pesquisador`).
   - **Sub-agentes (`sub_agents`):** `agente_estrategista`.

2. **`agente_pesquisador` (Market Analyst)**
   - **Função:** Focado em educação financeira de forma puramente didática, explicando conceitos de produtos (como CDB, LCI, Tesouro Direto, FIIs e Ações).
   - **Encapsulamento:** Utilizado diretamente como uma ferramenta (`ferramenta_pesquisador`) pelo agente raiz.

3. **`agente_estrategista` (Lead Advisor)**
   - **Função:** Cérebro responsável por consolidar o perfil do cliente e gerar alocações de carteira personalizadas.
   - **Sub-agentes:** Possui o `analista_tecnico` vinculado na árvore de execução.

4. **`analista_tecnico` (Agente de Dados B3)**
   - **Função:** Especialista técnico focado em extrair cotações atuais, indicadores fundamentalistas e tendências de ativos.
   - **Ferramentas (`tools`):** Utiliza nativamente a ferramenta `consultar_bolsa_ai_tool`.

---

## 🛠️ Ferramentas (Tools) e Integrações

* **`consultar_bolsa_ai_tool`:** 
  - *Descrição:* Realiza uma requisição HTTP `GET` autenticada via header (`X-API-Key`) na API externa da **BolsaAI** (`https://api.usebolsai.com/api/v1/fundamentals/{ticker}`).
  - *Retorno:* Retorna um dicionário contendo o status da requisição e os dados fundamentalistas estruturados em formato JSON para interpretação técnica do `analista_tecnico`.
* **`ferramenta_pesquisador` (`AgentTool`):**
  - *Descrição:* Permite que o agente raiz invoque o `agente_pesquisador` como uma função interna para lidar com dúvidas conceituais dos usuários.

---

## 🚀 Fluxo de Execução

1. **Iniciação:** O sistema é acionado através da entrada controlada `PROMPT_INICIAL_SISTEMA`, gerando a saudação institucional do `atendimento_quantum`.
2. **Roteamento:** 
   - Se o usuário busca **aprendizado/conceitos**, o agente raiz aciona o `agente_pesquisador`.
   - Se o usuário busca **recomendações/estratégias de investimento**, o fluxo é direcionado para o `agente_estrategista`, que por sua vez consulta o `analista_tecnico` e a API da BolsaAI caso precise de dados concretos da B3.
