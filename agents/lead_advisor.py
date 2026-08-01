import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from tools.mcp_brapi_client import consultar_dados_b3_mcp

# 1. Subagente B3
b3_data_agent = Agent(
    model='gemini-2.5-flash',
    name='b3_data_agent',
    description='Acionado para buscar preços de ações e indicadores fundamentalistas.',
    instruction='Sempre utilize a ferramenta consultar_dados_b3_mcp para buscar o ticker.',
    tools=[consultar_dados_b3_mcp]
)

# 2. Subagente Pesquisador
market_analyst = Agent(
    model='gemini-2.5-flash',
    name='market_analyst',
    description='Acionado para explicar conceitos como Selic, IPCA, FIIs e CDB.',
    instruction='Use a pesquisa web para obter o cenário macroeconômico atual.',
    tools=[google_search]
)

# 3. Agente Principal
lead_advisor = Agent(
    model='gemini-2.5-pro',
    name='lead_advisor',
    description='Consultor Financeiro Principal da Quantum Finance.',
    instruction='''Você é o Consultor Financeiro da Quantum Finance.
    Sua missão é rotear a pergunta do cliente para o b3_data_agent (se envolver ações) 
    ou para o market_analyst (se envolver conceitos e economia).
    Consolide a resposta de forma profissional.''',
    sub_agents=[b3_data_agent, market_analyst]
)