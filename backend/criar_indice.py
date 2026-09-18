import sqlite3
import os

# Caminho para o banco de dados do projeto
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bula_facil.db")

def criar_indices():
    if not os.path.exists(DB_PATH):
        print(f"Erro: Banco de dados não encontrado em {DB_PATH}")
        return

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    print("Criando índice de performance na tabela de medicamentos...")
    
    # Cria um índice na coluna 'nome' para acelerar as buscas na API
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_medicamentos_nome 
        ON medicamentos (nome);
    """)

    conexao.commit()
    conexao.close()
    
    print("Sucesso! Índice criado. As consultas por nome agora serão muito mais rápidas.")

if __name__ == "__main__":
    criar_indices()