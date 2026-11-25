---
name: ig-comentario
description: >-
  Escreve comentários em posts e reels de outras pessoas que soam como alguém
  com opinião, não como robô. Use quando o usuário colar um post ou reel e
  quiser um comentário, disser "comenta nisso", "interage com isso", "o que eu
  falo aqui", ou quiser um lote para a rodada diária de interação.
---

# ig-comentario

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Comentar são os vinte minutos de maior retorno no Instagram e os mais fáceis de
fazer mal. Um comentário no topo de um reel com 40 mil views é visto por mais
gente que a maioria dos posts de uma conta, e é o único lugar em que um
desconhecido toca direto no perfil.

Comentário genérico é pior que nenhum. Gasta um toque que não leva a lugar
nenhum e marca a conta como "conta de grupo de engajamento" para a única pessoa
cuja opinião importava: o criador.

## Entrada

O usuário cola o texto do post ou reel, ou manda print, com o nome da conta. Se
ele mandar um link que você não consegue abrir, peça para colar. Não use
navegador para varrer o feed e não poste nada.

## Os nove tipos de comentário

Escolha pelo que o post realmente é. Nunca vá no tipo 1 por padrão.

| # | tipo | quando | formato |
| --- | --- | --- | --- |
| 1 | **Acrescenta um dado** | o post afirma algo que você sustenta com número | "Aqui foi igual: 40% dos..." |
| 2 | **O caso que faltou** | o post está certo mas incompleto | "Isso vale até {condição}." |
| 3 | **Discordar com respeito** | você acha de verdade que está errado | diga primeiro onde concorda, depois onde diverge |
| 4 | **Estende uma frase** | uma frase do post é a boa | cite, construa em cima |
| 5 | **A pergunta de verdade** | o post pulou a parte difícil | uma pergunta, específica |
| 6 | **O recibo** | você já fez o que ele descreve | o que aconteceu, duas frases |
| 7 | **A correção** | tem um erro de fato | esteja certo, seja breve, gentil e seguro |
| 8 | **Outro ângulo** | fatos certos, enquadramento errado | "Outro jeito de ler isso:" |
| 9 | **A frase curta** | o post não precisa de nada, você quer presença | menos de 10 palavras, tem que ser engraçada ou verdadeira |

## Regras

- **Uma a três frases.** Comentário no Instagram é lido numa coluna estreita
  embaixo de um vídeo. Parágrafo vira "ver mais" e ninguém toca.
- **Nunca comece com** "Que post incrível", "Amei", "Verdade demais", "Isso 👏",
  "Precisava ler isso hoje", "Arrasou" ou o nome do criador com exclamação. Tudo
  isso é invisível.
- **Nada de comentário só com emoji**, e nenhum emoji como primeiro caractere.
- **Nunca repita o reel.** Todo mundo que está vendo acabou de assistir.
- **Uma ideia.** Comentário com dois pontos parece sequestro do post.
- **Diga a coisa específica.** Se o comentário serviria em qualquer post do
  assunto, não é comentário, é ruído.
- **Nunca venda. Nunca.** Nem a oferta, nem o link, nem "dá uma olhada no meu
  perfil", nem "chama no direct". É o jeito mais rápido de ser bloqueado
  justamente pela pessoa que você queria alcançar.
- **Cedo importa mais aqui que em qualquer lugar.** Um comentário na primeira
  hora de um reel que depois viaja é levado junto.

## Saída

Dê **duas opções de tipos diferentes**, com rótulo, mais uma linha dizendo qual
você postaria e por quê. Passe as duas pelo `/ig-humano` antes: comentário é
curto, então um travessão ou uma frase pronta pesa mais que numa legenda.

```
OPÇÕES DE COMENTÁRIO  (no reel da @conta sobre preço)

[6 · Recibo]
A gente subiu 40% em março do ano passado e perdeu exatamente um cliente, o que
ocupava metade da caixa de entrada. Levou oito meses pra perder o medo.

[3 · Discordar com respeito]
Concordo na ancoragem. Onde eu discordaria é fazer isso no meio do projeto. A
gente tentou e perdeu uma renovação que estava tudo certo.

Posta o primeiro. Ele cede alguma coisa e tem número.
```

Os números do exemplo mostram formato. No comentário do usuário, só entra
número que ele deu.

## Modo lote

Para a rodada de interação, peça os 5 a 10 posts como texto colado numa
mensagem só, devolva um comentário para cada num bloco único, e mantenha uma
anotação em `{pasta da conta}/historico.md` de quem já recebeu comentário
na semana. Comentar nas mesmas três contas todo dia é visível e parece
exatamente o que é.

## Nunca

Não poste automaticamente, não automatize comentários e não use navegador para
publicar no lugar do usuário. Interação automatizada viola os Termos de Uso do
Instagram e bloqueia a conta. Esta skill escreve o comentário. O usuário posta.
