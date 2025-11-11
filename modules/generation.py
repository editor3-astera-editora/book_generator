"""Impleta as técnicas de geração de texto."""
import random 
import time 
import itertools
from langchain_community.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
from modules.utils import extrair_numeros_ord
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
import config
from modules.prompts import (
    SUMMARY_INTRO_PROMPT, SUMMARY_BULLETS_PROMPT,
    SUMMARY_APPLICATIONS_PROMPT,
    MULTIPLE_CHOICE_PROMPT, DISCURSIVE_PROMPT, OPEN_ENDED_CALC_DRAW_PROMPT,
    OPEN_ENDED_SCENARIO_PROMPT, 
    REVISE_EXERCISES_SIMILARITY_PROMPT, TRUE_FALSE_PROMPT,
    CAPTION_FIGURE_PROMPT
)

def _call_llm_with_tracking(prompt_template: str, input_variables: dict, temperature: float = 0.2) -> tuple[str, dict]:
    """
    Função auxiliar que chama o LLM, rastreia o uso de tokens e aceita
    um dicionário de variáveis para o prompt.
    """

    time.sleep(2)

    prompt = PromptTemplate.from_template(prompt_template)
    llm = ChatOpenAI(api_key=config.OPEN_AI_API_KEY, model=config.GENERATION_MODEL, temperature=temperature)
    chain = prompt | llm | StrOutputParser()

    with get_openai_callback() as cb:
        result = chain.invoke(input_variables)
        token_info = {
            "prompt": cb.prompt_tokens,
            "completion": cb.completion_tokens,
            "total": cb.total_tokens,
            "cost_usd": cb.total_cost
        }

    return result, token_info

def generate_structured_summary(retriever, key_concepts: list[str], book_name: str) -> tuple[str, dict]:
    """Gera um resumo estruturado e simplificado do capítulo."""

    print(" - Gerando resumo estruturado (simplificado)...")
    total_token_info = {"prompt": 0, "completion": 0, "total": 0, "cost_usd": 0.0}

    docs = retriever.invoke("Forneça o contexto geral e os pontos principais deste capítulo.")
    full_context = "\n\n".join([doc.page_content for doc in docs])

    parts = {}

    summary_generation_plan = [
        ("Introdução", SUMMARY_INTRO_PROMPT),
        ("Aplicações", SUMMARY_APPLICATIONS_PROMPT),
        ("Conceitos-Chave", SUMMARY_BULLETS_PROMPT),
        #("Principais conceitos", SUMMARY_MAIN_CONCEPTS_PROMPT),
    ]
    
    for part_name, prompt_template in summary_generation_plan:
        print(f"      - Gerando parte do resumo: {part_name}...")

        input_vars = {"context": full_context}

        if part_name == "Aplicações":
            input_vars["key_concepts_list"] = ", ".join(key_concepts)
            input_vars["book_name"] = book_name
        
        parts[part_name], tokens = _call_llm_with_tracking(prompt_template, input_vars)
        for key in total_token_info: total_token_info[key] += tokens.get(key, 0)

    # 1. Monta as principais partes do resumo
    final_summary_parts = [
        "## Resumo do Capítulo",
        "### Introdução",
        parts['Introdução'],
        #"\n### Principais conceitos",
        #parts['Principais conceitos'],
        "\n### Aplicações",
        parts['Aplicações'],
        "\n### Conceitos-Chave",
        parts['Conceitos-Chave']
    ]
    final_summary = "\n".join(final_summary_parts)
    return final_summary, total_token_info

def _generate_single_exercise(retriever, concept: str, exercise_type: str, bloom_level: str, formula_map: list, current_unit: int, current_chapter: int) -> dict:
    """
    Gera um único exercício, usando o mapa de fórmulas pré-processado.
    """
    
    context_docs = retriever.invoke(f"Qual o contexto e explicação para o conceito '{concept}'?")
    context = "\n\n".join([doc.page_content for doc in context_docs])
    time.sleep(2)

    prompt_template = OPEN_ENDED_SCENARIO_PROMPT

    if exercise_type == "Aberta":
        print(f"      - Consultando mapa de fórmulas para o conceito '{concept}'...")

        posicao_atual = (current_unit, current_chapter)

        formulas_disponiveis = []
        for f in formula_map:
            if 'source_chapter' not in f:
                continue

            posicao_formula = extrair_numeros_ord(f['source_chapter'])

            if posicao_formula == posicao_atual:
                formulas_disponiveis.append(f)
        
        print(f" -> {len(formula_map)} fórmulas no total. {len(formulas_disponiveis)} disponíveis para U{current_unit}-C{current_chapter}.")

        formulas_relevantes = [
            f["formula"] for f in formulas_disponiveis
            if any(map_concept.lower() in concept.lower() for map_concept in f.get("concepts", []))
        ]

        if formulas_relevantes:
            print(f"        -> Fórmulas associadas encontradas: {formulas_relevantes}. Gerando exercício de cálculo.")
            prompt_template = OPEN_ENDED_CALC_DRAW_PROMPT
        else:
            print("        -> Nenhuma fórmula associada encontrada. Gerando exercício de cenário.")
            # prompt_template já é Cenário, não precisa mudar.
    else:
        # Lógica para outros tipos de questão
        prompt_map = { "Múltipla Escolha": MULTIPLE_CHOICE_PROMPT, "Discursiva": DISCURSIVE_PROMPT, "Verdadeiro ou Falso": TRUE_FALSE_PROMPT }
        prompt_template = prompt_map.get(exercise_type)

    final_input_vars = {"context": context, "concept": concept, "bloom_level": bloom_level}
    if prompt_template == OPEN_ENDED_CALC_DRAW_PROMPT:
        final_input_vars["context"] += "\n\nFórmulas Relevantes do Livro que podem ser usadas: " + ", ".join(formulas_relevantes)
        
    exercise_text, exercise_tokens = _call_llm_with_tracking(prompt_template, final_input_vars, temperature=0.5)

    return {
        "text": exercise_text,
        "token_info": exercise_tokens,
        "inputs": {"retriever": retriever, "concept": concept, "exercise_type": exercise_type, "bloom_level": bloom_level}
    }
    
def generate_exercises(retriever, key_concepts: list[str], formula_map: list, current_unit: int, current_chapter: int) -> tuple[str, dict]:
    """Gera uma lista de 7 exercícios variados."""

    print(" - Gerando uma lista de 7 exercícios com progressão de dificuldade exercícios...")
    total_token_info = {"prompt": 0, "completion": 0, "total": 0, "cost_usd": 0.0}

    if not key_concepts:
        print(" - Nenhum conceito-chave encontrado. Pulando a geração de exercícios.")
        return "## Exercícios\n\nNenhum exercício pôde ser gerado para este capítulo.", total_token_info
    
    bloco_facil = [
        ("Verdadeiro ou Falso", "Entender"),
        ("Múltipla Escolha", "Lembrar"),
        ("Discursiva", "Entender"),
    ]

    bloco_medio = [
        ("Múltipla Escolha", "Aplicar"),
        ("Múltipla Escolha", "Aplicar"),
        ("Aberta", "Aplicar")
    ]

    bloco_dificil = [
        ("Discursiva", "Analisar"),
        ("Aberta", "Analisar"),
    ]

    random.shuffle(bloco_facil)
    random.shuffle(bloco_medio)
    random.shuffle(bloco_dificil)

    exercise_plan = bloco_facil + bloco_medio + bloco_dificil

    generated_exercises = []
    concept_cycler = itertools.cycle(key_concepts)

    for i, (exercise_type, bloom_level) in enumerate(exercise_plan):
        concept = next(concept_cycler)
        print(f" - Gerando exercício {i + 1}/8 (Tipo: {exercise_type}, Nível: {bloom_level}, Conceito: '{concept}')...")

        exercise_data = {"text": ""}
        max_retries = 2
        retries = 0
        while not exercise_data.get("text", "").strip() and retries <= max_retries:
            if retries > 0:
                print(f"        - TENTATIVA {retries + 1}: Exercício {i+1} saiu em branco. Gerando novamente...")
            # A chamada agora passa o mapa de fórmulas
            exercise_data = _generate_single_exercise(retriever, concept, exercise_type, bloom_level, formula_map, current_unit, current_chapter)
            retries += 1
        
        if not exercise_data.get("text", "").strip():
            print(f"        - AVISO: Não foi possível gerar o exercício {i+1} após {max_retries + 1} tentativas.")

        generated_exercises.append(exercise_data)
        for key in total_token_info: total_token_info[key] += exercise_data.get("token_info", {}).get(key, 0)

    print("   - Iniciando ciclo de revisão de similaridade (máx. 3 iterações)")
    max_review_cycles = 3
    for cycle in range(max_review_cycles):
        print(f"      - Ciclo de revisão {cycle + 1}/{max_review_cycles}...")

        exercise_texts_for_review = [f"**Questão {i+1}:**\n{data['text']}\n" for i, data in enumerate(generated_exercises)]
        review_context_string = "---\n".join(exercise_texts_for_review)
        review_input_vars = {"exercise_list": review_context_string}
        review_result, review_tokens = _call_llm_with_tracking(
            REVISE_EXERCISES_SIMILARITY_PROMPT, review_input_vars, temperature=0.0
        )
        for key in total_token_info: total_token_info[key] += review_tokens.get(key, 0)

        if "NENHUM" in review_result.upper():
            print("      - REVISÃO: Todas as questões são distintas. Ciclo de revisão encerrado.")
            break
        
        try:
            index_to_redo = int(review_result.strip()) - 1
            if 0 <= index_to_redo < len(generated_exercises):
                print(f" - REVISÃO: Questão {index_to_redo + 1} marcada como similar. Recriando com novo conceito...")
                original_inputs = generated_exercises[index_to_redo]["inputs"]

                # Estratégia de rotação de conceito 
                new_concept = next(concept_cycler)
                print(f" - Rotacionando conceito '{original_inputs['concept']}' para '{new_concept}'.")

                new_exercise_data = _generate_single_exercise(
                    original_inputs["retriever"],
                    new_concept,
                    original_inputs["exercise_type"],
                    original_inputs["bloom_level"],
                    formula_map,
                    current_unit,
                    current_chapter
                )

                generated_exercises[index_to_redo] = new_exercise_data
                print(f" - Questão {index_to_redo + 1} recriada com sucesso.")
            else:
                break 
        except ValueError:
            break 
    else:
        print(" - AVISO: Máximo de ciclos de revisão atingido.")
    
    final_exercise_texts = [data["text"] for data in generated_exercises]
    return "## Exercícios\n\n" + "\n\n---\n\n".join(final_exercise_texts), total_token_info


def generate_figure_caption(chapter_title: str) -> tuple[str, dict]:
    """Gera uma legenda para a figura de abertura da unidade."""
    print(f"   - Gerando legenda para a figura de abertura (Título: {chapter_title})...")
    
    input_vars = {"chapter_title": chapter_title}
    
    caption, token_info = _call_llm_with_tracking(
        CAPTION_FIGURE_PROMPT,
        input_vars,
        temperature=0.6
    )
    
    return caption, token_info