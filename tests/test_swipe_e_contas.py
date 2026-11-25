"""Swipe file (ig-viral/swipe.py) e contas (ig-contas/contas.py)."""

import json

import pytest

from conftest import carregar, rodar

swipe = carregar("ig-viral/swipe.py")

TSV = (
    "conta\tseguidores\tmediana\tviews\tgancho\n"
    "@confeitaria_ana\t4.800\t1.200\t96 mil\tNinguém te conta que bolo de pote dá mais lucro\n"
    "@chef_rui\t2,1 mi\t180 mil\t240.000\tOi gente, hoje eu vou mostrar minha rotina\n"
    "@doces_bia\t12k\t3.000\t41.000\tPerdi R$ 900 numa encomenda por causa de uma palavra\n"
)


# ---------- swipe.py ----------

@pytest.mark.parametrize("texto,valor", [
    ("400.000", 400000), ("48 mil", 48000), ("48mil", 48000), ("412k", 412000),
    ("1,2 mi", 1200000), ("1.5k", 1500), ("2,1 mi", 2100000), ("", None), ("—", None),
])
def test_le_numeros_como_o_instagram_mostra(texto, valor):
    assert swipe.to_int(texto) == valor


def test_cabecalho_em_portugues_e_ranking_por_multiplo(arquivo):
    a = swipe.analyse(swipe.read_rows(str(arquivo(TSV))), swipe.load_formulas(str(swipe.HOOKS)))
    contas = [r["account"] for r in a["reels"]]
    assert contas[0] == "@confeitaria_ana"          # 80x a própria mediana
    assert contas[-1] == "@chef_rui"                # 240 mil views, mas 1,3x
    assert a["baseline"] == "mediana da conta"


def test_sem_mediana_usa_seguidores(arquivo):
    tsv = "conta\tseguidores\tviews\tgancho\n@a\t1000\t5000\tPare de postar todo dia\n"
    a = swipe.analyse(swipe.read_rows(str(arquivo(tsv))), None)
    assert a["baseline"] == "número de seguidores" and a["reels"][0]["outlier"] == 5.0


def test_linha_sem_gancho_ou_views_e_ignorada(arquivo):
    tsv = "conta\tviews\tgancho\n@a\t\tsem views\n@b\t100\t\n@c\t100\tok\n"
    assert [r["account"] for r in swipe.read_rows(str(arquivo(tsv)))] == ["@c"]


def test_cli_sem_linhas_sai_com_2(arquivo):
    assert rodar("ig-viral/swipe.py", arquivo("conta\tviews\tgancho\n")).returncode == 2


def test_cli_grava_markdown(arquivo, tmp_path):
    saida = tmp_path / "swipe.md"
    r = rodar("ig-viral/swipe.py", arquivo(TSV), "--saida", saida)
    assert r.returncode == 0 and saida.read_text(encoding="utf-8").startswith("# Swipe file")


# ---------- contas.py ----------

def contas(*args, base):
    return rodar("ig-contas/contas.py", *args, env={"IG_BR_DIR": str(base)})


def test_slug():
    c = carregar("ig-contas/contas.py")
    assert c.slug("Café Aurora") == "cafe-aurora"
    assert c.slug("@lia.criadora") == "lia-criadora"


def test_criar_copia_o_modelo_de_voz(base_contas):
    r = contas("criar", "Lia", "--arroba", "@lia.criadora", "--tipo", "persona",
               "--persona", "lia-persona", base=base_contas)
    assert r.returncode == 0, r.stderr
    pasta = base_contas / "contas" / "lia"
    assert (pasta / "voz.md").read_text(encoding="utf-8").startswith("# voz.md")
    meta = json.loads((pasta / "conta.json").read_text(encoding="utf-8"))
    assert meta == {"nome": "lia", "arroba": "@lia.criadora", "tipo": "persona",
                    "persona": "lia-persona", "fuso": "America/Sao_Paulo"}


def test_primeira_conta_vira_ativa_e_a_segunda_nao(base_contas):
    contas("criar", "a", base=base_contas)
    contas("criar", "b", base=base_contas)
    assert contas("ativa", base=base_contas).stdout.startswith("a\t")


def test_criar_com_usar_troca_a_ativa(base_contas):
    contas("criar", "a", base=base_contas)
    contas("criar", "b", "--usar", base=base_contas)
    assert contas("ativa", base=base_contas).stdout.startswith("b\t")


def test_criar_conta_repetida_nao_altera_nada(base_contas):
    contas("criar", "a", "--arroba", "@original", base=base_contas)
    r = contas("criar", "a", "--arroba", "@outro", base=base_contas)
    assert r.returncode == 1
    meta = json.loads((base_contas / "contas" / "a" / "conta.json").read_text(encoding="utf-8"))
    assert meta["arroba"] == "@original"


def test_usar_pelo_arroba(base_contas):
    contas("criar", "lia", "--arroba", "@lia.criadora", base=base_contas)
    contas("criar", "outra", base=base_contas)
    assert contas("usar", "@lia.criadora", base=base_contas).returncode == 0
    dados = json.loads(contas("ativa", "--json", base=base_contas).stdout)
    assert dados["nome"] == "lia"


def test_usar_conta_que_nao_existe(base_contas):
    contas("criar", "a", base=base_contas)
    assert contas("usar", "zzz", base=base_contas).returncode == 1


def test_varias_contas_sem_ativa_pede_para_perguntar(base_contas):
    contas("criar", "a", base=base_contas)
    contas("criar", "b", base=base_contas)
    (base_contas / "ativa").unlink()
    r = contas("ativa", base=base_contas)
    assert r.returncode == 1 and "Pergunte" in r.stdout


def test_nenhuma_conta(base_contas):
    assert contas("ativa", base=base_contas).returncode == 1
    assert contas("listar", base=base_contas).returncode == 1


def test_migrar_move_sem_apagar(base_contas):
    base_contas.mkdir(parents=True)
    (base_contas / "voz.md").write_text("voz antiga", encoding="utf-8")
    (base_contas / "historico.md").write_text("histórico antigo", encoding="utf-8")
    assert contas("migrar", "pessoal", base=base_contas).returncode == 0
    pasta = base_contas / "contas" / "pessoal"
    assert (pasta / "voz.md").read_text(encoding="utf-8") == "voz antiga"
    assert (pasta / "historico.md").exists() and not (base_contas / "voz.md").exists()
    assert contas("ativa", base=base_contas).stdout.startswith("pessoal\t")


def test_migrar_nao_sobrescreve(base_contas):
    contas("criar", "pessoal", base=base_contas)
    (base_contas / "voz.md").write_text("voz antiga", encoding="utf-8")
    contas("migrar", "pessoal", base=base_contas)
    assert (base_contas / "voz.md").exists(), "o arquivo antigo deveria continuar onde estava"
    assert (base_contas / "contas" / "pessoal" / "voz.md").read_text(encoding="utf-8").startswith("# voz.md")


def test_migrar_mantem_a_conta_em_uso(base_contas):
    contas("criar", "principal", base=base_contas)
    (base_contas / "ativa").unlink()                  # conta única, ativa implícita
    contas("criar", "outra", base=base_contas)
    assert contas("ativa", base=base_contas).stdout.startswith("principal\t")


def test_swipe_grava_na_pasta_da_conta(base_contas, arquivo):
    contas("criar", "lia", "--arroba", "@lia.criadora", base=base_contas)
    r = rodar("ig-viral/swipe.py", arquivo(TSV), "--conta", "@lia.criadora", env={"IG_BR_DIR": str(base_contas)})
    assert r.returncode == 0, r.stderr
    assert (base_contas / "contas" / "lia" / "swipe.md").exists()


def test_swipe_conta_inexistente(base_contas, arquivo):
    r = rodar("ig-viral/swipe.py", arquivo(TSV), "--conta", "nada", env={"IG_BR_DIR": str(base_contas)})
    assert r.returncode == 2
