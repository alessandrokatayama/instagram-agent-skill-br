#!/usr/bin/env python3
"""
swipe.py - ranqueia os reels que você coletou pelo quanto cada um superou a
própria conta, dá nome à fórmula de gancho de cada um e escreve o swipe file.

A ideia do script é uma correção só: view bruta não é evidência. Uma conta de
2 milhões de seguidores fazendo 400 mil views teve um dia fraco. Uma conta de
4 mil seguidores fazendo 400 mil views achou alguma coisa. O ranking é pelo
múltiplo sobre a base da própria conta, a única versão de "viralizou" que
ensina algo que dá pra copiar.

A entrada é um arquivo separado por TAB que você preenche enquanto navega, um
reel por linha, com uma linha de cabeçalho dizendo as colunas (em português ou
em inglês):

    conta     seguidores  mediana  views    gancho
    @alguem   48000       11000    412000   ninguém te conta que os 30 primeiros flopam

`mediana` é a média típica de views recentes daquela conta, a melhor base.
Se você só tem `seguidores`, deixe a mediana de fora e o script avisa.
`gancho` é a primeira frase do reel, falada ou na tela, nas palavras da pessoa.

Uso
  python3 swipe.py coletados.tsv
  python3 swipe.py coletados.tsv --conta lia      # grava no swipe.md da conta
  python3 swipe.py coletados.tsv --saida swipe.md
  python3 swipe.py coletados.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "ganchos.json")
WORD_RE = re.compile(r"(?:R\$\s?)?[\w%'’-]+")

COLS = {"conta": "account", "perfil": "account", "seguidores": "followers", "mediana": "median",
        "visualizacoes": "views", "visualizações": "views", "gancho": "hook"}

try:                                              # opcional: dar nota aos ganchos também
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from gancho import run as score_hook          # noqa: E402
except Exception:                                 # ig-viral copiado sozinho
    score_hook = None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"], re.compile(by_id[i]["match"], re.IGNORECASE))
            for i in order if i in by_id]


def classify(hook, formulas):
    for fid, name, pattern in formulas or []:
        if pattern.search(hook):
            return fid, name
    return None, "sem fórmula"


def to_int(value):
    v = (value or "").strip().lower().replace(" ", "")
    mult = 1
    if v.endswith(("mil", "k")):
        mult, v = 1000, re.sub(r"(mil|k)$", "", v)
    elif v.endswith(("mi", "m")):
        mult, v = 1_000_000, re.sub(r"(mi|m)$", "", v)
    if mult > 1 and re.fullmatch(r"\d+[.,]\d{1,2}", v):   # "1,2 mi", "1.5k"
        return int(float(v.replace(",", ".")) * mult)
    digits = re.sub(r"[^\d]", "", v)
    return int(digits) * mult if digits else None


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [COLS.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = to_int(r.get("views")) or 0
        for k in ("followers", "median"):
            r[k] = to_int(r.get(k))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {"baseline": "mediana da conta" if used_median else "número de seguidores",
            "n": len(ranked), "accounts": len({r.get("account", "") for r in ranked}),
            "reels": ranked, "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
            "top_hook_score": med(top, "hook_score"), "bottom_hook_score": med(bottom, "hook_score"),
            "top_words": med(top, "words"), "bottom_words": med(bottom, "words"),
            "unclassified": sum(1 for r in ranked if r["formula"] == "sem fórmula")}


def br(n):
    return f"{n:,}".replace(",", ".")


def render(a, out=sys.stdout):
    head = f"SWIPE FILE  ·  {a['n']} reels  ·  {a['accounts']} contas  ·  base: {a['baseline']}"
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>7}  nota {score:>3}  {fid} {r['formula'][:24]:<24} "
              f"{r.get('account', '')[:16]:<16} {br(r['views']):>11}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("O QUE ESTÁ FUNCIONANDO NESTE LOTE", file=out)
    if a["top_formulas"]:
        print("  terço de cima:         " + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  nota mediana:          cima {a['top_hook_score']:.0f}  x  baixo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  tamanho mediano:       cima {a['top_words']} palavras  x  baixo {a['bottom_words']} palavras", file=out)
    print(f"  sem fórmula:           {a['unclassified']} de {a['n']}. Leia esses na mão: é ali que se "
          "esconde a fórmula que você ainda não tem.", file=out)
    print("\n  Lote coletado na mão é evidência, não prova. Doze reels não mostram nada;\n"
          "  quarenta em seis contas mostram alguma coisa. Colete mais antes de acreditar.\n", file=out)


def to_markdown(a):
    lines = ["# Swipe file", "", f"{a['n']} reels em {a['accounts']} contas. Ranqueado pelo múltiplo sobre {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- views: {br(r['views'])}  base: {br(r['baseline'])}",
                  f"- nota do gancho: {r['hook_score']}  palavras: {r['words']}",
                  f"- gancho: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ranqueia reels coletados pelo múltiplo sobre a própria conta.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo TSV, ou - para stdin")
    ap.add_argument("--ganchos", default=HOOKS, help="caminho do ig-reel/ganchos.json")
    ap.add_argument("--conta", help="grava o swipe file na pasta desta conta (ver /ig-contas)")
    ap.add_argument("--saida", help="grava o swipe file em markdown neste caminho")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("nenhuma linha usável. Precisa de um arquivo separado por TAB com pelo menos views e gancho.",
              file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.ganchos)
    a = analyse(rows, formulas)
    if not formulas:
        print("aviso: ganchos.json não encontrado, fórmulas sem nome. Use --ganchos.", file=sys.stderr)
    if score_hook is None:
        print("aviso: gancho.py não pôde ser importado, notas puladas.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    path = None
    if args.conta:
        base = os.path.expanduser(os.environ.get("IG_BR_DIR", "~/.claude/instagram-br"))
        nome = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFD", args.conta.lstrip("@"))
                      .encode("ascii", "ignore").decode().lower()).strip("-")
        try:                                      # aceita também o @ da conta
            sys.path.insert(0, os.path.join(HERE, "..", "ig-contas"))
            import contas                         # noqa: E402
            nome = contas.resolver(args.conta) or nome
        except Exception:
            pass
        pasta = os.path.join(base, "contas", nome)
        if not os.path.isdir(pasta):
            print(f"conta \"{args.conta}\" não existe. Crie com: contas.py criar {nome}", file=sys.stderr)
            sys.exit(2)
        path = os.path.join(pasta, "swipe.md")
    elif args.saida:
        path = os.path.expanduser(args.saida)
    if path:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"gravado em {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
