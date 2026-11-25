#!/usr/bin/env python3
"""
gancho.py - dá nota para a primeira frase de um Reel nas cinco coisas que os
ganchos fortes têm em comum, e ranqueia um lote de opções entre si.

O que isto é: cinco heurísticas locais, calculadas na sua máquina só a partir
do texto. Elas medem propriedades que ganchos que seguram atenção costumam
ter: um tamanho que se fala em menos de três segundos, algo concreto, algo em
jogo, o conteúdo na frente e não no fim, e um espectador a quem falar.

O que isto NÃO é: previsor de views. A versão original, em inglês, foi testada
em 74 ganchos reais: separou bem um gancho real de um gancho ruim de propósito
(AUC 0,83), mas mal separou os acertos de um criador dos erros do mesmo
criador (AUC 0,56, onde 0,50 é cara ou coroa). Esta adaptação para o português
ainda não foi medida num corpus brasileiro, então trate as notas como filtro de
gancho fraco, não como previsão.

Use para o que funciona: pega saudação, preâmbulo, gancho sem nada concreto e
gancho que leva cinco segundos pra falar. Não diz qual de dois ganchos bons vai
viajar, e nada que lê texto consegue, porque isso depende do seu rosto, da sua
edição, do seu áudio e de pra quem o Instagram mostra. Confie no gráfico de
retenção mais do que neste script.

Cada critério vai de 0 a 100. Quanto maior, melhor.

Uso
  python3 gancho.py ganchos.txt                 # um gancho por linha, ranqueados
  python3 gancho.py --gancho "Perdi R$ 18 mil por causa de um contrato."
  python3 gancho.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys

WORD_RE = re.compile(r"(?:R\$\s?)?[\w%'’-]+")
NUMBER_RE = re.compile(
    r"R\$\s?\d[\d.]*(?:,\d+)?(?:\s?(?:mil|k|mi|milhões|milhão|bi))?"   # dinheiro
    r"|\b\d[\d.]*(?:,\d+)?\s?"                                        # um número,
    r"(?:%|k\b|mil\b|x\b|h\b|horas?\b|min\b|minutos?\b|seg\b|segundos?\b"  # com ou sem
    r"|dias?\b|semanas?\b|mês\b|meses\b|anos?\b|reais\b)?",           # unidade
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
CAP_WORD = re.compile(r"[A-ZÀ-Ý][a-zà-ÿ]{2,}$")   # nome próprio no meio da frase
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Gancho falado diz os números por extenso. "Zero real" e "vinte mil" são tão
# concretos quanto "R$ 0" e "R$ 20.000". "Um/uma" e "primeiro" ficam de fora de
# propósito: são enchimento muito mais vezes do que são quantidade.
SPOKEN_NUMBERS = {
    "zero", "dois", "duas", "três", "tres", "quatro", "cinco", "seis", "sete",
    "oito", "nove", "dez", "onze", "doze", "quinze", "vinte", "trinta",
    "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa", "cem",
    "cento", "duzentos", "trezentos", "quinhentos", "mil", "milhão", "milhões",
    "bilhão", "dúzia", "metade", "dobro", "triplo", "dobrei", "tripliquei",
}
MONEY_WORDS = {
    "reais", "real", "conto", "contos", "pila", "pau", "centavos", "porcento",
    "faturamento", "faturei", "lucro", "salário", "aluguel", "milionário",
    "prejuízo", "boleto", "pix",
}

# Palavras que colocam algo em jogo. Gancho sem nenhuma é constatação; com uma,
# vira motivo pra continuar assistindo.
STAKES = {
    "pare", "parei", "parar", "nunca", "jamais", "errado", "errada", "erro",
    "erros", "erramos", "errei", "perdi", "perder", "perdendo", "perdeu",
    "perca", "custou", "custa", "custo", "quebrei", "quebrou", "faliu",
    "falência", "falhei", "fracasso", "fracassei", "ninguém", "ninguem", "não",
    "nao", "nem", "desisti", "desistir", "demitido", "demitida", "demiti",
    "apaguei", "apague", "apaga", "matou", "mata", "substituiu", "substitui",
    "cortei", "corta", "ganhei", "grátis", "paguei", "cobrei", "cobra",
    "contratei", "economizei", "proibido", "ilegal", "pior", "odeio", "odiava",
    "desperdicei", "golpe", "mentira", "mentiram", "verdade", "segredo",
    "escondido", "roubaram", "roubou", "antes", "até", "mas", "exceto",
    "problema", "risco", "perigo", "cuidado", "alerta", "arrependo",
    "arrependimento", "deveria", "devia", "ainda", "já", "sem", "versus", "vs",
    "multa", "prejuízo", "calote", "bloqueado", "bloqueio", "flopou", "flopar",
    "flop", "primeira", "nada", "zero", "dívida", "reembolso", "devolução",
    # verbos de virada, comuns em gancho de história, notícia e esporte
    "abandonou", "abandonar", "desistiu", "expulso", "expulsou", "proibiu",
    "obrigou", "obrigado", "morreu", "sumiu", "acabou", "fechou", "quase",
    "rebaixado", "eliminado", "virou", "perdemos", "ganhamos", "humilhou",
    "derrota", "vitória", "título", "campeão", "recorde", "último", "única",
    "proibiram", "obrigaram", "abandonaram", "tiraram", "perderam",
}

# Aberturas que gastam o primeiro segundo sem dizer nada.
WEAK_OPENERS = [
    "oi", "olá", "ola", "e aí", "e ai", "eai", "fala galera", "fala pessoal",
    "galera", "pessoal", "gente", "bom dia", "boa tarde", "boa noite", "salve",
    "então", "entao", "bom", "tipo", "basicamente", "sinceramente", "hoje",
    "seja bem", "sejam bem", "bem-vindo", "bem-vindos", "vem comigo",
    "vamos lá", "bora", "eu queria", "eu quero", "queria", "um dos", "uma das",
    "você sabia", "vocês sabiam", "vc sabia", "nesse vídeo", "neste vídeo",
    "no vídeo", "existe", "existem", "tem muita", "isso é", "é isso",
    "quando se", "como sabemos", "sabe", "vocês", "vamos falar",
]

# Imperativos que merecem a primeira posição.
IMPERATIVES = {
    "pare", "para", "rouba", "roube", "copia", "copie", "apaga", "apague",
    "testa", "teste", "assiste", "assista", "olha", "olhe", "veja", "lê",
    "leia", "salva", "salve", "usa", "use", "faz", "faça", "escreve",
    "escreva", "manda", "mande", "começa", "comece", "nunca", "sempre", "não",
    "confere", "confira", "guarda", "guarde", "esquece", "esqueça", "troca",
    "troque", "anota", "anote", "corta", "corte", "cobra", "cobre",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:para|pare|espera,? não) (?:de )?(?:rolar|passar|pula|pular)\b|^\s*não (?:passa|pula|role)\b"),
     "Abre com \"para de rolar\". Pedir atenção prova que você ainda não conquistou."),
    (re.compile(r"(?i)\b(?:n(?:ess|est)e (?:vídeo|video|reel)|no (?:vídeo|video|reel) de hoje|hoje eu vou (?:te )?(?:mostrar|ensinar|falar)|vou te (?:mostrar|ensinar) como)\b"),
     "Preâmbulo de vídeo. Apague e comece pelo resultado."),
    (re.compile(r"(?i)^\s*(?:oi|olá|ola|e a[ií]|eai|fala (?:galera|pessoal|gente)|bom dia|boa tarde|boa noite|salve|sejam? bem[- ]vind[oa]s?)\b"),
     "Saudação. Ninguém abre o feed pra ser cumprimentado."),
    (HASHTAG_RE,
     "Hashtag no gancho. Hashtag vai no fim da legenda, se for em algum lugar."),
    (EMOJI_RE,
     "Emoji no gancho. Texto de tela no tamanho de gancho tem espaço para palavra ou para emoji, não os dois."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def normalize(text):
    # "R$ 18.000" é uma palavra quando falado ("dezoito mil"), então aqui também.
    t = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text)
    return re.sub(r"R\$\s+(?=\d)", "R$", t)


def words(text):
    return WORD_RE.findall(normalize(text))


def low_tokens(text):
    return [x.lower().strip("'’") for x in words(text)]


def check_length(text):
    """O gancho precisa chegar antes do dedo mexer. Uns dois segundos."""
    n = len(words(text))
    secs = n / 2.67                      # ~160 palavras por minuto, falado
    chars = len(text.strip())
    # Alinhado com o batidas.py: o gancho cabe em ~3,5s, umas 10 palavras a 160 ppm.
    if 5 <= n <= 10:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 10) * 11)
    if chars > 65:                       # duas linhas de texto grande na tela
        score -= 12
    return clamp(score), f"{n} palavras, {chars} caracteres, ~{secs:.1f}s falado (ideal 5 a 10 palavras)"


def check_specificity(text):
    """Uma coisa concreta vale mais que três abstratas."""
    nums = [n.strip() for n in NUMBER_RE.findall(normalize(text)) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = low_tokens(text)
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marcador(es) concreto(s)" + (f": {found}" if found else
                   " - sem número, sem nome, nada verificável"))


def check_stakes(text):
    """Tensão, custo, negação. Algo que o espectador pode perder."""
    markers = sorted(set(x for x in low_tokens(text) if x in STAKES))
    if re.search(r"R\$\s?\d", text):
        markers.append("um preço")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensão" + (f": {', '.join(markers[:4])}" if markers else
                                              " - nada está em jogo nesta frase")
    return clamp(score), detail


def check_frontload(text):
    """A palavra interessante não pode estar na posição nove."""
    w = words(text)
    if not w:
        return 0.0, "vazio"
    low = [x.lower().strip("'’") for x in w]
    opener = " ".join(low[:3])
    penalty, hit_opener = 0, None
    for weak in WEAK_OPENERS:
        if opener == weak or opener.startswith(weak + " ") or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i])
                or (i and CAP_WORD.match(w[i]) and not re.search(r"[.!?]$", w[i - 1]))):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "nenhuma palavra de conteúdo na frase"
    elif payload <= 3:
        base, where = 100.0, f"conteúdo na palavra {payload + 1}"
    elif payload <= 6:
        base, where = 70.0, f"conteúdo na palavra {payload + 1}, dá pra trazer pra frente"
    else:
        base, where = 40.0, f"conteúdo na palavra {payload + 1}, tarde demais"
    detail = where + (f"; abertura fraca \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Falando com uma pessoa, ou solto no ar."""
    low = text.lower()
    w = low_tokens(text)
    if re.search(r"\b(você|voce|vc|cê|ce|seu|sua|seus|suas|te|ti|contigo|tu|teu|tua)\b", low):
        return 100.0, "fala com o espectador"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"abre com imperativo (\"{w[0]}\")"
    if re.search(r"\b(eu|meu|minha|meus|minhas|me|mim|comigo|nós|nos|nosso|nossa|a gente)\b", low):
        return 70.0, "primeira pessoa, sem espectador"
    return 35.0, "terceira pessoa, ninguém na sala"


CHECKS = ["TAMANHO", "CONCRETO", "EM JOGO", "NA FRENTE", "DIREÇÃO"]


def run(text):
    results = {
        "TAMANHO": check_length(text),
        "CONCRETO": check_specificity(text),
        "EM JOGO": check_stakes(text),
        "NA FRENTE": check_frontload(text),
        "DIREÇÃO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # A propriedade mais fraca limita o gancho: basta uma ruim pro dedo seguir.
    overall = clamp(statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15)
    verdict = "FORTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "FRACO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nNOTA DO GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  ELIMINATÓRIO  {f}", file=out)
    if verdict != "FORTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Ponto mais fraco: {weakest}. Corrija esse e rode de novo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<6} {hook}", file=out)
        print(f"        mais fraco: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        eliminatório: {f}", file=out)
    print("\nGrave o primeiro. Se o primeiro está abaixo de 50, nenhum destes é o gancho.\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota para o gancho de um Reel em cinco critérios.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo com um gancho por linha, ou -")
    ap.add_argument("--gancho", help="avalia um único gancho passado na linha de comando")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.gancho:
        lines = [args.gancho]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("nada para avaliar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return
    if len(payload) == 1:
        render_one(lines[0], *run(lines[0]))
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))
    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
