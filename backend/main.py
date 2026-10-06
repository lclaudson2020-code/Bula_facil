from fastapi import FastAPI, HTTPException
import sqlite3
import os
import re
from backend.servicos.extrator_bula import extrair_secoes_bula

# 1. Inicializa o FastAPI no topo do ficheiro
app = FastAPI(title="Bula Fácil API", version="0.3")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bula_facil.db")
BULAS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bulas")

def limpar_nome_para_arquivo(nome: str) -> str:
    """Converte o nome do medicamento num formato seguro para nome de arquivo (ex: 'NEOSALDINA' -> 'neosaldina')"""
    if not nome:
        return ""
    # Remove acentos, caracteres especiais e espaços extras
    nome_limpo = nome.lower().strip()
    nome_limpo = re.sub(r'[^a-z0-9]', '_', nome_limpo)
    return nome_limpo

@app.get("/")
def home():
    return {"mensagem": "API do Bula Fácil rodando com sucesso! 🚀"}

@app.get("/medicamentos/{nome}")
def buscar_medicamento(nome: str):
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM medicamentos 
        WHERE nome LIKE ? OR principio_ativo LIKE ?
        LIMIT 1
    """, (f"%{nome}%", f"%{nome}%"))
    
    registro = cursor.fetchone()
    conexao.close()

    if not registro:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado na base da Anvisa.")

    medicamento_info = dict(registro)
    nome_medicamento = medicamento_info.get("nome", "")
    
    # Gera o nome esperado do arquivo PDF com base no nome do medicamento (ex: neosaldina.pdf)
    nome_arquivo_pdf = f"{limpar_nome_para_arquivo(nome_medicamento)}.pdf"
    caminho_pdf = os.path.join(BULAS_PATH, nome_arquivo_pdf)

    dados_bula = {
        "tipo": "Bula não cadastrada localmente",
        "como_usar": "Indisponível no momento",
        "esquecimento": "Indisponível no momento",
        "superdosagem": "Indisponível no momento"
    }

    # Verifica estritamente se o PDF correspondente a ESTE medicamento existe
    if os.path.exists(caminho_pdf):
        secoes = extrair_secoes_bula(caminho_pdf)
        if secoes:
            dados_bula = {
                "tipo": f"Bula oficial extraída com sucesso",
                **secoes
            }

    return {
        "medicamento": medicamento_info,
        "bula": dados_bula
    }