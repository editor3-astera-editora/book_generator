# Arquivo: auditoria_formulas.py

import sys
import os
import re
import json
import config
from modules.ingestion import extract_chapters_from_word
from modules.generation import _call_llm_with_tracking
from modules.prompts import FORMULA_EXTRACTOR_PROMPT

def auditar_formulas_do_livro(docx_path: str):
    """
    Lê um livro inteiro, capítulo por capítulo, e usa a IA para extrair
    todas as fórmulas explícitas, gerando um relatório final.
    """
    print("="*80)
    print("INICIANDO AUDITORIA DE FÓRMULAS NO LIVRO COMPLETO")
    print(f"Livro: {docx_path}")
    print("="*80)

    # 1. Extrai todos os capítulos do documento
    chapters = extract_chapters_from_word(docx_path)
    if not chapters:
        print("Nenhum capítulo encontrado. Encerrando auditoria.")
        return

    resultados_auditoria = {}
    total_formulas_encontradas = 0

    # 2. Itera sobre cada capítulo para extrair as fórmulas
    for chapter_data in sorted(chapters, key=lambda d: (d['unit'], d['chapter'])):
        unit = chapter_data['unit']
        chap = chapter_data['chapter']
        title = chapter_data['title']
        chapter_text = chapter_data['text']
        
        capitulo_id = f"U{unit}-C{chap}: {title}"
        print(f"\n--- Auditando Capítulo: {capitulo_id} ---")

        # 3. Chama a IA para extrair as fórmulas do texto original do capítulo
        extractor_vars = {"text_to_scan": chapter_text}
        formulas_str_raw, _ = _call_llm_with_tracking(FORMULA_EXTRACTOR_PROMPT, extractor_vars, temperature=0.0)

        # 4. Processa a resposta da IA de forma robusta
        try:
            json_match = re.search(r'\[.*\]', formulas_str_raw, re.DOTALL)
            if json_match:
                clean_json_str = json_match.group(0)
                formulas_encontradas = json.loads(clean_json_str)
            else:
                formulas_encontradas = []
        except json.JSONDecodeError:
            formulas_encontradas = []
            print(f"   - AVISO: Resposta da IA para este capítulo não era um JSON válido: '{formulas_str_raw}'")
        
        resultados_auditoria[capitulo_id] = formulas_encontradas
        if formulas_encontradas:
            print(f"   - Fórmulas encontradas: {len(formulas_encontradas)}")
            total_formulas_encontradas += len(formulas_encontradas)
        else:
            print("   - Nenhuma fórmula explícita encontrada.")

    # 5. Imprime o relatório final
    print("\n\n" + "="*80)
    print("RELATÓRIO FINAL DA AUDITORIA DE FÓRMULAS")
    print("="*80)
    for capitulo, formulas in resultados_auditoria.items():
        print(f"\n[ CAPÍTULO: {capitulo} ]")
        if formulas:
            for i, formula in enumerate(formulas):
                print(f"  {i+1}. {formula}")
        else:
            print("  Nenhuma fórmula explícita encontrada.")
    
    print("\n" + "="*80)
    print(f"Total de Fórmulas Encontradas em Todo o Livro: {total_formulas_encontradas}")
    print("="*80)


if __name__ == "__main__":
    # Tenta encontrar o livro automaticamente na pasta de originais
    try:
        livro_path_default = os.path.join(config.PASTA_LIVROS_ORIGINAIS, [f for f in os.listdir(config.PASTA_LIVROS_ORIGINAIS) if f.endswith('.docx')][0])
    except (FileNotFoundError, IndexError):
        livro_path_default = None

    # Pega o caminho do arquivo do argumento da linha de comando ou usa o padrão
    if len(sys.argv) > 1:
        livro_path_arg = sys.argv[1]
    elif livro_path_default:
        livro_path_arg = livro_path_default
    else:
        print("ERRO: Nenhum arquivo .docx encontrado na pasta 'livros_originais/'.")
        print("Uso: python auditoria_formulas.py [caminho_para_o_livro.docx]")
        sys.exit(1)

    if not os.path.exists(livro_path_arg):
        print(f"ERRO: O arquivo especificado não foi encontrado: {livro_path_arg}")
        sys.exit(1)
        
    auditar_formulas_do_livro(livro_path_arg)