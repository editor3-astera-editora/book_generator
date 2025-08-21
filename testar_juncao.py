import os
import re

# ==============================================================================
# CONFIGURAÇÃO DO TESTE
# Estas variáveis simulam o estado do seu script principal no momento da junção.
# ==============================================================================
LIVRO_NOME = "Desenho técnico de plantas arquitetônicas em CAD"
PASTA_RESULTADOS = "resultados"

# Recriando a lógica de caminhos exatamente como em main.py
pasta_livro_resultado = os.path.join(PASTA_RESULTADOS, LIVRO_NOME)
pasta_tex_capitulos = os.path.join(pasta_livro_resultado, "tex_por_capitulo")
pasta_final_tex = os.path.join(pasta_livro_resultado, f"tex_{LIVRO_NOME}")
arquivo_saida_teste = os.path.join(pasta_final_tex, "TESTE_Livro_Completo.tex")

# ==============================================================================
# FUNÇÕES AUXILIARES
# Copiadas ou recriadas a partir do seu projeto para garantir consistência.
# ==============================================================================

def extrair_numeros_ord(nome_arquivo):
    """
    Recriação da função para extrair (Unidade, Capitulo) do nome do arquivo
    para ordenação correta. Ex: 'U1_C10.tex' -> (1, 10)
    """
    match = re.search(r'U(\d+)_C(\d+)', nome_arquivo)
    if match:
        unidade = int(match.group(1))
        capitulo = int(match.group(2))
        return (unidade, capitulo)
    return (0, 0) # Fallback para arquivos com nomes inesperados

# Simulação do template principal para o teste.
MAIN_TEX_TEMPLATE_TESTE = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\title{ARQUIVO DE TESTE: {BOOK_NAME_PLACEHOLDER}}
\\author{Script de Teste de Junção}
\\date{\\today}
\\begin{document}
\\maketitle

% --- INÍCIO DO CONTEÚDO DOS CAPÍTULOS ---
{BODY_PLACEHOLDER}
% --- FIM DO CONTEÚDO DOS CAPÍTULOS ---

\\end{document}
"""

# ==============================================================================
# LÓGICA PRINCIPAL DO TESTE
# ==============================================================================

print("="*60)
print("INICIANDO SCRIPT DE TESTE DE JUNÇÃO DE ARQUIVOS LATEX")
print("="*60)

# 1. Verificar se a pasta de snippets existe
print(f"\n[PASSO 1] Verificando a pasta de snippets...")
print(f"    - Caminho alvo: '{pasta_tex_capitulos}'")

if not os.path.isdir(pasta_tex_capitulos):
    print("\n[ERRO FATAL] A pasta de snippets não foi encontrada.")
    print("    - Verifique se o nome do livro e a estrutura de pastas estão corretos.")
    exit()
else:
    print("    - SUCESSO: Pasta encontrada.")

# 2. Tentar listar os arquivos na pasta
print(f"\n[PASSO 2] Listando todos os arquivos na pasta de snippets...")
try:
    todos_os_arquivos = os.listdir(pasta_tex_capitulos)
    print(f"    - SUCESSO: {len(todos_os_arquivos)} arquivos/pastas encontrados.")
    print(f"    - Conteúdo: {todos_os_arquivos}")
except Exception as e:
    print(f"\n[ERRO FATAL] Falha ao tentar listar arquivos: {e}")
    exit()

# 3. Filtrar e ordenar os arquivos .tex
print("\n[PASSO 3] Filtrando e ordenando os arquivos .tex...")
arquivos_tex_filtrados = [f for f in todos_os_arquivos if f.endswith('.tex')]
print(f"    - Arquivos .tex encontrados ({len(arquivos_tex_filtrados)}): {arquivos_tex_filtrados}")

if not arquivos_tex_filtrados:
    print("\n[ERRO] Nenhum arquivo .tex foi encontrado na pasta. A junção não pode continuar.")
else:
    print("    - Ordenando os arquivos por Unidade e Capítulo...")
    nomes_arquivos_tex_ordenados = sorted(arquivos_tex_filtrados, key=extrair_numeros_ord)
    print(f"    - Ordem final para junção: {nomes_arquivos_tex_ordenados}")

    # 4. Ler e juntar o conteúdo
    print("\n[PASSO 4] Lendo o conteúdo de cada snippet .tex...")
    partes_latex = []
    for nome_arquivo in nomes_arquivos_tex_ordenados:
        caminho_completo = os.path.join(pasta_tex_capitulos, nome_arquivo)
        try:
            with open(caminho_completo, "r", encoding="utf-8") as f:
                conteudo = f.read()
                partes_latex.append(conteudo)
                print(f"    - LIDO: '{nome_arquivo}' ({len(conteudo)} caracteres)")
        except Exception as e:
            print(f"    - ERRO ao ler o arquivo '{nome_arquivo}': {e}")
    
    final_latex_body = "\\n\\n\\newpage\\n\\n".join(partes_latex)
    print(f"\n    - SUCESSO: Conteúdo de {len(partes_latex)} snippets juntado.")
    print(f"    - Tamanho total do corpo do texto: {len(final_latex_body)} caracteres.")

    # 5. Montar e salvar o arquivo final de teste
    print("\n[PASSO 5] Montando e salvando o arquivo .tex de teste...")
    os.makedirs(pasta_final_tex, exist_ok=True) # Garante que a pasta de saída exista
    
    final_tex_content = MAIN_TEX_TEMPLATE_TESTE.replace("{BODY_PLACEHOLDER}", final_latex_body)
    final_tex_content = final_tex_content.replace("{BOOK_NAME_PLACEHOLDER}", LIVRO_NOME)
    
    try:
        with open(arquivo_saida_teste, "w", encoding="utf-8") as f:
            f.write(final_tex_content)
        print(f"    - SUCESSO: Arquivo de teste foi salvo em:")
        print(f"      '{arquivo_saida_teste}'")
    except Exception as e:
        print(f"    - ERRO FATAL ao tentar salvar o arquivo final: {e}")

print("\n" + "="*60)
print("TESTE CONCLUÍDO.")
print("="*60)