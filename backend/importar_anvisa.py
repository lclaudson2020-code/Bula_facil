import csv
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bula_facil.db")
CSV_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "medicamentos_anvisa.csv"
)

# Mapeamento dos códigos de tarja da ANVISA
MAPA_TARJAS = {
    "1": "Sem Tarja",
    "2": "Tarja Vermelha",
    "3": "Tarja Preta",
    "4": "Tarja Vermelha (Retenção de Receita)",
    "-1": "Não APLICÁVEL",
}


def importar_em_massa():
  if not os.path.exists(CSV_PATH):
    print(f"Erro: Ficheiro CSV não encontrado em {CSV_PATH}")
    return

  conexao = sqlite3.connect(DB_PATH)
  cursor = conexao.cursor()

  print("A limpar a base de dados anterior...")
  cursor.execute("DELETE FROM medicamentos;")
  conexao.commit()

  print("A iniciar importação em massa...")

  lote = []
  contador_total = 0
  tamanho_lote = 1000

  # Utilizado iso-8859-1 para ler corretamente a acentuação (ex: 'cafeína')
  with open(
      CSV_PATH, mode="r", encoding="iso-8859-1", newline="", errors="replace"
  ) as arquivo_csv:
    leitor = csv.DictReader(arquivo_csv, delimiter=";")

    for linha in leitor:
      # Limpa as chaves do dicionário
      linha_limpa = {
          k.strip().replace("\ufeff", ""): (v.strip() if v else "")
          for k, v in linha.items()
          if k
      }

      nome = linha_limpa.get("NO_PRODUTO", "")
      principio_ativo = linha_limpa.get("SUBSTANCIAS_MEDICAMENTOS", "")
      if not principio_ativo:
        principio_ativo = linha_limpa.get("DS_REFERENCIA", "N/A")

      fabricante = linha_limpa.get(
          "NO_RAZAO_SOCIAL_EMPRESA", "Desconhecido"
      )
      categoria = linha_limpa.get("DS_TIPO_CATEGORIA_REGULATORIA", "")

      # Mapeia o código da tarja para o nome descritivo
      tarja_codigo = linha_limpa.get("CO_TARJA", "").strip()
      tarja_texto = MAPA_TARJAS.get(tarja_codigo, tarja_codigo)

      detalhes = []
      if categoria:
        detalhes.append(f"Categoria: {categoria}")
      if tarja_texto:
        detalhes.append(f"Tarja: {tarja_texto}")

      apresentacao = (
          " | ".join(detalhes)
          if detalhes
          else "Registro Oficial Anvisa"
      )

      if nome:
        lote.append((nome, principio_ativo, fabricante, apresentacao))
        contador_total += 1

      if len(lote) >= tamanho_lote:
        cursor.executemany(
            """
                    INSERT INTO medicamentos (nome, principio_ativo, fabricante, apresentacao)
                    VALUES (?, ?, ?, ?)
                """,
            lote,
        )
        conexao.commit()
        lote = []
        print(f"Processados {contador_total} registos oficiais...")

    if lote:
      cursor.executemany(
          """
                INSERT INTO medicamentos (nome, principio_ativo, fabricante, apresentacao)
                VALUES (?, ?, ?, ?)
            """,
          lote,
      )
      conexao.commit()

  conexao.close()
  print(
      f"\nImportação concluída com sucesso! Total de {contador_total} registos"
      " oficiais cadastrados no SQLite."
  )


if __name__ == "__main__":
  importar_em_massa()