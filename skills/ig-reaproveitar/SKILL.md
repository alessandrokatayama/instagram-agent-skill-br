---
name: ig-reaproveitar
description: >-
  Transforma um material longo (vídeo do YouTube, podcast, live, newsletter,
  post de blog, aula ou reunião com cliente) numa semana de reels e
  carrosséis. Use quando o usuário disser "reaproveita isso", "transforma em
  reels", "tenho um vídeo/podcast/transcrição", "corta isso", ou colar algo
  longo e quiser no Instagram.
---

# ig-reaproveitar

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Um bom material longo tem quatro a seis posts dentro. A maioria tira um e joga o
resto fora.

## Entrada

Uma transcrição, um artigo, uma newsletter, um roteiro, um resumo de reunião,
uma live. Se o usuário mandar um link e esta sessão tiver ferramenta de
transcrição, use; senão, peça para colar. Leia tudo antes de extrair qualquer
coisa.

Se a fonte é um vídeo do próprio usuário, peça o arquivo também. Reel feito com
a filmagem dele vale mais que um feito com as palavras dele lidas de novo.

Se a fonte é de outra pessoa (o vídeo de outro criador, uma palestra, um
podcast alheio), pare: reaproveitar conteúdo de terceiro como se fosse seu não
é reaproveitar. Dá para comentar, citar um trecho curto com crédito ou reagir,
mas não recortar e postar.

## Extraia, não resuma

Resumo de vídeo não é Reel. Ninguém quer o resumo. Percorra o material e tire as
coisas que ficam em pé sozinhas:

| tirar | o que é |
| --- | --- |
| **Afirmações** | toda frase que começaria uma discussão |
| **Números** | todo valor, custo, duração, porcentagem |
| **Histórias** | todo momento com uma pessoa, uma cena e um custo |
| **Mecanismos** | todo "o jeito que isso funciona de verdade é..." |
| **Erros** | toda admissão de algo que deu errado |
| **Frases** | toda frase que já dá para citar como está |

Liste o que encontrou, com contagem, antes de escrever qualquer coisa. Se o
material rende menos de quatro itens, ele é fraco, e quatro posts espremidos
dele vão ser fracos também. Diga isso.

## Depois escolha o formato de cada extração

Nem tudo é Reel.

- **Afirmação, erro, história** viram Reel. Precisam de voz e rosto.
- **Mecanismo, lista numerada** viram carrossel. Precisam ser relidos.
- **Uma frase citável** vira quadro de story, não post.

## Depois monte a semana

Cada extração vira um post, e cada post se sustenta sozinho por completo. Quem
assiste não viu a fonte e nunca vai ver. Nunca escreva "como eu falei no meu
último vídeo". O post é a coisa.

Dê uma fórmula de gancho de `ig-reel/ganchos.json` para cada um, e varie. Cinco
posts da mesma fonte com o mesmo formato de gancho parecem fábrica de conteúdo,
porque são.

Se a fonte é vídeo do próprio usuário, **use a filmagem de verdade**. O trecho
em que ele disse a coisa, com a reação real, vale mais que regravar, sempre.
Corte na frase, não na respiração. Confira se a trilha do vídeo original pode
ser usada no Instagram; música de fundo de live costuma derrubar o Reel por
direito autoral.

Ordene na semana para a afirmação mais forte ir primeiro, a história cair no
meio da semana, e o mecanismo ir por último, quando quem gostou dos anteriores
está esperando por ele.

## Saída

```
FONTE: "Por que a gente acabou com a reunião de diagnóstico" (podcast de 42 min, 8.900 palavras)

ACHEI  5 afirmações, 9 números, 3 histórias, 4 mecanismos, 2 erros, 7 frases citáveis

SEMANA
TER  REEL       #2  Ordem Negativa    Pare de fazer reunião de diagnóstico
                                      usa o trecho de 14:20, ele ri no fim
QUA  CARROSSEL  legenda Função B      O formulário de 4 perguntas que substituiu a reunião
SEX  REEL       #21 Começo no Meio    "...e ele pediu reembolso nove dias depois"
DOM  REEL       #5  Tempo Encolhido   Seis horas por semana de volta, um link apagado

Diga "escreve terça" que eu faço o rascunho.
```

Depois escreva sob pedido, um de cada vez, cada um pelo `/ig-reel` e pelo
`/ig-humano`. Não despeje quatro roteiros prontos de uma vez. Vão soar todos
iguais e o usuário não vai gravar nenhum.
