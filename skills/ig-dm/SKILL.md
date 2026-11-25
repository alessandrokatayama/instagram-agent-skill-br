---
name: ig-dm
description: >-
  Escreve DMs de Instagram que recebem resposta: a entrega da palavra-chave, a
  primeira mensagem para quem interagiu, a proposta de collab ou de publi para
  uma marca, e os dois follow-ups. Use quando o usuário disser "manda DM pra
  essa pessoa", "o que eu mando pra ela", "mensagem de prospecção", "como faço
  o follow-up", "proposta pra essa marca", ou estiver abordando alguém
  específico.
---

# ig-dm

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

O direct é o único lugar da plataforma onde o dinheiro realmente troca de mão,
e também é onde a maioria das contas queima a boa vontade que o conteúdo
conquistou. A diferença está toda em quem se mexeu primeiro.

## Os três tipos de DM, e só três valem a pena

**1. A resposta a uma mão levantada.** A pessoa comentou a palavra-chave,
respondeu a enquete, respondeu um story, ou salvou e perguntou. Ela se mexeu
primeiro. São 90% das DMs que valem a pena e convertem porque não são
prospecção.

**2. A abordagem morna.** Alguém em cujos posts o usuário vem comentando de
verdade há semanas. Já existe uma conversa em andamento.

**3. A proposta de collab ou de publi.** Uma proposta específica para uma conta
específica, com um motivo para ser ela.

Todo o resto é DM fria para desconhecido, que é o que todo mundo faz, e é por
isso que a taxa de resposta é a que é. Se o usuário pedir uma sequência fria,
diga com clareza que é a coisa de menor retorno que ele pode fazer com a mesma
hora, e ofereça a alternativa: comentar nessas dez contas por duas semanas
antes. Depois escreva, se ele ainda quiser.

## Antes de escrever, consiga os detalhes

Pergunte numa mensagem só, agrupada:

1. **Quem**: @, o que faz, e o que postou ou fez que começou isso.
2. **O gatilho**: o motivo real de mandar mensagem hoje. Uma palavra que
   comentou, um story que respondeu, um post que publicou. Não "tem o perfil do
   meu cliente ideal".
3. **O que o usuário quer**: conversa, venda, collab, indicação. Seja honesto
   internamente, mesmo que a mensagem não comece por isso.

Sem gatilho, não tem mensagem. Diga isso.

## A entrega da palavra-chave

A DM mais comum do pacote e a mais fácil de estragar. A pessoa comentou uma
palavra. Ela está esperando a coisa. Então:

```
{nome da pessoa}, aqui está: {a coisa, ou o link}.

{uma linha de como usar}

{uma pergunta que ela responde em quatro palavras}
```

Mande a coisa **primeiro**, na primeira mensagem, sem condição. Post de
palavra-chave que entrega "antes de mandar, me conta o que você faz?" é isca e
troca, e a pessoa lembra. A pergunta no fim é o que começa a conversa, e é
opcional para ela.

Não peça WhatsApp, e-mail ou CPF em troca da entrega. Se o usuário quer o
contato para lista, isso é outra mensagem, com a pessoa escolhendo, e o dado
precisa ser tratado conforme a LGPD.

Resposta automática a palavra-chave é recurso permitido para contas
profissionais, pelas ferramentas do Instagram ou por parceiro aprovado. Usar é
tranquilo. Mandar DM em massa sem a pessoa pedir não é, e é o caminho mais
rápido para a conta restrita.

## A primeira mensagem para alguém morno

- **Duas a quatro frases.** Tela cheia de texto é apagada.
- **Cite a coisa específica.** O comentário, o post, a resposta. Nas palavras
  da pessoa.
- **Dê antes de pedir.** Um número, um modelo, uma indicação, uma resposta.
- **Um pedido, pequeno.** "Topa uma call rápida?" vale mais que "deixa eu te
  apresentar a plataforma".
- **Sem link e sem agenda na primeira mensagem.** Parece funil porque é.
- **Sem áudio para desconhecido.** No Brasil áudio é comum, mas é para quem já
  conhece a voz do usuário. Áudio de dois minutos para quem não te conhece é
  ignorado.
- **Trate como a pessoa trata.** Se ela escreve "oi, td bem?", não responda em
  português de ofício.

## A proposta de collab ou de publi

Quatro linhas, nesta ordem: o que você viu a pessoa fazer, a ideia específica,
o que ela ganha, o que você precisa dela. Post em collab aparece nas duas
grades e alcança os dois públicos, que é a mecânica de crescimento mais forte do
Instagram que não envolve pagar ninguém. Apresente assim, e seja concreto sobre
quem faz o quê.

Se for publi paga para uma marca, inclua na proposta que o post vai ser
identificado como publicidade (rótulo de parceria paga e "#publi"), como pede
o guia do CONAR. Marca séria espera isso, e combinar antes evita discussão
depois.

## Follow-ups

Dois. É esse o número.

- **+4 dias**: traga algo novo. Nunca "só passando pra lembrar". Se não tem
  nada novo, não tem follow-up.
- **+10 dias**: a mensagem que fecha o assunto. Diga que vai parar, e pare. Ela
  traz uma fatia surpreendente das respostas, porque tira a pressão.

Depois disso, pare. Um terceiro não converte ninguém e custa a relação.

## Nunca

- Nunca automatize DM de prospecção, e nunca use ferramenta que manda em
  horário agendado para quem não interagiu. Viola os Termos de Uso do
  Instagram e restringe a conta.
- Nunca invente que assistiu algo, que tem amigo em comum, ou qualquer coisa em
  comum.
- Nunca comece com "Oi! Tudo bem? Posso te fazer uma pergunta?" e depois não
  pergunte nada.
- Nunca mande a proposta na mesma mensagem do elogio.
- Nunca peça dado de cartão ou senha por DM, nem mande chave Pix para quem não
  pediu para pagar.

## Saída

A mensagem, a contagem de caracteres, e os dois follow-ups com o dia de cada um,
tudo passado pelo `/ig-humano`. O usuário manda cada uma na mão, ou pela própria
automação aprovada, só no caso de palavra-chave.
