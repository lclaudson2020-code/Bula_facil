import csv
import os

# Caminho onde o CSV será gerado na pasta data/
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "medicamentos_anvisa.csv")

def gerar_csv_gigante():
    print("Gerando arquivo CSV de teste com 5.000 medicamentos...")
    
    with open(csv_path, mode='w', encoding='utf-8-sig', newline='') as arquivo_csv:
        leitor_escrita = csv.writer(arquivo_csv, delimiter=';')
        
        # Escreve o cabeçalho padrão da Anvisa
        leitor_escrita.writerow(['PRODUTO', 'PRINCIPIO_ATIVO', 'EMPRESA', 'APRESENTACAO'])
        
        # Gera 5.000 linhas de medicamentos simulados
        for i in range(1, 5001):
            leitor_escrita.writerow([
                f"MEDICAMENTO TESTE {i}",
                f"PRINCIPIO ATIVO EXEMPLO {i}",
                "LABORATORIO FARMACEUTICO S.A.",
                "500mg comp ct bl al plas x 20"
            ])

    print("Arquivo 'medicamentos_anvisa.csv' com 5.000 linhas gerado com sucesso na pasta data/!")

if __name__ == "__main__":
    gerar_csv_gigante()