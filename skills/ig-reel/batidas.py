#!/usr/bin/env python3
"""
batidas.py - transforma o roteiro de um Reel num mapa de batidas cronometrado,
antes de você gravar.

Estima quanto tempo cada linha leva pra ser falada, empilha em minutagem e
aponta as quatro coisas que matam um Reel na edição: gancho que passa dos três
segundos, batida longa o bastante pra pessoa sair, sequência de linhas sem nada
concreto e duração que não bate com o que você disse que ia fazer.

As durações são estimativa por contagem de palavras a um ritmo de palavras por
minuto. Servem pra planejar a edição, não substituem gravar. Ajuste o seu
ritmo com --ppm depois de cronometrar você mesmo lendo um roteiro em voz alta.
O padrão aqui é 160; em português, quem fala rápido passa de 180.

Uso
  python3 batidas.py roteiro.txt
  python3 batidas.py roteiro.txt --alvo 30
  python3 batidas.py roteiro.txt --ppm 180 --alvo 45
  python3 batidas.py roteiro.txt --json
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"(?:R\$\s?)?[\w%'’-]+")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(r"R\$\s?\d|\b\d[\d.,]*\b|(?<![.!?]\s)(?<!^)\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b", re.MULTILINE)
STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "e", "ou", "mas", "se",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "por",
    "pra", "pro", "para", "com", "que", "isso", "esse", "essa", "este", "esta",
    "é", "são", "foi", "era", "ser", "ter", "tem", "tá", "está", "você", "vc",
    "seu", "sua", "eu", "meu", "minha", "me", "a gente", "nós", "eles", "elas",
    "ele", "ela", "então", "só", "não", "já", "faz", "fiz", "vai", "vou", "ao",
    "à", "aí", "aqui", "lá", "mais", "muito", "todo", "toda", "tudo", "como",
}

HOOK_WINDOW = 3.75       # segundos: 10 palavras a 160 ppm, o mesmo limite do gancho.py
MAX_BEAT = 4.0           # segundos numa ideia sem mudar nada na tela.
ABSTRACT_RUN = 3         # batidas seguidas sem nada verificável.


def normalize(text):
    t = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text)        # 18.000 -> 18000
    return re.sub(r"R\$\s+(?=\d)", "R$", t)


def words(text):
    return WORD_RE.findall(normalize(text))


def pretty(token):
    """Volta o separador de milhar só para exibir."""
    if re.fullmatch(r"(?:1[89]|20)\d\d", token):      # ano: 1942 fica 1942
        return token
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    """Uma linha é uma batida, a não ser que a linha seja longa demais pra ser uma."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, ppm=160, target=None):
    wps = ppm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({"n": i + 1, "start": round(clock, 2), "dur": round(dur, 2), "words": n,
                     "text": text, "concrete": len(CONCRETE_RE.findall(text)),
                     "label": "", "flags": []})
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "GANCHO" else "GANCHO/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MEIO"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"gancho leva {rows[0]['dur']:.1f}s, passou dos {HOOK_WINDOW:g}s")
        notes.append(f"A batida 1 leva {rows[0]['dur']:.1f}s pra ser falada. Corte para "
                     f"{int(HOOK_WINDOW * wps)} palavras ou menos, senão o gancho chega depois "
                     "que a decisão já foi tomada.")
    if rows[0]["concrete"] == 0:
        notes.append("A batida 1 não tem número nem nome. Gancho sem nada verificável é o que "
                     "a pessoa rola pra cima.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s numa batida só")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Batida(s) {', '.join(map(str, long_beats))} passam de {MAX_BEAT:.0f}s. "
                     "Quebre a frase ou mude o que está na tela dentro dela. "
                     "Quadro parado é onde as pessoas saem.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"As batidas {start} a {r['n']} não têm nada concreto. "
                             "Coloque um número, um nome ou um preço em uma delas.")
        else:
            run, start = 0, None

    first = {w.lower() for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {w.lower() for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Loop: a última batida repete \"{', '.join(loop[:3])}\" do gancho. "
                     "Segunda visualização é alcance de graça.")
    else:
        notes.append("Sem loop. A última batida não repete nenhuma palavra do gancho, então o "
                     "vídeo termina chapado. Ecoar uma palavra da batida 1 é o replay mais barato que existe.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Duração no alvo ({total:.1f}s para {target:g}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s acima do alvo. Corte umas {int(delta * wps)} palavras.")
        else:
            notes.append(f"{-delta:.1f}s abaixo do alvo. Acrescente {int(-delta * wps)} palavras "
                         "ou grave mais curto. Mais curto costuma ser o certo.")

    return {"ppm": ppm, "target": target, "total_seconds": round(total, 2),
            "total_words": sum(r["words"] for r in rows), "beats": rows, "notes": notes}


def render(a, out=sys.stdout):
    head = (f"MAPA DE BATIDAS  ·  {a['total_words']} palavras  ·  ~{a['total_seconds']:.1f}s "
            f"a {a['ppm']:g} ppm" + (f"  ·  alvo {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<11}" if r["label"] else " " * 11
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<11}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Cronometra o roteiro de um Reel em batidas.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo do roteiro, ou - para stdin")
    ap.add_argument("--ppm", type=float, default=160, help="palavras por minuto (padrão 160)")
    ap.add_argument("--alvo", type=float, help="duração desejada em segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, ppm=args.ppm, target=args.alvo)
    if not a:
        print("roteiro vazio", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
