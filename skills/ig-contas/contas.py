#!/usr/bin/env python3
"""
contas.py - gerencia as contas de Instagram do pacote: uma pasta por conta,
com voz, swipe file, histórico e plano separados, e uma conta ativa.

Estrutura (a base pode ser trocada com a variável IG_BR_DIR):

    ~/.claude/instagram-br/
        ativa                     nome da conta em uso
        contas/
            lia/
                conta.json        @, tipo, skill de persona, fuso
                voz.md            perfil de voz desta conta
                swipe.md          escrito pelo /ig-viral
                historico.md      escrito pelo /ig-reel, /ig-comentario...
                plano.md          escrito pelo /ig-plano
            cafeaurora/
                ...

Nenhum arquivo é apagado por este script. "remover" não existe de propósito:
para tirar uma conta, apague a pasta você mesmo.

Uso
  python3 contas.py listar
  python3 contas.py criar lia --arroba @lia.criadora --tipo persona --persona lia-persona
  python3 contas.py usar lia
  python3 contas.py ativa                 # nome e pasta da conta em uso
  python3 contas.py pasta cafeaurora     # só a pasta, para usar em outro comando
  python3 contas.py migrar                # move arquivos do formato antigo (uma conta só)
  python3 contas.py listar --json
"""

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "voz.md")
FILES = ("voz.md", "swipe.md", "historico.md", "plano.md")
TIPOS = ("pessoal", "marca", "nicho", "persona")


def base_dir():
    return os.path.expanduser(os.environ.get("IG_BR_DIR", "~/.claude/instagram-br"))


def contas_dir():
    return os.path.join(base_dir(), "contas")


def slug(name):
    """'Café Aurora' -> 'cafe-aurora'. '@lia.criadora' -> 'lia-criadora'."""
    s = unicodedata.normalize("NFD", name.strip().lstrip("@"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def pasta(nome):
    return os.path.join(contas_dir(), slug(nome))


def ler_meta(nome):
    try:
        with open(os.path.join(pasta(nome), "conta.json"), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {"nome": slug(nome)}


def todas():
    d = contas_dir()
    if not os.path.isdir(d):
        return []
    return sorted(n for n in os.listdir(d) if os.path.isdir(os.path.join(d, n)))


def ativa():
    """A conta ativa, se ela existe. Com uma conta só, ela é a ativa."""
    try:
        with open(os.path.join(base_dir(), "ativa"), encoding="utf-8") as fh:
            nome = fh.read().strip()
        if nome and nome in todas():
            return nome
    except OSError:
        pass
    lista = todas()
    return lista[0] if len(lista) == 1 else None


def resolver(nome):
    """Aceita o nome, o slug ou o @ de uma conta já criada."""
    if not nome:
        return None
    alvo = slug(nome)
    if alvo in todas():
        return alvo
    for n in todas():
        if slug(ler_meta(n).get("arroba", "")) == alvo:
            return n
    return None


def cmd_listar(args):
    lista, atual = todas(), ativa()
    if args.json:
        print(json.dumps([dict(ler_meta(n), nome=n, pasta=pasta(n), ativa=(n == atual),
                               arquivos=[f for f in FILES if os.path.exists(os.path.join(pasta(n), f))])
                          for n in lista], indent=2, ensure_ascii=False))
        return 0
    if not lista:
        print("Nenhuma conta criada. Use: contas.py criar <nome> --arroba @perfil")
        return 1
    for n in lista:
        m = ler_meta(n)
        tem = [f.replace(".md", "") for f in FILES if os.path.exists(os.path.join(pasta(n), f))]
        mark = "*" if n == atual else " "
        extra = f"  persona: {m['persona']}" if m.get("persona") else ""
        print(f" {mark} {n:<18} {m.get('arroba', ''):<20} {m.get('tipo', ''):<9} [{', '.join(tem)}]{extra}")
    if not atual:
        print("\nNenhuma conta ativa. Use: contas.py usar <nome>")
    return 0


def cmd_criar(args):
    nome = slug(args.nome)
    if not nome:
        print("nome inválido", file=sys.stderr)
        return 2
    p = pasta(nome)
    anterior = ativa()                        # inclui a conta única sem arquivo "ativa"
    if os.path.exists(os.path.join(p, "conta.json")):
        print(f"A conta {nome} já existe em {p}. Nada foi alterado.", file=sys.stderr)
        return 1
    os.makedirs(p, exist_ok=True)
    meta = {"nome": nome, "arroba": args.arroba or "", "tipo": args.tipo,
            "persona": args.persona or "", "fuso": args.fuso}
    with open(os.path.join(p, "conta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
    voz = os.path.join(p, "voz.md")
    if not os.path.exists(voz) and os.path.exists(TEMPLATE):
        shutil.copyfile(TEMPLATE, voz)
    if args.usar:
        _gravar_ativa(nome)
    elif not _arquivo_ativa():
        _gravar_ativa(anterior or nome)       # a conta em uso continua em uso
    print(f"Conta {nome} criada em {p}")
    print("Próximo passo: preencher o voz.md dessa pasta, ou mandar três reels da conta e pedir para escrever.")
    return 0


def _arquivo_ativa():
    """True se o arquivo 'ativa' existe e aponta para uma conta que existe."""
    try:
        with open(os.path.join(base_dir(), "ativa"), encoding="utf-8") as fh:
            return fh.read().strip() in todas()
    except OSError:
        return False


def _gravar_ativa(nome):
    os.makedirs(base_dir(), exist_ok=True)
    with open(os.path.join(base_dir(), "ativa"), "w", encoding="utf-8") as fh:
        fh.write(nome + "\n")


def cmd_usar(args):
    nome = resolver(args.nome)
    if not nome:
        print(f"Conta \"{args.nome}\" não encontrada. Existentes: {', '.join(todas()) or 'nenhuma'}",
              file=sys.stderr)
        return 1
    _gravar_ativa(nome)
    print(f"Conta ativa: {nome}  ({pasta(nome)})")
    return 0


def cmd_ativa(args):
    nome = ativa()
    if not nome:
        lista = todas()
        msg = ("nenhuma conta criada" if not lista else
               f"várias contas e nenhuma ativa: {', '.join(lista)}. Pergunte ao usuário qual usar.")
        print(json.dumps({"ativa": None, "contas": lista, "mensagem": msg}, ensure_ascii=False)
              if args.json else msg)
        return 1
    m = ler_meta(nome)
    if args.json:
        print(json.dumps(dict(m, nome=nome, pasta=pasta(nome)), ensure_ascii=False))
    else:
        print(f"{nome}\t{pasta(nome)}")
    return 0


def cmd_pasta(args):
    nome = resolver(args.nome) if args.nome else ativa()
    if not nome:
        print("conta não encontrada ou nenhuma ativa", file=sys.stderr)
        return 1
    print(pasta(nome))
    return 0


def cmd_migrar(args):
    """Move voz.md, swipe.md, historico.md e plano.md soltos na base para uma conta."""
    soltos = [f for f in FILES if os.path.isfile(os.path.join(base_dir(), f))]
    if not soltos:
        print("Nada para migrar.")
        return 0
    nome = slug(args.nome)
    p = pasta(nome)
    os.makedirs(p, exist_ok=True)
    movidos = []
    for f in soltos:
        dst = os.path.join(p, f)
        if os.path.exists(dst):
            print(f"{dst} já existe; {f} ficou onde estava.", file=sys.stderr)
            continue
        shutil.move(os.path.join(base_dir(), f), dst)
        movidos.append(f)
    if not os.path.exists(os.path.join(p, "conta.json")):
        with open(os.path.join(p, "conta.json"), "w", encoding="utf-8") as fh:
            json.dump({"nome": nome, "arroba": "", "tipo": "pessoal", "persona": "", "fuso": "America/Sao_Paulo"},
                      fh, indent=2, ensure_ascii=False)
    if not _arquivo_ativa():
        _gravar_ativa(nome)
    print(f"Movidos para {p}: {', '.join(movidos) or 'nada'}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Gerencia as contas de Instagram do pacote.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("listar", help="mostra as contas")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_listar)

    s = sub.add_parser("criar", help="cria a pasta de uma conta")
    s.add_argument("nome")
    s.add_argument("--arroba", help="o @ da conta")
    s.add_argument("--tipo", choices=TIPOS, default="pessoal",
                   help="pessoal, marca, nicho (página temática ou de fã) ou persona (personagem feito com IA)")
    s.add_argument("--persona", help="nome da skill de persona que deve ser lida junto (ex.: lia-persona)")
    s.add_argument("--fuso", default="America/Sao_Paulo", help="fuso do público (padrão America/Sao_Paulo)")
    s.add_argument("--usar", action="store_true", help="já deixa esta conta ativa")
    s.set_defaults(fn=cmd_criar)

    s = sub.add_parser("usar", help="troca a conta ativa")
    s.add_argument("nome")
    s.set_defaults(fn=cmd_usar)

    s = sub.add_parser("ativa", help="mostra a conta ativa")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_ativa)

    s = sub.add_parser("pasta", help="imprime a pasta de uma conta (ou da ativa)")
    s.add_argument("nome", nargs="?")
    s.set_defaults(fn=cmd_pasta)

    s = sub.add_parser("migrar", help="move os arquivos do formato antigo para uma conta")
    s.add_argument("nome", nargs="?", default="principal")
    s.set_defaults(fn=cmd_migrar)

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
