---
name: ig-carrossel
description: >-
  Monta um carrossel de Instagram em português: a capa que ganha o arraste, o
  texto slide a slide e os arquivos 1080x1350 para subir. Use quando o usuário
  disser "carrossel", "slides", "post de arrastar", "transforma isso num
  carrossel", ou tiver uma ideia em formato de lista ou passo a passo que
  morreria como imagem única.
---

# ig-carrossel

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Carrossel é o formato da grade que mais segura tempo de tela, porque arrastar é
interação e rolar não é. Ele também ganha uma segunda chance: o Instagram pode
mostrar o carrossel de novo, a partir de um slide mais adiante, para quem não
interagiu da primeira vez. Então o slide dois também precisa se sustentar
sozinho.

O formato premia uma ideia quebrada em passos. Pune legenda picada em pedaços.

## Quando usar em vez de Reel

Use carrossel quando a ideia tem **sequência e precisa ser relida**: passo a
passo, um método com partes, um antes e depois, uma lista que merece print. Use
Reel quando a ideia tem movimento, rosto, ou um resultado que precisa ser visto
acontecendo.

Se a ideia é uma afirmação só, não é nenhum dos dois. Passe para o `/ig-reel` e
diga isso.

## Estrutura

6 a 10 slides. O limite é 20, e 20 quase sempre é um livro que ninguém termina.
Abaixo de 5, o arraste nem começa.

```
1         CAPA      o gancho. 6 palavras ou menos, num tamanho que dá pra ler
                    na grade em miniatura. Uma linha de promessa embaixo.
2         O QUE     por que isso importa, numa frase. Este slide também é uma
          ESTÁ EM   segunda capa, então não pode ser preparação.
          JOGO
3 a N     UMA IDEIA POR SLIDE. Título de 3 a 7 palavras, no máximo 25 palavras
                    embaixo. Se um slide precisa de parágrafo, são dois slides.
N+1       RESUMO    tudo numa lista. É o slide do print.
ÚLTIMO    CTA       uma ação. Salvar, comentar uma palavra ou seguir. Uma.
```

## Regras do texto

- **A capa é 80% do resultado.** Seis palavras. Grande. Nada no resto salva uma
  capa que ninguém arrasta.
- **Português ocupa mais espaço que inglês.** Título que cabia em inglês estoura
  em português. Corte palavra, não diminua a fonte.
- **Pense no corte da grade.** A grade do perfil corta num retângulo em pé, e a
  proporção exata já mudou mais de uma vez. Faça em 1080x1350 e mantenha o texto
  da capa bem no meio, longe dos 120 pixels de cada borda, e o corte deixa de
  importar.
- **Numere os slides** (3/8). A conclusão sobe quando a pessoa vê o fim.
- **Nenhum slide é parágrafo.** Se não cabe em 25 palavras, divida.
- **O slide de resumo é o que vai pro print e é enviado.** Envio é o sinal mais
  forte que dá pra ganhar. Faça ele se sustentar sozinho, legível sem contexto.
- **O @ em todo slide**, pequeno, num canto de baixo. Print viaja sem você.
- **Texto alternativo pelo menos na capa.** É lido por leitor de tela e pelo
  Instagram.
- **Publi é publi.** Se o carrossel é pago ou tem link de afiliado, a
  identificação vai na primeira linha da legenda ou no rótulo de parceria paga,
  e é bom que apareça também na capa. Ver `/ig-legenda`.

## Gerando os arquivos

O Instagram quer 1080x1350 (4:5), JPEG ou PNG, até 20 itens. Monte em HTML e
imprima cada slide:

```bash
# uma <section> por slide, 1080x1350, page-break-after: always
# depois Chrome headless --print-to-pdf, ou o conversor HTML para imagem que você já usa
```

Escreva o HTML com `width:1080px; height:1350px`, uma cor de destaque só, e
fonte de no mínimo 32px, porque vai ser lido num celular a um terço do tamanho
real. Use uma fonte com acentuação completa (á, ã, ç, õ); fonte decorativa sem
"ç" quebra o slide. Se o projeto tem uma skill de marca ou um design system,
use, e não invente paleta.

## Saída

Primeiro o texto slide a slide, numa lista numerada que o usuário lê em dez
segundos e edita antes de qualquer coisa ser gerada. Depois a **legenda**, que
num carrossel é a Função B do `/ig-legenda`: aqui a legenda trabalha, porque a
capa já gastou suas seis palavras.

Passe os dois pelo `/ig-humano`. Gere os arquivos só depois que o usuário
aprovar o texto.

```
CARROSSEL  ·  8 slides

1  CAPA      A CLÁUSULA DE R$ 18 MIL
             A frase que eu coloco hoje em todo contrato.
2  EM JOGO   Eu aprovei o trabalho. Nove dias depois pediram o dinheiro de volta.
3            O QUE ELA DIZ
             Pagamento na entrega, não na aprovação.
...
7  RESUMO    As quatro linhas, em ordem.
8  CTA       Comenta CONTRATO que eu te mando a cláusula inteira.

Legenda: Função B, gancho na linha 1, um pedido, 3 hashtags.
```

Os valores do exemplo mostram formato. Nunca use número que o usuário não deu.

Nada é enviado. O usuário posta.
