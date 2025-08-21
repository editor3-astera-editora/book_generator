import sys
import random
from langchain.schema import Document

# Adicione o caminho do seu projeto ao sys.path para encontrar os módulos
# Altere '.' para o caminho correto se executar de um diretório diferente
sys.path.append('.')

# Importe a função diretamente do seu módulo
from modules.rag_builder import rerank_with_cross_encoder

def teste_reranking():
    """
    Script para testar e validar a lógica de re-ranking de documentos.
    """
    print("--- INICIANDO TESTE DE RE-RANKING ---")

    # 1. Defina a consulta e os documentos de exemplo
    query = "Qual a definição de juros compostos?"

    # Documentos com relevância variada. O doc[0] é o mais relevante.
    documentos = [
        Document(page_content="Juros compostos são calculados considerando o capital inicial somado aos juros acumulados de períodos anteriores, gerando um efeito 'juros sobre juros'."),
        Document(page_content="Para calcular juros simples, a fórmula é J = C * i * t, onde a taxa incide apenas sobre o capital inicial."),
        Document(page_content="A inflação é um conceito econômico que representa o aumento generalizado dos preços de bens e serviços."),
        Document(page_content="O mercado de ações oferece oportunidades de investimento com diferentes perfis de risco e retorno."),
        Document(page_content="O cálculo de juros sobre juros é a principal característica do sistema de capitalização composta."),
        Document(page_content="Investir em tecnologia pode ser uma boa estratégia, mas o retorno não é garantido."),
    ]

    # Embaralha a lista para garantir que a ordem inicial seja aleatória
    random.shuffle(documentos)

    print("\n[Consulta]:")
    print(f"'{query}'")

    print("\n[Ordem dos Documentos ANTES do Re-ranking]:")
    for i, doc in enumerate(documentos):
        print(f"  {i+1}. {doc.page_content[:80]}...")

    # 2. Execute a função de re-ranking
    # No seu código, a função real que usa o Cross-Encoder está comentada,
    # então estamos testando a simulação. O comportamento esperado é o mesmo.
    documentos_reordenados = rerank_with_cross_encoder(query, documentos)

    print("\n[Ordem dos Documentos DEPOIS do Re-ranking]:")
    for i, doc in enumerate(documentos_reordenados):
        # Adiciona um marcador para destacar os documentos mais relevantes
        marcador = "✅" if "juros compostos" in doc.page_content.lower() or "juros sobre juros" in doc.page_content.lower() else "❌"
        print(f"  {i+1}. {marcador} {doc.page_content[:80]}...")

    # 3. Validação
    print("\n--- AVALIAÇÃO DO TESTE ---")
    if "juros compostos" in documentos_reordenados[0].page_content.lower() or "juros sobre juros" in documentos_reordenados[0].page_content.lower():
        print("✅ SUCESSO: O documento mais relevante foi classificado em primeiro lugar.")
    else:
        print("❌ FALHA: O documento mais relevante NÃO foi classificado em primeiro lugar.")

    print("--- TESTE CONCLUído ---")

if __name__ == "__main__":
    teste_reranking()