# Book Generator - Sistema de Geração Automática de Livros Educacionais

## Descrição

O **Book Generator** é um sistema de processamento e geração automática de conteúdo educacional. Ele transforma livros em formato `.docx` em material didático estruturado, completo com resumos, exercícios e formatação LaTeX profissional.

O sistema utiliza tecnologias de IA (OpenAI GPT-4o) e técnicas avançadas de RAG (Retrieval-Augmented Generation) para criar conteúdo educacional de alta qualidade, mantendo a coerência pedagógica e o rigor técnico necessários para materiais acadêmicos.

## Arquitetura RAG (Retrieval-Augmented Generation)

### Importância do RAG no Sistema

O RAG é fundamental para garantir que o conteúdo gerado seja contextualmente relevante e factualmente preciso. Em vez de depender apenas do conhecimento parametrizado do modelo de linguagem, o sistema recupera informações específicas do próprio livro sendo processado, garantindo:

- **Consistência Terminológica**: Mantém o vocabulário e definições consistentes com o material original
- **Precisão Contextual**: Gera exercícios e resumos baseados no conteúdo real do capítulo
- **Redução de Alucinações**: Minimiza informações incorretas ao fundamentar as respostas em dados recuperados
- **Eficiência de Tokens**: Reduz o contexto enviado ao LLM ao recuperar apenas informações relevantes

### Implementação Técnica do RAG

O sistema implementa um pipeline RAG robusto utilizando:

1. **Vetorização com OpenAI Embeddings**
   - Modelo: `text-embedding-3-small`
   - Gera representações vetoriais de 1536 dimensões para cada chunk de texto
   - Captura semântica e relações contextuais do conteúdo

2. **Indexação com FAISS-CPU**
   - Utiliza o Facebook AI Similarity Search (FAISS) para busca vetorial eficiente
   - Cria índices L2 (distância euclidiana) para busca por similaridade
   - Otimizado para CPU, eliminando dependência de GPU
   - Suporta busca k-NN (k-nearest neighbors) em tempo logarítmico

3. **Reranking com Cross-Encoder**
   - Modelo: `cross-encoder/ms-marco-MiniLM-L-6-v2`
   - Reordena os top-20 resultados iniciais para os 5 mais relevantes
   - Melhora significativamente a precisão da recuperação
   - Reduz ruído e informações irrelevantes no contexto

### Pipeline de Processamento RAG

```
Texto do Capítulo -> Chunking (RecursiveCharacterTextSplitter) -> 
Embeddings (OpenAI) -> Indexação (FAISS) -> 
Busca Inicial (k=20) -> Reranking (Cross-Encoder, top=5) -> 
Contexto para LLM
```

## Principais Funcionalidades

- **Extração Inteligente de Conteúdo**: Processa arquivos `.docx` extraindo capítulos e unidades automaticamente
- **Geração Contextualizada**: Cria resumos e exercícios baseados no conteúdo real do livro
- **Processamento Paralelo**: Utiliza `ProcessPoolExecutor` para processar múltiplos capítulos simultaneamente
- **Formatação LaTeX Profissional**: Converte automaticamente o conteúdo para LaTeX com templates customizados
- **Gestão de Fórmulas Matemáticas**: Extrai e preserva fórmulas matemáticas do Word
- **Rastreamento de Custos**: Monitora uso de tokens da API OpenAI e calcula custos em tempo real

## Resultado Final e Compilação

### Arquivo de Saída

O resultado final do processamento é um arquivo `.tex` completamente formatado e pronto para compilação, localizado em:
```
resultados/tex_{nome_do_livro}/Livro_Completo.tex
```

### Compilação no Overleaf

É **recomendado** que o arquivo `.tex` seja compilado no Overleaf para garantir a melhor qualidade de renderização. A estrutura necessária no Overleaf deve ser:

```
projeto_overleaf/
├── Livro_Completo.tex    # Arquivo principal gerado pelo sistema
├── preambulo.tex          # Arquivo de preâmbulo com configurações
└── imagens/
    └── fundo_decorativo.pdf  # Fundo padrão dos livros Inovatech
```

### Características do Documento Final

- **Livro Completamente Diagramado**: Pronto para impressão ou distribuição digital
- **Gabarito do Professor**: Respostas dos exercícios aparecem automaticamente na quinta cor
- **Design Profissional**: Utiliza o padrão visual Inovatech com fundo decorativo
- **Formatação Acadêmica**: Segue normas de publicação educacional

## Estrutura do Projeto

```
book_generator/
│
├── main.py                        # Orquestrador principal do pipeline
├── config.py                      # Configurações e variáveis de ambiente
├── requirements.txt               # Dependências do projeto
│
├── modules/                       # Módulos do sistema
│   ├── ingestion.py              # Extração de conteúdo de .docx
│   ├── rag_builder.py            # Construção do sistema RAG com FAISS
│   ├── generation.py             # Geração de conteúdo com GPT-4
│   ├── formatting.py             # Conversão Markdown para LaTeX
│   ├── preambulo.py              # Templates e preâmbulos LaTeX
│   ├── preprocessar_formulas.py  # Processamento de fórmulas matemáticas
│   ├── prompts.py                # Templates de prompts para o LLM
│   └── utils.py                  # Funções auxiliares
│
├── livros_originais/             # Entrada: livros .docx para processar
├── resultados/                   # Saída: livros processados
├── FEITO/                        # Arquivos processados com sucesso
└── teste/                        # Suite de testes unitários
```

## Stack Tecnológica

### Core
- **Python 3.8+**: Linguagem base do sistema
- **OpenAI GPT-4**: Modelo de linguagem para geração de conteúdo
- **LangChain**: Framework para orquestração de LLMs

### Sistema RAG
- **FAISS-CPU**: Busca vetorial de alta performance
- **OpenAI Embeddings**: Geração de embeddings semânticos
- **HuggingFace Cross-Encoder**: Reranking de resultados
- **Sentence Transformers**: Modelos de embeddings alternativos

### Processamento
- **python-docx**: Leitura e parsing de arquivos Word
- **RecursiveCharacterTextSplitter**: Divisão inteligente de texto
- **multiprocessing**: Paralelização de processamento

### Formatação
- **LaTeX**: Sistema de tipografia científica
- **Markdown**: Formato intermediário de processamento

## Requisitos do Sistema

### Hardware
- CPU: Mínimo 4 cores (recomendado 8+ para processamento paralelo)
- RAM: Mínimo 8GB (recomendado 16GB+ para livros grandes)
- Armazenamento: 10GB+ livre para processamento e cache

### Software
- Python 3.8 ou superior
- Chave de API da OpenAI com acesso ao GPT-4o
- Dependências especificadas em `requirements.txt`

## Instalação e Configuração

1. **Configuração do Ambiente**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Instalação de Dependências**
```bash
pip install -r requirements.txt
```

3. **Configuração de Credenciais**

Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=...
```

4. **Verificação da Instalação**
```bash
python -c "import faiss; print(f'FAISS version: {faiss.__version__}')"
```

## Uso do Sistema

### Processamento de Livros

1. Adicione arquivos `.docx` em `livros_originais/`
2. Execute o pipeline principal:
```bash
python main.py
```

### Estrutura de Saída

Para cada livro processado, o sistema gera:

```
resultados/{nome_livro}/
├── md_por_capitulo/      # Capítulos em Markdown
├── tex_por_capitulo/     # Capítulos em LaTeX individuais
├── tex_{nome_livro}/     # Livro completo compilável
│   ├── Livro_Completo.tex  # Arquivo principal para Overleaf
│   └── preambulo.tex        # Configurações LaTeX
├── mapa_de_formulas.json # Mapeamento de fórmulas
└── relatorio_de_custos.txt # Análise de uso e custos
```

### Preparação para Overleaf

1. Faça upload do `Livro_Completo.tex` e `preambulo.tex` para o Overleaf
2. Crie a pasta `imagens/` no projeto
3. Adicione o arquivo `fundo_decorativo.pdf` (padrão Inovatech)
4. Compile o documento usando XeLaTeX ou LuaLaTeX

## Pipeline de Processamento Detalhado

1. **Ingestão e Parsing**
   - Extração de texto e estrutura do .docx
   - Identificação de unidades e capítulos
   - Limpeza de metadados e formatação

2. **Pré-processamento**
   - Extração e catalogação de fórmulas matemáticas
   - Chunking adaptativo do texto (chunk_size=1000, overlap=200)

3. **Construção do Sistema RAG**
   - Geração de embeddings via API OpenAI
   - Construção de índice FAISS
   - Configuração de retriever com reranking

4. **Geração de Conteúdo**
   - Extração de conceitos-chave
   - Geração de resumos estruturados
   - Criação de exercícios contextualizados

5. **Pós-processamento**
   - Conversão Markdown para LaTeX
   - Aplicação de templates e formatação
   - Compilação do documento final

## Configurações Avançadas

### Ajuste de Paralelização

Em `main.py`:
```python
MAX_WORKERS = 2  # Ajuste baseado em CPU e memória disponíveis
```

### Parâmetros de Chunking

Em `modules/ingestion.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " "]
)
```

### Configuração do RAG

Em `modules/rag_builder.py`:
```python
# Busca inicial
search_kwargs={"k": 20}

# Reranking final
top_n=5
```

## Monitoramento e Logs

### Sistema de Logging

- **Arquivo**: `processamento_livros.log`
- **Níveis**: INFO, WARNING, ERROR, CRITICAL
- **Formato**: timestamp - processo - nível - mensagem

### Métricas Rastreadas

- Tokens consumidos por operação
- Tempo de processamento por capítulo
- Taxa de sucesso de extração
- Custos estimados da API

## Formato de Entrada Esperado

Os arquivos `.docx` devem seguir a estrutura:

```
Unidade 1 - Capítulo 1

Título do Capítulo
[Conteúdo do capítulo]

Unidade 1 - Capítulo 2

Outro Título
[Conteúdo do capítulo]
```

## Tratamento de Erros

O sistema implementa tratamento robusto de erros:

- Retry automático para falhas de API
- Fallback para processamento sequencial em caso de erro paralelo
- Logs detalhados de exceções com traceback completo
- Movimentação segura de arquivos processados

### Recomendações de Otimização

1. Ajuste `MAX_WORKERS` baseado em recursos disponíveis. Idealmente, com 20gb de memória ram recomendo o uso de no máximo 4 workers
2. Configure rate limiting para evitar throttling da API
3. Utilize cache local para embeddings recorrentes
4. Monitore memória durante processamento de livros grandes

## Segurança e Compliance

- Credenciais armazenadas em variáveis de ambiente
- Logs sem informações sensíveis
- Processamento local sem transmissão de dados além da API
- Backup automático de arquivos originais

# Métricas conhecidas

- Em geral, a geração de um livro de exercícios de 120 páginas leva em torno de 55 minutos utilizando somente um worker. Para calcular o tempo final, faça: 55/n onde n é o número de workers que você está utilizando no projeto
- O custo médio para um livro de 120 páginas é de $1.34 dólares, equivalente a R$ 7.37 na cotação atual e a quantidade de workers não influencia no custo final
