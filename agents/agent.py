import os
import logging
from typing import List
from dotenv import load_dotenv
import requests

# Importações do Google ADK
from google.adk import Agent
from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.models import Gemini
from google.adk.apps.app import App
from google.adk.tools import AgentTool
from google.genai import types
from google.adk.tools import TransferToAgentTool

load_dotenv()
logging.basicConfig(level=logging.INFO)

MODELO = os.getenv("MODEL", "gemini-3.5-flash-lite")
RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

# ==========================================
# 1. FERRAMENTAS (TOOLS)
# ==========================================

def consultar_bolsa_ai_tool(tool_context: ToolContext, ticker: str) -> dict:
    """Busca dados fundamentalistas de um ativo utilizando a API externa."""
    url = f"https://api.usebolsai.com/api/v1/fundamentals/{ticker.upper()}"
    headers = {"X-API-Key": os.getenv("BOLSA_AI_KEY")}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            return {"status": "success", "dados": dados}
        else:
            return {"status": "error", "mensagem": f"Erro HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "mensagem": str(e)}

# ==========================================
# 2. AGENTES ESPECIALISTAS (INTERNOS)
# ==========================================
analista_tecnico = Agent(
    name="analista_tecnico",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="Analisa cotações e indicadores técnicos do mercado financeiro.",
    instruction="""
    Você é o Agente de Dados B3. Sua única função é fornecer cotações atuais, indicadores fundamentalistas cruos e tendências de ativos da B3.
    Seja extremamente técnico, direto e focado em números. Nunca tente dar conselhos de investimento.

    DIRETRIZES DE COMPORTAMENTO: 
    1. SEMPRE TRAZER O VALOR DA AÇÃO, A DATA DE REFERÊNCIA E A FONTE PESQUISA.
    2. SEJA SUCINTO, MAS ENTREGUE UMA ANÁLISE DE TENDÊNCIA DA AÇÃO.
    3. Sua resposta será lida apenas por outro agente (Conselheiro de Risco). Nunca saúde o usuário.
    4. Utilize os dados do consultar_bolsa_ai_tool retornados em JSON usando as informações mais apropriadas.
    """,
    tools=[consultar_bolsa_ai_tool]
)

agente_pesquisador = Agent(
    name="agente_pesquisador",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="Responsável por buscar informações públicas para explicar conceitos e produtos (CDB, Tesouro Direto, FIIs).",
    instruction="""
    Você é o Market Analyst. Sua missão é explicar conceitos financeiros (como CDB, LCI, Tesouro Direto, FIIs, Ações) de forma puramente educacional e informativa.
    Forneça uma resposta rica em conteúdo conceitual, estruturada e limpa. Não faça saudações.
    Sua resposta será processada pelo EXCLUSIVAMENTE para o atendimento_quantum para formatação final. 
    """
)

# Encapsula o agente_pesquisador como ferramenta para o conselheiro
ferramenta_pesquisador = AgentTool(agent=agente_pesquisador)

agente_estrategista = Agent(
    name="agente_estrategista",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="O cérebro que consolida o perfil do cliente e os dados dos subagentes para gerar a recomendação final.",
    instruction="""
        Você é o Lead Advisor da Quantum Finance. Você assume o atendimento após o cliente detalhar o perfil dele.
        
        Sua missão é:
        1. Analisar o perfil do cliente recebido no histórico.
        2. Utilizar o 'analista_tecnico' (Agente B3) caso precise de dados de ações para fundamentar sua recomendação.
        3. Montar uma alocação de carteira detalhada e personalizada.
        4. Se necessário solicite mais informações.
        5. SE O CLIENTE QUISER APRENDER CONCEITOS transira para o atendimento_quantum

        TOM DE VOZ:

        1. Seja CORDIAL, EMPÁTICO e DIDÁDICO.
        2. Seja altamente profissional, estratégico e focado em gerar valor de longo prazo para o investidor.
    """,
    sub_agents=[analista_tecnico] # Ele pode consultar o analista_tecnico se precisar
)

# ==========================================
# 4. AGENTE RAIZ (ÚNICA INTERFACE COM O CLIENTE)
# ==========================================
system_prompt = """
Você é o consultor de recepção da Quantum Finance. Você é o ponto de contato inicial com o cliente.

REQUISITO 4 (DO CONTEXTO ANTERIOR): GATILHO DE INICIALIZAÇÃO
Se a entrada for exatamente "PROMPT_INICIAL_SISTEMA", você deve saudar calorosamente o cliente, 
se apresentar como Atendimento Quantum e perguntar se ele gostaria de aprender sobre algum produto financeiro 
ou se prefere criar uma estratégia personalizada de investimentos informando seu perfil e capital.

REGRAS DE DIRECIONAMENTO:
1. SE O CLIENTE QUISER APRENDER CONCEITOS (Ex: "O que é CDB?", "Como funcionam FIIs?"):
   Use IMEDIATAMENTE e SEMPRE a ferramenta 'agente_pesquisador'. Pegue a resposta técnica dele, 
   formate de maneira extremamente didática, simpática e amigável e entregue ao cliente.
   
2. SE O CLIENTE QUISER UMA RECOMENDAÇÃO / ESTRATÉGIA (Ex: "Tenho 50k e sou moderador, onde invisto?"):
   Assim que você identificar o perfil e o capital dele, utilize IMEDIATAMENTE a ferramenta 'transfer_to_agent' 
   (ou a ferramenta de transferência correspondente ao agente_estrategista) para delegar o atendimento.
"""

root_agent = Agent(
    name="atendimento_quantum",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="Recepciona o usuário, explica conceitos usando o pesquisador ou delega para o estrategista.",
    instruction=system_prompt,
    # Possui o pesquisador como ferramenta interna e o estrategista como destino de transferência
    tools=[ferramenta_pesquisador],
    sub_agents=[agente_estrategista], # Necessário declarar no ADK para permitir a transferência
    generate_content_config=types.GenerateContentConfig(temperature=0.2)
)

app = App(
    name="agents",
    root_agent=root_agent
)

# ==========================================
# TESTE DO FLUXO PROATIVO
# ==========================================
if __name__ == "__main__":
    print("--- Sistema Pronto ---")
    # Força o start inicial do atendimento_quantum
    resposta_boas_vindas = app.run(user_input="PROMPT_INICIAL_SISTEMA")
    print(f"Robô: {resposta_boas_vindas}")
