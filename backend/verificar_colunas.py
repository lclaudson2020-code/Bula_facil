import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "medicamentos_anvisa.csv")

with open(CSV_PATH, mode='r', encoding='latin-1') as f:
    # Lê a primeira linha do arquivo (cabeçalho)
    primeira_linha = f.readline().strip()
    print("Cabeçalho encontrado no arquivo CSV:")
    print(primeira_linha)