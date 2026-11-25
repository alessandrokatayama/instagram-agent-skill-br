"""Mapa de batidas (ig-reel/batidas.py)."""

import json

from conftest import carregar, rodar

batidas = carregar("ig-reel/batidas.py")

ROTEIRO = (
    "Perdi R$ 18.000 por causa de uma cláusula.\n"
    "Aprovação não é pagamento.\n"
    "Cláusula 4. Pagamento na entrega.\n"
    "Essa troca vale R$ 18.000 pra mim.\n"
)


def test_tempos_somam_o_total():
    a = batidas.analyse(ROTEIRO)
    assert abs(sum(b["dur"] for b in a["beats"]) - a["total_seconds"]) < 0.05


def test_primeira_batida_e_gancho_e_ultima_e_cta():
    a = batidas.analyse(ROTEIRO)
    assert a["beats"][0]["label"].startswith("GANCHO")
    assert a["beats"][-1]["label"].endswith("CTA")


def test_valor_em_reais_e_uma_palavra():
    assert batidas.words("Paguei R$ 18.000 nisso") == ["Paguei", "R$18000", "nisso"]


def test_detecta_loop_com_o_gancho():
    notas = " ".join(batidas.analyse(ROTEIRO)["notes"])
    assert "Loop" in notas and "18.000" in notas


def test_sem_loop_avisa():
    a = batidas.analyse("Perdi um cliente ontem.\nFoi por causa de um prazo.\nAgora eu cobro antes.\n")
    assert any("Sem loop" in n for n in a["notes"])


def test_gancho_longo_e_batida_longa_sao_apontados():
    longo = "Essa é a história de como eu perdi dinheiro com um cliente que parecia ótimo no começo\n"
    a = batidas.analyse(longo + "Fim.\n")
    assert a["beats"][0]["flags"], "gancho acima de 3s deveria ser apontado"


def test_sequencia_sem_nada_concreto():
    texto = "Isso aconteceu comigo.\nFoi bem difícil.\nAprendi bastante.\nHoje faço diferente.\n"
    assert any("nada concreto" in n for n in batidas.analyse(texto)["notes"])


def test_alvo_acima_e_abaixo():
    curto = batidas.analyse(ROTEIRO, target=60)
    assert any("abaixo do alvo" in n for n in curto["notes"])
    longo = batidas.analyse(ROTEIRO, target=3)
    assert any("acima do alvo" in n for n in longo["notes"])


def test_ritmo_mais_rapido_encurta_o_video():
    assert batidas.analyse(ROTEIRO, ppm=200)["total_seconds"] < batidas.analyse(ROTEIRO, ppm=140)["total_seconds"]


def test_cli_json_e_vazio(arquivo):
    r = rodar("ig-reel/batidas.py", arquivo(ROTEIRO), "--alvo", "20", "--json")
    assert json.loads(r.stdout)["target"] == 20
    assert rodar("ig-reel/batidas.py", arquivo("\n")).returncode == 2
