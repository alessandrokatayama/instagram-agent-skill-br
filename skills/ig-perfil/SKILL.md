---
name: ig-perfil
description: >-
  Dá nota de 0 a 100 para um perfil de Instagram numa rubrica de 12 partes e
  reescreve o que perde ponto: campo de nome, bio, link, destaques, os três
  fixados e a grade. Use quando o usuário disser "otimiza meu perfil", "arruma
  minha bio", "avalia meu Instagram", "por que ninguém me segue", ou colar o
  perfil e perguntar como ele soa.
---

# ig-perfil

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Quase todo mundo otimiza a coisa errada aqui. O perfil não é vitrine em que as
pessoas passeiam. É uma **tela de decisão**, que a pessoa abre depois de ver um
reel, e ele tem uns três segundos para responder uma pergunta: tem mais disso
aqui, e é pra mim?

## Entrada

Peça ao usuário para colar ou mandar print de: campo de nome, @, bio, para onde
o link aponta, nomes dos destaques, o que está fixado e as nove primeiras capas
da grade. Um print do topo do perfil mais as duas primeiras linhas da grade
basta para uma primeira avaliação.

Não entre no Instagram no lugar dele.

## Dê a nota

Leia `rubrica.json` nesta pasta. Doze itens, 100 pontos, cada um com o que é
nota máxima e como costuma falhar. Pontue todos, mostre a tabela, dê o total.
Seja honesto. A maioria dos perfis fica entre 30 e 49 na primeira avaliação, e
nota generosa não serve para nada.

```
NOTA DO PERFIL  38/100

  campo de nome      2/12   só o nome, nenhuma palavra que alguém pesquisa
  bio, 1ª linha      3/12   três substantivos e um emoji de café
  três fixados       0/10   nada fixado
  destaques          2/8    "Aleatório", "Vida", "2023"
  grade legível      4/8    seis de nove capas são um rosto no meio de uma frase
  ...
```

## Depois reescreva, nesta ordem

Corrija em ordem decrescente de pontos perdidos. Não reescreva tudo de uma vez:
o usuário precisa ir lá e trocar cada uma dessas coisas.

**1. O campo de nome (30 caracteres).** A linha em negrito embaixo da foto, não
o @. É o campo que a busca do Instagram compara, e a maioria das contas coloca
só o nome. Formato que funciona: `{Nome} | {o que faz, em palavras que se
buscam}`. Pense em como o brasileiro busca: "Bolo de pote Jundiaí", "Contador
para MEI", "Personal em casa". Cidade no nome ajuda quem vende localmente. Dê
três opções.

**2. Primeira linha da bio.** Para quem é e o que muda. Não é cargo, não são
adjetivos, não é lista de identidades separadas por barra. O resto dos 150
caracteres traz uma prova ou uma oferta simples.

**3. Os três fixados.** Três espaços, três funções: a melhor prova, a
explicação mais clara da oferta, a melhor apresentação da pessoa. É a correção
de maior impacto no perfil todo e leva quatro toques. Grade sem fixado mostra o
que foi postado por último, que é cara ou coroa.

**4. Destaques.** Quatro a seis, com o nome das perguntas que o comprador faz:
Preços, Resultados, Como funciona, Sobre, Entrega, Depoimentos. Não
"Aleatório". Apague o resto. Depoimento precisa ser real e com autorização de
quem falou.

**5. O link.** Um destino que combina com o que a bio acabou de prometer. Se a
venda acontece no WhatsApp, o link vai direto pro WhatsApp com uma mensagem
pronta (`wa.me/55...?text=...`), e não para um agregador com dez botões. São
permitidos até cinco links; dois já é cardápio, e cardápio converte pior que
porta.

**6. Capas da grade.** As nove primeiras em miniatura. Capa de reel é
escolhida, não deixada no primeiro quadro. Quatro palavras de texto na capa
deixam a grade legível de uma vez.

## Saída

A tabela de notas, depois as reescritas em blocos prontos para copiar, na ordem
de correção, cada uma passada pelo `/ig-humano`. No fim, dê a nota de novo e
mostre a diferença com honestidade. Se a reescrita chega a 84 e não a 98, diga
84, e diga o que falta, que normalmente é a grade, o hábito de story e um post
fixado que ainda não existe. Nada disso é reescrita.

Esta skill não salva nada no Instagram. O usuário edita cada campo.
