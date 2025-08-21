import os
import re
import sys
import config
import json
from modules.utils import find_book_file, extrair_numeros_ord
from modules.ingestion import extract_chapters_from_word, get_text_chunks
from modules.rag_builder import create_chapter_vector_store, get_key_concepts
from modules.generation import generate_structured_summary, generate_exercises
from modules.formatting import markdown_to_latex_string
from modules.preambulo import PREAMBULO_TEX_CONTENT, MAIN_TEX_TEMPLATE
from modules.preprocessar_formulas import criar_mapa_de_formulas

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

def main():
    """Orquestra o pipeline completo de processamento do livro."""
    livro_path, livro_nome = find_book_file(config.PASTA_LIVROS_ORIGINAIS)
    if not livro_path:
        sys.exit(1)

    print(f">>> INICIANDO PROCESSAMENTO PARA O LIVRO: '{livro_nome}' <<<")

    # Criação de pastas e extração de fórmulas
    pasta_livro_resultado = os.path.join(config.PASTA_RESULTADOS, livro_nome)
    pasta_md_capitulos = os.path.join(pasta_livro_resultado, "md_por_capitulo")
    pasta_tex_capitulos = os.path.join(pasta_livro_resultado, "tex_por_capitulo")
    pasta_final_tex = os.path.join(pasta_livro_resultado, f"tex_{livro_nome}")

    os.makedirs(pasta_md_capitulos, exist_ok=True)
    os.makedirs(pasta_tex_capitulos, exist_ok=True)
    os.makedirs(pasta_final_tex, exist_ok=True)

    caminho_mapa = os.path.join(pasta_livro_resultado, "mapa_de_formulas.json")
    if not os.path.exists(caminho_mapa):
        print("\n" + "="*80)
        print(f"AVISO: Mapa de fórmulas não encontrado.")
        print("ACIONANDO SCRIPT DE PRÉ-PROCESSAMENTO AUTOMATICAMENTE...")
        print("="*80)
        criar_mapa_de_formulas(livro_path, livro_nome)

    with open(caminho_mapa, "r", encoding="utf-8") as f:
        formula_map = json.load(f)
    print(f"   - Mapa com {len(formula_map)} fórmulas carregado com sucesso.")

    pipeline_total_tokens = {"prompt": 0, "completion": 0, "total": 0, "cost_usd": 0.0}

    chapters = extract_chapters_from_word(livro_path)
    if not chapters:
        return

    for chapter_data in sorted(chapters, key=lambda d: (d['unit'], d['chapter'])):
        unit, chap, title, chapter_text = chapter_data.values()
        print(f"\n--- PROCESSANDO: Unidade {unit} - Capítulo {chap} ('{title}') ---")

        chapter_title_md = f"# Unidade {unit} - Capítulo {chap}: {title}"
        chunks = get_text_chunks(chapter_text)
        if not chunks:
            print("   - AVISO: Capítulo vazio. Pulando.")
            continue

        # --- SEÇÃO MODIFICADA ---
        vector_store = create_chapter_vector_store(chunks)

        base_retriever = vector_store.as_retriever(search_kwargs={"k": 20})

        model = HuggingFaceCrossEncoder(model_name='cross-encoder/ms-marco-MiniLM-L-6-v2')
        compressor = CrossEncoderReranker(model=model, top_n=5)

        retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
        print(f"   - RAG para U{unit}-C{chap} criado com re-ranking (Cross-Encoder).")
        # --- FIM DA SEÇÃO MODIFICADA ---

        key_concepts, tokens = get_key_concepts(chapter_text, livro_nome)
        if not key_concepts:
            print("   - AVISO: Não foi possível extrair conceitos-chave para este capítulo.")
            continue
        for key in pipeline_total_tokens: pipeline_total_tokens[key] += tokens.get(key, 0)

        summary, tokens = generate_structured_summary(retriever, key_concepts, livro_nome)
        for key in pipeline_total_tokens: pipeline_total_tokens[key] += tokens.get(key, 0)

        exercises, tokens = generate_exercises(retriever, key_concepts, formula_map, unit, chap)
        for key in pipeline_total_tokens: pipeline_total_tokens[key] += tokens.get(key, 0)

        # ... (o resto do arquivo continua exatamente igual) ...
        chapter_markdown_content = f"{chapter_title_md}\n\n{summary}\n\n{exercises}"

        md_capitulo_path = os.path.join(pasta_md_capitulos, f"U{unit}_C{chap}.md")
        with open(md_capitulo_path, "w", encoding="utf-8") as f:
            f.write(chapter_markdown_content)
        print(f"   - Markdown do capítulo salvo em: {md_capitulo_path}")

        print(f"   - Convertendo U{unit}-C{chap}.md para snippet LaTeX...")
        latex_snippet = markdown_to_latex_string(chapter_markdown_content)

        tex_capitulo_path = os.path.join(pasta_tex_capitulos, f"U{unit}_C{chap}.tex")
        with open(tex_capitulo_path, "w", encoding="utf-8") as f:
            f.write(latex_snippet)
        print(f"   - Snippet LaTeX salvo em: {tex_capitulo_path}")

        
    # 1. Pega a lista ordenada de snippets .tex
    nomes_arquivos_tex = sorted(
        [f for f in os.listdir(pasta_tex_capitulos) if f.endswith('.tex')],
        key=extrair_numeros_ord
    )

    # 2. Junta os conteúdos, adicionando os comandos de unidade/capítulo
    partes_latex = []
    current_unit = 0
    for nome_arquivo in nomes_arquivos_tex:
        unidade, capitulo = extrair_numeros_ord(nome_arquivo)

        if unidade > current_unit:
            partes_latex.append("\\iniciarunidade")
            current_unit = unidade
        elif not (unidade == 1 and capitulo == 1):
             partes_latex.append("\\newpage")
        
        with open(os.path.join(pasta_tex_capitulos, nome_arquivo), "r", encoding="utf-8") as f:
            partes_latex.append(f.read())

    final_latex_body = "\n\n".join(partes_latex)

    # 3. Monta o arquivo final
    final_tex_content = MAIN_TEX_TEMPLATE.replace("{BODY_PLACEHOLDER}", final_latex_body)
    final_tex_content = final_tex_content.replace("{BOOK_NAME_PLACEHOLDER}", livro_nome.replace('_', ' '))

    # 4. Salva os arquivos finais
    tex_completo_path = os.path.join(pasta_final_tex, "Livro_Completo.tex")
    with open(tex_completo_path, "w", encoding="utf-8") as f:
        f.write(final_tex_content)

    with open(os.path.join(pasta_final_tex, "preambulo.tex"), "w", encoding="utf-8") as f:
        f.write(PREAMBULO_TEX_CONTENT)


    print("\n" + "="*50)
    print(">>> RELATÓRIO FINAL DE USO DE TOKENS DO PIPELINE <<<")
    print(f"   - Tokens de Prompt: {pipeline_total_tokens['prompt']:,}")
    print(f"   - Tokens de Conclusão: {pipeline_total_tokens['completion']:,}")
    print(f"   - Total de Tokens: {pipeline_total_tokens['total']:,}")
    print(f"   - Custo Estimado (USD): ${pipeline_total_tokens['cost_usd']:.6f}")
    print("="*50)

if __name__ == "__main__":
    main()