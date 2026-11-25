---
name: ig-auditoria
description: >-
  Análise do que o usuário já postou: quais reels funcionaram de verdade, por
  quê, e o que parar de fazer. Use quando o usuário colar os insights do
  Instagram ou posts antigos e perguntar "o que está funcionando", "por que
  esse flopou", "lê minhas métricas", "audita meu conteúdo", ou quiser saber do
  que fazer mais.
---

# ig-auditoria

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

A única fonte honesta do que funciona para uma conta é a própria conta. Toda
regra de todo guia de Instagram, inclusive as deste pacote, é um palpite
inicial. Os últimos 30 posts do usuário são a evidência.

## Entrada

Peça o que o usuário tiver:

- Insights por post: visualizações, contas alcançadas, interações, tempo de
  visualização, salvamentos, compartilhamentos, seguidores ganhos e a parte do
  alcance que veio de não seguidores. Print serve.
- Ou o gráfico de retenção do melhor e do pior reel recente. Esse print sozinho
  vale mais que o resto junto.
- Ou só os posts e as visualizações, que dá para uma primeira passada.

Os nomes no aplicativo mudam de tempos em tempos ("Contas alcançadas",
"Visualizações", "Compartilhamentos"). Se o print estiver em inglês, traduza
sem drama; a métrica é a mesma.

Leia também `{pasta da conta}/historico.md` se existir, porque ele
registra qual fórmula de gancho cada post usou.

## O que medir de verdade

Visualização bruta é o número menos útil da tela, porque depende sobretudo de
quantas pessoas já seguem a conta. Calcule estes e mostre a conta:

| métrica | como | o que diz |
| --- | --- | --- |
| **Múltiplo** | views / mediana de views da própria conta | se foi acerto de verdade ou um dia normal |
| **Alcance de não seguidores** | % do alcance vindo de quem não segue | se viajou |
| **Retenção aos 3s** | quem ainda estava aos 3s / quem começou | se o gancho funcionou. É a nota do gancho. |
| **Tempo médio** | direto dos insights | se o meio funcionou |
| **Envios por alcance** | compartilhamentos / alcance | o sinal mais forte que dá para ganhar. Enviar é a pessoa colocar o nome dela. |
| **Seguidores por alcance** | seguidores ganhos / alcance | se o perfil converteu a atenção |

Ranqueie por múltiplo e por envios por alcance, não por views. Um reel com
4.000 views e 90 envios venceu o de 60.000 views e 11 envios.

Use número no formato brasileiro na saída: 4.100 views, 18,2x, 62%.

## Depois ache o padrão

Com os cinco melhores e os cinco piores lado a lado, procure o que separa uns
dos outros, e esteja disposto a concluir algo de que o usuário não vai gostar:

- **Retenção aos 3 segundos.** Se os melhores e os piores diferem aqui, é o
  gancho e nada mais, e todo o resto é distração.
- **Fórmula de gancho.** Quais números de `ig-reel/ganchos.json` estão nos
  cinco melhores?
- **Formato.** Reel, carrossel, imagem única.
- **Duração.** Agrupe em menos de 15s, 15 a 30s, 30 a 60s, mais de 60s.
- **Tema.**
- **Se o usuário respondeu comentários na primeira hora.**
- **Publi ou não.** Post identificado como publicidade costuma ter alcance
  diferente; compare só publi com publi.
- **Dia e horário.** Olhe isso **por último** e só se o resto não mostrar
  nada. Quase nunca é a causa, e é onde as pessoas querem que seja.

Apresente a conclusão como afirmação com a evidência junto, e diga o quanto
você confia nela. Com 30 posts dá para ver padrão. Com 6 não dá, e dizer isso é
melhor que inventar um.

## A distinção que economiza meses

**Reel com view e sem seguidor não é reel que falhou, é problema de perfil.**
Reel sem view é problema de gancho. Separe os dois antes de recomendar qualquer
coisa. Se o alcance de não seguidores é alto e seguidores por alcance é baixo,
pare de reescrever gancho e vá para o `/ig-perfil`.

## Saída

```
AUDITORIA  ·  31 posts  ·  12/jun a 5/set  ·  mediana de 4.100 views

5 MELHORES POR MÚLTIPLO
  18,2x  #3  Ninguém Te Conta     74.600 views  62% não seguidores  ret.3s 71%  128 envios
   6,4x  #1  Confissão de Custo   26.300 views  48% não seguidores  ret.3s 64%   71 envios
  ...

5 PIORES
   0,3x  #11 Lista Com Favorito    1.200 views   9% não seguidores  ret.3s 31%    2 envios
  ...

O QUE OS DADOS DIZEM
1. Retenção aos 3 segundos é a história inteira. Os cinco melhores têm média de
   66%, os cinco piores, 33%. Tudo o mais que te preocupa vem depois dos dois
   primeiros segundos.
2. Os posts em que quem se deu mal foi você: média de 8,1x contra 0,9x do resto.
   n=5. O sinal mais forte aqui, e com folga.
3. Lista de ferramentas dá view e mais nada. Muito alcance, nenhum envio,
   nenhum seguidor. Três dos seus cinco piores.
4. Dia da semana não mostra nada. As médias de terça e sexta estão dentro do
   ruído. Pare de otimizar isso.

PARE: listas de ferramenta.
FAÇA MAIS: os que têm um custo que você pagou e um número junto.
```

Os números acima mostram o formato da saída. Na auditoria real, use só os
números do usuário.

Depois passe as conclusões para o `/ig-plano`, para a próxima semana ser feita
com a evidência do próprio usuário e não com padrões, e para o `/ig-viral`,
para o swipe file ser filtrado pelas fórmulas que funcionam nesta conta.
