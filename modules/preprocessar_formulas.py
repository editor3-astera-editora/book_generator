import sys
import os
import re
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from .ingestion import extract_chapters_from_word
from .generation import _call_llm_with_tracking
from .prompts import FORMULA_MAPPING_PROMPT
from .utils import find_book_file

def criar_mapa_de_formulas(docx_path: str, book_name: str):
    """
    Lê um livro, extrai/filtra/mapeia todas as fórmulas e salva um mapa em JSON.
    """
    print("="*80)
    print(f"INICIANDO PRÉ-PROCESSAMENTO DE FÓRMULAS PARA O LIVRO: {book_name}")
    print("="*80)

    chapters = extract_chapters_from_word(docx_path)
    if not chapters:
        return

    mapa_de_formulas_completo = []
    
    for chapter_data in sorted(chapters, key=lambda d: (d['unit'], d['chapter'])):
        unit, chap, title, chapter_text = chapter_data.values()
        capitulo_id = f"U{unit}-C{chap}"
        print(f"\n--- Processando Capítulo: {capitulo_id}: {title} ---")

        if not chapter_text.strip():
            print("   - Capítulo vazio. Pulando.")
            continue

        input_vars = {"chapter_text": chapter_text}
        response_str, _ = _call_llm_with_tracking(FORMULA_MAPPING_PROMPT, input_vars, temperature=0.0)

        try:
            json_match = re.search(r'\[.*\]', response_str, re.DOTALL)
            if json_match:
                formulas_do_capitulo = json.loads(json_match.group(0))
                if formulas_do_capitulo:
                    print(f"   - {len(formulas_do_capitulo)} fórmulas encontradas e mapeadas.")
                    for formula_info in formulas_do_capitulo:
                        formula_info['source_chapter'] = capitulo_id
                    mapa_de_formulas_completo.extend(formulas_do_capitulo)
                else:
                    print("   - Nenhuma fórmula geral encontrada neste capítulo.")
        except json.JSONDecodeError:
            print(f"   - AVISO: Não foi possível decodificar a resposta JSON: '{response_str}'")

    pasta_livro_resultado = os.path.join(config.PASTA_RESULTADOS, book_name)
    os.makedirs(pasta_livro_resultado, exist_ok=True)
    caminho_mapa = os.path.join(pasta_livro_resultado, "mapa_de_formulas.json")

    with open(caminho_mapa, "w", encoding="utf-8") as f:
        json.dump(mapa_de_formulas_completo, f, ensure_ascii=False, indent=2)

    print("\n" + "="*80)
    print(f"SUCESSO! Mapa de Fórmulas salvo em: {caminho_mapa}")
    print("="*80)

if __name__ == "__main__":
    livro_path, livro_nome = find_book_file(config.PASTA_LIVROS_ORIGINAIS)
    if not livro_path:
        sys.exit(1)
    criar_mapa_de_formulas(livro_path, livro_nome)