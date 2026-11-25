---
name: ig-resposta
description: >-
  Cuida dos comentários embaixo dos reels e posts do próprio usuário: escreve
  respostas para os que valem a pena, separados por quanto valem. Use quando o
  usuário colar os comentários, disser "responde esses", "cuida dos meus
  comentários", "alguém falou X no meu reel", ou estiver lidando com crítica,
  hater ou um cliente em potencial nos comentários.
---

# ig-resposta

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

A conversa embaixo do seu próprio post é onde o alcance se decide. Cada resposta
é mais uma interação no post, as respostas da primeira hora fazem a maior parte
do trabalho, e no Instagram uma resposta também pode ser um Reel, que é a
jogada mais subutilizada da plataforma.

Mas o valor não é igual entre os comentários, então esta skill separa antes de
escrever.

## Entrada

O usuário cola os comentários, de preferência com os @. Print serve. Não varra
a conversa com navegador.

## Triagem primeiro

Coloque cada comentário num de seis grupos e diga as contagens:

| grupo | o que é | o que recebe |
| --- | --- | --- |
| **PALAVRA** | a palavra que você pediu para comentarem | o que foi prometido, mandado na mão ou pela sua ferramenta aprovada |
| **CLIENTE** | alguém descrevendo o problema que você resolve | uma resposta de verdade em público, depois uma porta |
| **CONTEÚDO** | traz dado, discorda, complementa | a resposta mais longa da conversa |
| **PERGUNTA** | uma pergunta que muita gente tem | essa vira Reel, não só resposta |
| **APOIO** | "🔥", "amei", uma marcação | uma curtida e 3 a 8 palavras, no máximo |
| **RUÍDO** | propaganda, spam, má-fé, provocação, golpe | nada, ou uma linha e pronto |

Escreva nessa ordem e pare quando o valor acabar.

## A jogada que quase todo mundo perde

Se uma pergunta nos comentários é uma que trinta outras pessoas também têm,
**responda com um Reel**. O Instagram prende o comentário no novo vídeo como
figurinha, quem perguntou é avisado, e uma pergunta com demanda real vira um
post com o gancho já escrito. Marque toda PERGUNTA que se encaixa e passe para
o `/ig-reel` como fórmula #16.

## Como responder

- **Responda a pergunta de verdade.** Se perguntaram como, diga como, na
  resposta. Não mande para o direct alguém que podia ter a resposta ali.
- **Use o nome da pessoa uma vez**, no começo, sem exclamação.
- **Acompanhe o tamanho.** Comentário de quatro palavras não recebe resposta
  de quatro linhas.
- **Para crítica:** reconheça primeiro a parte verdadeira, nas palavras da
  pessoa, depois sustente sua posição. Nunca apague, nunca fique na defensiva,
  nunca responda duas vezes na mesma conversa.
- **Para hater:** nada. Resposta é alcance, e alcance é o que ele veio buscar.
  Oculte o comentário se for ofensivo. Os controles de comentário do Instagram
  existem, e usar não é perder.
- **Para cliente em potencial:** responda por completo em público. A porta é
  uma frase no fim e é oferta de ajuda, não venda. A resposta pública é o que
  faz a próxima pessoa te chamar no direct.
- **Para pergunta de preço:** se o preço é público, responda o preço. "Chama no
  direct que eu passo" para quem só perguntou quanto custa afasta muita gente,
  e todo mundo nos comentários percebe.
- **Para golpe e perfil falso** (alguém se passando pela marca, oferecendo
  "suporte" ou "promoção"): avise o usuário, sugira denunciar e ocultar, e
  escreva uma resposta curta dizendo que o perfil oficial é só este.

## Comentários de palavra-chave

Se o post usou um pedido de palavra-chave, esses comentários são a razão do
post existir. Cada um é uma pessoa que levantou a mão. Responda cada um e
mande o que foi prometido. Se o usuário tem automação pelas ferramentas do
próprio Instagram ou por um parceiro aprovado, diga isso e deixe rodar; se não
tem, as respostas são na mão, e tudo bem nesse volume. Nunca mande DM em massa
para quem não comentou.

## Saída

Um bloco, agrupado, cada resposta pronta para copiar e já humanizada:

```
RESPOSTAS  ·  84 comentários  ·  41 PALAVRA, 2 CLIENTE, 3 CONTEÚDO, 2 PERGUNTA, 34 APOIO, 2 RUÍDO

PALAVRA  (41)  mandar a cláusula. Uma linha cada, mesmo calor, sem copiar e colar.

CLIENTE
@perfil - "aconteceu exatamente isso com a gente em junho"
> O que resolveu pra gente foi tirar o pagamento da aprovação de vez. Se for
> útil, te mando o texto da cláusula.

PERGUNTA -> REEL
@perfil - "e se o cliente se recusar a assinar?"
  34 curtidas nesse comentário. Isso é Reel, não resposta. Fórmula #16.

RUÍDO  (2)  pulados. Responder dá alcance pra eles.
```

Depois a trava: nada é postado até o usuário dizer sim. Ele cola as respostas.
