LATEX_BULLETS_PROMPT = r"""
Converta a seguinte lista de marcadores em Markdown para um ambiente itemize do LaTeX.

**Entrada:**
- Item 1 com **negrito** falando sobre algum tópico \[V_{{2}} = 3*7\].
- Item 2.

**Sua Saída LaTeX:**
\begin{{itemize}}
   \item Item 1 com \textbf{{negrito}} e ambiente matemático $V_{{2}} = 3*7$.
   \item Item 2.
\end{{itemize}}
---

**REGRAS OBRIGATÓRIAS:**
1. Utilizar o ambiente itemize 
2. Caso exista alguma equação ou símbolo matemático, colocar no ambiente $...$

**LISTA PARA CONVERTER:**

{bullet_list}
"""


PROMPT_HEADER = r"""
Você é um especialista em formatação LaTeX. Sua tarefa é converter o exercício em Markdown fornecido para o formato LaTeX exato, seguindo o exemplo abaixo.

**REGRAS:**
1. Sua saída deve ser APENAS o código LaTeX. Não inclua explicações. 
2. Faça o escape de todos os caracteres especiais do LaTeX no texto (e.g, %, &, _, $).
3. O enunciado de cada exercício deve começar com '\item'.

**REGRA FORMATAÇÃO OBRIGATÓRIA:**
1. **MATEMÁTICA:** Qualquer expressão matemática, fórmula, variável ou símbolo (como =, +, -, *, ^) deve ser OBRIGATORIAMENTE envolvida em um ambiente matemático do LaTeX. Use `$ ... $` para expressões na mesma linha e `\[ ... \]` para equações em linhas separadas.
2. **SÍMBOLOS GREGOS:** Converta todos os símbolos gregos (e.g, α, β, γ, Δ, Σ) para seus comandos LaTeX correspondentes dentro do modo matemático (e.g., `$\alpha$`, `$\beta$`, `$\gamma$`, `$\Delta$`, `$\Sigma$`).
---
"""

# Prompt para Múltipla Escolha 
LATEX_MC_PROMPT = PROMPT_HEADER + r"""
**EXEMPLO DE MÚLTIPLA ESCOLHA:**

**Entrada:**
**Tipo:** Múltipla Escolha
**Pergunta:**
Qual é o único número primo entre 10 e 20?
**Alternativas:**
(A) 12
(B) 15
(C) 17
(D) 19
**Resposta Correta:** (C)
**Justificativa:** 17 é o único número na lista que só é divisível por 1 e por ele mesmo.

**Sua Saída LaTeX:**
\item Qual é o único número primo entre 10 e 20?
\begin{{itemize}}
   \item[A)] 12
   \item[B)] 15
   \item[C)] 17
   \item[D)] 19
\end{{itemize}}

\textcolor{{Gabarito}}{{(C) 17 é o único número na lista que só é divisível por 1 e por ele mesmo.}}
---
**EXERCÍCIO PARA CONVERTER:**

{exercise_markdown}
 """

# Prompt para questão discursiva
LATEX_DISCURSIVE_PROMPT = PROMPT_HEADER + r"""
**EXEMPLO DE QUESTÃO DISCURSIVA:**

**Entrada:**
**Tipo:** Discursiva
**Pergunta:**
Explique o conceito de Juros Compostos, incluindo sua fórmula coma  variável de tempo 'n'.
**Resposta Ideal (Gabarito):**
Juros compostos são juros calculados sobre o principal mais os juros acumulados. A fórmula é M = P(1 +i)^n.

**Sua Saída LaTeX:**
\item Explique o conceito de Juros Compostos.

\answerlines{{Juros compostos são juros calculados sobre o principal mais os juros acumulados. A fórmula é $M = P(1 +i)^n$.}}
---
**EXERCÍCIO PARA CONVERTER:**

{exercise_markdown}
"""

# Prompt para questão aberta (Cálculo/Desenho)
LATEX_OPEN_ENDED_PROMPT = PROMPT_HEADER + r"""
**EXEMPLO DE QUESTÃO ABERTA (CÁLCULO/DESENHO):**

**Entrada:**
**Tipo:** Questão Aberta (Cálculo/Desenho)
**Pergunta:**
Uma loja vende camisetas a R$ 50 cada. Para compras acima de 10 unidades, a loja oferece um desconto de 10%. Se um cliente comprar 12 camisetas, qual será o valor total da compra? Mostre os passos do cálculo.
**Resolução (Gabarito):**
1. **Calcular o valor sem desconto:**
   \[
   12 \times 50 = 600
   \]
2. **Calcular o valor do desconto:**
   \[
   600 \times 0.10 = 60
   \]
3. **Calcular o valor final:**
   \[
   600 - 60 = 540
   \]
O valor total será de R$ 540,00.

**Sua Saída LaTeX:**
\item Uma loja vende camisetas a R\$ 50 cada. Para compras acima de 10 unidades, a loja oferece um desconto de 10\%. Se um cliente comprar 12 camisetas, qual será o valor total da compra? Mostre os passos do cálculo.
\begin{{tcolorbox}}[quadrodesenho]
\begin{{enumerate}}
    \item \textbf{{Calcular o valor sem desconto:}}
    \[
    12 \times 50 = 600
    \]
    \item \textbf{{Calcular o valor do desconto:}}
    \[
    600 \times 0.10 = 60
    \]
    \item \textbf{{Calcular o valor final:}}
    \[
    600 - 60 = 540
    \]
\end{{enumerate}}
O valor total será de R\$ 540,00.
\end{{tcolorbox}}
---
**EXERCÍCIO PARA CONVERTER:**

{exercise_markdown}
"""

# Prompt para questão de cenário aplicado
LATEX_SCENARIO_PROMPT = PROMPT_HEADER + r"""
**EXEMPLO DE QUESTÃO ABERTA (CENÁRIO APLICADO):**

**Entrada:**
**Tipo:** Questão Aberta (Cenário Aplicado)
**Pergunta:**
Uma empresa está decidindo entre duas estratégias de marketing para um novo produto: uma focada em mídias sociais e outra em marketing de conteúdo (blogs, e-books). Usando o conceito de 'Funil de Vendas', descreva qual estratégia seria mais adequada para a etapa de 'Topo de Funil' e por quê.
**Resolução (Gabarito):**
A estratégia de marketing de conteúdo é mais adequada para o 'Topo de Funil'. Nesta etapa, o objetivo é atrair um grande público e gerar conscientização sobre um problema, o que é efetivamente alcançado com artigos de blog e e-books informativos que não pressionam a venda imediata.

**Sua Saída LaTeX:**
\item Uma empresa está decidindo entre duas estratégias de marketing para um novo produto: uma focada em mídias sociais e outra em marketing de conteúdo (blogs, e-books). Usando o conceito de 'Funil de Vendas', descreva qual estratégia seria mais adequada para a etapa de 'Topo de Funil' e por quê.

\answerlines{{A estratégia de marketing de conteúdo é mais adequada para o 'Topo de Funil'. Nesta etapa, o objetivo é atrair um grande público e gerar conscientização sobre um problema, o que é efetivamente alcançado com artigos de blog e e-books informativos que não pressionam a venda imediata.}}

---
**EXERCÍCIO PARA CONVERTER:**

{exercise_markdown}
"""

LATEX_TRUE_FALSE_PROMPT = PROMPT_HEADER + r"""
**EXEMPLO DE QUESTÃO DE VERDADEIRO OU FALSO:**

**Entrada:**
**Tipo:** Verdadeiro ou Falso
**Pergunta:**
Julgue as afirmativas a seguir e assinale a alternativa que apresenta a sequência correta.
( ) Afirmativa 1.
( ) Afirmativa 2.
**Alternativas:**
(A) V - V
(B) V - F
(C) F - V
(D) F - F
**Resposta Correta:** (B)
**Justificativa:** A afirmativa 2 é falsa porque [...].

**Sua Saída LaTeX:**
\item Julgue as afirmativas a seguir e assinale a alternativa que apresenta a sequência correta.
\begin{{itemize}}[label=(\phantom{{V}})]
    \item Afirmativa 1.
    \item Afirmativa 2.
\end{{itemize}}
\vspace{{5mm}}
\begin{{itemize}}[labelsep=5.5mm, leftmargin=*]
    \item[A)] V - V
    \item[B)] V - F
    \item[C)] F - V
    \item[D)] F - F
\end{{itemize}}
\textcolor{{Gabarito}}{{(B) A afirmativa 2 é falsa porque [...].}}
---
**EXERCÍCIO PARA CONVERTER:**

{exercise_markdown}
"""