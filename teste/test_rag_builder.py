# teste/test_rag_builder.py
import json
from langchain_community.vectorstores import FAISS
from modules.rag_builder import create_chapter_vector_store, get_key_concepts

def test_create_chapter_vector_store():
    """Testa se a função retorna um objeto FAISS."""
    chunks = ["primeiro chunk de teste.", "segundo chunk de teste."]
    vector_store = create_chapter_vector_store(chunks)
    assert isinstance(vector_store, FAISS)

def test_get_key_concepts_with_correct_mock(mocker):
    """
    Testa a extração de conceitos-chave mockando apenas a chamada ao LLM.
    Esta é a abordagem mais limpa e recomendada.
    """
    # 1. Este é o resultado que esperamos que o LLM (a parte cara) retorne.
    #    Note que é uma string, exatamente como a API da OpenAI retornaria.
    expected_llm_output = json.dumps(["Célula", "DNA", "Fotossíntese"])

    # 2. A Correção Definitiva: Mockamos o método 'invoke' da classe ChatOpenAI.
    #    Quando `llm.invoke` for chamado dentro da sua função, ele será interceptado
    #    e retornará nosso valor, em vez de fazer uma chamada de rede.
    mocker.patch(
        'langchain_openai.ChatOpenAI.invoke',
        return_value=expected_llm_output
    )

    # 3. Executa a função.
    #    - O PromptTemplate será criado normalmente.
    #    - O llm.invoke será interceptado pelo mock.
    #    - O StrOutputParser irá processar a saída do nosso mock (expected_llm_output).
    #    - O json.loads irá decodificar a string corretamente.
    concepts = get_key_concepts("qualquer texto")

    # 4. Verifica se o resultado final está correto.
    assert concepts == ["Célula", "DNA", "Fotossíntese"]