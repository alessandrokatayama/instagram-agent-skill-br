"""Revisão de legenda (ig-legenda/legenda.py)."""

import json

import pytest

from conftest import carregar, rodar

legenda = carregar("ig-legenda/legenda.py")

BOA = (
    "Perdi R$ 18 mil por causa de uma cláusula que faltou no contrato.\n\n"
    "A cláusula que eu uso hoje em toda proposta comercial: pagamento na entrega.\n\n"
    "Comenta CONTRATO que eu te mando o texto completo no direct.\n\n"
    "#freelancer #contratos"
)


def status(texto, nome, **kw):
    a = legenda.analyse(texto, **kw)
    achados = [c for c in a["checks"] if c["check"] == nome]
    return achados[0]["status"] if achados else None


def test_legenda_boa_fica_pronta():
    a = legenda.analyse(BOA)
    assert a["verdict"] == "PRONTA", a["checks"]


def test_mostra_so_os_125_primeiros_caracteres():
    a = legenda.analyse("x" * 300)
    assert len(a["visible"]) == 125 and a["truncated"]


def test_mais_de_cinco_hashtags_e_erro():
    texto = "Linha um com R$ 10.\n\n#a #b #c #d #e #f"
    assert status(texto, "HASHTAGS") == "ERRO"


def test_cinco_hashtags_e_o_limite():
    assert status("Linha um com R$ 10.\n\n#a #b #c #d #e", "HASHTAGS") == "OK"


def test_hashtag_generica_e_apontada():
    assert status("Linha um com R$ 10.\n\n#viral #reelsbrasil", "HASHTAGS") == "ATENÇÃO"


def test_comecar_com_hashtag_e_erro():
    assert status("#publi produto novo", "1ª LINHA") == "ERRO"


def test_publi_escondida_depois_do_corte_e_erro():
    texto = "Testei a air fryer por 30 dias. " + "Detalhe. " * 20 + "\n\n#publi"
    assert status(texto, "PUBLICIDADE") == "ERRO"


@pytest.mark.parametrize("inicio", ["#publi Testei a air fryer.", "Publicidade: testei a air fryer.",
                                    "Parceria paga com a loja X. Testei."])
def test_publi_na_primeira_linha_passa(inicio):
    assert status(inicio + " " + "Detalhe. " * 20, "PUBLICIDADE") == "OK"


def test_link_de_afiliado_tambem_e_publicidade():
    texto = "Achadinho de cozinha que eu uso todo dia. " + "Detalhe. " * 20 + " Link de afiliado na bio."
    assert status(texto, "PUBLICIDADE") == "ERRO"


def test_sem_publi_nao_cria_o_criterio():
    assert status(BOA, "PUBLICIDADE") is None


def test_hashtag_com_acento_e_avisada():
    assert status("Linha um com R$ 10.\n\n#promoção", "ACENTO TAGS") == "ATENÇÃO"


@pytest.mark.parametrize("link", ["https://loja.com.br/x", "wa.me/5511999999999", "minhaloja.com.br"])
def test_link_na_legenda_e_avisado(link):
    assert status(f"Compra aqui: {link}", "LINKS") == "ATENÇÃO"


@pytest.mark.parametrize("pedido,nome", [
    ("Comenta CONTRATO que eu te mando.", "comentar uma palavra"),
    ("Me chama no direct.", "chamar no direct"),
    ("Salva esse post.", "salvar"),
    ("Link na bio.", "link na bio"),
    ("Chama no zap.", "chamar no WhatsApp"),
])
def test_reconhece_pedidos_em_portugues(pedido, nome):
    assert nome in legenda.analyse(pedido)["asks"]


def test_dois_pedidos_e_atencao():
    assert status("Salva esse post e me segue pra mais.", "UM PEDIDO") == "ATENÇÃO"


def test_busca_ignora_acento():
    texto = "Como montar um orçamento de festa sem susto."
    assert status(texto, "BUSCA", keywords=["orcamento de festa"]) == "OK"


def test_busca_faltando():
    assert status(BOA, "BUSCA", keywords=["proposta comercial", "nota fiscal"]) == "ATENÇÃO"


def test_excesso_de_emoji():
    assert status("Oi 😍🔥✨💥🎉🙌", "EMOJI") == "ATENÇÃO"


def test_cli_codigos_de_saida(arquivo):
    assert rodar("ig-legenda/legenda.py", arquivo(BOA)).returncode == 0
    r = rodar("ig-legenda/legenda.py", arquivo("#a #b #c #d #e #f"), "--json")
    assert r.returncode == 1 and json.loads(r.stdout)["verdict"] == "CORRIGIR"
