---
name: ig-plano
description: >-
  Monta a semana no Instagram: o que postar, em qual formato, em que horário
  (de Brasília) e com quem interagir. Use quando o usuário disser "planeja
  minha semana", "o que eu posto", "calendário de conteúdo", "não tenho nada
  pra postar", ou quiser um cronograma de posts e uma lista de interação.
---

# ig-plano

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

A sala de controle. Tudo mais neste pacote executa; esta skill decide o que é
executado. Rode uma vez por semana, sempre no mesmo dia.

## Entrada

Se existirem `voz.md`, `swipe.md` e `historico.md` na `{pasta da conta}`,
leia. O swipe file é a evidência do próprio usuário, vinda do `/ig-viral`,
sobre quais fórmulas estão funcionando no nicho dele agora, e vale mais que
qualquer coisa neste arquivo. O histórico impede o plano de repetir um tema das
últimas duas semanas.

Se não existirem, peça quatro coisas e anote:

1. O que o usuário vende, e para quem.
2. Os três ou quatro temas pelos quais ele quer ser conhecido.
3. O que aconteceu de verdade nesta semana: uma conversa com cliente, um
   número, um erro, algo que ele construiu, uma discussão que teve. É daqui que
   saem os posts.
4. Dez contas para as quais vale a pena aparecer.

## O que postar

Quatro a cinco posts por semana, pelo menos três deles Reels. Reels são o único
formato do Instagram que alcança com regularidade quem não segue a conta.
Carrossel aprofunda com quem já segue. Stories são diários e planejados à
parte.

Misture ao longo da semana, nunca dois do mesmo tipo seguidos:

| tipo | frequência | função |
| --- | --- | --- |
| **Prova** | 1 por semana | algo que aconteceu, com número. Reel. |
| **Ensino** | 1 a 2 por semana | uma coisa que a pessoa pode fazer hoje. Reel ou carrossel. |
| **Opinião** | 1 por semana | uma posição que pode te custar seguidor. Reel. |
| **História** | 1 a cada 15 dias | uma cena com um custo. Reel. |
| **Oferta** | 1 a cada 15 dias | o que você vende, dito com clareza, sem pedir desculpa. Carrossel ou stories. |

Para cada espaço, dê: o tema, o ângulo específico tirado do que aconteceu na
semana, o formato e o número da fórmula de gancho em `ig-reel/ganchos.json`.
Não é tema, é ângulo. "IA" não é plano. "A proposta que a gente perdeu porque o
rascunho tinha travessão" é um Reel.

## Datas do Brasil

Olhe o calendário antes de fechar a semana. Feriado nacional, Carnaval, Dia das
Mães (segundo domingo de maio), Dia dos Namorados (12 de junho), Dia dos Pais
(segundo domingo de agosto), Dia do Cliente (15 de setembro), Black Friday e
Natal mudam o que o público quer ver e quando está no celular. Só use uma data
se ela combina com o que o usuário vende. Ação de data comemorativa com sorteio
precisa de autorização prévia; ver `/ig-legenda`.

## Quando postar

Use o horário de Brasília (UTC-3). O Brasil não tem horário de verão desde
2019, mas tem outros fusos: uma hora a menos no Amazonas, Mato Grosso, Mato
Grosso do Sul, Rondônia e Roraima; duas a menos no Acre e no oeste do Amazonas;
uma a mais em Fernando de Noronha. Se o público é regional, use o fuso dele.

Poste quando o público está acordado e fora do trabalho. Para público
consumidor, costuma ser o começo da noite, entre 19h e 22h. Para público de
negócios, cedo, entre 7h e 8h30, ou no almoço. Isso é ponto de partida, não
regra: os insights do próprio perfil mostram quando os seguidores dele estão
online.

Mas diga isto com clareza: **o horário importa muito menos que os dois
primeiros segundos.** O Instagram continua mostrando um Reel por dias se ele
performa, e enterra um bem cronometrado que não performa. Se o usuário está
otimizando horário antes de os ganchos funcionarem, ele está polindo a coisa
errada, e você deve dizer isso.

## A rodada de interação, que não é opcional

20 minutos por dia, antes de postar, não depois. Monte uma lista de 10:

- **5 de alcance**: contas com o público que o usuário quer, onde um bom
  comentário é visto. Comente cedo, antes de a conversa ter 200 respostas.
- **3 pares**: mesmo tamanho, mesma área. É o grupo que retribui.
- **2 compradores**: pessoas que podem realmente comprar. Comente por semanas
  antes de qualquer DM, e nunca ofereça nada em comentário.

Passe a lista para o `/ig-comentario`.

## Saída

```
SEMANA DE 15 DE SETEMBRO  (horário de Brasília)

SEG  só interação  (20 min, lista abaixo)
TER  19h30  REEL       PROVA     #5  Tempo Encolhido   - proposta de 5h pra 20 min
QUA  só stories + interação
QUI  19h00  CARROSSEL  ENSINO    legenda Função B      - a cláusula em 4 slides
SEX  19h30  REEL       OPINIÃO   #2  Ordem Negativa    - pare de fazer reunião de diagnóstico
SÁB  -
DOM  18h00  REEL       HISTÓRIA  #21 Começo no Meio    - o e-mail de reembolso

STORIES  todo dia, 3 a 5 quadros, caixa de perguntas na quinta.
DATA     15/9 é Dia do Cliente: vale um story de agradecimento, sem oferta forçada.

INTERAÇÃO  (5 alcance / 3 pares / 2 compradores)
  ...

Diga "escreve terça" que eu faço o rascunho.
```

## Várias contas na mesma semana

Se o usuário pedir "a semana de todas as contas", rode `contas.py listar`,
leia voz, swipe e histórico de cada uma e monte um plano por conta, mais uma
grade final com todas juntas. Nessa grade, cuide de três coisas: o mesmo tema
não sai na mesma semana em contas que falam com o mesmo público; se é a mesma
pessoa gravando, os posts não caem no mesmo horário nem sobrecarregam o mesmo
dia; e nenhuma conta vira cópia de outra. Cada plano vai para o `plano.md` da
sua conta.

Grave o plano em `{pasta da conta}/plano.md` para as outras skills
lerem. Nada é agendado nem postado em lugar nenhum. É um plano e o usuário
executa.
