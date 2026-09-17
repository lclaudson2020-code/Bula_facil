// Função assíncrona disparada quando o usuário clica no botão "Pesquisar"
async function buscarMedicamento() {
    // Pega o valor digitado no input e remove espaços vazios nas pontas (.trim())
    const nome = document.getElementById('medicamentoInput').value.trim();
    const resultadoDiv = document.getElementById('resultado');

    // Validação básica: se o campo estiver vazio, avisa o usuário e interrompe a função
    if (!nome) {
        resultadoDiv.innerHTML = "<p style='color: #e74c3c;'>Por favor, digite o nome de um medicamento.</p>";
        return;
    }

    // Mostra uma mensagem de carregamento enquanto aguarda a resposta da API
    resultadoDiv.innerHTML = "<p>Buscando informações oficiais...</p>";

    try {
        // Faz uma requisição HTTP GET para a nossa API FastAPI usando fetch()
        const resposta = await fetch(`http://127.0.0.1:8000/medicamentos/${nome}`);
        
        // Se a API retornar um erro (como 404 - não encontrado), dispara uma exceção
        if (!resposta.ok) {
            throw new Error("Medicamento não encontrado.");
        }

        // Converte a resposta da API de JSON para um objeto JavaScript legível
        const dados = await resposta.json();

        // Mapeia o array de seções da bula para gerar blocos HTML dinamicamente (.map)
        let secoesHtml = dados.bula.secoes.map(sec => `
            <div class="secao-titulo">${sec.titulo}</div>
            <p><strong>Resumo Simples:</strong> ${sec.resumo_simples}</p>
            <p style="font-size: 14px; color: #555;"><em>Texto oficial:</em> ${sec.conteudo_oficial}</p>
        `).join(''); // Junta todos os blocos gerados em uma única string HTML

        // Injeta o HTML estruturado com os dados reais do banco dentro da div de resultado
        resultadoDiv.innerHTML = `
            <h3>${dados.medicamento.nome} <span style="font-size: 14px; font-weight: normal; color: #7f8c8d;">(${dados.medicamento.apresentacao})</span></h3>
            <p><strong>Princípio Ativo:</strong> ${dados.medicamento.principio_ativo}</p>
            <p><strong>Fabricante:</strong> ${dados.medicamento.fabricante}</p>
            <hr style="border: 0; border-top: 1px solid #e1e8ed; margin: 15px 0;">
            ${secoesHtml}
            <div class="aviso-fonte">
                Fonte: ${dados.bula.fonte} | Atualizado em: ${dados.bula.data_atualizacao}
            </div>
        `;

    } catch (erro) {
        // Caso ocorra qualquer erro (pesquisa inválida ou API fora do ar), exibe mensagem amigável
        resultadoDiv.innerHTML = "<p style='color: #e74c3c;'>Medicamento não encontrado no banco de dados. Tente pesquisar por 'Paracetamol'.</p>";
    }
}