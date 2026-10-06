import pdfplumber
import re
import os

def extrair_secoes_bula(caminho_pdf):
    if not os.path.exists(caminho_pdf):
        return None

    texto_completo = ""
    
    # Lê todo o texto do PDF página por página
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"

    # Função auxiliar para recortar trechos entre títulos regulados pela Anvisa
    def extrair_trecho(titulo_inicio, titulo_fim):
        padrao = rf"{titulo_inicio}(.*?)(?={titulo_fim}|$)"
        resultado = re.search(padrao, texto_completo, re.DOTALL | re.IGNORECASE)
        if resultado:
            texto_limpo = re.sub(r'\s+', ' ', resultado.group(1)).strip()
            return texto_limpo
        return "Informação não especificada de forma clara nesta bula."

    # Secções obrigatórias baseadas no padrão da Anvisa
    como_usar = extrair_trecho(
        r"6\. COMO DEVO USAR ESTE MEDICAMENTO\?", 
        r"7\. O QUE DEVO FAZER QUANDO EU ME ESQUECER"
    )
    
    esquecimento = extrair_trecho(
        r"7\. O QUE DEVO FAZER QUANDO EU ME ESQUECER DE USAR ESTE MEDICAMENTO\?", 
        r"8\. QUAIS OS MALES QUE ESTE MEDICAMENTO PODE CAUSAR"
    )
    
    superdosagem = extrair_trecho(
        r"9\. O QUE FAZER SE ALGUÉM USAR UMA QUANTIDADE MAIOR DO QUE A INDICADA", 
        r"DIZERES LEGAIS"
    )

    return {
        "como_usar": como_usar,
        "esquecimento": esquecimento,
        "superdosagem": superdosagem
    }