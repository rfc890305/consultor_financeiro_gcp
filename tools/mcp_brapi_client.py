import json
import requests
import os

def consultar_dados_b3_mcp(ticker: str) -> str:
    """
    Consulta dados de ações da B3 através do provedor Brapi.
    
    Args:
        ticker: O código da ação na bolsa brasileira (ex: PETR4, BBDC4).
    """
    token = os.environ.get("BRAPI_TOKEN", "")
    url = f"https://brapi.dev/api/quote/{ticker}?fundamental=true&token={token}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            ativo = data["results"][0]
            # Seleciona apenas o que importa para a tomada de decisão do agente
            resultado = {
                "ticker": ativo.get("symbol"),
                "preco_atual": ativo.get("regularMarketPrice"),
                "p_l": ativo.get("priceEarnings", "N/A"),
                "dividend_yield": ativo.get("dividendsData", {}).get("yield", "N/A")
            }
            return json.dumps(resultado, indent=2)
        return json.dumps({"erro": f"Ticker {ticker} não encontrado."})
    except Exception as e:
        return json.dumps({"erro": str(e)})