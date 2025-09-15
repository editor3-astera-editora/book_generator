# modules/preambulo.py

# Conteúdo do arquivo preambulo.tex que será salvo
PREAMBULO_TEX_CONTENT = r"""
% --- Pacotes de idioma e codificação ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}

% --- Geometria e layout ---
\usepackage{geometry}
\usepackage{changepage}
\usepackage{fancyhdr}
\usepackage{tocloft}
\usepackage{titlesec}

% --- Tipografia ---
\usepackage{lmodern}

% --- Cores e gráficos ---
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{graphicx}
\usepackage{colorspace}

% --- Matemática ---
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{calc}

% --- Lógica e automação ---
\usepackage{ifthen}
\usepackage{etoolbox}
\usepackage{atbegshi}
\raggedbottom

% --- Quadros e caixas ---
\usepackage[most]{tcolorbox}

% --- Inserção de elementos no fundo ---
\usepackage{eso-pic}

\usepackage{enumitem}

\setlist[itemize,1]{label=\textbullet}
\setlist[itemize,2]{label=$\cdot$} 

\usepackage{caption}

\setlist[itemize,3]{label=$\cdot$}

% --- Definições de cor spot ---
\definespotcolor{Gabarito}{Gabarito}{0.0 1.0 0.0 0.0}

% --- Paleta de cores personalizada ---
\definecolor{dollarbill}{rgb}{0.52, 0.73, 0.4}
\definecolor{etonblue}{rgb}{0.59, 0.78, 0.64}
\definecolor{grannysmithapple}{rgb}{0.66, 0.89, 0.63}
\definecolor{persianred}{rgb}{0.8, 0.2, 0.2}
\definecolor{persianblue}{rgb}{0.11, 0.22, 0.73}
\definecolor{cadetblue}{rgb}{0.37, 0.62, 0.63}
\definecolor{ceruleanblue}{rgb}{0.16, 0.32, 0.75}
\definecolor{flame}{rgb}{0.89, 0.35, 0.13}

\newcommand{\answerlines}[1]{%
    \vspace{0.5cm}% espaço fixo entre o enunciado e o bloco de resposta
    \begin{tikzpicture}[overlay=false, remember picture]
        \foreach \i in {0,...,7} {
            \draw[gray, thin] (0, -\i*0.8cm) -- (\linewidth, -\i*0.8cm);
        }
        \node[
              text width=\linewidth, 
              inner sep=0pt,
              anchor=north west] 
              at (0.2cm, 0.4cm) {%
              \color{Gabarito}
                \parbox{\linewidth}{%
                    \setlength{\baselineskip}{0.8cm}%
                    \setlength{\lineskip}{0pt}%
                    \setlength{\parskip}{0pt}%
                    \raggedright%
                    #1%
                }%
              };
    \vspace{1cm}
    \end{tikzpicture}%
}

\newcommand{\emptylines}{%
    \begin{tikzpicture}[overlay=false, remember picture]
        \foreach \i in {0,...,7} {
            \draw[gray, thin] (0, -\i*0.8cm) -- (\linewidth, -\i*0.8cm);
        }
    \end{tikzpicture}%
    % Sem \vspace aqui também
}

% Comando para questões de lacunas com linha embaixo
\newcommand{\fillblank}[2][3cm]{%
    \underline{\makebox[#1]{\textcolor{handwritingblue}{\itshape #2}}}%
}

% --- Controle de unidades ---
\newcounter{unitcounter}
\setcounter{unitcounter}{0}
\newif\ifunitcoverpage
\unitcoverpagefalse

\newcommand{\iniciarunidade}{%
    \newpage
    \stepcounter{unitcounter}%
    \unitcoverpagetrue
    \thispagestyle{empty}%
    \mbox{}
    \newpage
    \global\unitcoverpagefalse
}

% --- Estilos de título ---
\titleformat{\section}
  {\Huge\color{flame}\bfseries}{}{0pt}{}
\titleformat{\subsection}
  {\Large\bfseries}{}{0pt}{}

% --- Estilos tcolorbox ---
\tcbset{
  destaque/.style={
    colback=dollarbill!10,
    colframe=dollarbill,
    arc=4mm,
    boxrule=0.8pt,
    left=4mm, right=4mm, top=2mm, bottom=2mm,
    enhanced,
  },
  quadrodesenho/.style={
    colback=white,
    colframe=black,
    coltext=Gabarito, % cor que o xcolor entende
    boxrule=0.5mm,
    arc=3mm,
    width=\dimexpr\linewidth\relax,
    boxsep=5pt,
    left=5pt, right=5pt, top=5pt, bottom=5pt,
    before skip=20pt,
    after skip=20pt
},
  exemploresolucao/.style={
    colback=white,
    colframe=black,
    boxrule=0.5mm,
    arc=3mm,
    width=\linewidth,
    height=7cm,
    boxsep=5pt,
    left=5pt, right=5pt, top=5pt, bottom=5pt,
    before skip=20pt,
    after skip=20pt
  },
  resposta/.style={
    colback=persianred!50,
    colframe={rgb:red,0.9;green,0.3;blue,0.24},
    fonttitle=\bfseries,
    boxrule=0.5mm,
    arc=2mm,
    top=4mm, bottom=4mm, left=4mm, right=4mm,
    width=\linewidth,
  },
  conclusao/.style={
    colback=persianblue!25,
    colframe=persianblue!50,
    boxrule=0.5mm,
    arc=2mm,
    top=4mm, bottom=4mm, left=4mm, right=4mm,
    width=\linewidth,
  }
}

% --- Fundo decorativo ---
\AddToShipoutPictureBG{%
    \ifcase\value{page}%
    \or
        \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=17]{imagens/fundo_decorativo.pdf}}%
    \or
        \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=15]{imagens/fundo_decorativo.pdf}}%
    \else
        \ifunitcoverpage
            \ifcase\value{unitcounter}%
            \or
                \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=1]{imagens/fundo_decorativo.pdf}}%
            \or
                \ifthenelse{\isodd{\value{page}}}{%
                    \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=3]{imagens/fundo_decorativo.pdf}}%
                }{%
                    \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=4]{imagens/fundo_decorativo.pdf}}%
                }%
            \or
                \ifthenelse{\isodd{\value{page}}}{%
                    \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=5]{imagens/fundo_decorativo.pdf}}%
                }{%
                    \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=6]{imagens/fundo_decorativo.pdf}}%
                }%
            \or
                \ifthenelse{\isodd{\value{page}}}{%
                    \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=7]{imagens/fundo_decorativo.pdf}}%
                }{%
                    \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=8]{imagens/fundo_decorativo.pdf}}%
                }%
            \fi
        \else
            \ifthenelse{\isodd{\value{page}}}{%
                \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=9]{imagens/fundo_decorativo.pdf}}%
            }{%
                \put(0,0){\includegraphics[width=\paperwidth,height=\paperheight,page=10]{imagens/fundo_decorativo.pdf}}%
            }%
        \fi
    \fi
}
"""

# Template para o arquivo .tex principal
MAIN_TEX_TEMPLATE = r"""
\documentclass[12pt, a4paper, oneside]{book}

\input{preambulo.tex}

\setlength{\cftbeforesecskip}{10pt}
\setlength{\cftbeforesubsecskip}{6pt}

\geometry{
  paperwidth=226.59mm,
  paperheight=313.59mm,
  left=33.295mm,
  right=33.295mm,
  top=60.595mm,
  bottom=40.295mm,
  footskip=1.9cm 
}

\newcommand{\sectiontoc}[1]{%
  \section*{#1}%
  \addcontentsline{toc}{section}{#1}%
}

\captionsetup{
  justification=centering,
  singlelinecheck=true,
  labelfont=bf,
}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt} 
\renewcommand{\footrulewidth}{0pt} 
% O placeholder BOOK_NAME_PLACEHOLDER para Python usa chaves simples
\fancyfoot[L]{\ifthenelse{\isodd{\value{page}}}{{livro_nome}}{\thepage}}
\fancyfoot[R]{\ifthenelse{\isodd{\value{page}}}{\thepage}{{livro_nome}}}

\begin{document}

\begin{center}
    \vspace*{5cm}
    \vspace{1cm}
\end{center}
\newpage

% Sumário
\newgeometry{
  top=3cm,      
  bottom=4cm,  
  left=1.5cm,  
  right=5.5cm, 
  footskip=2cm 
}
\renewcommand{\contentsname}{}
\tableofcontents
\restoregeometry

{BODY_PLACEHOLDER}

\end{document}
"""