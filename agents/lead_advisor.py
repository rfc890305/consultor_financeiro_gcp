import os
import logging
from typing import List
from dotenv import load_dotenv

# Importações do Google ADK
from google.adk import Agent
from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.models import Gemini
from google.adk.apps.app import App
from google.genai import types

load_dotenv()
logging.basicConfig(level=logging.INFO)

MODELO = os.getenv("MODEL", "gemini-2.5-pro")
RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

# ==========================================
# 1. FERRAMENTAS (TOOLS)
# ==========================================
def consultar_brapi_tool(
    tool_context: ToolContext, 
    ticket: str,
    analise: str
) -> dict[str, str]:
    """Busca dados de um ativo e salva no estado da sessão."""
    estado_atual = tool_context.state.get("dados_b3", [])
    tool_context.state["dados_b3"] = estado_atual + [f"Ativo {ticket}: {analise}"]
    logging.info(f"[Ferramenta] Dados salvos para {ticket}")
    return {"status": "success"}

# ==========================================
# 2. AGENTES ESPECIALISTAS
# ==========================================
analista_tecnico = Agent(
    name="analista_tecnico",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="Analisa cotações e indicadores técnicos do mercado financeiro.",
    instruction="""
    INSTRUÇÕES:
    Use sua ferramenta 'consultar_brapi_tool' para buscar dados do ativo solicitado.
    
    DADOS B3 ATUAIS:
    { dados_b3? } 
    """,
    tools=[consultar_brapi_tool]
)

analista_noticias = Agent(
    name="analista_noticias",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="Analisa o sentimento do mercado e notícias recentes.",
    instruction="""
    INSTRUÇÕES:
    Crie um relatório de sentimento de mercado sobre o ativo que o usuário deseja analisar.
    """,
    output_key="relatorio_mercado"
)

conselheiro_risco = Agent(
    name="conselheiro_risco",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="Consolida os relatórios e emite o parecer final.",
    instruction="""
    INSTRUÇÕES:
    Com base nos dados técnicos e no relatório de mercado, construa sua recomendação de investimento final.
    
    DADOS TÉCNICOS:
    { dados_b3? }
    
    RELATÓRIO DE MERCADO:
    { relatorio_mercado? }
    """
)

# ==========================================
# 3. WORKFLOWS (FLUXOS DE TRABALHO)
# ==========================================
equipe_pesquisa = ParallelAgent(
    name="equipe_pesquisa",
    sub_agents=[analista_tecnico, analista_noticias]
)

fluxo_consultoria = SequentialAgent(
    name="fluxo_consultoria",
    description="Fluxo completo de análise e recomendação.",
    sub_agents=[equipe_pesquisa, conselheiro_risco]
)

# ==========================================
# 4. AGENTE RAIZ E APLICATIVO
# ==========================================
root_agent = Agent(
    name="atendimento_quantum",
    model=Gemini(model=MODELO, retry_options=RETRY_OPTIONS),
    description="Recepciona o usuário e inicia a consultoria da Quantum Finance.",
    instruction="""
    INSTRUÇÕES:
    - Dê as boas-vindas à Quantum Finance.
    - Pergunte qual ação (ticket da B3) o usuário deseja analisar.
    - Quando ele responder, transfira o controle para a 'fluxo_consultoria'.
    """,
    sub_agents=[fluxo_consultoria]
)

app = App(
    name="consultor_financeiro_ai",
    root_agent=root_agent
)
