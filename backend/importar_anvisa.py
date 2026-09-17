import sqlite3
import csv
import os

# Caminho para o banco de dados e para o arquivo CSV de amostra
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bula_facil.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "medicamentos_anvisa.csv")

def importar_dados_anvisa():
    if not os.path.exists(CSV_PATH):
        print(f"Erro: O arquivo CSV não foi encontrado em {CSV_PATH}")
        return

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    print("Iniciando a importação do catálogo oficial...")
    contador = 0

    # Abre o arquivo CSV utilizando codificação utf-8-sig (para aceitar acentos)
    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as arquivo_csv:
        # O delimiter=';' indica que as colunas são separadas por ponto e vírgula
        leitor = csv.DictReader(arquivo_csv, delimiter=';')
        
        for linha in leitor:
            nome = linha.get('PRODUTO', '').strip()
            principio_ativo = linha.get('PRINCIPIO_ATIVO', '').strip()
            fabricante = linha.get('EMPRESA', '').strip()
            apresentacao = linha.get('APRESENTACAO', '').strip()

            if nome:
                cursor.execute("""
                    INSERT INTO medicamentos (nome, principio_ativo, fabricante, apresentacao)
                    VALUES (?, ?, ?, ?)
                """, (nome, principio_ativo, fabricante, apresentacao))
                contador += 1

    conexao.commit()
    conexao.close()
    print(f"Sucesso! {contador} medicamentos do catálogo oficial foram salvos no SQLite.")

if __name__ == "__main__":
    importar_dados_anvisa()