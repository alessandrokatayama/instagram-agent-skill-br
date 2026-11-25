"""Humanizador (ig-humano/humanizar.py), detector (detectar.py) e o léxico (cliches.json)."""

import json
import re

import pytest

from conftest import TEXTO_HUMANO, TEXTO_MAQUINA, carregar, ler_json, rodar

humanizar = carregar("ig-humano/humanizar.py")
detectar = carregar("ig-humano/detectar.py")
LEX = ler_json("ig-humano/cliches.json")


def limpar(texto):
    return humanizar.humanize(texto, LEX)


# ---------- cliches.json ----------

def test_lexico_sem_termo_duplicado():
    termos = [e["find"].lower() for e in LEX["words"] + LEX["phrases"]]
    assert len(termos) == len(set(termos))


def test_estruturas_compilam():
    for s in LEX["structures"]:
        re.compile(s["regex"], re.MULTILINE)


@pytest.mark.parametrize("palavra", ["fundamental", "jornada", "cenário", "incrível", "poderoso",
                                     "elevar", "transformador", "de nada", "bombar"])
def test_palavras_comuns_ficaram_fora_da_troca(palavra):
    """Trocar essas estraga frases normais ('ensino fundamental', 'Deus é poderoso')."""
    assert palavra not in {e["find"] for e in LEX["words"] + LEX["phrases"]}


@pytest.mark.parametrize("frase", ["Meu filho está no ensino fundamental.", "Deus é poderoso.",
                                   "Minha jornada de trabalho é de 8 horas.", "Isso não serve de nada.",
                                   "O cenário do vídeo foi a cozinha."])
def test_frases_normais_ficam_intactas(frase):
    texto, rel = limpar(frase)
    assert texto.strip() == frase and not rel["lexical"]


# ---------- humanizar.py ----------

def test_remove_caracteres_invisiveis():
    texto, rel = limpar("Olá​mundo aqui⁠.")
    assert texto.strip() == "Olámundo aqui." and rel["invisible"]


def test_travessao_vira_virgula():
    texto, _ = limpar("Funciona — e muito bem.")
    assert "—" not in texto and "Funciona, e muito bem." in texto


def test_aspas_curvas_viram_retas():
    texto, _ = limpar("Ele disse “sim”.")
    assert '"sim"' in texto


def test_troca_cliche_mantendo_maiuscula():
    texto, _ = limpar("Crucial para o negócio.")
    assert texto.startswith("Importante")


def test_nao_mexe_dentro_de_link():
    texto, _ = limpar("Veja em https://site.com.br/alavancar-crucial — hoje.")
    assert "https://site.com.br/alavancar-crucial" in texto


def test_apaga_vicio_do_instagram():
    texto, _ = limpar("Para de rolar o feed! Perdi R$ 5 mil numa semana.")
    assert "rolar" not in texto.lower()
    assert texto.startswith("Perdi"), texto


def test_aponta_estruturas_sem_reescrever():
    _, rel = limpar(TEXTO_MAQUINA)
    nomes = " ".join(f["name"] for f in rel["structures"])
    for esperado in ("Não é só X", "Regra de três", "Lista com emoji", "Muro de hashtags"):
        assert esperado in nomes, nomes


def test_limpeza_nao_deixa_pontuacao_orfa():
    texto, _ = limpar(TEXTO_MAQUINA)
    assert not re.search(r"(?m)^[ \t]*[,.;:!?]", texto), texto
    assert ".!" not in texto and "✅," not in texto


def test_texto_em_minusculas_continua_em_minusculas():
    texto, _ = limpar("vale ressaltar que eu escrevo assim. e gosto.")
    assert texto[0].islower()


def test_texto_limpo_nao_tem_mais_cliche():
    texto, _ = limpar(TEXTO_MAQUINA)
    _, rel = limpar(texto)
    assert not rel["lexical"]


def test_cli_arquivo_de_saida_e_relatorio(arquivo, tmp_path):
    saida = tmp_path / "limpo.txt"
    r = rodar("ig-humano/humanizar.py", arquivo(TEXTO_MAQUINA), "-o", saida, "--relatorio")
    assert r.returncode == 0 and saida.exists()
    assert "RELATÓRIO DO HUMANIZADOR" in r.stderr


# ---------- detectar.py ----------

def test_texto_humano_passa():
    _, nota, veredito = detectar.run(TEXTO_HUMANO, LEX)
    assert veredito == "PASSA", nota


def test_texto_de_maquina_e_sinalizado():
    _, nota, veredito = detectar.run(TEXTO_MAQUINA, LEX)
    assert veredito == "SINALIZADO", nota


def test_humanizar_melhora_a_nota():
    _, antes, _ = detectar.run(TEXTO_MAQUINA, LEX)
    _, depois, _ = detectar.run(limpar(TEXTO_MAQUINA)[0], LEX)
    assert depois > antes + 10


def test_marcas_de_fala_contam_como_voz():
    formal = ("Nós realizamos a análise dos dados do mês e identificamos uma redução no faturamento. "
              "A causa foi a demora no atendimento durante o fim de semana. Corrigimos o processo. "
              "Os pedidos aumentaram nas semanas seguintes de forma consistente e previsível.")
    falado = ("A gente olhou os números do mês e tá, o faturamento caiu. Foi a demora pra responder no fim de "
              "semana, né. Arrumei isso. Pra minha surpresa os pedidos voltaram rápido nas semanas seguintes.")
    assert detectar.check_voice(falado, LEX)[0] > detectar.check_voice(formal, LEX)[0]


def test_cli_comparacao(arquivo):
    r = rodar("ig-humano/detectar.py", arquivo(TEXTO_MAQUINA), arquivo(TEXTO_HUMANO), "--json")
    antes, depois = json.loads(r.stdout)
    assert depois["human_score"] > antes["human_score"]
    assert r.returncode == 0
