# teste/test_formatting.py
import pytest
from modules.formatting import markdown_to_latex_string

# --- DADOS DE TESTE ---
# Simulamos a saída Markdown de um capítulo completo, com todos os tipos de exercício
# e os novos marcadores '---'.
MOCK_MARKDOWN_CONTENT = """
# Unidade 1 - Capítulo 1: Título do Capítulo de Teste

## Resumo do Capítulo
### Introdução
Esta é a introdução.

## Exercícios

---

**Tipo:** Múltipla Escolha
**Nível Cognitivo:** Aplicar
**Pergunta:**
Qual é a capital do Brasil?
**Alternativas:**
(A) Rio de Janeiro
(B) São Paulo
(C) Brasília
(D) Salvador
(E) Belo Horizonte
**Resposta Correta:** (C)
**Justificativa:** Brasília foi inaugurada como capital em 1960.

---

**Tipo:** Discursiva
**Nível Cognitivo:** Analisar
**Pergunta:**
Discorra sobre a importância do RAG.
**Resposta Ideal (Gabarito):**
RAG é importante pois aterra a resposta do LLM em fatos concretos.

---

**Tipo:** Questão Aberta (Cálculo/Desenho)
**Nível Cognitivo:** Aplicar
**Problema:**
Calcule a área de um quadrado com lado 5cm.
**Resolução (Gabarito):**
A área é lado * lado, portanto 5 * 5 = 25cm².

---
"""

def test_converte_titulo_principal():
    """Verifica se o título principal (#) é convertido para \sectiontoc."""
    latex_output = markdown_to_latex_string("# Título de Teste")
    assert r"\sectiontoc{Título de Teste}" in latex_output

def test_formata_secao_exercicios_completa():
    """Verifica se a seção de exercícios é corretamente encapsulada."""
    latex_output = markdown_to_latex_string(MOCK_MARKDOWN_CONTENT)
    assert r"\newpage" in latex_output
    assert r"\section*{Exercícios}" in latex_output
    assert r"\begin{enumerate}" in latex_output
    assert r"\end{enumerate}" in latex_output
    assert r"\item Qual é a capital do Brasil?" in latex_output
    assert r"\item Discorra sobre a importância do RAG." in latex_output
    assert r"\item Calcule a área de um quadrado com lado 5cm." in latex_output

def test_formata_questao_multipla_escolha():
    """Verifica a formatação de uma questão de múltipla escolha."""
    latex_output = markdown_to_latex_string(MOCK_MARKDOWN_CONTENT)
    # Verifica o enunciado
    assert r"\item Qual é a capital do Brasil?" in latex_output
    # Verifica o ambiente das alternativas
    assert r"\begin{itemize}[labelsep=5.5mm, leftmargin=*]" in latex_output
    assert r"\item[(A)] Rio de Janeiro" in latex_output
    assert r"\item[(C)] Brasília" in latex_output
    assert r"\end{itemize}" in latex_output
    # Verifica o gabarito colorido
    assert r"\textcolor{Gabarito}{\textbf{Gabarito:} (C) - Brasília foi inaugurada como capital em 1960.}" in latex_output
    # Verifica se os metadados foram removidos
    assert "Tipo:" not in latex_output
    assert "Nível Cognitivo:" not in latex_output

def test_formata_questao_discursiva():
    """Verifica a formatação de uma questão discursiva."""
    latex_output = markdown_to_latex_string(MOCK_MARKDOWN_CONTENT)
    assert r"\item Discorra sobre a importância do RAG." in latex_output
    # Verifica se o comando customizado foi usado com o gabarito
    assert r"\linhasRespostaComGabarito{RAG é importante pois aterra a resposta do LLM em fatos concretos.}" in latex_output

def test_formata_questao_aberta():
    """Verifica a formatação de uma questão aberta."""
    latex_output = markdown_to_latex_string(MOCK_MARKDOWN_CONTENT)
    assert r"\item Calcule a área de um quadrado com lado 5cm." in latex_output
    # Verifica o ambiente tcolorbox
    assert r"\begin{tcolorbox}{quadrodesenho}" in latex_output
    # Verifica o gabarito colorido dentro da caixa
    assert r"\textcolor{Gabarito}{A área é lado * lado, portanto 5 * 5 = 25cm².}" in latex_output
    assert r"\end{tcolorbox}" in latex_output