import os
import sys
import config
import json
import shutil
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

from modules.utils import find_book_file, extrair_numeros_ord
from modules.ingestion import extract_chapters_from_word, get_text_chunks
from modules.rag_builder import create_chapter_vector_store, get_key_concepts
from modules.generation import generate_structured_summary, generate_exercises, generate_figure_caption
from modules.formatting import markdown_to_latex_string
from modules.preambulo import PREAMBULO_TEX_CONTENT, MAIN_TEX_TEMPLATE
from modules.preprocessar_formulas import criar_mapa_de_formulas

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
 
def processar_capitulo_worker(chapter_data, livro_nome, formula_map):
    """
    Processa um único capítulo. Esta função é executada em um worker paralelo.
    """
    try:
        unit, chap, title, chapter_text = chapter_data.values()
        log_prefix = f"[U{unit}-C{chap}]"
        logging.info(f"{log_prefix} Iniciando processamento para '{title}'.")

        chapter_title_md = f"# Unidade {unit} - Capítulo {chap}: {title}"
        chunks = get_text_chunks(chapter_text)
        if not chunks:
            logging.warning(f"{log_prefix} Capítulo vazio. Pulando.")
            return None
        
        # --- Seção RAG ---
        vector_store = create_chapter_vector_store(chunks)
        base_retriever = vector_store.as_retriever(search_kwargs={"k": 20})
        model = HuggingFaceCrossEncoder(model_name='cross-encoder/ms-marco-MiniLM-L-6-v2')
        compressor = CrossEncoderReranker(model=model, top_n=5)
        retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=base_retriever)
        logging.info(f"{log_prefix} RAG criado com sucesso.")

        # --- Seção de Geração (chamadas de API) ---
        chapter_tokens = {"prompt": 0, "completion": 0, "total": 0, "cost_usd": 0.0}

        figure_caption = None
        if chap == 1:
            caption, tokens = generate_figure_caption(title)
            figure_caption = caption
            for key in chapter_tokens: chapter_tokens[key] += tokens.get(key, 0)

        key_concepts, tokens = get_key_concepts(chapter_text, livro_nome)
        if not key_concepts:
            logging.warning(f"{log_prefix} Não foi possível extrair conceitos-chave.")
            return None
        for key in chapter_tokens: chapter_tokens[key] += tokens.get(key, 0)

        summary, tokens = generate_structured_summary(retriever, key_concepts, livro_nome)
        for key in chapter_tokens: chapter_tokens[key] += tokens.get(key, 0)

        exercises, tokens = generate_exercises(retriever, key_concepts, formula_map, unit, chap)
        for key in chapter_tokens: chapter_tokens[key] += tokens.get(key, 0)

        # --- Formatação Final ---
        chapter_markdown_content = f"{chapter_title_md}\n\n{summary}\n\n{exercises}"

        latex_snippet = markdown_to_latex_string(
            markdown_text=chapter_markdown_content,
            unit_number=unit,
            chapter_number=chap,
            figure_caption=figure_caption
            )
        
        logging.info(f"{log_prefix} Processamento concluído com sucesso.")

        return {
            "unit": unit,
            "chap": chap,
            "markdown_content": chapter_markdown_content,
            "latex_snippet": latex_snippet,
            "tokens": chapter_tokens
        }
    except Exception as e:
        unit = chapter_data.get('unit', 'Desconhecida')
        chap = chapter_data.get('chapter', 'Desconhecido')
        # Salva o erro completo no log, incluindo o traceback
        logging.error(f"[U{unit}-C{chap}] ERRO CRÍTICO ao processar capítulo", exc_info=True)
        return None

def processar_livro(livro_path, livro_nome):
    """
    Orquestra o pipeline completo de processamento para um único livro.
    """
    logging.info(f"================ INICIANDO PROCESSAMENTO PARA O LIVRO: '{livro_nome}' ================")

    # Criação de pastas e carregamento de mapa de fórmulas
    pasta_livro_resultado = os.path.join(config.PASTA_RESULTADOS, livro_nome)
    pasta_md_capitulos = os.path.join(pasta_livro_resultado, "md_por_capitulo")
    pasta_tex_capitulos = os.path.join(pasta_livro_resultado, "tex_por_capitulo")
    pasta_final_tex = os.path.join(pasta_livro_resultado, f"tex_{livro_nome}")
    os.makedirs(pasta_md_capitulos, exist_ok=True)
    os.makedirs(pasta_tex_capitulos, exist_ok=True)
    os.makedirs(pasta_final_tex, exist_ok=True)

    caminho_mapa = os.path.join(pasta_livro_resultado, "mapa_de_formulas.json")
    if not os.path.exists(caminho_mapa):
        logging.warning("Mapa de fórmulas não encontrado. Acionando script de pré-processamento...")
        criar_mapa_de_formulas(livro_path, livro_nome)
    with open(caminho_mapa, "r", encoding="utf-8") as f:
        formula_map = json.load(f)
    logging.info(f"Mapa com {len(formula_map)} fórmulas carregado com sucesso.")

    pipeline_total_tokens = {"prompt": 0, "completion": 0, "total": 0, "cost_usd": 0.0}
    chapters = extract_chapters_from_word(livro_path)
    if not chapters:
        logging.error(f"Não foi possível extrair capítulos do livro '{livro_nome}'. Pulando.")
        return

    MAX_WORKERS = 5
    resultados_capitulos = []
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(processar_capitulo_worker, chapter_data, livro_nome, formula_map) for chapter_data in chapters]
        for future in as_completed(futures):
            resultado = future.result()
            if resultado:
                resultados_capitulos.append(resultado)

    logging.info("Todos os capítulos foram processados. Iniciando montagem final.")
    
    resultados_capitulos.sort(key=lambda r: (r['unit'], r['chap']))

    for resultado in resultados_capitulos:
        unit, chap = resultado['unit'], resultado['chap']
        
        for key in pipeline_total_tokens:
            pipeline_total_tokens[key] += resultado['tokens'].get(key, 0)

        md_capitulo_path = os.path.join(pasta_md_capitulos, f"U{unit}_C{chap}.md")
        with open(md_capitulo_path, "w", encoding="utf-8") as f:
            f.write(resultado['markdown_content'])
        
        tex_capitulo_path = os.path.join(pasta_tex_capitulos, f"U{unit}_C{chap}.tex")
        with open(tex_capitulo_path, "w", encoding="utf-8") as f:
            f.write(resultado['latex_snippet'])
        logging.info(f"Artefatos salvos para: U{unit}-C{chap}")

    nomes_arquivos_tex = sorted(
        [f for f in os.listdir(pasta_tex_capitulos) if f.endswith('.tex')],
        key=extrair_numeros_ord
    )
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

    book_title = livro_nome.replace('_', ' ')

     # Prepara o conteúdo do arquivo .tex principal substituindo o placeholder CORRETO
    final_tex_content = MAIN_TEX_TEMPLATE.replace("{BODY_PLACEHOLDER}", final_latex_body)
    final_tex_content = final_tex_content.replace("{livro_nome}", book_title) # CORRIGIDO
    # Salva o Livro_Completo.tex processado
    tex_completo_path = os.path.join(pasta_final_tex, "Livro_Completo.tex")
    with open(tex_completo_path, "w", encoding="utf-8") as f:
        f.write(final_tex_content)
        
    with open(os.path.join(pasta_final_tex, "preambulo.tex"), "w", encoding="utf-8") as f:
        f.write(PREAMBULO_TEX_CONTENT)

    # Log do relatório final
    logging.info(f"--- RELATÓRIO FINAL PARA '{livro_nome}' ---")
    logging.info(f"  - Tokens de Prompt: {pipeline_total_tokens['prompt']:,}")
    logging.info(f"  - Tokens de Conclusão: {pipeline_total_tokens['completion']:,}")
    logging.info(f"  - Total de Tokens: {pipeline_total_tokens['total']:,}")
    logging.info(f"  - Custo Estimado (USD): ${pipeline_total_tokens['cost_usd']:.6f}")
    
    try:
        caminho_relatorio = os.path.join(pasta_livro_resultado, "relatorio_de_custos.txt")
        report_content = (
            f">>> RELATÓRIO FINAL PARA '{livro_nome}' <<<\n"
            f"--------------------------------------------------\n"
            f"Tokens de Prompt: {pipeline_total_tokens['prompt']:,}\n"
            f"Tokens de Conclusão: {pipeline_total_tokens['completion']:,}\n"
            f"Total de Tokens: {pipeline_total_tokens['total']:,}\n"
            f"Custo Estimado (USD): ${pipeline_total_tokens['cost_usd']:.6f}\n"
        )
        with open(caminho_relatorio, "w", encoding="utf-8") as f:
            f.write(report_content)
        logging.info(f"  - Relatório de custos salvo em: {caminho_relatorio}")
    except Exception as e:
        logging.warning(f"Não foi possível salvar o arquivo de relatório de custos. Erro: {e}")
    logging.info("-" * 40)

def main():
    """
    Gerencia a fila de livros, processando um por um até a pasta de origem ficar vazia.
    """
    # --- Configuração do Logging ---
    # Cria um logger para o arquivo e outro para o console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("processamento_livros.log", mode='w'), # 'w' para sobrescrever o log a cada execução
            logging.StreamHandler()
        ]
    )
    logging.info("Iniciando o sistema de processamento de livros.")
    
    pasta_feito = os.path.join(os.path.dirname(config.PASTA_LIVROS_ORIGINAIS), "FEITO")
    os.makedirs(pasta_feito, exist_ok=True)

    while True:
        livro_path, livro_nome = find_book_file(config.PASTA_LIVROS_ORIGINAIS)
        
        if not livro_path:
            logging.info("Fila vazia. Todos os livros foram processados.")
            break

        try:
            processar_livro(livro_path, livro_nome)
            
            nome_arquivo_original = os.path.basename(livro_path)
            caminho_destino = os.path.join(pasta_feito, nome_arquivo_original)
            
            logging.info(f"Processamento de '{livro_nome}' concluído. Movendo para a pasta 'FEITO'.")
            shutil.move(livro_path, caminho_destino)

        except Exception as e:
            logging.critical(f"ERRO CRÍTICO no processamento do livro '{livro_nome}'. O script será encerrado.", exc_info=True)
            sys.exit(1)

if __name__ == "__main__":
    main()