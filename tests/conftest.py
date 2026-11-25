"""Utilitários compartilhados pelos testes.

Os scripts ficam em pastas diferentes (uma por skill) e não formam um pacote,
então são carregados pelo caminho. Cada teste que mexe em contas usa uma pasta
temporária via IG_BR_DIR, para nunca tocar no ~/.claude de quem roda.
"""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
SKILLS = RAIZ / "skills"


def carregar(rel, nome=None):
    """Importa um script de skills/ como módulo. Ex.: carregar('ig-reel/gancho.py')."""
    caminho = SKILLS / rel
    nome = nome or "t_" + caminho.stem
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(caminho.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(caminho.parent))
    return mod


def rodar(rel, *args, entrada=None, env=None):
    """Roda um script como o usuário rodaria. Devolve o CompletedProcess."""
    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8", **(env or {}))
    return subprocess.run([sys.executable, str(SKILLS / rel), *map(str, args)],
                          input=entrada, capture_output=True, text=True, encoding="utf-8",
                          env=ambiente, timeout=60)


def ler_json(rel):
    with open(SKILLS / rel, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture
def base_contas(tmp_path, monkeypatch):
    """Pasta temporária no lugar de ~/.claude/instagram-br."""
    base = tmp_path / "instagram-br"
    monkeypatch.setenv("IG_BR_DIR", str(base))
    return base


@pytest.fixture
def arquivo(tmp_path):
    """Grava um texto num arquivo temporário e devolve o caminho."""
    contador = {"n": 0}

    def _gravar(texto, nome=None):
        contador["n"] += 1
        p = tmp_path / (nome or f"entrada{contador['n']}.txt")
        p.write_text(texto, encoding="utf-8")
        return p

    return _gravar


TEXTO_HUMANO = (
    "Ontem eu tava revisando os números do mês e tomei um susto. A gente faturou R$ 4.200 a menos que em outubro.\n"
    "Não foi o algoritmo. Foi a minha preguiça de responder direct no fim de semana, porque é ali que a cliente da "
    "Mooca decide se compra ou não.\n"
    "Voltei a responder em até uma hora. Duas semanas depois, três pedidos novos.\n"
    "Tá, é pouco. Mas é o meu pouco, e eu sei de onde veio.\n"
)

TEXTO_MAQUINA = (
    "Para de rolar o feed! 🚀 No mundo acelerado de hoje, é crucial alavancar o seu Instagram — não é só sobre "
    "postar, é sobre estratégia.\n\n"
    "✅ Além disso, vale ressaltar que o algoritmo ama consistência.\n"
    "✅ Nesse sentido, uma ampla gama de criadores já descobriu esse segredo.\n"
    "✅ Portanto, o futuro é agora e a escolha é sua.\n\n"
    "Em resumo: conteúdo, constância e comunidade. Pense nisso.\n"
    "Segue para mais dicas e marca alguém que precisa ver isso! #viral #fyp #reels #instagood #explore #marketing\n"
)
