---
name: ig-viral
description: >-
  Vai atrás dos reels que estão funcionando agora no nicho do usuário,
  ranqueia pelo quanto cada um superou a própria conta, dá nome à fórmula de
  gancho de cada um e transforma isso num swipe file para gravar. Use quando o
  usuário disser "acha vídeos virais", "o que está funcionando agora", "o que
  estão postando no meu nicho", "faz engenharia reversa dessa conta", "monta um
  swipe file", "por que esse reel está bombando", ou perguntar o que fazer em
  seguida sem ter evidência para responder.
---

# ig-viral

## Qual conta

Antes de começar, descubra para qual conta é, pela regra do `/ig-contas`: a
que o usuário disse (nome ou @), senão a conta ativa (`python3 contas.py ativa`,
na pasta `ig-contas`, ou o arquivo `~/.claude/instagram-br/ativa`), senão
pergunte. Diga a conta na primeira linha da resposta. Leia o `voz.md` dela e,
se o `conta.json` indicar uma skill de persona, leia essa skill também: as
regras dela valem por cima das deste arquivo. Nada de uma conta entra no
trabalho de outra.

A skill de pesquisa. Todo o resto deste pacote escreve; esta vai lá e olha.
Rode uma vez por mês, não todo dia. Fórmula dura uma estação.

Uma ferramenta fica nesta pasta e ela roda:

```bash
python3 swipe.py coletados.tsv --conta <conta>
```

## A ideia que faz isso valer a pena

**View bruta não é evidência.** Uma conta com dois milhões de seguidores
fazendo 400 mil views teve uma terça fraca. Uma conta com quatro mil
seguidores fazendo 400 mil views achou alguma coisa, e essa coisa dá para
copiar.

Então tudo aqui é ranqueado pelo **múltiplo**: views divididas pela mediana
recente daquela conta. Acima de 3x é sinal. Abaixo de 1,5x é o dia normal da
conta e não ensina nada, por maior que pareça o número.

Colete contas **de até umas 10 vezes o tamanho da conta do usuário**. Uma
fórmula que funciona com 2 milhões muitas vezes funciona porque a conta tem 2
milhões.

## Passo 1: escolha as contas

Peça ao usuário de 6 a 12 contas, ou proponha e peça aprovação:

- **4 diretas**: mesmo nicho, mesma oferta, um pouco à frente. De preferência
  brasileiras, porque humor, gíria e referência mudam o que funciona.
- **4 vizinhas**: outro nicho, mesmo público. É daqui que se pega formato antes
  de alguém do nicho ter.
- **2 a 4 gigantes**: contas bem maiores, só para formato, nunca para
  frequência ou tom. Aqui vale olhar fora do Brasil também: formato que está
  começando lá fora costuma chegar aqui alguns meses depois.

Peça também para o usuário abrir a coleção de **Salvos** dele. É o acervo mais
rápido e mais relevante que existe, e já vem filtrado pelo gosto dele.

## Passo 2: vá olhar

Use a ferramenta de navegação que esta sessão realmente tiver: um navegador
dentro do app, uma extensão ligada ao Chrome do próprio usuário, ou uma
ferramenta de uso do computador. Não existe API para isso e não precisa,
porque o volume é pequeno o bastante para ler.

**Regras inegociáveis:**

- **Nunca entre no Instagram no lugar do usuário e nunca peça senha.** Se a
  página exige login, quem está logado é o usuário. Conduza o navegador dele
  com ele presente, ou peça para ele colar.
- **Isto é leitura, não raspagem.** Dez contas, uma dúzia de reels cada, em
  velocidade humana. Coleta automatizada em volume viola os Termos de Uso do
  Instagram e bloqueia a conta. Não monte robô, não use serviço de scraping e
  não deixe isso rodando em segundo plano.
- **Copie a fórmula, nunca o vídeo.** O formato do gancho, a estrutura, a
  duração, o padrão de cortes. Não o roteiro, não a voz, não a edição de
  ninguém. Cada linha do swipe file leva o @ de onde veio.

**O que anotar de cada reel**, nas palavras do criador:

| campo | observação |
| --- | --- |
| conta | o @ |
| seguidores | do perfil |
| mediana | olhe os últimos 12 reels e pegue a view do meio |
| views | deste reel |
| gancho | a primeira frase, falada ou na tela, literal, inclusive com o português errado |
| tela | o primeiro texto na tela, se for diferente |
| duração | segundos |
| cta | o que pediram no fim |

A mediana é a importante. Sem ela, você volta a ranquear por número de
seguidores, que é justamente o que esta skill existe para evitar. O
`swipe.py` aceita números do jeito que o Instagram mostra: "48 mil", "1,2 mi",
"412k", "400.000".

**Quando o Instagram não mostrar o suficiente:** a mesma gramática de gancho
roda no YouTube Shorts, onde views e transcrições são públicas e não precisa
de login. É um segundo acervo legítimo, e o gancho falado é mais fácil de
pegar:

```bash
# views dos shorts de um canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# a primeira frase falada de um short, pelas legendas automáticas em português
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "pt.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DO_VIDEO"
```

Pegue toda palavra da legenda com tempo abaixo de 3,0 segundos. Esse é o
gancho, do jeito que foi falado e não do jeito que foi escrito. A legenda
automática em português erra nome próprio e gíria; confira antes de anotar.

## Passo 3: ranqueie

Preencha um arquivo separado por TAB com linha de cabeçalho e rode o script:

```
conta	seguidores	mediana	views	gancho
@alguem	48 mil	11 mil	412 mil	ninguém te conta que os seus 30 primeiros reels vão flopar
```

```bash
python3 swipe.py coletados.tsv --conta <conta>
```

Ele calcula o múltiplo, dá nome à fórmula de gancho usando as mesmas 26
fórmulas com que o `/ig-reel` escreve, dá nota a cada gancho com o
`gancho.py` e mostra o que separa o terço de cima do terço de baixo.

## Passo 4: diga o que significa, com cuidado

Relate três coisas e nada mais:

1. **Quais fórmulas aparecem mais** no terço de cima, com contagem. Duas
   fórmulas aparecendo quatro vezes cada em seis contas é achado. Uma
   aparecendo duas vezes não é.
2. **O que o terço de cima tem em comum** na estrutura e o de baixo não:
   tamanho do gancho, se o resultado é visual, se o primeiro quadro se mexe,
   onde fica o pedido.
3. **As linhas sem fórmula.** Todo gancho que o classificador não nomeou é
   ruído ou uma fórmula que ainda não está no `ganchos.json`. Leia na mão. É a
   coluna mais valiosa da saída, e é por isso que o script mostra a contagem.
   Se aparecer um formato que se repete, proponha ao usuário acrescentá-lo ao
   `ganchos.json`.

Depois diga o tamanho da amostra e a confiança em palavras simples. Quarenta
reels em seis contas sustentam uma afirmação. Doze não, e dizer isso é a
diferença entre pesquisa e horóscopo.

## Passo 5: transforme em algo para gravar

Para as três fórmulas de cima, escreva **a versão do usuário**: a história
dele, o número dele, no formato que está funcionando. Passe cada uma para o
`/ig-reel` com o número da fórmula já escolhido.

Nunca entregue "faz um reel igual a esse". Entregue uma frase de gancho que ele
possa falar amanhã.

## Saída

```
SWIPE  ·  38 reels  ·  7 contas  ·  base: mediana da conta

ACIMA DE 3x
  38,4x  nota 86  #3  Ninguém Te Conta   @conta_a   412.000  (mediana 10.700)
  11,2x  nota 79  #9  Rouba Isso         @conta_c   180.000  (mediana 16.100)
  ...

O QUE ESTÁ APARECENDO MAIS
  #3 Ninguém Te Conta   x5 no terço de cima, 0 no de baixo
  #2 Ordem Negativa     x4
  tamanho do gancho     8 palavras em cima, 19 embaixo

SEM FÓRMULA (6)
  Dois deles têm o mesmo formato, que não está no ganchos.json: um gancho que
  abre lendo em voz alta o comentário de outra pessoa. Vale acrescentar.

SUA VERSÃO
  #3  "Ninguém te conta que as 20 primeiras propostas são pra perder."
  ...
```

Grave o swipe file em `{pasta da conta}/swipe.md`. O `/ig-reel` e o
`/ig-plano` leem esse arquivo, e esse é o ponto: depois que isto roda uma vez,
o resto do pacote trabalha com a evidência do próprio usuário e não com
padrões.

Esta skill não posta, não segue, não curte e não manda mensagem. Ela lê.
