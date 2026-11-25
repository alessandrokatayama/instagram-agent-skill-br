# Instagram Agent Skill BR: skills de Instagram para o Claude, em português

[![Testes](https://github.com/alessandrokatayama/instagram-agent-skill-br/actions/workflows/testes.yml/badge.svg)](https://github.com/alessandrokatayama/instagram-agent-skill-br/actions/workflows/testes.yml)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green.svg)](LICENSE)
![Idioma: português do Brasil](https://img.shields.io/badge/idioma-pt--BR-009c3b.svg)

**Um agente de IA para Instagram que roda no Claude e no Claude Code, feito
para o Brasil.** São catorze skills que escrevem roteiro de Reels, legenda,
carrossel e stories, revisam hashtags, dão nota ao perfil, planejam a semana
de posts e tiram a "cara de ChatGPT" do texto. Funciona com uma ou várias
contas de Instagram ao mesmo tempo.

Grátis, licença MIT, sem cadastro, sem chave de API, nada para conectar. E
nada é postado sem você.

**Para quem é:** criador de conteúdo, social media, agência, loja, pequeno
negócio, página temática ou de fã e quem cria personagem ou influenciador
virtual com IA.

## O que ele faz

Uma das skills escreve seus Reels a partir de 26 fórmulas de gancho e dá nota ao
gancho antes de você gastar um take. Uma vai atrás dos reels que estão
funcionando no seu nicho e ranqueia pelo quanto cada um superou a própria
conta. Uma escreve a legenda e mostra exatamente o que aparece no feed antes do
"... mais", e avisa se a `#publi` ficou escondida. Uma dá nota de 0 a 100 para o
seu perfil e reescreve o que perdeu ponto. Uma planeja a semana no horário de
Brasília.

E uma é o humanizador, que é o que torna o resto utilizável. Ele tira
travessões, clichês de IA, traduções literais do inglês e caracteres
invisíveis de um rascunho, e dá nota ao que sobrou num painel de cinco
critérios antes de você ver.

**Nada é postado até você dizer sim.** Estas skills escrevem. Você posta.

Esta é uma adaptação para o Brasil do
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill),
de Jake Schincariol. Veja [o que mudou](#o-que-mudou-em-relação-ao-original).

## Instalar

Cole isto no Claude:

```
https://github.com/alessandrokatayama/instagram-agent-skill-br

Instala essas skills e confirma que o /ig-reel funciona.
```

Ou faça você mesmo, no Claude Code:

```bash
git clone https://github.com/alessandrokatayama/instagram-agent-skill-br.git
cp -r instagram-agent-skill-br/skills/ig-* ~/.claude/skills/
```

Ou como plugin:

```
/plugin marketplace add alessandrokatayama/instagram-agent-skill-br
/plugin install instagram-agent-br
```

Para usar só num projeto, copie as mesmas pastas para `.claude/skills/` do seu
repositório. Sem Claude Code? Cole qualquer `SKILL.md` no começo de uma
conversa e ele funciona como um modo. Você perde as ferramentas em Python, que
são boa parte da graça do `/ig-reel` e do `/ig-humano`, mas o resto funciona.

Depois crie sua conta com o `/ig-contas` ("cria a conta do @meuperfil") e
gaste dez minutos no `voz.md` dela, ou mande ao Claude três reels da conta e
diga "escreve o voz.md dessa conta a partir disso". Toda skill lê esse arquivo.
No Instagram ele importa mais do que em outras redes, porque alguém precisa
falar as palavras em voz alta.

## As catorze skills

| comando | o que faz |
| --- | --- |
| `/ig-contas` | Várias contas no mesmo pacote: uma pasta por conta com voz, swipe file, histórico e plano separados, a conta em uso, e a skill de persona de cada uma. |
| `/ig-reel` | Uma ideia vira Reel. Três ganchos a partir de [26 fórmulas](skills/ig-reel/ganchos.json), com nota, depois o roteiro, o texto de tela e um mapa de batidas cronometrado. |
| `/ig-viral` | Vai atrás do que está funcionando no seu nicho, ranqueia pelo múltiplo sobre a mediana de cada conta, dá nome à fórmula e escreve o swipe file. |
| `/ig-legenda` | A legenda, revisada. Mostra os 125 caracteres que o feed exibe antes do toque e confere hashtag, pedido, busca e identificação de publi. |
| `/ig-carrossel` | Post de arrastar. A capa que ganha o arraste, o texto de cada slide e os arquivos 1080x1350. |
| `/ig-stories` | A sequência de stories do dia, qual figurinha faz o quê, e o funil para o direct ou o WhatsApp que começa com a pessoa se mexendo primeiro. |
| `/ig-perfil` | Dá nota ao seu perfil numa [rubrica de 12 partes](skills/ig-perfil/rubrica.json) de 0 a 100 e reescreve na ordem do que mais perde ponto. |
| `/ig-plano` | A semana. O que postar, em qual formato, em que horário de Brasília, as datas comemorativas que importam e as 10 contas para interagir. |
| `/ig-humano` | O humanizador. Dois scripts que rodam de verdade. Veja abaixo. |
| `/ig-comentario` | Comentários nos posts dos outros. Nove tipos, escolhidos pelo que o post realmente é. Nunca "🔥🔥🔥". |
| `/ig-resposta` | Os comentários do seu post. Separa em palavra-chave / cliente / conteúdo / pergunta / apoio / ruído e responde nessa ordem. |
| `/ig-dm` | A entrega da palavra-chave, a primeira mensagem, a proposta de collab ou de publi, e os dois follow-ups. Dois. |
| `/ig-reaproveitar` | Um vídeo, podcast, live ou newsletter vira uma semana de reels e carrosséis que se sustentam sozinhos. |
| `/ig-auditoria` | Análise do que você já postou. Ranqueia por múltiplo e envios por alcance, não por views. |

## Várias contas de Instagram

Quem cuida de mais de um perfil não pode ter um voz.md só: o tom do perfil
pessoal vaza para a marca e o swipe file de culinária manda gancho para o
perfil de tecnologia. Cada conta tem a sua pasta:

```
~/.claude/instagram-br/
    ativa                 a conta em uso
    contas/
        lia/              conta.json  voz.md  swipe.md  historico.md  plano.md
        cafeaurora/       conta.json  voz.md  plano.md
```

```bash
python3 contas.py criar lia --arroba @lia.criadora --tipo persona --persona lia-persona
python3 contas.py criar cafeaurora --arroba @cafeaurora --tipo marca
python3 contas.py usar cafeaurora
python3 contas.py listar
```

```
   lia            @lia.criadora       persona   [voz, swipe, historico]  persona: lia-persona
 * cafeaurora     @cafeaurora         marca     [voz, plano]
```

Toda skill segue a mesma regra: usa a conta que você disser ("faz um reel pra
Lia"), senão a ativa, senão pergunta, e diz na primeira linha da resposta
para qual conta está escrevendo. Nada de uma conta entra no trabalho de outra.

Uma conta do tipo **persona** aponta para uma skill de persona (um personagem
ou influenciador feito com IA). As regras dessa skill valem por cima do pacote,
e as skills nunca inventam vivência para o personagem nem escondem que ele é
feito com IA.

O `/ig-plano` também monta a semana de todas as contas juntas, sem repetir tema
para o mesmo público e sem dois posts no mesmo horário quando é a mesma pessoa
gravando. Quem usava a versão de uma conta só roda `contas.py migrar` e os
arquivos antigos vão para uma pasta de conta, sem apagar nada.

## As ferramentas que rodam de verdade

Sem dependências, sem internet, nada enviado. Rodam na sua máquina, no seu
texto, com Python 3.

### Ganchos

```bash
python3 gancho.py ganchos.txt                 # ranqueia suas opções
python3 batidas.py roteiro.txt --alvo 30      # cronometra antes de gravar
```

```
RANKING DE GANCHOS
==============================================================================
->  79.3 FORTE  Ninguém te conta que seus primeiros 30 reels são feitos pra...
        mais fraco: TAMANHO (66)
    61.9 OK     Perdi R$ 18.000 por causa de uma cláusula que faltou no con...
        mais fraco: DIREÇÃO (35)
    17.2 FRACO  Para de rolar o feed se você quer crescer no Instagram em 2...
        eliminatório: Abre com "para de rolar". Pedir atenção prova que você ainda não conquistou.
     9.6 FRACO  Oi gente, hoje eu queria falar sobre estratégia de conteúdo
        eliminatório: Saudação. Ninguém abre o feed pra ser cumprimentado.
```

O `batidas.py` estima quanto tempo cada linha leva para ser falada, empilha em
minutagem e aponta as quatro coisas que matam um Reel na edição: gancho que
passa de dez palavras (uns 3,7 segundos), batida longa o bastante para a pessoa sair, sequência
de linhas sem nada concreto, e falta de loop com a primeira frase. O ritmo
padrão é 160 palavras por minuto; cronometre o seu e passe `--ppm`.

### A legenda

```bash
python3 legenda.py legenda.txt --busca "proposta comercial,contrato de freelancer"
```

O Instagram mostra uns 125 caracteres da legenda no feed e esconde o resto
atrás de um toque. Quase toda legenda que falha, falha ali. Então a primeira
coisa que o script imprime é essa janela, numa caixa, do jeito que um
desconhecido lê:

```
  O QUE O FEED MOSTRA
  +------------------------------------------------------+
  | Perdi R$ 18 mil por causa de uma cláusula que faltou |
  | no contrato, e o pior é que eu tinha lido o          |
  | documento duas vezes antes d                         |
  +-------------------------------------------- ... mais +

  ATENÇÃO  1ª LINHA         135 caracteres, então é cortada no 125 no meio do pensamento
  OK       HASHTAGS         4 hashtag(s): #publi #freelancer #contratos #propostacomercial
  OK       UM PEDIDO        uma chamada para ação: comentar uma palavra
  ERRO     PUBLICIDADE      "#publi" só aparece depois do "... mais". O guia do CONAR pede a
                            identificação visível sem precisar abrir a legenda
  ATENÇÃO  BUSCA            1/2 presentes. Faltando: contrato de freelancer
```

Ele aplica o limite atual de **cinco hashtags por post**, que o Instagram
adotou em 18 de dezembro de 2025, avisa quando uma hashtag tem acento (a versão
com e a sem acento são hashtags diferentes), procura os termos de busca
ignorando acento e reconhece pedidos em português ("comenta", "me chama no
direct", "link na bio", "chama no zap").

### O humanizador

```bash
python3 humanizar.py rascunho.txt --relatorio    # limpa e mostra cada mudança
python3 detectar.py rascunho.txt                 # dá nota em cinco critérios
python3 detectar.py antes.txt depois.txt         # prova a diferença
```

**O que sai automaticamente:**

- **Caracteres invisíveis.** Espaço de largura zero, junções, marcador de
  palavra, hífen suave, BOM, caracteres de tag Unicode, separadores invisíveis,
  espaços rígidos e estreitos. Seu teclado não produz isso.
- **Tipografia.** Travessão vira vírgula, meia-risca vira hífen, aspas curvas
  viram retas, reticências de um caractere viram três pontos.
- **O léxico.** Cerca de 190 palavras e expressões em
  [`cliches.json`](skills/ig-humano/cliches.json), em quatro famílias: cara de
  redação ("além disso", "vale ressaltar que", "nesse sentido"), vocabulário
  de IA ("alavancar", "potencializar", "crucial"), **tradução literal do
  inglês** ("não durma nisso", "no final do dia", "mudança de jogo") e vícios do
  Instagram brasileiro ("para de rolar o feed", "assista até o final", "marca
  aquele amigo que", "o algoritmo ama"). O arquivo é para ser editado.

**O que é apontado em vez de corrigido:** "não é só X, é Y", "não só X, mas
também Y", regra de três, preâmbulo de vídeo, lista com emoji como marcador,
palavras gritadas em sequência, muro de hashtags, isca automática de seguir e
marcar, frases todas do mesmo tamanho. Mudar o formato de uma frase pede
julgamento, então essas voltam para reescrever em vez de serem estragadas por
uma regex.

Uma legenda escrita para ser a pior possível tira 24,9. Um parágrafo escrito
por uma pessoa, com "tá", "a gente" e número de verdade, tira 79,7 e passa.

### O swipe file

```bash
python3 swipe.py coletados.tsv --conta lia
```

View bruta não é evidência. Uma conta de 2 milhões fazendo 400 mil views teve
uma terça fraca. Uma conta de 4 mil fazendo 400 mil achou alguma coisa. O
`swipe.py` ranqueia pelo múltiplo sobre a mediana de cada conta, dá nome à
fórmula do gancho e mostra o que separa o terço de cima do terço de baixo.
Aceita cabeçalho em português e números como o Instagram mostra ("48 mil",
"1,2 mi").

```
SWIPE FILE  ·  4 reels  ·  4 contas  ·  base: mediana da conta
==============================================================================
    80.0x  nota  81  #3  Ninguém Te Conta         @confeitaria_ana      96.000
    13.7x  nota  63  #1  Confissão de Custo       @doces_bia            41.000
     1.3x  nota   0  -   sem fórmula              @chef_rui            240.000
```

As contas acima são exemplos inventados para mostrar a saída.

## O que mudou em relação ao original

- **Tudo em português do Brasil**: as skills, as mensagens dos scripts e os
  arquivos de dados. Os comandos foram renomeados (`/ig-legenda`,
  `/ig-humano`, `/ig-perfil`...) para conviver com o pacote original instalado.
- **As 26 fórmulas de gancho foram reescritas**, não traduzidas. Cada uma tem
  exemplo em português e uma regex que reconhece o jeito brasileiro de falar
  ("ninguém te conta", "pare de", "rouba esse", "carrossel x reels"). As 26
  frases de exemplo são classificadas na própria fórmula.
- **Os scripts entendem português**: acentos, `R$ 18.000`, "18 mil", números
  por extenso ("cinco horas", "vinte mil"), saudações ("oi gente", "fala
  galera"), preâmbulos ("nesse vídeo eu vou te mostrar"), pronomes ("você",
  "vc", "cê", "a gente").
- **O detector troca contração por marca de fala.** Em inglês ele contava
  "don't" e "it's". Português não tem isso, então ele conta "tá", "pra", "né",
  "a gente", que texto gerado quase nunca usa.
- **Regras do Brasil**: identificação de publicidade pelo guia do CONAR
  (atualizado em maio de 2026), autorização prévia para sorteio, LGPD ao levar
  conversa para o WhatsApp, horário de Brasília e os outros fusos do país,
  datas comemorativas que mexem com o comércio.
- **Várias contas**: o `/ig-contas` é novo, não existe no original, que trabalha
  com uma conta só.
- **Hábitos do Brasil**: venda que fecha no WhatsApp, link direto `wa.me` na
  bio, hashtag com e sem acento, áudio no direct, Pix.

## Letra miúda, que é a parte honesta

**Estas skills não postam no Instagram.** Existe uma API oficial de publicação
para contas profissionais, e ela exige um app de desenvolvedor da Meta, página
vinculada, token de longa duração e revisão do app, que não é algo que uma
skill entrega. Tudo o mais que as pessoas usam para automatizar post,
comentário, seguir ou DM é automação de navegador ou ferramenta de terceiros,
e as duas violam os [Termos de Uso do Instagram](https://help.instagram.com/581066165581870)
e bloqueiam contas. Então toda skill termina igual: um bloco pronto para
copiar, e você posta.

A exceção é a resposta automática a palavra-chave no direct, que o Instagram
permite pelas ferramentas próprias e por parceiros aprovados, e que só dispara
depois que alguém comenta primeiro. O `/ig-dm` diz onde fica essa linha.

**O `/ig-viral` lê, não raspa.** Dez contas, uma dúzia de reels cada, em
velocidade humana, com você conduzindo o seu próprio navegador. Nunca pede sua
senha e nunca entra no seu lugar.

**A nota de gancho não foi medida em português.** O autor original testou o
avaliador em 74 ganchos reais em inglês: ele separa bem gancho real de gancho
ruim de propósito (AUC 0,83), mas quase não separa o acerto do erro de um mesmo
criador (AUC 0,56, onde 0,50 é cara ou coroa). Esta adaptação ainda não foi
medida num acervo brasileiro. Use para matar gancho obviamente fraco antes de
gravar, e confie no seu gráfico de retenção para o resto. Se você medir num
acervo brasileiro, eu quero saber o resultado.

**Os cinco critérios do detector são heurísticas locais, não APIs de
detector.** Não são GPTZero, Originality, Copyleaks, Winston ou Turnitin, não
chamam esses serviços e não garantem o veredito deles. Ninguém pode te vender
"indetectável" com honestidade. E se o seu perfil é uma persona feita com IA,
humanizar o texto não substitui avisar que é IA.

**A passada de caracteres invisíveis é real e é estreita.** Remove caracteres
de largura zero e de formatação que acabam em texto gerado. Não é uma promessa
de derrotar marca d'água criptográfica.

**Nada aqui inventa.** Nenhuma métrica, cliente ou resultado inventado vai no
seu nome. Se um rascunho precisa de um número que você não deu, ele volta com
`{{seu número}}` e um aviso, sempre.

**Regra de plataforma envelhece.** O limite de hashtags caiu de 30 para 5 em
dezembro de 2025. Se algo aqui contradiz o que o Instagram estiver fazendo
quando você ler, o Instagram está certo. Isto também não é assessoria jurídica:
para publi, sorteio e dados pessoais, na dúvida, consulte um advogado.

## Testes

São mais de 200 testes automáticos, que rodam no GitHub a cada envio, em
Linux, Windows e macOS e em várias versões do Python. Eles conferem os sete
scripts (nota do gancho, mapa de batidas, revisão de legenda, humanizador,
detector, swipe file e contas), os arquivos de dados (as 26 fórmulas, o léxico
e a rubrica) e a coerência do pacote: toda skill segue a regra de contas, todo
script ou comando que uma skill cita existe, e nenhum nome do pacote original
ficou para trás.

Alguns exemplos do que é verificado:

- cada uma das 26 frases de exemplo é reconhecida pela própria fórmula;
- `#publi` escondida depois do "... mais" dá erro, e na primeira linha passa;
- "ensino fundamental", "Deus é poderoso" e "não serve de nada" saem do
  humanizador intactos;
- um texto humano passa no detector e um texto de máquina é sinalizado;
- "48 mil", "1,2 mi" e "412k" viram os números certos no swipe file;
- criar, trocar e migrar contas nunca apaga nem sobrescreve nada.

O arquivo `tests/test_regressao.py` guarda os erros que apareceram no primeiro
teste com um perfil real: nome próprio no
meio da frase que não contava, "Conta aqui nos comentários" que não era
reconhecido como pedido, fonte tratada como link, hashtag sem o `#`, ano que
virava "1.942" e as regras de tamanho do gancho que não batiam entre os dois
scripts. Se um desses testes falhar, o erro voltou.

Para rodar na sua máquina:

```bash
python3 -m pip install pytest
python3 -m pytest tests
```

Os testes de contas usam uma pasta temporária e nunca mexem no seu
`~/.claude`. Se você mudar um script ou o `ganchos.json` e algum teste
quebrar, ou o teste pegou um erro, ou a regra mudou de propósito e o teste
precisa ser atualizado junto.

## Arquivos

```
skills/ig-reel/ganchos.json         26 fórmulas: modelo, exemplo, versão de tela,
                                    para que serve, como estraga e uma regex
skills/ig-reel/gancho.py            o painel de cinco critérios do gancho
skills/ig-reel/batidas.py           roteiro para mapa de batidas cronometrado
skills/ig-legenda/legenda.py        a prévia do corte e a revisão da legenda
skills/ig-humano/cliches.json       o léxico: ~190 termos, 18 classes invisíveis, 16 vícios
skills/ig-humano/humanizar.py       as três passadas de limpeza
skills/ig-humano/detectar.py        o painel de cinco critérios
skills/ig-viral/swipe.py            ranking por múltiplo e classificação por fórmula
skills/ig-perfil/rubrica.json       a nota de 100 pontos do perfil
skills/ig-contas/contas.py          cria, lista e troca as contas
skills/ig-contas/voz.md             modelo do perfil de voz, copiado para cada conta
tests/                              os testes automáticos
.github/workflows/testes.yml        roda os testes no GitHub a cada envio
```

## Perguntas frequentes

**O que é uma skill do Claude?**
Uma pasta com instruções (o `SKILL.md`) e, às vezes, scripts, que ensina o
Claude a fazer uma tarefa específica do jeito certo. Com este pacote
instalado, pedir "faz um roteiro de Reels" ou "revisa essa legenda" aciona a
skill certa sozinho.

**Funciona no Claude comum ou só no Claude Code?**
Nos dois. No Claude Code e no app do Claude com skills ativadas, tudo
funciona, inclusive os scripts em Python. Colando um `SKILL.md` numa conversa
comum, as instruções funcionam e os scripts ficam de fora.

**Ele posta no meu Instagram?**
Não. Ele escreve, revisa e planeja. Você posta. Automação de post, curtida,
comentário e DM fora das ferramentas oficiais viola os Termos de Uso do
Instagram e pode bloquear a conta.

**Serve para mais de uma conta?**
Sim. Cada conta tem a própria pasta, com tom de voz, histórico e plano
separados. Veja [Várias contas de Instagram](#várias-contas-de-instagram).

**Serve para página de fã, loja ou personagem feito com IA?**
Sim. Cada conta tem um tipo (pessoal, marca, nicho ou persona), e as regras
mudam conforme o tipo: página de fã deixa claro que não é oficial, persona
avisa que é IA, e toda conta identifica publicidade do jeito que o CONAR pede.

**O texto sai com cara de IA?**
Tudo passa pelo `/ig-humano`, que tira travessões, clichês, tradução literal
do inglês e caracteres invisíveis, e dá uma nota ao resultado. Ele não promete
texto "indetectável"; ninguém pode prometer isso com honestidade.

**Quanto custa?**
Nada. Licença MIT. Você só precisa de acesso ao Claude.

## Créditos

Adaptação para o Brasil por Alessandro Katayama.

Baseado no [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill),
de Jake Schincariol ([opusjake.ai](https://opusjake.ai)), publicado sob licença
MIT. A estrutura das skills, a lógica dos scripts e o método de pesquisa vêm de
lá.

## Licença

MIT. Pegue, mude, distribua. Mantenha os dois avisos de copyright do arquivo
[LICENSE](LICENSE).
