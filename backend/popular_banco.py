from database import conectar

def popular_dados():
    conexao = conectar()
    cursor = conexao.cursor()

    # Limpa os dados antigos para evitar duplicação caso o script rode de novo
    cursor.execute("DELETE FROM secoes_bula")
    cursor.execute("DELETE FROM bulas")
    cursor.execute("DELETE FROM medicamentos")

    # Lista com os medicamentos que queremos cadastrar no piloto
    medicamentos_dados = [
        {
            "nome": "Paracetamol",
            "principio_ativo": "Paracetamol",
            "fabricante": "Laboratório Genérico",
            "apresentacao": "500mg - Comprimido",
            "tipo_bula": "Bula do Paciente",
            "fonte": "Bulário Eletrônico / Anvisa",
            "data_atualizacao": "2026-01-10",
            "secoes": [
                (
                    "Para que serve", 
                    "Este medicamento é indicado para a redução da febre e para o alívio temporário de dores leves a moderadas, tais como dores de cabeça, resfriados comuns, dores musculares e de dente.",
                    "Ajuda a baixar a febre e alivia dores comuns (como dor de cabeça ou dores musculares leves)."
                ),
                (
                    "Contraindicações", 
                    "Este medicamento não deve ser utilizado por pacientes com alergia conhecida ao paracetamol ou a qualquer outro componente de sua fórmula. Não deve ser usado por pacientes com doença grave do fígado.",
                    "Evite tomar se você tem alergia ao paracetamol ou algum problema grave no fígado."
                )
            ]
        },
        {
            "nome": "Dipirona",
            "principio_ativo": "Dipirona Sódica",
            "fabricante": "Laboratório Genérico",
            "apresentacao": "500mg/mL - Solução Oral (Gotas)",
            "tipo_bula": "Bula do Paciente",
            "fonte": "Bulário Eletrônico / Anvisa",
            "data_atualizacao": "2026-02-15",
            "secoes": [
                (
                    "Para que serve", 
                    "Este medicamento é utilizado no tratamento de febre e dor. Dor de cabeça, cólicas, dores musculares e articulares são exemplos de condições tratadas.",
                    "Indicado para baixar a febre e aliviar dores fortes, como cólicas, dor de cabeça ou dores musculares."
                ),
                (
                    "Contraindicações", 
                    "Este medicamento não deve ser utilizado caso haja alergia à dipirona ou a qualquer um dos componentes da formulação. Não deve ser usado por gestantes no primeiro trimestre sem orientação médica.",
                    "Não use se tiver alergia à dipirona. Gestantes devem consultar o médico antes de tomar."
                )
            ]
        }
    ]

    # Laço de repetição para cadastrar cada medicamento e suas respectivas seções
    for med in medicamentos_dados:
        # 1. Insere o medicamento principal
        cursor.execute("""
            INSERT INTO medicamentos (nome, principio_ativo, fabricante, apresentacao)
            VALUES (?, ?, ?, ?)
        """, (med["nome"], med["principio_ativo"], med["fabricante"], med["apresentacao"]))
        
        medicamento_id = cursor.lastrowid

        # 2. Insere a referência da bula
        cursor.execute("""
            INSERT INTO bulas (medicamento_id, tipo_bula, fonte, data_atualizacao)
            VALUES (?, ?, ?, ?)
        """, (medicamento_id, med["tipo_bula"], med["fonte"], med["data_atualizacao"]))
        
        bula_id = cursor.lastrowid

        # 3. Prepara e insere as seções da bula vinculadas
        secoes_formatadas = [
            (bula_id, titulo, conteudo, resumo) for titulo, conteudo, resumo in med["secoes"]
        ]
        
        cursor.executemany("""
            INSERT INTO secoes_bula (bula_id, titulo, conteudo_oficial, resumo_simples)
            VALUES (?, ?, ?, ?)
        """, secoes_formatadas)

    conexao.commit()
    conexao.close()
    print("Banco populado com Paracetamol e Dipirona com sucesso!")

if __name__ == "__main__":
    popular_dados()