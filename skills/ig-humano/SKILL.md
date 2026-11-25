---
name: ig-humano
description: >-
  Tira a marca de máquina de qualquer rascunho em português (travessões,
  clichês de IA, traduções literais do inglês, caracteres invisíveis) e dá nota
  num painel de cinco critérios antes de sair. Use sempre que um texto precisar
  soar humano, quando o usuário disser "humaniza", "isso tá com cara de IA",
  "tira os travessões", "parece ChatGPT", ou antes de mostrar qualquer legenda,
  roteiro, comentário, resposta ou DM ao usuário.
---

# ig-humano

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

Duas ferramentas ficam nesta pasta e as duas rodam de verdade. Use as duas. Não
faça isso no olho.

```bash
python3 humanizar.py rascunho.txt --relatorio       # limpa e mostra o que mudou
python3 detectar.py rascunho.txt                    # dá nota em cinco critérios
python3 detectar.py antes.txt depois.txt            # prova a diferença
```

As duas leem `cliches.json`: cerca de 190 palavras e expressões com
substituição simples, 18 classes de caractere invisível, 11 trocas
tipográficas e 16 vícios de estrutura. Tem três blocos que só existem em
português: **tradução literal** ("não durma nisso", "no final do dia",
"mudança de jogo"), que é um dos sinais mais fortes de texto gerado; **cara de
redação** ("além disso", "vale ressaltar que", "nesse sentido"); e o bloco do
**Instagram brasileiro** ("para de rolar o feed", "assista até o final",
"marca aquele amigo que", "o algoritmo ama"). O arquivo é para ser editado. Se
o usuário fala de verdade uma palavra que a lista tira, apague ela do arquivo.

## Por que isso pesa mais no Instagram do que parece

Legenda é curta e roteiro é falado. Uma frase com cara de texto escrito numa
legenda de 600 caracteres é uma fatia maior do texto do que a mesma frase numa
redação, e uma locução que ninguém falaria naturalmente aparece no primeiro
take. O problema aqui não é um detector marcar o post. É alguém rolar o feed e
passar por algo que soa como marca, ou o criador tropeçar no próprio roteiro.

## O que é corrigido sozinho

**1. Caracteres invisíveis.** Espaço de largura zero, junções, hífen suave, BOM,
caracteres de tag Unicode, separadores invisíveis, espaços rígidos e estreitos.
Teclado não produz isso. Sobrevive ao copiar e colar, é invisível em qualquer
editor e é a coisa mais mecânica de um texto gerado. O `humanizar.py` apaga
todos, inclusive qualquer caractere de formatação que ele não conheça pelo nome.

**2. Tipografia.** Travessão vira vírgula, meia-risca vira hífen, aspas curvas
viram retas, reticências de um caractere viram três pontos. O travessão é o que
importa: no celular ninguém digita travessão, então numa legenda ele entrega.
Aspa curva pesa pouco no detector, porque o iPhone troca aspa reta por curva
sozinho.
Exceção: diálogo de ficção com travessão é norma em português. Se o texto é
conto ou roteiro de cena, avise o usuário antes de trocar.

**3. Os clichês.** "Alavancar", "crucial", "potencializar", "no mundo acelerado
de hoje", "vale ressaltar que", mais o bloco do Instagram. Cada um vira uma
palavra simples ou é apagado, mantendo maiúsculas e sem mexer em links.

Depois de apagar, sempre releia: às vezes a frase fica sem verbo ou com
concordância errada ("uma ampla gama de criadores descobriu" vira "muitos
criadores descobriu"). Conserte na mão.

## O que NÃO é corrigido sozinho

Vícios de estrutura são **apontados, não reescritos**, porque mudar o formato
de uma frase pede julgamento:

- "Não é só X, é Y", "não só X, mas também Y", "não se trata de X, e sim de Y"
- Regra de três
- Linha de pergunta retórica: "O resultado?"
- Preâmbulo de vídeo: "nesse vídeo eu vou te mostrar"
- Lista com emoji como marcador
- Três ou mais palavras gritadas seguidas
- Muro de hashtags
- Isca automática: "segue pra mais", "marca alguém", "toque duas vezes"

Essa lista é sua. Reescreva cada linha apontada na mão, mantendo o sentido, e
rode o `detectar.py` de novo. É essa parte que leva a nota de REVISAR para
PASSA, e é a parte que script nenhum faz.

## Os cinco critérios

O `detectar.py` dá nota de 0 a 100 em cinco sinais; quanto maior, mais humano:

| critério | o que mede | cara de máquina |
| --- | --- | --- |
| VARIAÇÃO | variação do tamanho das frases | toda frase do mesmo tamanho |
| CONCRETO | números, nomes, marcadores concretos a cada 100 palavras | substantivo abstrato, nenhum número |
| CLICHÊS | ocorrências do léxico a cada 100 palavras | vocabulário pronto |
| TIPOGRAFIA | invisíveis, travessões, aspas curvas a cada mil caracteres | tipografia perfeita demais |
| VOZ | marcas de fala ("tá", "pra", "a gente"), pessoa, vícios de estrutura | português de redação, revelações encenadas |

O critério VOZ é o que mais mudou em relação à versão em inglês: lá ele contava
contrações ("don't", "it's"). Em português não existe isso, então ele conta
marcas de fala, que texto gerado quase nunca usa.

Em conta do tipo `nicho` ou `marca` com texto informativo (história, notícia,
ficha técnica), VOZ baixa é esperada: é texto em terceira pessoa por natureza.
Não force "tá" e "a gente" num post de história só para subir a nota; olhe os
outros quatro critérios e diga isso ao usuário.

O veredito pesa a média em 60% e o **critério mais fraco** em 40%, porque basta
um sinal. PASSA exige nota geral 70 ou mais, sem nenhum critério abaixo de 55.

## Diga isso com honestidade

São cinco heurísticas locais inspiradas nos sinais que detectores públicos
usam. Rodam inteiramente na máquina do usuário e nada é enviado. **Não** são
GPTZero, Originality, Copyleaks, Winston ou Turnitin, não chamam esses
serviços e não garantem o veredito deles. Corrigir o que elas medem costuma
mexer nesses números, porque medem as mesmas coisas de fundo. É essa a
afirmação. Não faça uma maior em nome do usuário, e nunca diga que um texto é
indetectável.

Se o perfil é de uma persona feita com IA, humanizar o texto não substitui
avisar que é IA. Esconder a origem do conteúdo não é o objetivo desta skill.

## Ordem das operações

1. `humanizar.py rascunho.txt -o limpo.txt --relatorio`
2. Leia os vícios apontados. Reescreva essas linhas você mesmo, e releia o que
   ficou depois das deleções.
3. `detectar.py rascunho.txt limpo.txt` para mostrar o antes e o depois.
4. Se o veredito não for PASSA, corrija o critério mais fraco que aparece na
   saída e rode de novo. Duas rodadas é normal. Cinco quer dizer que o
   rascunho foi escrito por fórmula, e a solução é outro rascunho, não mais
   rodadas.
5. Mostre ao usuário o texto limpo e a nota. Nunca só a nota.
