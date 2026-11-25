---
name: ig-reel
description: >-
  Escreve um Reel de Instagram em português do Brasil a partir de uma ideia
  crua: opções de gancho a partir de 26 fórmulas, o roteiro falado, o texto de
  tela e um mapa de batidas cronometrado, na voz do usuário e com nota antes de
  gravar. Use sempre que o usuário pedir um Reel, roteiro de vídeo curto,
  gancho, locução, "faz um reel sobre X", "o que eu falo nesse vídeo", ou
  estiver prestes a gravar sem a primeira frase.
---

# ig-reel

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Transforma uma ideia crua num Reel que alguém assiste até o fim.

Duas ferramentas ficam nesta pasta e as duas rodam de verdade. Use as duas. Não
avalie o gancho no olho e não chute a duração.

```bash
python3 gancho.py ganchos.txt                 # ranqueia as opções de gancho
python3 gancho.py --gancho "uma frase"        # avalia uma só
python3 batidas.py roteiro.txt --alvo 30      # mapa de batidas antes de gravar
```

## Antes de escrever

1. Leia `{pasta da conta}/voz.md` se existir. É o perfil de voz do
   usuário: como fala na câmera, o que nunca diz, com quem fala, se usa "você"
   ou "tu". Se não existir, peça **três reels dele**, transcreva ou leia,
   deduza a voz e escreva o arquivo. Roteiro na voz errada é inútil, porque ele
   precisa falar em voz alta.
2. Leia `ganchos.json` nesta pasta. São 26 fórmulas, cada uma com modelo,
   exemplo preenchido, versão de tela, para que serve e como costuma ser
   estragada. Os valores em reais dos exemplos mostram formato, não são dados.
3. Se a ideia é rasa, não encha linguiça. Faça uma pergunta só, agrupada: o que
   aconteceu, com quem, e quanto custou ou rendeu. Um Reel precisa de uma coisa
   verdadeira e específica. Consiga antes de escrever.
4. Se `{pasta da conta}/swipe.md` existir, leia. O `/ig-viral` escreve
   esse arquivo, e ele é a evidência do próprio usuário sobre quais fórmulas
   estão funcionando no nicho dele agora. Vale mais que os padrões deste arquivo.

## O formato

Um Reel é decidido nos dois primeiros segundos e mantido nos cinco seguintes.

```
0:00 - 0:02   GANCHO      a afirmação. Frase falada e frase de tela, escritas
                          separadas. Movimento no primeiro quadro, não rosto parado.
0:02 - 0:07   O QUE ESTÁ  por que isso importa pra quem assiste. Uma frase.
              EM JOGO
0:07 - ...    O CORPO     uma ideia por batida, e o quadro muda a cada batida.
ÚLTIMOS 3s    A ENTREGA   cumpra o que o gancho prometeu, depois o único pedido.
ÚLTIMA FRASE  O LOOP      repita uma palavra do gancho pra o replay emendar.
```

Duração: 15 a 45 segundos é a faixa que funciona. Reels vão até 3 minutos e
quase ninguém deveria usar. Abaixo de 7 segundos só a contagem de loop sobe.

## O ciclo

**1. Escolha três ganchos, não um.** Passe a ideia por `ganchos.json`, escolha
três fórmulas que realmente servem e escreva a frase falada e a de tela de cada
uma. Fórmulas diferentes, não três versões da mesma.

**2. Dê nota.** Coloque as três frases faladas num arquivo, uma por linha, e
rode `gancho.py`. Mostre o ranking ao usuário. Se o primeiro está abaixo de 50,
você ainda não tem o gancho, e edição nenhuma resolve isso.

**3. Escreva o roteiro** em cima do gancho vencedor. Português falado, do jeito
que o usuário realmente fala: "pra", "tá", "a gente". Frases curtas. Nenhuma
frase que ele precise ensaiar.

**4. Cronometre.** Rode `batidas.py roteiro.txt --alvo {duração}`. Se o
`voz.md` tiver a velocidade de fala, passe `--ppm`. Corrija todo alerta: gancho
acima de 10 palavras (uns 3,7 segundos), batida acima de 4 segundos, sequência de batidas sem nada concreto,
falta de loop. Rode de novo até ficar limpo.

**5. Humanize.** Passe o roteiro pelo `/ig-humano` antes de mostrar. Frase com
cara de texto escrito fica óbvia no momento em que alguém fala em voz alta.

**6. Entregue o bloco.** O roteiro num bloco de código, o texto de tela como
lista separada com os tempos, e depois:

```
REEL PRONTO
gancho:     #3 Ninguém Te Conta, nota 86 FORTE
duração:    28,4s em 9 batidas a 160 ppm
tela:       6 cartelas
humano:     4 marcas removidas, nota humana 81 PASSA
legenda:    rode /ig-legenda em seguida

Responda "sim" para registrar, ou diga o que mudar.
```

**7. Nunca publique.** Esta skill produz roteiro. O usuário grava e posta. No
"sim", acrescente em `{pasta da conta}/historico.md` a data, a fórmula de
gancho usada e a primeira frase, para o `/ig-auditoria` ter histórico depois.

## Texto de tela é outro roteiro

Escreva separado, sempre. Ele é lido antes de ser ouvido.

- **Seis palavras ou menos por cartela.** Está sendo lido à distância do braço
  por alguém que ainda não está ouvindo.
- **A cartela do gancho aparece no quadro 1**, não depois de um silêncio.
- **Fique dentro da área segura.** Num quadro de 1080x1920, nada acima de
  y=230 ou abaixo de y=1440, e deixe livres os 230 pixels da direita. A
  interface fica por cima de tudo que está fora disso: legenda, botões e faixa
  do áudio.
- **Nunca ponha o gancho onde fica a legenda.** É a parte de baixo do quadro, e
  ela fica coberta.
- **Legenda queimada no corpo do vídeo.** A maioria assiste sem som primeiro.

## Regras que fazem diferença

- **Uma ideia por Reel.** Se o roteiro tem duas, são dois Reels. Diga isso.
- **Número em vez de adjetivo.** "R$ 4.200" vale mais que "muito". Se o usuário
  não deu o número, peça em vez de escrever em volta do buraco.
- **Corte a introdução.** Sem "oi gente", sem "nesse vídeo", sem nome, sem
  vinheta. O vídeo começa na frase que você diria no segundo seis.
- **Mude o quadro a cada batida.** Plano parado por 8 segundos é onde as
  pessoas saem, e o `batidas.py` aponta.
- **Um pedido no fim.** Comentar uma palavra, salvar ou seguir. Um.
- **Nunca invente.** Nada de métrica, cliente, faturamento ou resultado
  inventado no nome do usuário, nem como exemplo. Se precisa de um número e ele
  não deu, deixe `{{seu número}}` no roteiro e avise.
- **Publi é publi.** Se o Reel é pago, recebido de presente ou tem link de
  afiliado, diga no começo, na fala ou na tela, e lembre o usuário de marcar
  "parceria paga" no Instagram. Ver `/ig-legenda`.
- **Não escreva em cima de um áudio em alta que o usuário não pode usar.**
  Conta comercial tem biblioteca de áudio restrita. Se a ideia depende da voz
  dele, diga isso.

## Exemplo

```
/ig-reel a gente cortou o tempo de proposta de 5 horas pra 20 minutos com um modelo
```

```
GANCHOS  (com nota)
  86  FORTE  #5  Tempo Encolhido     "Proposta me tomava cinco horas. Hoje leva vinte minutos."
                                     tela: 5 HORAS -> 20 MIN
  71  FORTE  #1  Confissão de Custo  "Eu cobrava quatro horas por semana só de formatação. Por dois anos."
                                     tela: 2 ANOS JOGADOS FORA
  54  OK     #9  Rouba Isso          "Rouba o modelo de proposta que fez isso."
                                     tela: ROUBA ISSO

Gravando o #5: a proporção é crível, lê de uma vez na tela, e o número é seu.
```
