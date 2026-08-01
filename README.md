# Consultor Financeiro Multiagente (GCP) 📈

MVP do sistema de IA Agêntica para recomendação financeira da Quantum Finance, construído com Google Agent Development Kit (ADK) e interface em Streamlit.

## 🎯 Requisitos Atendidos
1. **Interface Web:** Implementada via Streamlit.
2. **Documentação:** Código modularizado e amplamente comentado.
3. **Evidência de Execução:** A interface utiliza `st.status` para expor visualmente quando o orquestrador aciona os subagentes de pesquisa web e de dados B3.
4. **Viabilidade Técnica (GCP):** Aplicação encapsulada via Docker para implantação serverless no Google Cloud Run.

## 🚀 Como fazer o Deploy no Google Cloud Platform (GCP)

Siga este passo a passo usando o terminal do **Google Cloud Shell** (diretamente no portal do GCP).

### Passo 1: Clone e Configuração
1. Abra o Cloud Shell no GCP.
2. Clone seu repositório:
   ```bash
   git clone [https://github.com/rfc890305/estudos-alura.git](https://github.com/rfc890305/estudos-alura.git)
   cd estudos-alura/consultor_financeiro_gcp