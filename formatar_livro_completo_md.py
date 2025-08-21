import sys
import os
import re
from modules.formatting import markdown_to_latex_string
from modules.preambulo import PREAMBULO_TEX_CONTENT, MAIN_TEX_TEMPLATE

def extrair_numeros(nome_arquivo):
    match = re.search(r'U(\d+)_C(\d+)', nome_arquivo)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (0, 0)

def formatar_livro_de_md(caminho_pasta_md: str):
    print(f">>> INICIANDO FORMATAÇÃO PARA A PASTA: {caminho_pasta_md} <<<")
    if not os.path.isdir(caminho_pasta_md):
        print(f"ERRO: A pasta '{caminho_pasta_md}' não foi encontrada.")
        return

    nomes_arquivos_md = sorted(
        [f for f in os.listdir(caminho_pasta_md) if f.endswith('.md')],
        key=extrair_numeros
    )
    if not nomes_arquivos_md:
        print(f"ERRO: Nenhum arquivo .md encontrado na pasta '{caminho_pasta_md}'.")
        return
        
    print(f"   - {len(nomes_arquivos_md)} arquivos de capítulo encontrados e ordenados.")

    # NOVA LÓGICA: Processa cada capítulo e junta os resultados em LaTeX
    partes_latex = []
    current_unit = 0
    for nome_arquivo in nomes_arquivos_md:
        unidade, capitulo = extrair_numeros(nome_arquivo)

        # Adiciona os comandos de nova unidade/capítulo em LaTeX DIRETAMENTE
        if unidade > current_unit:
            if unidade > 1: # Não adiciona \iniciarunidade antes da primeira
                partes_latex.append(f"\\iniciarunidade{{{unidade}}}")
            current_unit = unidade
        elif not (unidade == 1 and capitulo == 1):
             partes_latex.append("\\newpage")
        
        caminho_completo = os.path.join(caminho_pasta_md, nome_arquivo)
        with open(caminho_completo, "r", encoding="utf-8") as f:
            markdown_capitulo = f.read()
        
        print(f"   - Formatando U{unidade}-C{capitulo}...")
        # Chama a função de formatação para cada capítulo individualmente
        latex_capitulo = markdown_to_latex_string(markdown_capitulo)
        partes_latex.append(latex_capitulo)

    # Junta todas as partes de LaTeX formatadas
    final_latex_body = "\n\n".join(partes_latex)
    print("   - Todo o conteúdo LaTeX foi consolidado.")

    # Define os caminhos de saída
    nome_livro = os.path.basename(os.path.dirname(caminho_pasta_md))
    pasta_saida = os.path.join("resultados", "teste_livro_completo_de_md", nome_livro)
    os.makedirs(pasta_saida, exist_ok=True)
    
    caminho_saida_tex = os.path.join(pasta_saida, "Livro_Completo.tex")
    caminho_saida_preambulo = os.path.join(pasta_saida, "preambulo.tex")

    # Monta e salva os arquivos .tex finais
    print("   - Montando o arquivo .tex final...")
    final_tex_content = MAIN_TEX_TEMPLATE.replace("{BODY_PLACEHOLDER}", final_latex_body)
    final_tex_content = final_tex_content.replace("{BOOK_NAME_PLACEHOLDER}", nome_livro.replace('_', ' '))
    
    with open(caminho_saida_tex, "w", encoding="utf-8") as f:
        f.write(final_tex_content)
    
    with open(caminho_saida_preambulo, "w", encoding="utf-8") as f:
        f.write(PREAMBULO_TEX_CONTENT)

    print("\n--- SUCESSO! ---")
    print(f"Arquivo LaTeX de teste salvo em: {caminho_saida_tex}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERRO: Forneça o caminho para a PASTA que contém os arquivos .md dos capítulos.")
        print("Exemplo de uso:")
        print("python formatar_livro_completo_md.py \"resultados/Matematica Financeira/md_Matematica Financeira\"")
    else:
        formatar_livro_de_md(sys.argv[1])