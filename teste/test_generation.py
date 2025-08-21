"""Testa a estrutura da saída das funções de geração"""
import pytest 
from modules.generation import generate_structured_summary, generate_exercises

@pytest.mark.vcr # Marca para testes que fazem chamadas de API reais 
def test_generate_structured_summary(sample_retriever):
    """Testa a estrutura do resumo gerado."""
    summary = generate_structured_summary(sample_retriever)
    assert isinstance(summary, str)
    assert "### Introdução" in summary
    assert "### Conceitos-Chave" in summary
    assert "### Análise de Fórmulas" in summary
    assert "### Conclusão" in summary

@pytest.mark.vcr
def test_generate_exercises(sample_retriever):
    """Testa a estrutura dos exercícios gerados."""
    key_concepts = ["Célula", "DNA"]
    exercises = generate_exercises(sample_retriever, key_concepts)
    assert isinstance(exercises, str)
    assert "## Exercícios" in exercises
    assert "**Pergunta:**" in exercises
    assert "**Resposta:**" in exercises
    # Testa se gerou para ambos os conceitos
    assert exercises.count("**Pergunta:**") == 2