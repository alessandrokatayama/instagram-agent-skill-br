"""Nota do gancho (ig-reel/gancho.py) e as 26 fórmulas (ig-reel/ganchos.json)."""

import json
import re

import pytest

from conftest import carregar, ler_json, rodar

gancho = carregar("ig-reel/gancho.py")
DADOS = ler_json("ig-reel/ganchos.json")


# ---------- ganchos.json ----------

def test_tem_26_formulas_com_ids_de_1_a_26():
    assert sorted(h["id"] for h in DADOS["hooks"]) == list(range(1, 27))


def test_ordem_de_classificacao_cobre_todas_uma_vez():
    assert sorted(DADOS["classify_order"]) == list(range(1, 27))


@pytest.mark.parametrize("campo", ["name", "template", "example", "on_screen", "best_for", "trap", "match"])
def test_toda_formula_tem_todos_os_campos(campo):
    for h in DADOS["hooks"]:
        assert h.get(campo, "").strip(), f"fórmula {h['id']} sem {campo}"


def test_toda_regex_compila():
    for h in DADOS["hooks"]:
        re.compile(h["match"], re.IGNORECASE)


def test_texto_de_tela_tem_no_maximo_seis_palavras():
    for h in DADOS["hooks"]:
        assert len(h["on_screen"].split()) <= 6, h["on_screen"]


def test_cada_exemplo_cai_na_propria_formula():
    """O exemplo de cada fórmula precisa ser reconhecido por ela, na ordem de classificação."""
    swipe = carregar("ig-viral/swipe.py")
    formulas = swipe.load_formulas(str(swipe.HOOKS))
    erros = []
    for h in DADOS["hooks"]:
        fid, nome = swipe.classify(h["example"], formulas)
        if fid != h["id"]:
            erros.append(f"#{h['id']} {h['name']} -> {fid} {nome}: {h['example']}")
    assert not erros, "\n".join(erros)


@pytest.mark.parametrize("frase,esperado", [
    ("Ninguém te conta que vender no Instagram é mais chato do que parece.", 3),
    ("Pare de postar todo dia.", 2),
    ("Rouba esse roteiro de três linhas.", 9),
    ("Carrossel x Reels: qual dá mais seguidor?", 17),
    ("Se você vende bolo de pote, presta atenção.", 10),
    ("Você não precisa de mil seguidores pra vender.", 20),
])
def test_frases_brasileiras_comuns_sao_reconhecidas(frase, esperado):
    swipe = carregar("ig-viral/swipe.py")
    fid, _ = swipe.classify(frase, swipe.load_formulas(str(swipe.HOOKS)))
    assert fid == esperado


# ---------- gancho.py ----------

def nota(frase):
    _, overall, veredito, flags = gancho.run(frase)
    return overall, veredito, flags


def test_gancho_forte_passa():
    overall, veredito, flags = nota("Ninguém te conta que seus primeiros 30 reels são feitos pra flopar.")
    assert veredito == "FORTE" and overall >= 70 and not flags


@pytest.mark.parametrize("frase,trecho", [
    ("Oi gente, hoje eu queria falar sobre estratégia de conteúdo", "Saudação"),
    ("Fala galera, tudo bem com vocês?", "Saudação"),
    ("Para de rolar o feed se você quer crescer", "para de rolar"),
    ("Nesse vídeo eu vou te mostrar como crescer", "Preâmbulo"),
    ("Perdi R$ 5 mil com isso #empreendedorismo", "Hashtag"),
    ("Perdi R$ 5 mil com isso 🔥", "Emoji"),
])
def test_eliminatorios(frase, trecho):
    _, veredito, flags = nota(frase)
    assert any(trecho in f for f in flags), flags
    assert veredito != "FORTE"


def test_gancho_concreto_vence_gancho_vago():
    concreto, _, _ = nota("Perdi R$ 18.000 por causa de uma cláusula no contrato.")
    vago, _, _ = nota("Algumas coisas sobre contratos que podem ajudar bastante.")
    assert concreto > vago + 20


def test_reais_e_mil_contam_como_concreto():
    for frase in ("Faturei R$ 18.000 em março.", "Faturei dezoito mil em março.", "Faturei 18 mil em março."):
        score, detalhe = gancho.check_specificity(frase)
        assert score >= 75, (frase, detalhe)


def test_inicio_de_frase_nao_conta_como_nome_proprio():
    _, detalhe = gancho.check_specificity("Proposta me tomava horas. Hoje leva pouco.")
    assert "Hoje" not in detalhe


def test_fala_com_o_espectador():
    for frase in ("Seu reel não engaja por isso.", "Cê tá errando o gancho.", "Vc não precisa disso."):
        assert gancho.check_address(frase)[0] == 100.0, frase


def test_gancho_longo_perde_ponto_de_tamanho():
    longo = " ".join(["palavra"] * 25)
    assert gancho.check_length(longo)[0] < 20


def test_cli_ranking_e_codigo_de_saida(arquivo):
    p = arquivo("Oi gente, tudo bem?\nNinguém te conta que seus primeiros 30 reels são feitos pra flopar.\n")
    r = rodar("ig-reel/gancho.py", p)
    assert r.returncode == 0, r.stderr
    assert "RANKING DE GANCHOS" in r.stdout
    assert r.stdout.index("Ninguém") < r.stdout.index("Oi gente")


def test_cli_so_ganchos_fracos_sai_com_1(arquivo):
    r = rodar("ig-reel/gancho.py", arquivo("Oi gente, tudo bem?\nBom dia pessoal\n"))
    assert r.returncode == 1


def test_cli_json():
    r = rodar("ig-reel/gancho.py", "--gancho", "Pare de postar todo dia.", "--json")
    dados = json.loads(r.stdout)
    assert set(dados["checks"]) == set(gancho.CHECKS)


def test_cli_entrada_vazia_sai_com_2(arquivo):
    assert rodar("ig-reel/gancho.py", arquivo("\n\n")).returncode == 2
