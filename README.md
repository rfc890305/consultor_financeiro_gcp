# Quantum Finance - Multi-Agent Financial Advisor

Sistema multiagente inteligente construído com o **Google Agent Development Kit (ADK)** e **Gemini**, projetado para atuar como um consultor financeiro automatizado, fornecendo desde conceitos educacionais até recomendações de alocação de carteira baseadas em dados reais da B3.

## 🏗️ Arquitetura e Fluxo dos Agentes

O sistema opera sob uma hierarquia de agentes gerenciada pelo agente raiz:

1. **`atendimento_quantum` (Root Agent)**
   - **Função:** Ponto de contato inicial com o cliente. Gerencia a recepção e direciona o fluxo com base na intenção do usuário.
   - **Ferramentas (`tools`):** Possui o `agente_pesquisador` encapsulado como ferramenta de função e utiliza o mecanismo nativo de `sub_agents` para transferência de contexto.

2. **`agente_pesquisador` (Sub-agente / Tool)**
   - **Função:** Focado em educação financeira. Explica conceitos de produtos (como CDB, Tesouro Direto, FIIs, Ações) de forma puramente didática e informativa.

3. **`agente_estrategista` (Lead Advisor)**
   - **Função:** Cérebro responsável por consolidar o perfil do investidor e gerar alocações de carteira personalizadas.
   - **Sub-agente vinculado:** `analista_tecnico`.

4. **`analista_tecnico` (Agente B3)**
   - **Função:** Especialista técnico focado em cotações e indicadores do mercado financeiro.
   - **Ferramenta (`tools`):** Utiliza a função `consultar_brapi_tool` para buscar dados de ativos e gerenciar o estado da sessão.

---

## 🛠️ Ferramentas (Tools) e Prompts Principais

* **`consultar_brapi_tool`:** 
  - *Descrição:* Busca dados de ativos da B3 e os armazena diretamente no `tool_context.state` para rastreabilidade ao longo da sessão.
* **Gatilho de Inicialização (`PROMPT_INICIAL_SISTEMA`):**
  - *Prompt do Root:* Aciona a saudação calorosa inicial e direciona o usuário a escolher entre aprender conceitos ou estruturar uma estratégia de investimentos informando seu perfil e capital.
