from database import conectar

def popular_dados():
    conexao = conectar()
    cursor = conexao.cursor()

    # 1. Inserir o medicamento de teste: Paracetamol
    cursor.execute("""
        INSERT INTO medicamentos (nome, principio_ativo, fabricante, apresentacao)
        VALUES (?, ?, ?, ?)
    """, ("Paracetamol", "Paracetamol", "Laboratório Genérico", "500mg - Comprimido"))
    
    # Pega o ID do medicamento que acabou de ser inserido
    medicamento_id = cursor.lastrowid

    # 2. Inserir a referência da bula
    cursor.execute("""
        INSERT INTO bulas (medicamento_id, tipo_bula, fonte, data_atualizacao)
        VALUES (?, ?, ?, ?)
    """, (medicamento_id, "Bula do Paciente", "Bulário Eletrônico / Anvisa", "2026-01-10"))
    
    # Pega o ID da bula inserida
    bula_id = cursor.lastrowid

    # 3. Inserir seções com o conteúdo oficial e o resumo simples
    secoes = [
        (
            bula_id, 
            "Para que serve", 
            "Este medicamento é indicado para a redução da febre e para o alívio temporário de dores leves a moderadas, tais como dores de cabeça,resfriados comuns, dores musculares e de dente.",
            "Ajuda a baixar a febre e alivia dores comuns (como dor de cabeça ou dores musculares leves)."
        ),
        (
            bula_id, 
            "Contraindicações", 
            "Este medicamento não deve ser utilizado por pacientes com alergia conhecida ao paracetamol ou a qualquer outro componente de sua fórmula. Não deve ser usado por pacientes com doença grave do fígado.",
            "Evite tomar se você tem alergia ao paracetamol ou algum problema grave no fígado."
        )
    ]

    cursor.executemany("""
        INSERT INTO secoes_bula (bula_id, titulo, conteudo_oficial, resumo_simples)
        VALUES (?, ?, ?, ?)
    """, secoes)

    conexao.commit()
    conexao.close()
    print("Medicamento de teste inserido com sucesso!")

if __name__ == "__main__":
    popular_dados()