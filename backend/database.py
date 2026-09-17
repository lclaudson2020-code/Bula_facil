import sqlite3
import os

# Garante que a pasta 'data' existe para salvar o banco
os.makedirs("data", exist_ok=True)
DB_PATH = "data/bula_facil.db"

def conectar():
    """Retorna uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    """Cria as tabelas iniciais do projeto se elas não existirem."""
    conexao = conectar()
    cursor = conexao.cursor()

    # 1. Tabela de Medicamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            principio_ativo TEXT NOT NULL,
            fabricante TEXT NOT NULL,
            apresentacao TEXT NOT NULL
        )
    """)

    # 2. Tabela de Bulas (vinculada ao medicamento)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicamento_id INTEGER,
            tipo_bula TEXT,
            fonte TEXT,
            data_atualizacao TEXT,
            FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id)
        )
    """)

    # 3. Tabela de Seções da Bula (conteúdo e resumo)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secoes_bula (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bula_id INTEGER,
            titulo TEXT,
            conteudo_oficial TEXT,
            resumo_simples TEXT,
            FOREIGN KEY (bula_id) REFERENCES bulas (id)
        )
    """)

    conexao.commit()
    conexao.close()
    print("Banco de dados e tabelas criados com sucesso!")

if __name__ == "__main__":
    criar_tabelas()