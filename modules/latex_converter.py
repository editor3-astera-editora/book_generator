import re 
import config 
import time
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from modules.prompts_latex import (
    LATEX_MC_PROMPT,
    LATEX_DISCURSIVE_PROMPT,
    LATEX_OPEN_ENDED_PROMPT,
    LATEX_SCENARIO_PROMPT,
    LATEX_BULLETS_PROMPT,
    LATEX_TRUE_FALSE_PROMPT,
)

def convert_bullets_to_latex(bullet_list_markdown: str) -> str:
    """
    Usa um LLM para converter uma lista de marcadores em Markdown
    para um ambiente 'itemize' do LaTeX.
    """
    print(" - Convertendo lista de Conceitos-Chave para LaTeX via LLM...")

    print(" - Time sleep de dois segundos")
    time.sleep(10)

    llm = ChatOpenAI(
        api_key=config.OPEN_AI_API_KEY,
        model="gpt-3.5-turbo",
        temperature=0.0
    )
    prompt = PromptTemplate.from_template(LATEX_BULLETS_PROMPT)
    chain = prompt | llm | StrOutputParser()

    latex_output = chain.invoke({"bullet_list": bullet_list_markdown})

    return latex_output.strip()


def convert_exercise_to_latex(exercise_markdown: str) -> str:
    """
    Converte o Markdown de um único exercício para LaTeX, selecionando o prompt
    apropriado com base no tipo de exercício.
    """

    # 1. Identificar o tipo de exercício com uma regex simples e confiável 
    tipo_match = re.search(r'\*\*Tipo:\*\*\s*(.*)', exercise_markdown)
    if not tipo_match:
        print(f"AVISO: Não foi possível determinar o tipo do exercício. Pulando conversão.")
        return ""
    
    exercise_type = tipo_match.group(1).strip()

    exercise_markdown = re.sub(
        r'^\s*\(([a-zA-Z])\)', 
        lambda m: f"({m.group(1).upper()})", 
        exercise_markdown, 
        flags=re.MULTILINE
    )

    # 2. Mapear o tipo de exercício para o prompt correto
    prompt_map = {
        "Múltipla Escolha": LATEX_MC_PROMPT,
        "Discursiva": LATEX_DISCURSIVE_PROMPT,
        "Questão Aberta (Cálculo/Desenho)": LATEX_OPEN_ENDED_PROMPT,
        "Questão Aberta (Cenário Aplicado)": LATEX_SCENARIO_PROMPT,
        "Verdadeiro ou Falso": LATEX_TRUE_FALSE_PROMPT
    }

    prompt_template_str = prompt_map.get(exercise_type)

    if not prompt_template_str:
        print(f"AVISO: Tipo de exercício desconhecido '{exercise_type}'. Pulando conversão.")
        return ""
    
    print(f"      - Convertendo exercício do tipo '{exercise_type}' para LaTeX...")

    # 3. Chama o LLM com o prompt selecionado 
    llm = ChatOpenAI(
        api_key=config.OPEN_AI_API_KEY,
        model="gpt-3.5-turbo", 
        temperature=0.0,
        request_timeout=30
    )
    prompt = PromptTemplate.from_template(prompt_template_str)
    chain = prompt | llm | StrOutputParser()

    latex_output = chain.invoke({"exercise_markdown": exercise_markdown})

    return latex_output.strip()

