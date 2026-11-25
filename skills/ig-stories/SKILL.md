---
name: ig-stories
description: >-
  Escreve os Stories do dia: a sequência quadro a quadro, qual figurinha usar
  em cada um e a que leva as pessoas para o direct ou para o WhatsApp. Use
  quando o usuário disser "stories", "o que eu posto no story", "sequência de
  story", "ideia de enquete", "não tenho nada pra postar no story", ou quiser
  vender alguma coisa sem fazer um post sobre ela.
---

# ig-stories

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Story não é um feed menor. O feed é como desconhecidos te encontram. O story é
como quem já te segue decide se você é alguém de quem vale comprar, e é o único
lugar do Instagram em que um toque vira conversa num movimento só.

Quase ninguém fora dos seus seguidores vê isso, então a função é outra:
profundidade, não alcance.

## O formato do dia

Três a sete quadros por dia. Passando de uns sete, a taxa de pular sobe e os
últimos quadros tocam para ninguém, que é exatamente onde as pessoas colocam o
pedido.

```
1       A ABERTURA   algo acontecendo hoje, com um rosto ou uma mão.
2-3     O MEIO       o conteúdo de verdade: o processo, o resultado, o erro.
4       O PEDIDO     uma figurinha. Enquete, caixa de perguntas, quiz ou link.
5       O FECHO      a resposta, o resultado ou a preparação de amanhã.
```

Ponha o pedido no quadro 4, não no 7. A retenção cai a cada toque e o pedido
precisa ser visto por quem ainda está lá.

## As figurinhas, e para que cada uma serve de verdade

| figurinha | função | use quando |
| --- | --- | --- |
| **Enquete** | o toque mais barato que existe | você quer volume de resposta, não informação |
| **Caixa de perguntas** | colher as palavras exatas que as pessoas usam | você precisa de ideia de conteúdo ou de objeção, palavra por palavra |
| **Quiz** | ensinar deixando a pessoa errar | existe um equívoco comum no nicho |
| **Controle deslizante** | termômetro de humor | nada importante. Divertido, pouco valor |
| **Link** | a única superfície clicável além da bio | existe um lugar de verdade pra ir: loja, WhatsApp, página |
| **Contagem regressiva** | um prazo em que a pessoa pode se inscrever | lançamento, live, data de fechamento |
| **Sua vez** | alcance além dos seguidores, de vez em quando | o convite é algo que qualquer pessoa do nicho pode responder |

A caixa de perguntas é a mais subestimada da lista. Cada resposta é uma
legenda, um gancho de Reel ou uma abertura de DM escrita nas palavras do
público. Passe para o `/ig-reel` como fórmula #16.

## Regras

- **Um rosto ou uma mão no primeiro quadro.** Texto em fundo colorido é pulado,
  e o primeiro quadro decide se o resto é visto.
- **Uma ideia por quadro.** Ninguém lê parágrafo em story.
- **Texto no meio.** Em 1080x1920, nada acima de y=250 ou abaixo de y=1600. A
  linha do perfil fica em cima e a barra de resposta fica embaixo.
- **Fale com uma pessoa.** "Você", no singular. Story é a coisa mais parecida
  com DM que não é DM.
- **Não repostar o próprio post no story sem comentário.** É o quadro mais
  ignorado da plataforma. Se você aponta para um post, diga o que aconteceu nos
  comentários e por que vale voltar lá.
- **Venda no story, não no post.** Três quadros de contexto, um de oferta, um
  de prova. Essa sequência vende mais que um post sobre a mesma coisa e não
  custa alcance.
- **Publi também no story.** Story pago, com produto recebido ou com link de
  afiliado precisa de identificação visível no próprio quadro (rótulo de
  parceria paga ou "#publi"), porque story não tem legenda.

## O funil para o direct, feito com honestidade

A sequência que funciona: um story que nomeia um problema, uma caixa de
perguntas ou enquete que deixa a pessoa dizer "sou eu", e depois uma resposta
para cada pessoa que respondeu. A conversa começa porque ela falou primeiro.

No Brasil a venda muitas vezes fecha no WhatsApp. Tudo bem levar a conversa
para lá, **desde que a pessoa peça ou aceite**. Nunca adicione alguém a lista
ou grupo de WhatsApp sem consentimento, e não guarde número de telefone de
quem só respondeu uma enquete: isso é dado pessoal e cai na LGPD.

Resposta automática a palavra-chave é um recurso real e permitido para contas
profissionais, pelas ferramentas do próprio Instagram e por parceiros
aprovados. Mandar DM em massa para quem não interagiu não é, e é o que faz a
conta ser restringida. A regra é simples: **a pessoa age primeiro, depois você
responde.**

## Saída

Os quadros em ordem, cada um com o que aparece, o que é dito e qual figurinha,
mais o que fazer com as respostas:

```
STORIES  ·  terça  ·  5 quadros

1  [selfie, andando]      "Terceiro pedido de reembolso do ano. Mesmo motivo."
2  [gravação de tela]     a cláusula, marcada
3  [falando]              "Aprovação é sentimento. Entrega é data."
4  [enquete]              "Você já tomou calote por aprovação atrasada?"  Já / Ainda não
5  [texto na foto]        "Me responde aqui que eu te mando a cláusula."

Depois: todo mundo que votou "Já" recebe uma resposta. Esse é o funil inteiro.
```

Nada é postado. O usuário posta.
