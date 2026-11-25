---
name: ig-legenda
description: >-
  Escreve a legenda do Instagram em português (a linha que sobrevive ao corte
  do "... mais", o corpo, o único pedido, os termos de busca, até cinco
  hashtags e a identificação de publi quando houver) e revisa antes de sair.
  Use quando o usuário disser "escreve a legenda", "legenda pra isso", "o que eu
  coloco na descrição", tiver um reel ou carrossel pronto e precisar do texto,
  ou perguntar de hashtags.
---

# ig-legenda

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Uma ferramenta fica nesta pasta e ela roda:

```bash
python3 legenda.py legenda.txt
python3 legenda.py legenda.txt --busca "proposta comercial,preço de agência"
```

Ela imprime a legenda do jeito que o feed imprime: os primeiros 125 caracteres
numa caixa, o resto atrás do toque. Leia essa caixa antes de ler qualquer outra
coisa que você escreveu.

## Primeiro, decida qual é a função desta legenda

É a decisão que estraga legendas quando é pulada.

**Função A: o vídeo já fisgou.** Um Reel traz o próprio gancho nos dois
primeiros segundos, falado e na tela. A legenda não é um segundo gancho, e
competir com o vídeo é o jeito de perder os dois. A função dela é o pedido, o
contexto que faz o pedido fazer sentido e as palavras que as pessoas buscam.

**Função B: a legenda é o conteúdo.** Uma foto, uma imagem única, a capa de um
carrossel que abre um suspense. Aqui a linha um é o gancho e funciona igual ao
gancho de um Reel: concreta, curta e cortada num suspense, não no meio de uma
oração.

Diga qual você está escrevendo. Se o usuário tem um Reel com gancho forte,
escreva A e explique por quê.

## O formato

```
Linha 1     125 caracteres visíveis. Função A: o pedido, direto.
            Função B: o gancho.
            Nunca saudação, nunca hashtag, nunca emoji como primeiro caractere.
            Se é publi, a identificação vem aqui (ver abaixo).
Corpo       parágrafos curtos, uma linha em branco entre eles. De dois a seis.
            É aqui que moram os termos de busca.
O pedido    um. Comentar uma palavra, salvar ou chamar no direct. Um.
Hashtags    até cinco, numa linha só no fim, ou nenhuma.
```

O limite é 2.200 caracteres e quase nada precisa disso. Uma legenda que ganha o
toque e entrega 600 caracteres vence uma que entrega 1.800.

## Hashtags, com honestidade

Hashtag não é mais alavanca de alcance, e a plataforma disse isso com uma
mudança de produto. **O Instagram limitou a cinco hashtags por post em 18 de
dezembro de 2025**, contra trinta antes, orientando criadores a usar menos e
mais específicas. Adam Mosseri já tinha dito no começo de 2025 que hashtag não
aumenta alcance e funciona como etiqueta.

Então: até cinco, específicas, como etiqueta de assunto. Se o usuário tem um
bloco de vinte salvo no bloco de notas, esse bloco virou peso morto, e o
revisor reprova.

`#viral`, `#fyp`, `#explorar`, `#reelsbrasil`, `#instabrasil` não descrevem
nada. Corte.

**Acento importa.** `#promoção` e `#promocao` (ou `#salãodebeleza` e
`#salaodebeleza`) são hashtags diferentes. Muita gente digita sem acento no
celular. Antes de escolher, abra as duas versões na busca e use a que o
público realmente usa. O revisor avisa quando uma hashtag tem acento.

## Termo de busca importa mais que hashtag

A busca do Instagram lê o texto da legenda. Então a frase pela qual o usuário
quer ser encontrado vai na legenda como alguém digitaria, numa frase que soa
normal. "Proposta comercial" como palavras na linha três, e não
"#propostacomercial" num bloco no fim. Pense em como o brasileiro digita: às
vezes sem acento, às vezes com abreviação ("orçamento" e "orcamento").

Peça dois ou três desses termos e passe para o revisor:

```bash
python3 legenda.py rascunho.txt --busca "proposta comercial,preço de agência"
```

O revisor ignora acento ao procurar os termos, então "orcamento" encontra
"orçamento".

## Publicidade: regra do Brasil

Se o post é pago, foi feito com produto ou viagem recebidos de uma marca, ou
tem **link de afiliado**, ele precisa ser identificado como publicidade. O guia
do CONAR para influenciadores, atualizado em maio de 2026, pede:

- de preferência, a ferramenta da própria plataforma (o rótulo **"Parceria
  paga"** do Instagram);
- ou termos claros como `#publi` ou `#publicidade`;
- e que a identificação apareça **sem precisar abrir o "... mais"**.

Por isso o revisor dá ERRO quando acha "#publi", "publicidade", "parceria paga"
ou "afiliado" só depois do corte. Não decida pelo usuário se um post é publi ou
não; pergunte, e se for, coloque na primeira linha.

**Sorteio exige autorização.** Sorteio, concurso ou vale-brinde feito por
empresa para divulgar produto precisa de autorização prévia da Secretaria de
Prêmios e Apostas do Ministério da Fazenda, que leva em média 15 dias. Se o
usuário pedir legenda de sorteio, avise disso antes de escrever, e não escreva
como se fosse só "comenta e marca três amigos".

## Regras

- **Fonte não é link.** "Fonte: site.com.br" é citação e o revisor não reclama.
  Em página de história e notícia, dar a fonte é obrigatório.
- **Toda palavra da linha de hashtags precisa do #.** `ArrancadaHeroica` sem o
  `#` é só texto; o revisor dá ERRO.
- **Sem link na legenda.** Legenda não é clicável. URL no texto é letra morta
  que diz "eu não uso esta rede". Bio, direct, ou o adesivo de link no story.
- **Um pedido.** Dois pedidos valem o mesmo que nenhum. O `legenda.py` conta.
- **A palavra-chave precisa ser fácil de digitar.** Uma palavra, sem espaço,
  sem emoji e **sem acento**, e falada no vídeo também. `Comenta CONTRATO`
  funciona. `Comenta "o guia do contrato"` não. Sem acento porque metade das
  pessoas digita sem, e uma automação de resposta pode não reconhecer a outra
  metade.
- **Escreva o primeiro comentário separado** se tiver link. Diga isso no recibo.
- **Emoji como pontuação, não como enfeite.** O revisor aponta mais de 4 a cada
  100 caracteres.
- **Texto alternativo vale 20 segundos.** Em carrossel e foto, escreva. É lido
  por leitor de tela e pelo Instagram.

## O ciclo

1. Decida Função A ou B e diga qual.
2. Pergunte se é publi, presente de marca ou tem link de afiliado.
3. Escreva.
4. Rode o `/ig-humano`. Legenda é curta, então clichê aparece mais aqui do que
   em qualquer outro lugar do pacote.
5. Rode o `legenda.py` com os termos de busca do usuário. Corrija todo ERRO.
   Decida cada ATENÇÃO em voz alta, não em silêncio.
6. Entregue o bloco pronto para copiar, e depois o recibo:

```
LEGENDA PRONTA
função:     A - o reel carrega o gancho
visível:    118 de 125 caracteres usados antes do corte
publi:      não
pedido:     um, comentar CONTRATO
hashtags:   3
busca:      "proposta comercial" na linha 3, "preço de agência" na linha 5
revisor:    PRONTA
```

Nada é postado. O usuário cola.
