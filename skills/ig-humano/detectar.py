#!/usr/bin/env python3
"""
detectar.py - um painel de cinco critérios que dá nota a quanto um rascunho
em português parece escrito por máquina.

O que isto é: cinco heurísticas locais inspiradas nos sinais que detectores
públicos de IA medem: variação de tamanho de frase, coisas concretas,
vocabulário de clichê, marca tipográfica e voz. Tudo é calculado na sua
máquina, só a partir do texto. Nada é enviado.

O que isto NÃO é: GPTZero, Originality, Copyleaks, Winston ou Turnitin. Não
chama esses serviços e não garante o veredito deles. Pega as coisas que todos
eles observam, por isso corrigir costuma mexer nas notas deles também. Mas a
única afirmação honesta é a desta linha.

Cada critério devolve uma nota HUMANA de 0 a 100. Quanto maior, melhor.

Uso
  python3 detectar.py rascunho.txt
  python3 detectar.py rascunho.txt --json
  python3 detectar.py antes.txt depois.txt      # compara dois rascunhos
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "cliches.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+")
# Português não tem contração com apóstrofo como o inglês. O equivalente é a
# marca de fala: "tá", "pra", "né", "a gente". Texto gerado quase nunca usa.
FALA = re.compile(r"\b(?:tá|tô|tava|tavam|pra|pro|pras|pros|né|cê|vc|vcs|tb|tbm|num|numa|"
                  r"dum|duma|daí|beleza|tipo assim|a gente|bora|vamo|tamo|tô)\b", re.IGNORECASE)
PRONOUNS = re.compile(r"\b(?:eu|me|mim|meu|minha|meus|minhas|comigo|nós|nosso|nossa|a gente|"
                      r"você|vc|cê|te|ti|seu|sua|seus|suas|tu|teu|tua)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d.,]*%?|R\$\s?\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b", re.MULTILINE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Leva o valor para 0-100, onde `human` -> 100 e `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def lex_pattern(find):
    return re.compile(r"(?<!\w)" + re.escape(find).replace(r"\ ", r"\s+") + r"(?!\w)", re.IGNORECASE)


def check_burstiness(text):
    """Gente varia muito o tamanho da frase. Modelo escreve tudo igual."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "curto demais para julgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    return scale(cv, human=0.70, machine=0.22), f"variação {cv:.2f} em {len(lens)} frases (ideal 0,55+)"


def check_specificity(text):
    """Números, nomes e coisas concretas. Clichê é abstrato."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais para julgar"
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * 100 / len(w)
    return scale(density, human=6.0, machine=0.5), f"{hits} marcadores concretos, {density:.1f} a cada 100 palavras (ideal 4+)"


def check_slop(text, lex):
    """Densidade de vocabulário de clichê."""
    w = words(text)
    if not w:
        return 50.0, "vazio"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(lex_pattern(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    detail = f"{hits} clichês, {density:.1f} a cada 100 palavras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return scale(density, human=0.0, machine=4.0), detail


def check_fingerprint(text):
    """Caracteres que o teclado do celular não produz."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    # O iPhone troca aspas retas por curvas sozinho ("pontuação inteligente"),
    # então aspa curva é sinal fraco: pesa um quarto.
    total = invisible * 4 + em * 2 + curly * 0.25 + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    detail = (f"{invisible} invisível(is), {em} travessão(ões), {curly} aspa(s) curva(s), "
              f"{ellip} reticência(s) em um caractere, {nbsp} espaço(s) rígido(s)")
    return scale(per1k, human=0.0, machine=12.0), detail


def check_voice(text, lex):
    """Marca de fala, pessoa e os formatos que modelo usa por padrão."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais para julgar"
    per100 = 100 / len(w)
    fala = len(FALA.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells, names = 0, []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6
    score = (scale(fala, human=2.5, machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("marcadores-iguais")
    detail = (f"{fala:.1f} marcas de fala, {person:.1f} pronomes pessoais a cada 100 palavras, "
              f"{tells} vício(s) de estrutura")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIAÇÃO", "CONCRETO", "CLICHÊS", "TIPOGRAFIA", "VOZ"]


def run(text, lex):
    results = {
        "VARIAÇÃO": check_burstiness(text),
        "CONCRETO": check_specificity(text),
        "CLICHÊS": check_slop(text, lex),
        "TIPOGRAFIA": check_fingerprint(text),
        "VOZ": check_voice(text, lex),
    }
    scores = [results[c][0] for c in CHECKS]
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASSA" if overall >= 70 and min(scores) >= 55 else ("REVISAR" if overall >= 50 else "SINALIZADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PAINEL DE DETECÇÃO" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASSA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Sinal mais fraco: {weakest}. Corrija esse primeiro.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota a quanto um rascunho parece escrito por máquina.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo arquivo, para comparar antes e depois")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexico", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexico, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()
    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({"source": name,
                        "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
                        "human_score": round(overall, 1), "verdict": verdict})

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return
    for name, text in targets:
        render(*run(text, lex), label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  {b['human_score']:.1f} {b['verdict']}   "
              f"({b['human_score'] - a['human_score']:+.1f})\n")
    sys.exit(0 if payload[-1]["verdict"] == "PASSA" else 1)


if __name__ == "__main__":
    main()
