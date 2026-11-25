"""Erros achados no primeiro teste com um perfil real (nov/2026).

Cada teste aqui é um erro que já aconteceu. Se um deles falhar, o erro voltou.
"""

import pytest

from conftest import carregar, ler_json, rodar

gancho = carregar("ig-reel/gancho.py")
legenda = carregar("ig-legenda/legenda.py")
detectar = carregar("ig-humano/detectar.py")
LEX = ler_json("ig-humano/cliches.json")

LEGENDA_REAL = (
    "O adversário abandonou o campo. E foi assim que nasceu o Aurora. 💚\n\n"
    "Em 1942, um decreto obrigou o clube a mudar de nome. Seis dias depois veio a Arrancada Heroica.\n\n"
    "Você já conhecia a história da Arrancada Heroica? Conta aqui nos comentários 👇\n\n"
    "Fonte: aurorafc.com.br\n\n"
    "#AuroraFC #Aurora #Alvinegro #HistóriaDoAurora ArrancadaHeroica"
)


def status(texto, nome):
    achados = [c for c in legenda.analyse(texto)["checks"] if c["check"] == nome]
    return achados[0]["status"] if achados else None


def test_nome_proprio_no_meio_da_frase_conta_como_conteudo():
    """Antes, 'Aurora' nunca era reconhecido: a regex de nome próprio falhava em palavra solta."""
    _, detalhe = gancho.check_frontload("E foi assim que nasceu o Aurora")
    assert "nenhuma palavra de conteúdo" not in detalhe


def test_verbo_de_virada_e_tensao():
    assert gancho.check_stakes("O adversário abandonou o campo.")[0] >= 70


def test_gancho_historico_nao_e_fraco():
    _, nota, veredito, _ = gancho.run("O adversário abandonou o campo. E foi assim que nasceu o Aurora.")
    assert veredito != "FRACO", nota


def test_conta_aqui_nos_comentarios_e_pedido():
    assert status(LEGENDA_REAL, "UM PEDIDO") == "OK"


def test_fonte_nao_e_link_morto():
    assert status(LEGENDA_REAL, "LINKS") == "OK"
    assert status("Compra aqui: loja.com.br", "LINKS") == "ATENÇÃO"


def test_palavra_sem_cerquilha_na_linha_de_hashtags():
    assert status(LEGENDA_REAL, "TAG SEM #") == "ERRO"
    assert status(LEGENDA_REAL.replace(" ArrancadaHeroica", " #ArrancadaHeroica"), "TAG SEM #") is None


def test_camelcase_fora_da_linha_de_hashtags_nao_e_apontado():
    assert status("Comprei um PlayStation novo.\n\n#games #ps5", "TAG SEM #") is None


def test_aspas_curvas_do_iphone_pesam_pouco():
    texto = ("Em 1942 o clube mudou de nome e seis dias depois venceu o rival, que abandonou o campo. "
             "A frase da época virou lema: “Morreu líder, nasceu campeão”. Até hoje a torcida repete "
             "essa história em todo aniversário do clube, e ela abre a nossa série sobre o clube.")
    com_iphone = detectar.check_fingerprint(texto)[0]
    com_travessao = detectar.check_fingerprint(texto.replace("“", "— ").replace("”", " —"))[0]
    assert com_iphone > 80 and com_iphone > com_travessao


def test_tipo_nicho_existe(base_contas):
    r = rodar("ig-contas/contas.py", "criar", "historiafc", "--tipo", "nicho",
              env={"IG_BR_DIR": str(base_contas)})
    assert r.returncode == 0, r.stderr


def test_ano_nao_ganha_ponto_de_milhar():
    batidas = carregar("ig-reel/batidas.py")
    assert batidas.pretty("1942") == "1942" and batidas.pretty("18000") == "18.000"


def test_gancho_e_mapa_de_batidas_concordam_no_tamanho():
    """Antes o gancho tinha nota cheia com 13 palavras e o mapa reclamava a partir de 8."""
    batidas = carregar("ig-reel/batidas.py")
    frase = "Em 1942, proibiram o nome do seu time, ninguém avisou."   # 10 palavras
    assert gancho.check_length(frase)[0] == 100.0
    assert not batidas.analyse(frase + "\nFim.\n")["beats"][0]["flags"]


def test_verbo_no_plural_tambem_e_tensao():
    assert gancho.check_stakes("Em 1942, proibiram o nome do seu time.")[0] >= 70


def test_espaco_sem_preencher_impede_a_legenda_de_ficar_pronta():
    texto = "De 1951 a 1965, a Academia. {{seu número}}\n\nConta aqui nos comentários."
    a = legenda.analyse(texto)
    assert a["verdict"] == "CORRIGIR"
    assert any(c["check"] == "A PREENCHER" for c in a["checks"])


@pytest.mark.parametrize("pedido", [
    "Qual craque entraria no seu time de todos os tempos? 👇",
    "Onde você estava quando o seu time levantou a taça? Conta pra gente 👇",
])
def test_pergunta_com_seta_e_conta_pra_gente_sao_pedidos(pedido):
    assert "responder uma pergunta" in legenda.analyse(pedido)["asks"]


def test_pergunta_sem_seta_nem_convite_nao_vira_pedido():
    assert not legenda.analyse("Você sabia que o clube nasceu em 1914? Pois é.")["asks"]


def test_se_chama_nao_e_pedido_de_direct():
    """'que hoje se chama Nubank Parque' era lido como 'chamar no direct'."""
    assert "chamar no direct" not in legenda.analyse("O estádio hoje se chama Nubank Parque.")["asks"]


@pytest.mark.parametrize("pedido", ["Me chama no direct.", "Chama no direct que eu te explico.", "Manda um DM."])
def test_pedido_de_direct_continua_reconhecido(pedido):
    assert "chamar no direct" in legenda.analyse(pedido)["asks"]


def test_chama_no_zap_nao_conta_duas_vezes():
    assert legenda.analyse("Chama no zap.")["asks"] == ["chamar no WhatsApp"]
