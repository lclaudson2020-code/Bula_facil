import sqlite3
import csv
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bula_facil.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "medicamentos_anvisa.csv")

def importar_em_massa():
    if not os.path.exists(CSV_PATH):
        print(f"Erro: Ficheiro CSV não encontrado em {CSV_PATH}")
        return

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    print("A limpar a base de dados anterior...")
    cursor.execute("DELETE FROM medicamentos;")
    conexao.commit()

    print("A iniciar importação em massa com tratamento robusto de cabeçalhos...")
    
    lote = []
    contador_total = 0
    tamanho_lote = 1000

    with open(CSV_PATH, mode='r', encoding='latin-1') as arquivo_csv:
        leitor = csv.DictReader(arquivo_csv, delimiter=';')
        
        for linha in leitor:
            # Remove espaços e caracteres ocultos (como BOM) das chaves do dicionário
            linha_limpa = {k.strip().replace('\ufeff', ''): (v.strip() if v else '') for k, v in linha.items() if k}
            
            nome = linha_limpa.get('NOME_COMERCIAL', '')
            if not nome:
                nome = linha_limpa.get('NOME_TECNICO', '')
            
            principio_ativo = linha_limpa.get('NOME_TECNICO', 'N/A')
            
            fabricante = linha_limpa.get('NOME_FABRICANTE', '')
            if not fabricante:
                fabricante = linha_limpa.get('DETENTOR_REGISTRO_CADASTRO', 'Desconhecido')
            
            classe_risco = linha_limpa.get('CLASSE_RISCO', '')
            apresentacao = f"Classe de Risco: {classe_risco}" if classe_risco else "Registro Oficial Anvisa"

            if nome:
                lote.append((nome, principio_ativo, fabricante, apresentacao))
                contador_total += 1

            if len(lote) >= tamanho_lote:
                cursor.executemany("""
                    INSERT INTO medicamentos (nome, principio_ativo, fabricante, apresentacao)
                    VALUES (?, ?, ?, ?)
                """, lote)
                conexao.commit()
                lote = []
                print(f"Processados {contador_total} registos oficiais...")

        if lote:
            cursor.executemany("""
                INSERT INTO medicamentos (nome, principio_ativo, fabricante, apresentacao)
                VALUES (?, ?, ?, ?)
            """, lote)
            conexao.commit()

    conexao.close()
    print(f"\nImportação concluída com sucesso! Total de {contador_total} registos oficiais cadastrados no SQLite.")

if __name__ == "__main__":
    importar_em_massa()