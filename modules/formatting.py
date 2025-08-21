import re
from modules.latex_converter import convert_exercise_to_latex, convert_bullets_to_latex

GREEK_SYMBOLS_MAP = {
    'α': r'$\alpha$', 'β': r'$\beta$', 'γ': r'$\gamma$', 'δ': r'$\delta$',
    'ε': r'$\epsilon$', 'ζ': r'$\zeta$', 'η': r'$\eta$', 'θ': r'$\theta$',
    'ι': r'$\iota$', 'κ': r'$\kappa$', 'λ': r'$\lambda$', 'μ': r'$\mu$',
    'ν': r'$\nu$', 'ξ': r'$\xi$', 'ο': r'$o$', 'π': r'$\pi$',
    'ρ': r'$\rho$', 'σ': r'$\sigma$', 'ς': r'$\varsigma$', 'τ': r'$\tau$',
    'υ': r'$\upsilon$', 'φ': r'$\phi$', 'χ': r'$\chi$', 'ψ': r'$\psi$',
    'ω': r'$\omega$',
    'Α': r'$\Alpha$', 'Β': r'$\Beta$', 'Γ': r'$\Gamma$', 'Δ': r'$\Delta$',
    'Ε': r'$\Epsilon$', 'Ζ': r'$\Zeta$', 'Η': r'$\Eta$', 'Θ': r'$\Theta$',
    'Ι': r'$\Iota$', 'Κ': r'$\Kappa$', 'Λ': r'$\Lambda$', 'Μ': r'$\Mu$',
    'Ν': r'$\Nu$', 'Ξ': r'$\Xi$', 'Ο': r'$O$', 'Π': r'$\Pi$',
    'Ρ': r'$\Rho$', 'Σ': r'$\Sigma$', 'Τ': r'$\Tau$', 'Υ': r'$\Upsilon$',
    'Φ': r'$\Phi$', 'Χ': r'$\Chi$', 'Ψ': r'$\Psi$', 'Ω': r'$\Omega$',
}

def _processar_bloco_conceitos_chave(match):
    """
    Função auxiliar chamada pelo re.sub para formtar o bloco de Conceitos-Chave.
    """
    lista_markdown = match.group(1).strip()
    lista_latex_itemize = convert_bullets_to_latex(lista_markdown)

    bloco_final = (
        f"\\newpage\n"
        f"\\begin{{tcolorbox}}[destaque]\n"
        f"\\textbf{{Conceitos-Chave}}\n\n"  
        f"{lista_latex_itemize}\n"     
        f"\\end{{tcolorbox}}"
    )

    return bloco_final

def markdown_to_latex_string(markdown_text: str) -> str:
    """
    Converte o Markdown de UM ÚNICO capítulo para o formato LaTeX.
    Retorna uma string contendo o corpo LaTeX APENAS para este capítulo.
    """

    # 1. Divisão inicial: cria as varia´veis 'main_content' e 'exercises_markdown'
    parts = markdown_text.split("## Exercícios", 1)
    main_content = parts[0]
    exercises_markdown = parts[1] if len(parts) > 1 else ""

    # Deleta qualquer marcador de bloco de código como '```' ou '```markdown`' do texto principal
    main_content = re.sub(r'```(?:markdown)?\n?', '', main_content)

    # 1. Processa o título principal do capítulo
    processed_text = re.sub(r'^#\s*Unidade\s+\d+\s*[-–]\s*Capítulo\s+\d+:\s*(.*)', r'\\sectiontoc{\1}', main_content, flags=re.MULTILINE)

    # 2. Processa "Conceitos-Chave" com a LLM
    conceitos_chave_pattern = re.compile(
        r'^\s*###\s*Conceitos-Chave\s*\n(.*?)(?=\n^\s*###?|\Z)',
        re.MULTILINE | re.DOTALL
    )
    processed_text = re.sub(conceitos_chave_pattern, _processar_bloco_conceitos_chave, processed_text)

    # 3. Processa casos genéricos para os títulos restantes
    processed_text = re.sub(r'^###\s*(.*)', r'\\subsubsection*{\1}\n\\paragraph{}', processed_text, flags=re.MULTILINE)
    processed_text = re.sub(r'^##\s*(.*)', r'\\subsection*{\1}', processed_text, flags=re.MULTILINE)

    # 4. Aplica as formatações restantes (negrito, símbolos)
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', processed_text)
    greek_pattern = re.compile("|".join(GREEK_SYMBOLS_MAP.keys()))
    processed_text = greek_pattern.sub(lambda m: GREEK_SYMBOLS_MAP[m.group(0)], processed_text)

    # 5. Processa a SEÇÃO DE EXERCÍCIOS do capítulo, se existir
    processed_exercises_section = ""
    if exercises_markdown:
        exercise_items = exercises_markdown.strip().split('---\n\n')
        
        formatted_exercises = []
        # Linha corrigida
        for i, item in enumerate(exercise_items):
            if item.strip():
                try:
                    cleaned_item = re.sub(r'^\s*\*\*Nível Cognitivo:\*\*.*\n?', '', item.strip(), flags=re.MULTILINE)
                    latex_exercise = convert_exercise_to_latex(cleaned_item)
                    if latex_exercise:
                        formatted_exercises.append(latex_exercise)
                    else:
                        print(f" - AVISO: A conversão para LaTeX do exercício {i + 1} retornou vazio.")
                except Exception as e:
                    print(f" - ERRO: Falha ao converter o exercício {i + 1} para LaTeX. Erro: {e}")
                    print(f" - Pulando este exercício e continuando o processo...")
        
        if formatted_exercises:
            joined_exercises = "\n".join(formatted_exercises)
            processed_exercises_section = (
                f"\n\\newpage\n\\section*{{Exercícios}}\n"
                f"\\begin{{enumerate}}\n"
                f"{joined_exercises}\n"
                f"\\end{{enumerate}}"
            )

    return processed_text + processed_exercises_section
