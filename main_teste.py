import os
import re
import sys
import json
import config
from modules.utils import find_book_file, extrair_numeros_ord
from modules.ingestion import extract_chapters_from_word, get_text_chunks
from modules.rag_builder import create_chapter_vector_store, get_key_concepts
from modules.generation import generate_structured_summary, generate_exercises
from modules.formatting import markdown_to_latex_string
from modules.preambulo import PREAMBULO_TEX_CONTENT, MAIN_TEX_TEMPLATE
from modules.preprocessar_formulas import criar_mapa_de_formulas

def main():
    """Orquestra o pipeline para um único capítulo para fins de teste."""
    livro_path, livro_nome = find_book_file(config.PASTA_LIVROS_ORIGINAIS)
    if not livro_path:
        sys.exit(1)

    print(f">>> INICIANDO PROCESSAMENTO PARA O LIVRO (MODO DE TESTE - 1 CAPÍTULO): '{livro_nome}' <<<")

    pasta_livro_resultado = os.path.join(config.PASTA_RESULTADOS, livro_nome)
    pasta_md_capitulos = os.path.join(pasta_livro_resultado, "md_por_capitulo")
    pasta_tex_capitulos = os.path.join(pasta_livro_resultado, "tex_por_capitulo")
    pasta_final_tex = os.path.join(pasta_livro_resultado, f"tex_{livro_nome}")

    os.makedirs(pasta_md_capitulos, exist_ok=True)
    os.makedirs(pasta_tex_capitulos, exist_ok=True)
    os.makedirs(pasta_final_tex, exist_ok=True)

    caminho_mapa = os.path.join(pasta_livro_resultado, "mapa_de_formulas.json")
    if not os.path.exists(caminho_mapa):
        print("\nAVISO: Mapa de fórmulas não encontrado. Acionando script de pré-processamento...")
        criar_mapa_de_formulas(livro_path, livro_nome)
    
    with open(caminho_mapa, "r", encoding="utf-8") as f:
        formula_map = json.load(f)
    print(f"   - Mapa com {len(formula_map)} fórmulas carregado com sucesso.")

    chapters = extract_chapters_from_word(livro_path)
    if not chapters:
        return

    # --- LOOP DE TESTE: PROCESSA APENAS O PRIMEIRO CAPÍTULO ---
    for chapter_data in sorted(chapters, key=lambda d: (d['unit'], d['chapter'])):
        unit, chap, title, chapter_text = chapter_data.values()
        
        print(f"\n--- PROCESSANDO: Unidade {unit} - Capítulo {chap} ('{title}') ---")

        chapter_title_md = f"# Unidade {unit} - Capítulo {chap}: {title}"
        chunks = get_text_chunks(chapter_text)
        if not chunks:
            print("   - AVISO: Capítulo vazio. Pulando.")
            continue
        
        vector_store = create_chapter_vector_store(chunks)
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        print(f"   - RAG para U{unit}-C{chap} criado.")

        key_concepts, _ = get_key_concepts(chapter_text, livro_nome)
        summary, _ = generate_structured_summary(retriever, key_concepts, livro_nome)
        exercises, _ = generate_exercises(retriever, key_concepts, formula_map)

        chapter_markdown_content = f"{chapter_title_md}\n\n{summary}\n\n{exercises}"

        md_capitulo_path = os.path.join(pasta_md_capitulos, f"U{unit}_C{chap}.md")
        with open(md_capitulo_path, "w", encoding="utf-8") as f:
            f.write(chapter_markdown_content)
        print(f"   - Markdown do capítulo salvo em: {md_capitulo_path}")

        # --- CONVERSÃO IMEDIATA PARA .TEX (SEGUINDO A NOVA ARQUITETURA) ---
        print(f"   - Convertendo U{unit}-C{chap}.md para snippet LaTeX...")
        latex_snippet = markdown_to_latex_string(chapter_markdown_content)
        
        tex_capitulo_path = os.path.join(pasta_tex_capitulos, f"U{unit}_C{chap}.tex")
        with open(tex_capitulo_path, "w", encoding="utf-8") as f:
            f.write(latex_snippet)
        print(f"   - Snippet LaTeX salvo em: {tex_capitulo_path}")

        print("\n>>> MODO DE TESTE: Processando apenas o primeiro capítulo e encerrando o loop. <<<")
        break # Encerra o loop após o primeiro capítulo

    # --- MONTAGEM FINAL DE TESTE (USANDO O SNIPPET GERADO) ---
    print("\n--- MONTANDO E SALVANDO ARQUIVOS FINAIS (COM APENAS 1 CAPÍTULO) ---")
    
    nomes_arquivos_tex = sorted(
        [f for f in os.listdir(pasta_tex_capitulos) if f.endswith('.tex') and f.startswith(f"U{unit}_C{chap}")],
        key=extrair_numeros_ord
    )
    
    if not nomes_arquivos_tex:
        print("ERRO: Nenhum snippet .tex de teste foi encontrado para a montagem.")
        return

    # Lê o conteúdo do único snippet gerado
    with open(os.path.join(pasta_tex_capitulos, nomes_arquivos_tex[0]), "r", encoding="utf-8") as f:
        final_latex_body = f.read()
    
    final_tex_content = MAIN_TEX_TEMPLATE.replace("{BODY_PLACEHOLDER}", final_latex_body)
    final_tex_content = final_tex_content.replace("{BOOK_NAME_PLACEHOLDER}", livro_nome.replace('_', ' '))
    
    tex_completo_path = os.path.join(pasta_final_tex, "Livro_Teste_Completo.tex")
    with open(tex_completo_path, "w", encoding="utf-8") as f:
        f.write(final_tex_content)
    
    with open(os.path.join(pasta_final_tex, "preambulo.tex"), "w", encoding="utf-8") as f:
        f.write(PREAMBULO_TEX_CONTENT)

    print(f"Arquivo LaTeX de teste salvo com sucesso em: {tex_completo_path}")

if __name__ == "__main__":
    main()