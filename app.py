import streamlit as st
import asyncio
from agents.lead_advisor import lead_advisor

# Configuração da página Web
st.set_page_config(page_title="Quantum Finance - IA", page_icon="📈")
st.title("🤖 Consultor Multiagente - Quantum Finance")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra o histórico na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de input do usuário
if prompt := st.chat_input("Ex: Como está BBDC4? Qual a diferença para um CDB?"):
    
    # 1. Adiciona a pergunta do usuário na tela
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Prepara a resposta do assistente
    with st.chat_message("assistant"):
        # EVIDÊNCIA DE EXECUÇÃO: Mostra visualmente que os agentes estão trabalhando
        with st.status("🧠 Orquestrando agentes...", expanded=True) as status:
            st.write("🕵️‍♂️ **Lead Advisor** analisando a intenção...")
            st.write("🔄 Acionando subagentes (B3 Data / Market Analyst)...")
            
            # Função assíncrona para rodar o ADK
            async def get_agent_response():
                respostas = []
                # O ADK cuida do roteamento internamente
                async for evento in lead_advisor.run(ctx=None, node_input=prompt):
                    if evento.output:
                        respostas.append(str(evento.output))
                return "\n".join(respostas)
            
            # Executa o loop assíncrono
            resposta_final = asyncio.run(get_agent_response())
            
            status.update(label="✅ Análise concluída!", state="complete", expanded=False)
        
        # 3. Mostra a resposta consolidada
        st.markdown(resposta_final)
        st.session_state.messages.append({"role": "assistant", "content": resposta_final})