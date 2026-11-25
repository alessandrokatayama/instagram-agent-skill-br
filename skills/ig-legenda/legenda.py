#!/usr/bin/env python3
"""
legenda.py - revisa uma legenda de Instagram e mostra exatamente o que o feed
mostra antes do "... mais".

O Instagram mostra uns 125 caracteres da legenda no feed e esconde o resto
atrás de um toque. Quase toda legenda que falha, falha ali: o gancho está na
terceira frase, a primeira linha é uma saudação, ou tudo começa com hashtag.
O script imprime essa janela visível numa caixa, do jeito que um desconhecido
rolando o feed lê, e depois confere as coisas que valem a pena conferir.

O corte em 125 caracteres é aproximado. O número real muda com o aparelho, o
tamanho da fonte e onde caem as quebras de linha, e é por isso que você quer
folga, não uma legenda calculada pra terminar no 125. Mude com --corte.

Uso
  python3 legenda.py legenda.txt
  python3 legenda.py legenda.txt --busca "proposta comercial,contrato de freelancer"
  python3 legenda.py legenda.txt --json
"""

import argparse
import json
import re
import sys
import textwrap
import unicodedata

LIMIT = 2200             # Limite da legenda no Instagram.
TRUNCATE = 125           # Mais ou menos onde o feed corta pro "... mais".
HASHTAG_LIMIT = 5        # Limite por post ou reel desde 18/12/2025 (antes eram 30),
                         # anunciado pela conta @Creators do Instagram.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\bwa\.me/\S+|\b[a-z0-9-]+\.(?:com\.br|com|br|co|io|net|org|ai|app|shop|store)(?:/\S*)?",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(r"R\$\s?\d|\b\d[\d.,]*\b|(?<![.!?]\s)(?<!^)\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b", re.MULTILINE)
PUBLI_RE = re.compile(r"(?i)#?\b(?:publi|publicidade|parceria paga|conteúdo patrocinado|patrocinado|afiliad[oa]|link de afiliado|#ad)\b")

ASKS = [
    (re.compile(r"(?i)\b(?:comenta|comente|escreve|escreva|digita|digite)\s+(?:a palavra\s+|aqui\s+)?[\"“]?[A-ZÀ-Ý0-9]{2,}\b"), "comentar uma palavra"),
    (re.compile(r"(?i)(?<!\bse )\b(?:me chama|chama (?:no|na|aqui|lá|por)\b(?! (?:whats|zap))|me manda (?:um )?(?:direct|dm|mensagem)|manda (?:um )?(?:direct|dm))\b"), "chamar no direct"),
    (re.compile(r"(?i)\b(?:salva|salve|guarda|guarde) (?:esse|este|essa|esta|o post|pra|para)\b"), "salvar"),
    (re.compile(r"(?i)\b(?:compartilha|compartilhe|manda (?:pra|para)|envia (?:pra|para)|envie (?:pra|para))\b"), "compartilhar"),
    (re.compile(r"(?i)\b(?:me segue|siga|segue (?:o perfil|pra|para)|ativa (?:as )?notificações)\b"), "seguir"),
    (re.compile(r"(?i)\blink na bio\b|\blink no perfil\b"), "link na bio"),
    (re.compile(r"(?i)\b(?:arrasta|arraste|desliza|deslize|passa) (?:pro|para o|pra) lado\b"), "arrastar"),
    (re.compile(r"(?i)\b(?:me conta|me diz|me fala|qual (?:você|vc) (?:escolhe|prefere)|qual deles|o que (?:você|vc) (?:faria|acha))\b"
                r"|\b(?:conta|comenta|responde|deixa|escreve|fala)\b[^.!?\n]{0,25}\bcomentários?\b"
                r"|\b(?:conta|fala|diz) (?:pra|para) (?:gente|mim|nós)\b"
                r"|\?[ \t]*(?:👇|⬇️?|👉)"), "responder uma pergunta"),
    (re.compile(r"(?i)\b(?:chama no whats|chama no zap|me chama no whatsapp|whatsapp na bio)\b"), "chamar no WhatsApp"),
]

FILLER_TAGS = {"#viral", "#fyp", "#fy", "#explore", "#explorar", "#explorepage", "#foryou",
               "#foryoupage", "#paravoce", "#paravocê", "#trending", "#instagood", "#love",
               "#follow", "#like4like", "#reels", "#reelsinstagram", "#reelsbrasil", "#viralreels",
               "#instadaily", "#brasil", "#instabrasil", "#segue", "#sigo", "#seguidores",
               "#curtir", "#curtidas", "#viralizar", "#viralizou", "#engajamento"}


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def visible_window(text, cut):
    """O que o feed mostra. O Instagram corta no meio da palavra, então aqui também."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  O QUE O FEED MOSTRA", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... mais" if truncated else "(legenda inteira cabe)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    stripped = text.strip()
    chars = len(stripped)
    first_line = stripped.split("\n")[0].strip() if stripped else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    # "Fonte: site.com.br" é citação, não link para clicar.
    links = [l for l in LINK_RE.findall(stripped)
             if not re.search(r"(?i)\b(?:fonte|fontes|via|créditos?|crédito)\s*:?\s*$",
                              stripped[:stripped.find(l)].splitlines()[-1] if stripped.find(l) > 0 else "")]
    # Na linha de hashtags, palavra colada em CamelCase sem o # na frente ("ArrancadaHeroica").
    tag_lines = [l for l in stripped.split("\n") if len(HASHTAG_RE.findall(l)) >= 2]
    sem_cerquilha = sorted({w for l in tag_lines for w in re.findall(r"(?:^|\s)([A-ZÀ-Ý][a-zà-ÿ]+(?:[A-ZÀ-Ý][a-zà-ÿ]+)+)\b", l)})
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    faltando = re.findall(r"\{\{[^}]*\}\}", stripped)
    if faltando:
        add("A PREENCHER", "ERRO", f"{len(faltando)} espaço(s) ainda sem preencher: {', '.join(faltando[:3])}")

    add("TAMANHO", "ERRO" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} acima do limite" if chars > LIMIT else ""))

    if not first_line:
        add("1ª LINHA", "ERRO", "a legenda começa com linha em branco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("1ª LINHA", "ERRO", "começa com hashtag ou menção, na única posição que vale uma frase")
    elif len(first_line) > cut:
        add("1ª LINHA", "ATENÇÃO",
            f"{len(first_line)} caracteres, então é cortada no {cut} no meio do pensamento. "
            "Tudo bem se o corte é suspense, ruim se é no meio de uma oração")
    else:
        add("1ª LINHA", "OK", f"{len(first_line)} caracteres, aparece inteira")

    add("GANCHO CONCRETO", "OK" if CONCRETE_RE.search(window) else "ATENÇÃO",
        f"{len(CONCRETE_RE.findall(window))} número(s) ou nome(s) na parte visível"
        + ("" if CONCRETE_RE.search(window) else " - nada verificável antes do toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "ERRO", f"{len(tags)} hashtags, acima do limite de {HASHTAG_LIMIT} do Instagram")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "ATENÇÃO", f"{len(tags)} hashtags, no limite, e {len(filler)} genérica(s). "
                                   "Gaste as cinco em assunto")
    elif filler:
        add("HASHTAGS", "ATENÇÃO", f"{len(tags)} hashtags, {len(filler)} genérica(s) "
                                   f"({', '.join(filler[:3])}). Essas não descrevem nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("POSIÇÃO TAGS", "OK", "sem hashtags para posicionar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("POSIÇÃO TAGS", "ATENÇÃO", "tem hashtag na parte visível, gastando espaço do feed com etiqueta")
    else:
        add("POSIÇÃO TAGS", "OK", "hashtags abaixo do corte")

    if sem_cerquilha:
        add("TAG SEM #", "ERRO", f"{', '.join(sem_cerquilha)} está na linha de hashtags sem o #, "
                                "então não vira hashtag")

    accented = [t for t in tags if strip_accents(t) != t]
    if accented:
        add("ACENTO TAGS", "ATENÇÃO",
            f"{', '.join(accented[:3])} tem acento. No Instagram, a versão com e a sem acento são hashtags "
            "diferentes: veja qual das duas o seu público realmente usa")

    add("LINKS", "ATENÇÃO" if links else "OK",
        f"{len(links)} link(s) na legenda, e legenda não é clicável. Leve para a bio ou para o direct"
        if links else "nenhum link morto no texto")

    if len(asks) == 1:
        add("UM PEDIDO", "OK", f"uma chamada para ação: {asks[0]}")
    elif not asks:
        add("UM PEDIDO", "ATENÇÃO", "nenhuma chamada para ação. Decida para que serve este post")
    else:
        add("UM PEDIDO", "ATENÇÃO", f"{len(asks)} pedidos ({', '.join(asks)}). Dois pedidos valem o mesmo que nenhum")

    publi = PUBLI_RE.search(stripped)
    if publi:
        in_window = bool(PUBLI_RE.search(window))
        add("PUBLICIDADE", "OK" if in_window else "ERRO",
            "identificação de publicidade visível antes do corte" if in_window else
            f"\"{publi.group(0)}\" só aparece depois do \"... mais\". O guia do CONAR pede a "
            "identificação visível sem precisar abrir a legenda: leve para a primeira linha "
            "ou use o rótulo de parceria paga do Instagram")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "ATENÇÃO" if density > 4 else "OK",
        f"{len(emoji)} emoji, {density:.1f} a cada 100 caracteres" + (" - vira enfeite" if density > 4 else ""))

    if keywords:
        low = strip_accents(stripped.lower())
        found = [k for k in keywords if strip_accents(k.lower()) in low]
        missing = [k for k in keywords if strip_accents(k.lower()) not in low]
        in_window = [k for k in found if strip_accents(k.lower()) in strip_accents(window.lower())]
        status = "OK" if not missing else ("ATENÇÃO" if found else "ERRO")
        add("BUSCA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} na parte visível" if found else "")
            + (f". Faltando: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "ERRO")
    warns = sum(1 for c in checks if c["status"] == "ATENÇÃO")
    verdict = "CORRIGIR" if fails else ("REVISAR" if warns else "PRONTA")

    return {"characters": chars, "limit": LIMIT, "truncate_at": cut, "visible": window,
            "truncated": truncated, "first_line_chars": len(first_line), "hashtags": tags,
            "mentions": mentions, "links": links, "emoji": len(emoji), "asks": asks,
            "checks": checks, "verdict": verdict}


def render(a, out=sys.stdout):
    head = (f"REVISÃO DE LEGENDA  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<8} {c['check']:<16} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDITO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa uma legenda de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo da legenda, ou - para stdin")
    ap.add_argument("--corte", type=int, default=TRUNCATE,
                    help=f"caracteres mostrados antes do '... mais' (padrão {TRUNCATE})")
    ap.add_argument("--busca", default="", help="termos de busca separados por vírgula")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.corte, keywords=args.busca.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "PRONTA" else 1)


if __name__ == "__main__":
    main()
