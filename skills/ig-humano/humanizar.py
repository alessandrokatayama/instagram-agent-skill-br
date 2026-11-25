#!/usr/bin/env python3
"""
humanizar.py - tira a marca de máquina de um rascunho em português.

Três passadas, nesta ordem:

  1. INVISÍVEIS  apaga ou normaliza os caracteres que um teclado humano não
                 produz: espaço de largura zero, junções, hífen suave, BOM,
                 caracteres de tag Unicode, espaços rígidos e estreitos. Eles
                 sobrevivem ao copiar e colar e são a marca mais mecânica de
                 texto gerado.
  2. TIPOGRAFIA  travessão -> vírgula, meia-risca -> hífen, aspas curvas ->
                 retas, reticências em um caractere -> três pontos, marcador -> hífen.
  3. LÉXICO      troca os clichês de cliches.json por palavras simples,
                 mantendo maiúsculas e sem mexer em links.

Vícios de estrutura (regra de três, "não é só X, é Y", muro de hashtags) são
APONTADOS, nunca reescritos automaticamente: mudar o formato de uma frase pede
julgamento, então é trabalho do modelo, não de uma regex.

Uso
  python3 humanizar.py rascunho.txt
  python3 humanizar.py rascunho.txt --relatorio
  python3 humanizar.py rascunho.txt --json
  python3 humanizar.py rascunho.txt -o limpo.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "cliches.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+|\bwa\.me/\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200b;  'U+E0000-U+E007F' -> (início, fim)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            action = "apagar" if entry["action"] == "delete" else "virar espaço"
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n, "action": action})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Qualquer outro caractere de formatação (categoria Cf) é invisível por definição.
    # O marcador \x00 das URLs protegidas não é Cf, então fica.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "outros caracteres invisíveis de formatação", "count": len(stray), "action": "apagar"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espaço)"})
        if ch == "—":
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)       # 5–10 -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)             # usada como travessão
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    text = re.sub(r"(?m)^\s*,\s*", "", text)                 # diálogo com travessão no início da linha
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex):
    """Troca clichês. Os mais longos primeiro, para a expressão ganhar da palavra."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"], key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = re.compile(r"(?<!\w)" + re.escape(find).replace(r"\ ", r"\s+") + r"(?!\w)", re.IGNORECASE)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(apagado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpeza depois de apagar: sobra pontuação órfã ("sistema. ." ou linha começando com vírgula).
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = text.replace("...", "\x00RET\x00")
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00RET\x00", "...")
    # Linha que começa com ! ou ? porque a frase antes foi apagada.
    text = re.sub(r"(?m)^[ \t]*[!?]+[ \t]*", "", text)
    # Vírgula órfã logo depois de um emoji usado como marcador ("✅, muitos").
    text = re.sub(r"([\U0001F300-\U0001FAFF☀-➿])[ \t]*,[ \t]*", r"\1 ", text)
    # Conjunção que ficou sozinha no fim da frase ("Então, e." / "e!").
    text = re.sub(r",?[ \t]+(?:e|mas|ou)[ \t]*([.!?])", r"\1", text)
    text = re.sub(r"(?im)^[ \t]*(?:e|mas|ou|então)[ \t]*[.!?]?[ \t]*(?=#|$)", "", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Travessão que virou vírgula seguido de conectivo deixa frase emendada.
    text = re.sub(r",\s*(também|então|ainda|basicamente|no fim)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({"name": f"Frases todas do mesmo tamanho (variação {cv:.2f})", "count": len(lens),
                          "fix": "Quebre uma frase no meio. Deixe outra comprida. Máquina escreve tudo igual."})
    return flags


def restore_capitals(original, text):
    """Apagar uma abertura deixa a próxima palavra em minúscula.

    Só corrige para quem começa frase com maiúscula: escrever tudo em minúscula
    de propósito é estilo, não defeito.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*([A-Za-zÀ-ÿ])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*([a-zà-ÿ])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {"invisible": inv, "typographic": typo, "lexical": lexi,
                                 "structures": scan_structures(text, lex)}


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for k in ("invisible", "typographic", "lexical") for h in report[k])
    head("RELATÓRIO DO HUMANIZADOR")
    print(f"{total} marcas de máquina removidas, "
          f"{len(report['structures'])} vício(s) de estrutura apontado(s) para reescrever", file=out)
    if report["invisible"]:
        head("1. CARACTERES INVISÍVEIS")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFIA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. CLICHÊS")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. VÍCIOS DE ESTRUTURA  (não corrigidos sozinhos - reescreva você)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPO")
        print("  Nada para tirar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Tira a marca de máquina de um rascunho.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - para stdin")
    ap.add_argument("-o", "--out", help="grava o texto limpo aqui em vez de imprimir")
    ap.add_argument("--relatorio", action="store_true", help="mostra o que mudou (no stderr)")
    ap.add_argument("--json", action="store_true", help="devolve {text, report} em JSON")
    ap.add_argument("--lexico", default=LEX, help="caminho do cliches.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    clean, report = humanize(raw, load_lexicon(args.lexico))

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"gravado em {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.relatorio:
        render_report(report)


if __name__ == "__main__":
    main()
