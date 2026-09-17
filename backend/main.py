from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(title="Bula Fácil API", version="0.1")

# Configuração do CORS (Permite que o Frontend na porta 5500 acesse a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem (ótimo para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Caminho para o banco de dados criado na pasta data/
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bula_facil.db")

def conectar():
    """Abre conexão com o banco e configura para retornar dicionários."""
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row  # Facilita converter o resultado em JSON
    return conexao

@app.get("/")
def home():
    return {"mensagem": "API do Bula Fácil rodando com sucesso! 🚀"}

@app.get("/medicamentos/{nome}")
def buscar_medicamento(nome: str):
    """Busca um medicamento pelo nome no banco de dados, incluindo sua bula e seções."""
    conexao = conectar()
    cursor = conexao.cursor()

    # 1. Procura o medicamento (usando LIKE para busca parcial)
    cursor.execute("""
        SELECT m.id, m.nome, m.principio_ativo, m.fabricante, m.apresentacao,
               b.id as bula_id, b.tipo_bula, b.fonte, b.data_atualizacao
        FROM medicamentos m
        LEFT JOIN bulas b ON m.id = b.medicamento_id
        WHERE m.nome LIKE ?
    """, (f"%{nome}%",))
    
    med = cursor.fetchone()

    if not med:
        conexao.close()
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")

    # 2. Busca as seções da bula vinculadas a esse medicamento
    cursor.execute("""
        SELECT titulo, conteudo_oficial, resumo_simples
        FROM secoes_bula
        WHERE bula_id = ?
    """, (med["bula_id"],))
    
    secoes = [dict(row) for row in cursor.fetchall()]
    conexao.close()

    # 3. Retorna a resposta organizada em formato JSON
    return {
        "medicamento": {
            "id": med["id"],
            "nome": med["nome"],
            "principio_ativo": med["principio_ativo"],
            "fabricante": med["fabricante"],
            "apresentacao": med["apresentacao"]
        },
        "bula": {
            "tipo": med["tipo_bula"],
            "fonte": med["fonte"],
            "data_atualizacao": med["data_atualizacao"],
            "secoes": secoes
        }
    }