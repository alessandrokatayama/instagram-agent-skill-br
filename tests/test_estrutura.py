"""Coerência do pacote: as 14 skills, os arquivos que elas citam e os manifestos."""

import json
import re

import pytest

from conftest import RAIZ, SKILLS

PASTAS = sorted(p for p in SKILLS.iterdir() if p.is_dir())
NOMES = [p.name for p in PASTAS]


def frontmatter(pasta):
    texto = (pasta / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    assert m, f"{pasta.name}: SKILL.md sem frontmatter"
    return m.group(1), texto[m.end():]


def test_sao_catorze_skills():
    assert len(PASTAS) == 14


@pytest.mark.parametrize("pasta", PASTAS, ids=NOMES)
def test_frontmatter_nome_e_descricao(pasta):
    fm, _ = frontmatter(pasta)
    assert re.search(rf"^name: {re.escape(pasta.name)}$", fm, re.M)
    desc = fm.split("description:", 1)[1]
    assert len(" ".join(desc.split())) > 80
    assert "<" not in desc and ">" not in desc.replace(">-", "")


@pytest.mark.parametrize("pasta", PASTAS, ids=NOMES)
def test_toda_skill_segue_a_regra_de_contas(pasta):
    _, corpo = frontmatter(pasta)
    if pasta.name != "ig-contas":
        assert "## Qual conta" in corpo


@pytest.mark.parametrize("pasta", PASTAS, ids=NOMES)
def test_scripts_e_dados_citados_existem(pasta):
    _, corpo = frontmatter(pasta)
    for arq in set(re.findall(r"\b([a-z_]+\.(?:py|json))\b", corpo)):
        if arq in ("conta.json", "canal.json"):      # arquivos que a skill manda criar
            continue
        achou = list(SKILLS.glob(f"*/{arq}"))
        assert achou, f"{pasta.name} cita {arq}, que não existe"


@pytest.mark.parametrize("pasta", PASTAS, ids=NOMES)
def test_comandos_citados_existem(pasta):
    _, corpo = frontmatter(pasta)
    for cmd in set(re.findall(r"`/(ig-[a-z]+)`", corpo)):
        assert cmd in NOMES, f"{pasta.name} cita /{cmd}, que não existe"


def test_nenhum_resto_do_pacote_original():
    proibidos = re.compile(r"hookscore|beats\.py|slop\.json|caption\.py|humanize\.py\b|detect\.py\b|"
                           r"rubric\.json|hooks\.json|voice\.md|/ig-(?:human|caption|carousel|profile|plan|"
                           r"comment|reply|repurpose|audit)\b|\.claude/instagram/")
    for arq in list(SKILLS.rglob("*.md")) + list(SKILLS.rglob("*.py")) + [RAIZ / "README.md"]:
        texto = arq.read_text(encoding="utf-8")
        if arq.name == "README.md":
            texto = re.sub(r"\(https://github\.com/Jakeschincariol[^)]*\)", "", texto)
        assert not proibidos.search(texto), f"{arq}: {proibidos.search(texto).group(0)}"


@pytest.mark.parametrize("arq", [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"])
def test_manifestos(arq):
    dados = json.loads((RAIZ / arq).read_text(encoding="utf-8"))
    nome = dados.get("name") if arq.endswith("plugin.json") else dados["plugins"][0]["name"]
    assert nome == "instagram-agent-br"


def test_licenca_mantem_os_dois_creditos():
    texto = (RAIZ / "LICENSE").read_text(encoding="utf-8")
    assert "Jake Schincariol" in texto and "Alessandro Katayama" in texto


def test_readme_lista_todas_as_skills():
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for nome in NOMES:
        assert f"`/{nome}`" in readme, nome
