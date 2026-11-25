---
name: ig-contas
description: >-
  Gerencia várias contas de Instagram no mesmo pacote: cria uma pasta por
  conta (voz, swipe file, histórico e plano separados), troca a conta em uso,
  lista as contas e liga cada uma à sua skill de persona. Use quando o usuário
  disser "cria uma conta nova", "agora é pra outra conta", "troca pra conta X",
  "quais contas eu tenho", "esse conteúdo é do @perfil", ou cuidar de mais de
  um perfil (pessoal, marca, personagem feito com IA).
---

# ig-contas

Quem cuida de mais de um perfil não pode ter um voz.md só. O tom do perfil
pessoal vaza para a marca, o swipe file de culinária manda gancho para o perfil
de tecnologia, e o histórico de comentários mistura quem comentou de qual conta.
Esta skill separa tudo por conta.

Uma ferramenta fica nesta pasta e ela roda:

```bash
python3 contas.py listar
python3 contas.py criar lia --arroba @lia.criadora --tipo persona --persona lia-persona
python3 contas.py usar lia
python3 contas.py ativa
python3 contas.py pasta cafeaurora
python3 contas.py migrar
```

## Onde fica cada coisa

```
~/.claude/instagram-br/
    ativa                 nome da conta em uso
    contas/
        <conta>/
            conta.json    @, tipo, skill de persona, fuso do público
            voz.md        como esta conta fala
            swipe.md      o que funciona no nicho desta conta (/ig-viral)
            historico.md  o que foi postado e comentado (/ig-reel, /ig-comentario...)
            plano.md      a semana desta conta (/ig-plano)
```

Nas outras skills, `{pasta da conta}` quer dizer
`~/.claude/instagram-br/contas/<conta>/`. Para descobrir, rode
`contas.py pasta` (conta ativa) ou `contas.py pasta <nome>`.

## Criar uma conta

Pergunte numa mensagem só:

1. **O @** e um nome curto para a pasta (`lia`, `cafeaurora`).
2. **O tipo**: `pessoal` (a pessoa falando por ela mesma), `marca` (uma empresa
   ou loja), `nicho` (página temática ou de fã: um time, uma série, receitas,
   notícias de um assunto) ou `persona` (personagem ou influenciador feito com
   IA).
3. **Se existe uma skill de persona** para essa conta. Se o usuário já tem uma
   skill com o DNA do personagem ou da marca, registre o nome dela com
   `--persona`. Ela passa a valer por cima do voz.md.

Depois rode `contas.py criar`, e preencha o voz.md da conta, de preferência a
partir de três reels ou legendas reais dela.

A primeira conta criada vira a ativa sozinha. Com mais de uma, use `--usar` ou
`contas.py usar`.

## A regra que todas as skills seguem

Antes de ler ou gravar qualquer arquivo de conta:

1. **Se o usuário disse a conta** (nome, @ ou "pra Lia"), use essa, mesmo
   que outra esteja ativa. Não troque a ativa sem ele pedir.
2. **Senão, use a ativa** (`contas.py ativa`). Diga qual é na primeira linha da
   resposta ("Conta: lia"), para um engano aparecer na hora.
3. **Se há várias e nenhuma ativa**, pergunte qual. Não chute.
4. **Se não existe nenhuma**, ofereça criar. Dá para seguir sem conta, mas sem
   voz e sem histórico.
5. **Nunca misture.** O swipe file, o histórico e o plano de uma conta não
   entram no trabalho de outra, a menos que o usuário peça uma visão de todas.

## Contas do tipo persona

Quando `conta.json` tem `tipo: persona`:

- **Leia a skill de persona indicada em `persona` antes de escrever.** As regras
  dela (tom, vocabulário, o que o personagem nunca diz, como avisar que é IA)
  valem por cima de qualquer padrão deste pacote.
- **Nunca invente vivência.** Personagem feito com IA não "foi" a lugar
  nenhum, não "provou" produto nenhum e não tem cliente. Gancho do tipo
  Confissão de Custo ou O Recibo só se o fato for real e da operação por trás
  da conta, dito como tal.
- **Transparência de IA.** O perfil e o conteúdo precisam deixar claro que é um
  personagem feito com IA, do jeito que a skill de persona determina. Humanizar
  o texto nunca é esconder isso.
- **Publi da persona é publi.** Mesma regra do CONAR de qualquer conta.

## Contas do tipo nicho

Página temática ou de fã fala de um assunto, não de uma pessoa. Por isso:

- **Terceira pessoa é normal.** Gancho de história ou notícia ("O adversário
  abandonou o campo") tira nota mais baixa em DIREÇÃO e o detector dá VOZ baixa
  para texto informativo. Isso é esperado; olhe os outros critérios.
- **Fato precisa de fonte.** Data, placar, número e citação vêm de fonte
  confiável, dita na legenda. A skill nunca completa uma história com detalhe
  que não está na fonte.
- **Página de fã não é a oficial.** Se usa escudo, mascote ou nome de clube,
  marca ou artista, a bio precisa deixar claro que é página de torcedor ou de
  fã, não oficial. Escudo e marca registrada são do dono; usar como se fosse o
  perfil oficial pode render denúncia e remoção.
- **Música e hino têm dono.** Não ponha letra de hino, de música ou de canto de
  torcida protegido na legenda nem no roteiro. Citar o nome ou um verso curto
  como referência é diferente de reproduzir a letra.

## Contas irmãs

Se o usuário cuida de várias contas, ele pode pedir uma visão conjunta (por
exemplo, "planeja a semana de todas as contas"). Nesse caso, leia os arquivos
de cada uma e cuide de três coisas: não pôr o mesmo tema na mesma semana em
contas do mesmo público, não postar no mesmo horário se é a mesma pessoa
gravando, e não fazer uma conta parecer cópia da outra.

## Migrar do formato antigo

Se existir `voz.md`, `swipe.md`, `historico.md` ou `plano.md` solto em
`~/.claude/instagram-br/` (do tempo em que o pacote tinha uma conta só), rode
`contas.py migrar <nome>` para mover tudo para uma conta. Nada é apagado: se o
destino já tem o arquivo, o antigo fica onde está e o script avisa.

## Saída

```
CONTAS
 * lia            @lia.criadora       persona   [voz, swipe, historico]  persona: lia-persona
   cafeaurora     @cafeaurora         marca     [voz, plano]

Conta ativa: lia
```

Este script nunca apaga uma conta. Para remover, o usuário apaga a pasta.
