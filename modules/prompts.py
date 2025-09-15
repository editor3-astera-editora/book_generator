# Prompt para extrair os conceitos-chave de um capítulo
#KEY_CONCEPTS_PROMPT = """
#Com base no texto do capítulo a seguir, extraia uma lista dos 5 a 7 conceitos-chave mais importantes.
#Retorne apenas uma lista em formato JSON. Ex: ["Conceito 1", "Conceito 2"]
#
#Texto do Capítulo:
#{chapter_text}
#"""

KEY_CONCEPTS_PROMPT = """
Você é um editor acadêmico sênior criando um guia de estudos.

**TEMA GERAL DO LIVRO:** {book_name}

Com base no texto do capítulo fornecido, sua tarefa é extrair de 5 a 7 conceitos-chave. Priorize os conceitos que são mais fundamentais e diretamente alinhados ao tema geral do livro.

Retorne APENAS uma lista em formato JSON. Ex: ["Conceito 1", "Conceito 2"]

**Texto do Capítulo:**
{chapter_text}
"""

# Prompt para o texto da introdução
SUMMARY_INTRO_PROMPT = """
Você é um autor experiente de material didático. Com base no contexto a seguir, escreva um parágrafo introdutório envolvente e claro (2 - 4 frases) que apresenta o tema central do capítulo e sua importância, preparando o leitor para os conceitos que serão abordados.

**REGRAS PROIBIDAS:**
- Não use frases como "Este texto aborda", "O contexto fornecido discute" ou qualquer meta-linguagem que se refira ao texto em si.

Contexto:
{context}
"""

SUMMARY_APPLICATIONS_PROMPT = """
Você é um especialista em conectar teoria e prática no campo da **{book_name}**. Baseado nos conceitos principais do contexto fornecido, descreva de 2 a 3 exemplos ou aplicações práticas.

**EXEMPLO DE APLICAÇÃO IDEAL (PARA UM LIVRO DE MATEMÁTICA FINANCEIRA):**
Na análise de investimentos, o conceito de **juros compostos** é usado para projetar o crescimento de um capital ao longo do tempo. Uma empresa pode usar a **multiplicação** para calcular o retorno total de um investimento que rende 1% ao mês por 36 meses.
No planejamento de aposentadoria, a **subtração** é usada para determinar o montante que precisa ser economizado, subtraindo o patrimônio atual da meta financeira futura.

**REGRAS OBRIGATÓRIAS:**
1. **FOCO NO TEMA:** Os exemplos devem ser estritamente relevantes para o tema geral do livro, que é **{book_name}**. É proibido usar exemplos de domínios não relacionados, como culinária, tarefas domésticas ou esportes genéricos.
2. Em suas explicações, você deve obrigatoriamente utilizar e aplicar pelo menos dois dos seguintes **Conceitos-Chave**: {key_concepts_list}
3. Seja claro e direto. Cada aplicação deve ser explicada em 1-2 frases.
4. Os exemplos devem ser concretos e fáceis de entender para um estudante da área.
5. Formate a saída em múltiplos parágrafos, dedicando um parágrafo para cada exemplo ou aplicação.

**REGRAS PROIBIDAS:**
- Não use meta-linguagem como "Um exemplo de aplicação é...". Inicie a frase diretamente, por exemplo: "Na indústria farmacêutica, o conceito de **[conceito-chave]** é usado para..."
- Evite maneirismos de IA, metáforas, perguntas retóricas ou verbos informais.
- Proibição de Juízo de Valor: não use adjetivos ou frases que denotem opinião (ex: 'fundamental', 'essencial', 'incrível').

Contexto:
{context}
"""

SUMMARY_MAIN_CONCEPTS_PROMPT = """
Você é um especialista em síntese de conteúdo acadêmico. Sua tarefa é criar um parágrafo denso e informativo que explique os conceitos mais importantes do texto-fonte e como eles se relacionam.

**REGRAS OBRIGATÓRIAS:**
1. **OBJETIVIDADE MÁXIMA:** Vá direto ao ponto. Explique a relação lógica entre os conceitos (causa e efeito, hierarquia, sequência, etc.) de forma clara e sem rodeios.
2. **FOCO NO ESSENCIAL:** Concentre-se APENAS nos 3-4 conceitos mais críticos para a compreensão do tópico. Ignore detalhes secundários, exemplos fictícios ou informações de menor relevância.
3. **CONCISÃO:** Não adiciona frases de preenchimento ou introdutórias. O tamanho do parágrafo deve ser ditado pela complexidade do conteúdo, não por um número fixo de linhas.
4. **FORMATAÇÃO:** Use a sintaxe de Markdown para negrito (**termo importante**) para destacar os conceitos-chave à medida que os explica.

**REGRAS PROIBIDAS:**
- Não use frases como "De acordo com o texto", "No material fonte" ou qualquer meta-linguagem que se refira ao texto em si.

Contexto:
{context}
"""

# Prompt para os bullets
SUMMARY_BULLETS_PROMPT = "Baseado no contexto a seguir, identifique de 3 a 5 conceitos-chave e liste-os como bullet points em Markdown, cada um com uma breve explicação de uma 2-3 frases.\n\nContexto: {context}"

# Prompt para averiguar a presença de fórmulas
SUMMARY_FORMULA_CHECK_PROMPT = "O 'Texto Fonte' a seguir contém alguma fórmula matemática ou científica escrita de forma explícita (ex: E=mc^2, M = P(1+i)^n)? Responda apenas 'SIM' ou 'NÃO'. Não considere a menção de conceitos matemáticos, apenas fórmulas explícitas.\n\nTexto Fonte: {context}"

# Prompt para questões de múltipla escolha
#MULTIPLE_CHOICE_PROMPT = """
#Você é um designer instrucional sênior, especialista em criar avaliações que testam o raciocínio crítico. Baseado exclusivamente no Texto Fonte, crie uma questão de múltipla escolha desafiadora sobre o **{concept}**.
#
#**REGRAS OBRIGATÓRIAS:**
#1. Crie um enunciado contextualizado e completo, que apresente um cenário ou uma afirmação a ser analisada, em vez de uma pergunta direta.
#2. Gere exatamente 5 alternativas (A-E). Apenas UMA deve ser correta. As outras quatro devem ser "distratores" inteligentes, baseados em erros conceituais comuns.
#3. A dificuldade deve ser moderada, exigindo que o aluno aplique o conhecimento do texto, não apenas o localize.
#4. A justificativa da resposta correta deve ser uma **única frase, clara e direta.**
#5. **REGRA DE OURO - FIDELIDADE AO TEXTO:** Você está estritamente proibido de usar qualquer informação, sinônimo, exemplo ou conceito que não esteja explicitamente escrito no 'Texto Fonte' fornecido. A pergunta, todas as alternativas (corretas e incorretas) e a justificativa/resposta ideal devem ser 100% baseadas e verificáveis apenas com o conteúdo do 'Texto Fonte'.
#5. O Tipo SEMPRE deve ser Múltipla Escolha
#
#**REGRAS PROIBIDAS:**
#- O enunciado não deve usar verbos que peçam uma descrição ou dissertação, como "Descreva", "Explique", "Discorra sobre".
#- **NÃO use frases que façam referência ao material de estudo**, como "de acordo com o texto" ou "considerando os dados apresentados".
#
#**Texto Fonte:**
#{context}
#---
#**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**
#
#---
#**Tipo:** Múltipla Escolha
#**Nível Cognitivo:** {bloom_level}
#**Pergunta:**
#[Enunciado completo e contextualizado aqui]
#**Alternativas:**
#(A) [Texto da alternativa A]
#(B) [Texto da alternativa B]
#(C) [Texto da alternativa C]
#(D) [Texto da alternativa D]
#(E) [Texto da alternativa E]
#**Resposta Correta:** (X)
#**Justificativa:** [Explicação breve e direta em uma única frase.]
#"""

MULTIPLE_CHOICE_PROMPT = """
Você é um avaliador acadêmico rigoroso. Sua tarefa é criar uma questão de múltipla escolha sobre o **{concept}**.

**DIRETRIZ INEGOCIÁVEL: FIDELIDADE ABSOLUTA AO TEXTO-FONTE**
- **VERIFICAÇÃO OBRIGATÓRIA:** Antes de finalizar, você deve ser capaz de responder "SIM" à seguinte pergunta: "Cada palavra da minha pergunta, de TODAS as alternativas (corretas e incorretas) e da justificativa pode ser 100% verificada e justificada usando APENAS as frases contidas no 'Texto-Fonte' abaixo?".
- **PROIBIDO CONHECIMENTO EXTERNO:** É estritamente proibido usar sinônimos, exemplos, analogias ou informações que não estejam explicitamente escritos no texto. Se um conceito não está no texto, ele não existe para esta tarefa.

**REGRAS OBRIGATÓRIAS DA QUESTÃO:**
1. Crie um enunciado contextualizado e completo que apresente um cenário ou uma afirmação a ser analisada.
2. Gere exatamente 5 alternativas (A-E). Apenas UMA deve ser correta. As outras quatro devem ser "distratores" plausíveis, baseados em erros conceituais que poderiam surgir da leitura do próprio Texto-Fonte.
3. A dificuldade deve ser moderada, exigindo que o aluno aplique o conhecimento do texto, não apenas o localize.
4. A justificativa da resposta correta deve ser uma **única frase, clara e direta, que parafraseie ou cite diretamente a parte relevante do Texto-Fonte.**
5. O Tipo SEMPRE deve ser Múltipla Escolha.

**REGRAS PROIBIDAS:**
- O enunciado não deve usar verbos que peçam uma descrição, como "Descreva", "Explique".
- **NÃO use frases que façam referência ao material de estudo**, como "de acordo com o texto".

**Texto-Fonte:**
{context}
---
**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**

---
**Tipo:** Múltipla Escolha
**Nível Cognitivo:** {bloom_level}
**Pergunta:**
[Enunciado completo e contextualizado aqui]
**Alternativas:**
(A) [Texto da alternativa A]
(B) [Texto da alternativa B]
(C) [Texto da alternativa C]
(D) [Texto da alternativa D]
(E) [Texto da alternativa E]
**Resposta Correta:** (X)
**Justificativa:** [Explicação breve e direta em uma única frase, extraída do Texto-Fonte.]
"""

# Prompt para questão discursiva
DISCURSIVE_PROMPT = """
Você é um designer instrucional sênior. Baseado exclusivamente no Texto Fonte, crie uma questão **discursiva** aprofundada sobre o **{concept}**.

**REGRAS OBRIGATÓRIAS:**

1. Elabore uma pergunta simples e objetiva, usando apenas **um verbo de comando principal** (ex: "Explique o que é...", "Compare X e Y.", "Liste as características de...").
2. A pergunta deve focar em um único ponto central do conceito.
3. O enunciado completo deve possuir entre 3-4 frases.
4. Forneça uma "resposta ideal" como gabarito, que seja **detalhada, mas concisa e direta (2-3 frases no máximo)**, sempre se baseando nos conceitos do Texto Fonte.
5. **REGRA DE OURO:** A pergunta e a resposta ideal devem se ater **estritamente** ao escopo do Texto Fonte. Não peça ao aluno para comparar conceitos externos ou aplicar conhecimentos não fornecidos.
6. O Tipo SEMPRE deve ser Discursiva

**REGRAS PROIBIDAS:**
- Não use frases como "Segundo o autor", "Conforme o texto" etc.

**Texto Fonte:**
{context}
---
**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**

---
**Tipo:** Discursiva
**Nível Cognitivo:** {bloom_level}
**Pergunta:**
[Texto da pergunta discursiva e analítica aqui]
**Resposta Ideal (Gabarito):**
[Texto completo, porém conciso, da resposta esperada]
---
"""

# Prompt para questão de cálculo ou desenho
#OPEN_ENDED_CALC_DRAW_PROMPT = """
#Você é um designer instrucional sênior. Baseado exclusivamente no Texto Fonte, crie uma **questão aberta** que exija a aplicação prática do **{concept}** através de um cálculo.
#
#**REGRAS OBRIGATÓRIAS:**
#1.  **SIMPLICIDADE:** Crie um problema que use a fórmula de forma direta e com poucas etapas.
#2.  **NÚMEROS SIMPLES:** Use números inteiros ou de fácil cálculo para os exemplos.
#3.  **OBJETIVO:** O foco é testar a aplicação direta da fórmula, não a resolução de problemas matemáticos complexos.
#
#**REGRAS GERAIS:**
#1. Formule um problema que force o aluno a aplicar uma fórmula que esteja explicitamente presente no Texto Fonte fornecido.
#2. A questão deve ser autossuficiente e conter todos os dados necessários para sua resolução.
#3. **REGRA DE OURO - FIDELIDADE AO TEXTO:** Você está estritamente proibido de usar qualquer informação, sinônimo, exemplo ou conceito que não esteja explicitamente escrito no 'Texto Fonte' fornecido. A pergunta, todas as alternativas (corretas e incorretas) e a justificativa/resposta ideal devem ser 100% baseadas e verificáveis apenas com o conteúdo do 'Texto Fonte'.
#
#**REGRAS PROIBIDAS:**
#- **NÃO use fórmulas que não estejam contidas no Texto Fonte.**
#- **NÃO use frases que façam referência ao material de estudo**, como "use as faixas de imposto de renda fornecidas", "de acordo com o texto" ou "conforme visto no capítulo".
#
#**Texto Fonte:**
#{context}
#---
#**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**
#
#---
#**Tipo:** Questão Aberta (Cálculo/Desenho)
#**Nível Cognitivo:** {bloom_level}
#**Pergunta:**
#[Descrição do problema ou cenário prático aqui]
#**Resolução (Gabarito):**
#Apresentação da fórmula (se aplicável), substituição de valores, e a resolução passo a passo, de forma direta e objetiva.]
#"""

OPEN_ENDED_CALC_DRAW_PROMPT = """
Você é um avaliador acadêmico rigoroso. Sua tarefa é criar uma **questão aberta** que exija a aplicação prática do **{concept}** através de um cálculo, baseando-se em fórmulas e cenários do texto.

**DIRETRIZ INEGOCIÁVEL: FIDELIDADE ABSOLUTA AO TEXTO-FONTE**
- **VERIFICAÇÃO OBRIGATÓRIA:** Antes de finalizar, responda "SIM" a esta pergunta: "A fórmula usada, todos os dados do problema e cada passo da resolução podem ser 100% justificados e verificados usando APENAS o 'Texto-Fonte' abaixo?".
- **PROIBIDO CONHECIMENTO EXTERNO:** É estritamente proibido usar fórmulas, constantes, variáveis ou contextos que não estejam explicitamente escritos no texto. Os números do problema podem ser novos, mas o cenário deve ser análogo aos apresentados no texto.

**REGRAS OBRIGATÓRIAS DA QUESTÃO:**
1. Formule um problema que force o aluno a aplicar uma fórmula que esteja **explicitamente presente** no Texto-Fonte.
2. O problema deve ser autossuficiente, contendo todos os dados numéricos necessários para sua resolução.
3. **REGRA DO GABARITO:** A "Resolução" deve apresentar a fórmula original do texto, a substituição dos valores e a resolução passo a passo de forma clara, como se fosse um exemplo do próprio livro.
4. O Tipo SEMPRE deve ser Questão Aberta (Cálculo/Desenho).

**REGRAS PROIBIDAS:**
- **NÃO use fórmulas que não estejam contidas no Texto-Fonte.**
- Não use frases que façam referência ao material de estudo, como "conforme visto no capítulo".
- Não crie problemas complexos que exijam múltiplas fórmulas não relacionadas ou conhecimento de domínio externo ao texto.

**Texto-Fonte:**
{context}
---
**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**

---
**Tipo:** Questão Aberta (Cálculo/Desenho)
**Nível Cognitivo:** {bloom_level}
**Pergunta:**
[Descrição do problema ou cenário prático aqui, usando termos do Texto-Fonte]
**Resolução (Gabarito):**
[Apresentação da fórmula (exatamente como no texto), substituição de valores, e a resolução passo a passo, de forma direta e objetiva.]
"""

# Prompt para questões baseadas em CENÁRIOS 
#OPEN_ENDED_SCENARIO_PROMPT = """
#Você é um designer instrucional sênior criando uma questão discursiva simples. Baseado exclusivamente no Texto Fonte, crie uma **questão aberta e direta** sobre o **{concept}**.
#
#**REGRAS OBRIGATÓRIAS:**
#1.  A pergunta deve se basear em um único ponto. Use verbos de comando de baixa complexidade como "O que é...", "Descreva...", "Liste as características de...", "Qual a finalidade de...".
#2.  A pergunta deve conter enunciado completo com um desenvolvimento que leve o aluno a resposta.
#2.  **FOCO NA MEMORIZAÇÃO E ENTENDIMENTO:** O objetivo é verificar se o aluno se lembra e entendeu um conceito-chave do texto. A pergunta NÃO deve exigir análise complexa, comparação com outros conceitos ou a solução de um problema com múltiplas etapas.
#3.  **CENÁRIO OPCIONAL E SIMPLES:** Se um cenário for usado, ele deve ser mínimo e servir apenas para contextualizar a pergunta (ex: "Em um projeto, por que o conceito de X é importante?").
#4.  **RESPOSTA DIRETA:** A resposta ideal no gabarito deve ser uma explicação concisa (1-3 frases) que poderia ser encontrada quase que literalmente no Texto Fonte.
#5.  **TIPO DA QUESTÃO:** O TIPO da questão sempre deve ser: Questão Aberta (Cenário Aplicado)
#6. **REGRA DE OURO - FIDELIDADE AO TEXTO:** Você está estritamente proibido de usar qualquer informação, sinônimo, exemplo ou conceito que não esteja explicitamente escrito no 'Texto Fonte' fornecido. A pergunta e a resposta devem ser TOTALMENTE baseadas e verificáveis apenas com o conteúdo 'Texto Fonte'.
#
#**REGRAS PROIBIDAS:**
#- Não crie estudos de caso complexos ou problemas que exijam que o aluno "tome uma decisão".
#- Evite perguntas que comecem com "Como você faria..." ou "Analise o seguinte caso...".
#
#**Texto Fonte:**
#{context}
#---
#**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**
#
#---
#**Tipo:** Questão Aberta (Cenário Aplicado)
#**Nível Cognitivo:** {bloom_level}
#**Pergunta:**
#[Texto da pergunta direta e simples aqui]
#**Resolução (Gabarito):**
#[Descrição da resposta esperada, de forma direta e objetiva.]
#"""

OPEN_ENDED_SCENARIO_PROMPT = """
Você é um avaliador acadêmico rigoroso. Sua tarefa é criar uma **questão aberta e direta** sobre o **{concept}** a partir de um cenário simples.

**DIRETRIZ INEGOCIÁVEL: FIDELIDADE ABSOLUTA AO TEXTO-FONTE**
- **VERIFICAÇÃO OBRIGATÓRIA:** Antes de finalizar, você deve ser capaz de responder "SIM" à seguinte pergunta: "O cenário que descrevi, a pergunta que fiz e cada frase da 'Resolução' podem ser 100% verificados e justificados usando APENAS as frases contidas no 'Texto-Fonte' abaixo?".
- **PROIBIDO CONHECIMENTO EXTERNO:** É estritamente proibido usar sinônimos, exemplos, analogias ou informações que não estejam explicitamente escritos no texto.

**REGRAS OBRIGATÓRIAS DA QUESTÃO:**
1. Crie um cenário simples que sirva apenas para contextualizar a pergunta (ex: "Em uma análise de projeto..."). O cenário deve usar termos e situações contidas no Texto-Fonte.
2. O enunciado completo deve possuir 3-4 frases.
2. A pergunta deve ser direta e de baixa complexidade (ex: "O que é...", "Descreva...", "Qual a finalidade de...").
3. **REGRA DO GABARITO:** A "Resolução" deve ser uma explicação concisa (1-3 frases) que poderia ser encontrada quase que literalmente no Texto-Fonte, servindo como a resposta direta à pergunta no contexto do cenário.
4. O Tipo SEMPRE deve ser Questão Aberta (Cenário Aplicado).

**REGRAS PROIBIDAS:**
- Não crie estudos de caso complexos ou problemas que exijam que o aluno "tome uma decisão" ou use criatividade.
- Não faça perguntas que exijam opinião, julgamento de valor ou "o que você faria".
- Evite perguntas que comecem com "Como você faria..." ou "Analise o seguinte caso...".

**Texto-Fonte:**
{context}
---
**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**

---
**Tipo:** Questão Aberta (Cenário Aplicado)
**Nível Cognitivo:** {bloom_level}
**Pergunta:**
[Texto da pergunta direta e simples, inserida em um cenário baseado no Texto-Fonte]
**Resolução (Gabarito):**
[Descrição da resposta esperada, de forma direta e objetiva, extraída do Texto-Fonte.]
"""


#TRUE_FALSE_PROMPT = """
#Você é um designer instrucional sênior. Baseado exclusivamente no Texto Fonte sobre o **{concept}**, crie uma questão de Verdadeiro ou Falso.
#
#**REGRAS OBRIGATÓRIAS:**
#1. Crie um conjunto de 4 a 5 afirmativas curtas sobre o conceito. Algumas devem ser verdadeiras, outras falsas.
#2. As afirmativas falsas devem se basear em erros conceituais comuns.
#3. Crie 5 alternativas de múltipla escolha (A-E) que representem as sequências de julgamento (ex: V - F - V - F). Apenas uma alternativa deve estar correta.
#4. Forneça a justificativa para CADA afirmativa falsa.
#
#**REGRAS PROIBIDAS:**
#- **NÃO use frases que façam referência ao material de estudo**, como "baseado no cenário descrito no capítulo" ou "conforme o conceito apresentado".
#
#**Texto Fonte:**
#{context}
#---
#**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**
#
#---
#**Tipo:** Verdadeiro ou Falso
#**Nível Cognitivo:** {bloom_level}
#**Pergunta:**
#Julgue as afirmativas a seguir sobre {concept} e assinale a alternativa que apresenta a sequência correta.
#( ) [Texto da primeira afirmativa]
#( ) [Texto da segunda afirmativa]
#( ) [Texto da terceira afirmativa]
#**Alternativas:**
#(A) V - V - F
#(B) V - F - V
#(C) F - V - F
#(D) F - F - V
#(E) V - V - V
#**Resposta Correta:** (B)
#**Justificativa:** A segunda afirmativa é falsa porque [...]. A terceira afirmativa é verdadeira porque [...].
#"""

TRUE_FALSE_PROMPT = """
Você é um avaliador acadêmico rigoroso. Sua tarefa é criar uma questão de **Verdadeiro ou Falso** sobre o **{concept}**.

**DIRETRIZ INEGOCIÁVEL: FIDELIDADE ABSOLUTA AO TEXTO-FONTE**
- **VERIFICAÇÃO OBRIGATÓRIA:** Antes de finalizar, responda "SIM" a esta pergunta: "Cada afirmativa (verdadeira ou falsa) e cada palavra da justificativa podem ser 100% verificadas, provadas ou refutadas usando APENAS as frases contidas no 'Texto-Fonte' abaixo?".
- **PROIBIDO CONHECIMENTO EXTERNO:** É estritamente proibido usar informações que não estejam no texto. As afirmativas falsas devem ser contradições diretas do texto, não apenas informações incorretas aleatórias.

**REGRAS OBRIGATÓRIAS DA QUESTÃO:**
1. Crie um conjunto de 3 a 5 afirmativas curtas sobre o conceito.
2. As afirmativas **verdadeiras** devem ser paráfrases próximas de declarações no Texto-Fonte.
3. As afirmativas **falsas** devem ser baseadas em erros conceituais que surgiriam de uma má interpretação do Texto-Fonte (ex: inverter uma causa e efeito descrita no texto).
4. Crie 5 alternativas de múltipla escolha (A-E) que representem as sequências de julgamento. Apenas uma deve estar correta.
5. **REGRA DO GABARITO:** Forneça uma justificativa clara e direta para **CADA afirmativa falsa**, apontando a informação correta presente no Texto-Fonte.

**REGRAS PROIBIDAS:**
- Não use frases que façam referência ao material de estudo, como "baseado no cenário descrito no capítulo".
- Não crie afirmativas ambíguas ou que dependam de interpretação subjetiva.

**Texto-Fonte:**
{context}
---
**Formato de Saída OBRIGATÓRIO (use Markdown e os marcadores ---):**

---
**Tipo:** Verdadeiro ou Falso
**Nível Cognitivo:** {bloom_level}
**Pergunta:**
Julgue as afirmativas a seguir sobre {concept} e assinale a alternativa que apresenta a sequência correta.
( ) [Texto da primeira afirmativa]
( ) [Texto da segunda afirmativa]
( ) [Texto da terceira afirmativa]
**Alternativas:**
(A) V - V - F
(B) V - F - V
(C) F - V - F
(D) F - F - V
(E) V - V - V
**Resposta Correta:** (X)
**Justificativa:** A afirmativa [número] é falsa porque o texto afirma que [...]. A afirmativa [número] é falsa porque [...].
"""

# Prompt verificador
EXERCISE_CALC_CHECK_PROMPT = """
Analise o Contexto fornecido abaixo. O texto contém alguma fórmula matemática ou científica escrita de forma explícita (ex: E=mc^2, M = P(1+i)^n)?
Responda apenas 'SIM' ou 'NÃO'. Ignore a simples menção de conceitos matemáticos; foque apenas em fórmulas explícitas que o aluno poderia usar para calcular algo.

Contexto:
{context}
"""

# Prompt focado em extrair fórmulas, incluindo as textuais
FORMULA_EXTRACTOR_PROMPT = """
Analise o texto fornecido e extraia TODAS as fórmulas e relações de cálculo, sejam elas simbólicas (ex: J = C*i*t) ou descritas em texto (ex: Custo Total = Preço + Impostos).

**REGRAS:**
1. Padronize a fórmula extraída para o formato "Resultado = Componente 1 + Componente 2", mantendo os nomes originais das variáveis.
2. Se nenhuma fórmula ou relação de cálculo explícita for encontrada, retorne uma lista vazia [].
3. **Sua saída deve ser APENAS uma lista em formato JSON, sem nenhum texto adicional, explicação ou marcadores de código.**

**Exemplo de Saída Perfeita:**
["J = C * i * t", "Custo Total = Preço do Ingresso + Valor da Taxa", "Montante = Capital + Juros"]

**Texto para Análise:**
{text_to_scan}
"""

# Prompt para validar a equivalência semântica da fórmulas 
FORMULA_VALIDATION_PROMPT = """
Você é um especialista em matemática e física. Sua tarefa é comparar duas listas de fórmulas e determinar se as fórmulas na "Lista de Fórmulas Usadas" são conceitualmente equivalentes ou diretamente deriváveis das fórmulas na "Lista de Fórmulas Permitidas".

**Contexto:**
- A "Lista de Fórmulas Permitidas" vem diretamente do material de estudo do aluno (ex: "Velocidade = distancia / tempo").
- A "Lista de Fórmulas Usadas" vem de um exercício gerado (ex: "V = d/t").
- As fórmulas podem estar em formatos diferentes (simbólica vs. textual) e usar abreviações comuns.

**Listas para Análise:**
- Lista de Fórmulas Permitidas: {allowed_formulas}
- Lista de Fórmulas Usadas: {used_formulas}

**Pergunta Crítica:**
Considerando abreviações comuns (ex: 'V' para 'Velocidade', 'd' para 'distancia'), as fórmulas na "Lista de Fórmulas Usadas" são essencialmente as mesmas que as da "Lista de Fórmulas Permitidas"?

Responda apenas 'SIM' se TODAS as fórmulas usadas forem equivalentes às permitidas, ou 'NÃO' caso contrário.
"""

# Prompt para extrair e mapear fórmulas e seus conceitos associados
FORMULA_MAPPING_PROMPT = """
Sua tarefa é atuar como um especialista no conteúdo e analisar o texto para extrair e catalogar todas as **fórmulas e regras de cálculo gerais e reutilizáveis**.

**REGRAS:**
1.  Extraia tanto fórmulas simbólicas (ex: `J = C*i*t`) quanto textuais (ex: `Montante = Capital + Juros`).
2.  Para cada fórmula encontrada, liste os principais conceitos-chave do texto aos quais ela se aplica diretamente.
3.  **IGNORE** exemplos de cálculos que usam apenas números específicos e concretos (ex: "R$ 1000 + R$ 50 = R$ 1050"). Extraia apenas a regra geral.
4.  Sua resposta deve ser uma lista de objetos JSON. Se nenhuma fórmula geral for encontrada, retorne uma lista vazia `[]`.

**EXEMPLO DE COMPORTAMENTO ESPERADO:**

**Texto de Exemplo para Análise:**
"Para calcular o montante, usamos a regra: Montante = Capital + Juros. Por exemplo, se o capital é R$ 1000 e os juros são R$ 50, o montante é R$ 1000 + R$ 50 = R$ 1050. A fórmula simbólica para juros simples é J = C*i*t."

**Sua Saída Perfeita (JSON):**
[
  {{
    "formula": "J = C * i * t",
    "concepts": ["juros simples", "cálculo de juros", "capital", "taxa de juros"],
    "description": "Fórmula para calcular juros simples."
  }},
  {{
    "formula": "Montante = Capital + Juros",
    "concepts": ["montante", "juros simples", "capital"],
    "description": "Fórmula para calcular o montante final em um regime de juros simples."
  }}
]
---
**Texto para Análise:**
{chapter_text}
"""

# Prompt de revisão de exercícios 
#REVISE_EXERCISES_SIMILARITY_PROMPT = """
#Você é um revisor pedagógico especialista. Analise a lista de exercícios fornecida abaixo.
#Sua tarefa é identificar se existem duas ou mais questões que são muito simliares ou pedagogicamente redundantes (avaliam exatamente o mesmo ponto da mesma maneira.)
#
#**Exercícios Gerados:**
#{exercise_list}
#
#---
#**Sua Resposta:**
#Se todas as questões forem suficientemente distintas, responda apenas com a palavra "NENHUM".
#Se você encontrar uma questão que é muito similar a outra, responda apenas com o número (índice) da questão que deve ser refeita. Por exemplo, se a Questão 3 for muito parecida com a Questão 1, responda apenas: 3 
#"""

REVISE_EXERCISES_SIMILARITY_PROMPT = """
Você é um revisor pedagógico especialista. Sua tarefa é analisar a lista de exercícios abaixo para identificar redundância pedagógica.

**Critérios de Análise:**
Avalie se duas ou mais questões são excessivamente similares com base em:
1.  **Conceito Central:** Testam exatamente a mesma definição, fato ou fórmula?
2.  **Estrutura do Problema:** Usam o mesmo cenário, contexto ou estrutura de pergunta?
3.  **Habilidade Cognitiva:** Exigem o mesmo tipo de raciocínio (ex: ambas são de memorização, ambas são de aplicação direta da mesma fórmula)?

**Exercícios Gerados:**
{exercise_list}

---
**Sua Resposta:**

Se todas as questões forem suficientemente distintas, responda apenas com a palavra "NENHUM".
Se você encontrar uma questão que é muito similar a outra, responda apenas com o número (índice) da questão que deve ser refeita. Por exemplo, se a Questão 3 for muito parecida com a Questão 1, responda apenas: 3 
"""

# Prompt para reescrever uma questão similar 
#EXERCISE_REWRITING_PROMPT = """
#Você é um designer instrucional sênior. Sua tarefa é criar uma nova questão do tipo **{exercise_type}** sobre o **{concept}**, com base no Texto Fonte.
#
#**CONTEXTO CRÍTICO:** A versão anterior da questão, mostrada abaixo, foi rejeitada por ser muito similar a outras questões.
#
#**Questão Rejeitada:**
#---
#{original_question}
#---
#
#**SUA TAREFA:**
#Crie uma **nova questão** que seja **substancialmente diferente** da versão rejeitada. Foque em um aspecto diferente do conceito, use um cenário completamente novo ou mude a estrutura do problema. NÃO faça apenas uma simples paráfrase.
#
#**REGRAS OBRIGATÓRIAS:**
#1. Siga todas as regras do formato de saída para o tipo de questão **{exercise_type}**.
#2. A nova questão deve ser fiel ao Texto Fonte e pedagogicamente sólida.
#
#**Texto Fonte:**
#{context}
#"""

EXERCISE_REWRITING_PROMPT = """
Você é um designer instrucional sênior com a tarefa de diversificar avaliações. Sua missão é criar uma **nova questão** do tipo **{exercise_type}** sobre o **{concept}**.

**CONTEXTO CRÍTICO:** A versão anterior da questão, mostrada abaixo, foi **rejeitada por ser pedagogicamente redundante** e muito similar a outras questões já existentes.

**Questão Rejeitada:**
---
{original_question}
---

**SUA TAREFA:**
Crie uma **nova questão** que seja **substancialmente diferente** da versão rejeitada. Mantenha o **mesmo conceito central ({concept})**, mas altere radicalmente a abordagem:
-   Se a original era teórica, torne a nova mais prática ou baseada em um cenário.
-   Se a original usava um cálculo simples, crie um cenário um pouco mais elaborado.
-   Foque em um aspecto diferente do conceito.
-   **NÃO FAÇA** uma simples paráfrase da questão rejeitada.

**LEMBRE-SE DA DIRETRIZ INEGOCIÁVEL: FIDELIDADE ABSOLUTA AO TEXTO-FONTE.**
A nova questão, suas alternativas e o gabarito devem ser 100% verificáveis usando apenas o Texto-Fonte fornecido.

**Texto-Fonte:**
{context}
---
**Instruções de Formato:**
Siga rigorosamente o formato de saída para o tipo de questão **{exercise_type}**.
"""

CAPTION_FIGURE_PROMPT = """
Você é um editor sênior criando o caption de uma figura em um livro didático. Para o capítulo com o título "{chapter_title}", crie uma legenda curta (1-2 frases) que comente o conteúdo que será abordado.

REGRAS:
- NUNCA mencione a palavra "imagem", "figura", "ilustração" ou "capítulo".
- Foque no tema do capítulo.
- A legenda deve explicar muito brevemente do que se trata o assunto.
- Retorne SOMENTE o caption, sem aspas.

Exemplo para um capítulo "O que são juros":
"O cálculo de juros permite determinar o acréscimo sobre um valor inicial ao longo do tempo, variando conforme a taxa aplicada e o tipo de capitalização."

Título do Capítulo: {chapter_title}
"""