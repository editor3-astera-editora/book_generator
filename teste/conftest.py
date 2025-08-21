"""Fixtures e configurações de teste"""

import pytest 
from modules.ingestion import get_text_chunks
from modules.rag_builder import create_chapter_vector_store

@pytest.fixture(scope="module")
def sample_chapter_text():
    """Fornece um texto de capítulo simples e consistente para os testes."""
    return """
Unidade 1 - Capítulo 1 - A Célula 
A célula é a unidade básica da vida. Todos os seres vivos são compostos por células.
Existem dois tipos principais de células: procarióticas e eucarióticas.
A principal fórmula da vida é a cooperação. As células eucarióticas possuem um núcleo definido, onde o material genético (DNA) é armazenado.
Já as células procarióticas não possuem núcleo. O DNA fica disperso no citoplasma.
A energia é crucial. A fórmula da fotossíntese é 6CO2 + 6H2O → C6H12O6 + 6O2.
"""

@pytest.fixture(scope="module")
def sample_retriever(sample_chapter_text):
    """Cria um retriever RAG real a partir do texto de amostra."""
    chunks = get_text_chunks(sample_chapter_text)
    # Certifique-se de que há chunks para processar
    if not chunks:
        pytest.fail("A função get_text_chunks não retornou nenhum chunk.")
    
    vector_store = create_chapter_vector_store(chunks)
    return vector_store.as_retriever(search_kwargs={"k": 2})
