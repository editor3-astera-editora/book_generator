# converter.py
import os
import argparse
import sys
from modules.formatting import markdown_to_latex_string
from modules.preambulo import PREAMBULO_TEX_CONTENT, MAIN_TEX_TEMPLATE

def convert_file(input_path: str, output_path: str, book_name: str):
    """
    Lê um arquivo Markdown, aplica a conversão para LaTeX customizado e
    salva o resultado em um arquivo .tex final com seu preâmbulo.
    """
    print(f"--- Iniciando conversão ---")
    print(f"  > Arquivo de entrada: {input_path}")
    print(f"  > Arquivo de saída:   {output_path}")
    print(f"  > Nome do Livro:      {book_name}")

    # 1. Valida se o arquivo de entrada existe
    if not os.path.exists(input_path):
        print(f"\nERRO: O arquivo de entrada não foi encontrado em '{input_path}'")
        sys.exit(1)

    # 2. Cria o diretório de saída se ele не existir
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"  > Diretório de saída criado: {output_dir}")

    # 3. Lê o conteúdo do arquivo Markdown
    with open(input_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # 4. Converte o corpo do Markdown para o corpo do LaTeX
    final_latex_body = markdown_to_latex_string(markdown_content)

    # 5. Monta o arquivo .tex principal usando o template
    final_tex_content = MAIN_TEX_TEMPLATE.replace("{BODY_PLACEHOLDER}", final_latex_body)
    final_tex_content = final_tex_content.replace("{BOOK_NAME_PLACEHOLDER}", book_name)

    # 6. Salva o preambulo.tex na mesma pasta do arquivo .tex final
    preambulo_path = os.path.join(output_dir, "preambulo.tex")
    with open(preambulo_path, "w", encoding="utf-8") as f:
        f.write(PREAMBULO_TEX_CONTENT)
    print(f"  > Arquivo 'preambulo.tex' salvo em: {preambulo_path}")

    # 7. Salva o arquivo .tex completo
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_tex_content)
    print(f"  > Arquivo LaTeX completo salvo em: {output_path}")

    print("\n--- Conversão concluída com sucesso! ---")


if __name__ == "__main__":
    # Configura o parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Converte um arquivo Markdown completo para LaTeX com formatação customizada."
    )
    parser.add_argument(
        "input_file",
        help="O caminho para o arquivo .md de entrada (ex: 'resultados/MeuLivro/md_MeuLivro/Livro_Completo.md')"
    )
    parser.add_argument(
        "output_file",
        help="O caminho para o arquivo .tex de saída (ex: 'resultados/MeuLivro/tex_MeuLivro/Livro_Final.tex')"
    )
    parser.add_argument(
        "--book-name",
        default="Título do Livro",
        help="O nome do livro para ser usado nos rodapés do LaTeX (ex: 'Matemática Financeira')"
    )

    args = parser.parse_args()

    # Chama a função principal com os argumentos fornecidos
    convert_file(args.input_file, args.output_file, args.book_name)