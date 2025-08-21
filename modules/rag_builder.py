import json 
import time 
from langchain_community.callbacks import get_openai_callback
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import config 
from modules.prompts import KEY_CONCEPTS_PROMPT

def create_chapter_vector_store(chunks: list[str]):
    """Cria um banco de dados vetorial FAISS a partir dos chunks de texto de um capítulo."""

    print(" - Gerando embeddings e criando banco de dados vetorial (FAISS)...")
    embeddings = OpenAIEmbeddings(api_key=config.OPEN_AI_API_KEY, model=config.EMBEDDING_MODEL)
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_store

def get_key_concepts(chapter_text: str, book_name: str) -> tuple[list[str], dict]:
    """Usa um LLM para extrair os conceitos-chave de um texto de capítulo."""

    print("   - Extraindo conceitos-chave com LLM...")
    llm = ChatOpenAI(api_key=config.OPEN_AI_API_KEY, model=config.GENERATION_MODEL, temperature=0)
    prompt = PromptTemplate.from_template(KEY_CONCEPTS_PROMPT)
    chain = prompt | llm | StrOutputParser()

    time.sleep(2)

    # Para rastrear a quantidade de tokens consumidos
    with get_openai_callback() as cb:
        response = chain.invoke({"chapter_text": chapter_text[:4000], "book_name": book_name})

        token_info = {
            "prompt": cb.prompt_tokens,
            "completion": cb.completion_tokens,
            "total": cb.total_tokens,
            "cost_usd": cb.total_cost
        }
        print(f" - [Uso de Tokens - Conceitos]: {token_info}")
    
    # Verifica se a resposta (potencialmente do mock) já é o objeto Python desejado
    if isinstance(response, list):
        print(f" - Conceitos-chave gerados: {response}")
        return response, token_info
        
    # Se for uma string (como na execução real), tenta decodificar
    try:
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
            
        concepts = json.loads(response)
        print(f" - Conceitos-chave gerados: {concepts}")
        return concepts, token_info
    except (json.JSONDecodeError, IndexError):
        print("   AVISO: Não foi possível decodificar a lista de conceitos.")
        return [], token_info

