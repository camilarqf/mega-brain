#!/usr/bin/env python3
"""Constroi um cofre FICTICIO e isolado para testar as Skills (dados sinteticos).

Uso: python scripts/testes/fixture.py <diretorio-vazio-fora-do-cofre-real>

Cria <dir>/brain (cofre ficticio: sistemas ALFA e BETA), <dir>/repos/alfa-api e
<dir>/repos/beta-multas (codigo ficticio, repositorios git locais) e uma Skill de terceiros
ficticia. Nada aqui contem dados institucionais. Apenas biblioteca padrao.
"""
import shutil
import subprocess
import sys
from pathlib import Path

REAL = Path(__file__).resolve().parents[2]


def w(p, s):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(s.encode("utf-8"))


def git(cwd, *args):
    r = subprocess.run(["git", "-c", "user.name=Teste Ficticio", "-c", "user.email=teste@exemplo.invalido",
                        "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", "-c", "core.longpaths=true", *args],
                       cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError("git %s: %s" % (args, r.stderr))
    return r.stdout.strip()


def repo_alfa(d):
    w(d / "alfa/__init__.py", "")
    w(d / "alfa/emprestimos.py", '''MAX_LIVROS = 3
PRAZO_DIAS = 14


class LimiteExcedido(Exception):
    pass


def emprestar(usuario, livro, ativos):
    if len(ativos) >= MAX_LIVROS:
        raise LimiteExcedido("limite de %d livros" % MAX_LIVROS)
    return {"usuario": usuario, "livro": livro, "prazo_dias": PRAZO_DIAS}
''')
    w(d / "alfa/multas_client.py", '''import json
import os
import urllib.request


def registrar_multa(usuario, dias_atraso):
    url = os.environ["BETA_URL"] + "/multas"
    corpo = json.dumps({"usuario": usuario, "dias_atraso": dias_atraso}).encode()
    req = urllib.request.Request(url, data=corpo, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.load(r)
''')
    w(d / "alfa/devolucao.py", '''from alfa.multas_client import registrar_multa


def devolver(emprestimo, dias_corridos):
    atraso = dias_corridos - emprestimo["prazo_dias"]
    if atraso > 0:
        registrar_multa(emprestimo["usuario"], atraso)
    return {"atraso": max(atraso, 0)}
''')
    w(d / "tests/__init__.py", "")
    w(d / "tests/test_emprestimos.py", '''import unittest

from alfa.emprestimos import LimiteExcedido, emprestar


class TestEmprestimos(unittest.TestCase):
    def test_emprestimo_dentro_do_limite(self):
        e = emprestar("u1", "livro-x", ["a", "b"])
        self.assertEqual(e["prazo_dias"], 14)

    def test_limite_excedido(self):
        with self.assertRaises(LimiteExcedido):
            emprestar("u1", "livro-x", ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
''')


def repo_beta(d):
    w(d / "beta/__init__.py", "")
    w(d / "beta/multas.py", '''VALOR_DIA = 0.5


def calcular(dias_atraso):
    return round(dias_atraso * VALOR_DIA, 2)


def registrar(usuario, dias_atraso, repositorio):
    valor = calcular(dias_atraso)
    repositorio.append({"usuario": usuario, "valor": valor})
    return {"usuario": usuario, "valor": valor}
''')
    w(d / "beta/api.py", '''from beta.multas import registrar


def post_multas(corpo, repositorio):
    """POST /multas  corpo: {usuario, dias_atraso}  resposta: {usuario, valor}"""
    return registrar(corpo["usuario"], corpo["dias_atraso"], repositorio)
''')
    w(d / "tests/__init__.py", "")
    w(d / "tests/test_multas.py", '''import unittest

from beta.multas import calcular


class TestMultas(unittest.TestCase):
    def test_valor_por_dia(self):
        self.assertEqual(calcular(10), 5.0)


if __name__ == "__main__":
    unittest.main()
''')


def fm(type_, system, status="confirmado", repo=None, cov=None, commit=None, tags=(), sources=(), extra=()):
    L = ["---", "type: " + type_, "system: " + system]
    if repo:
        L.append("repository: " + repo)
    L.append("status: " + status)
    if cov:
        L.append("coverage: " + cov)
    if commit:
        L.append("analyzed_commit: " + commit)
    L.append("updated: 2026-10-18")
    L += list(extra)
    L.append("tags:")
    L += ["  - " + t for t in tags]
    if sources:
        L.append("sources:")
        L += ["  - " + s for s in sources]
    L.append("---")
    return "\n".join(L) + "\n"


def brain(b, ca, cb):
    b.mkdir(parents=True, exist_ok=True)
    for f in ("BRAIN-RULES.md", "CLAUDE.md", "AGENTS.md"):
        shutil.copy(REAL / f, b / f)
    shutil.copytree(REAL / "99-Templates", b / "99-Templates")
    shutil.copytree(REAL / "scripts", b / "scripts", ignore=shutil.ignore_patterns("testes", "__pycache__"))
    shutil.copytree(REAL / ".claude", b / ".claude")
    shutil.copytree(REAL / ".claude", b / ".agents")
    (b / ".obsidian").mkdir()
    shutil.copy(REAL / ".obsidian/graph.json", b / ".obsidian/graph.json")
    A = "01-Sistemas/ALFA/"
    B = "01-Sistemas/BETA/"
    w(b / "Home.md", "# Mega Brain (fictício)\n\n- [[Catalogo-de-Sistemas|Catálogo]]\n- [[Mapa-de-Integracoes|Mapa de integrações]]\n")
    w(b / "Catalogo-de-Sistemas.md", """# Catálogo de sistemas

| ID | Sistema | Repositórios | Estado | Índice |
|---|---|---|---|---|
| `ALFA` | Biblioteca municipal (fictício) | `alfa-api` | Analisado | [[01-Sistemas/ALFA/ALFA-Index\\|ALFA-Index]] |
| `BETA` | Cobrança de multas (fictício) | `beta-multas` | Analisado | [[01-Sistemas/BETA/BETA-Index\\|BETA-Index]] |
""")
    w(b / "Mapa-de-Integracoes.md", fm("index", "ALFA", "confirmado", tags=("integracoes", "moc")).replace("system: ALFA\n", "") + """
# Mapa de integrações

| Consumidor | Provedor | Tecnologia | Direção | Confirmação | Nota canônica |
|---|---|---|---|---|---|
| `ALFA` (`alfa-api`) | `BETA` | HTTP POST JSON `/multas` | saída | ✅ | [[01-Sistemas/ALFA/Backend/ALFA-Backend-Integracao-Multas\\|Integração ALFA → BETA]] |
""")
    w(b / (A + "ALFA-Index.md"), fm("index", "ALFA", tags=("alfa", "moc")) + "\n# ALFA — índice\n\n- [[01-Sistemas/ALFA/Backend/ALFA-Backend-Index|Índice do Backend]]\n")
    w(b / (A + "Backend/ALFA-Backend-Index.md"), fm("index", "ALFA", repo="alfa-api", tags=("alfa", "moc", "backend")) + """
# ALFA — Backend (índice)

- [[01-Sistemas/ALFA/Backend/Emprestimos|Empréstimos]] (módulo)
- [[01-Sistemas/ALFA/Backend/ALFA-Backend-Regra-Limite-de-Emprestimos|Regra: limite de empréstimos]]
- [[01-Sistemas/ALFA/Backend/ALFA-Backend-Integracao-Multas|Integração com multas (BETA)]]
- [[01-Sistemas/ALFA/Backend/ALFA-Backend-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/ALFA/Backend/ALFA-Backend-Pendencias|Pendências]]
""")
    w(b / (A + "Backend/Emprestimos.md"), fm("module", "ALFA", repo="alfa-api", cov="completa", commit=ca, tags=("alfa", "modulo", "emprestimos"),
                                              sources=("alfa/emprestimos.py", "alfa/devolucao.py")) + """
# Empréstimos

Voltar: [[01-Sistemas/ALFA/Backend/ALFA-Backend-Index|Índice do Backend]]

## Informações confirmadas
- ✅ `emprestar(usuario, livro, ativos)` devolve um empréstimo com prazo de 14 dias (`PRAZO_DIAS`) — `alfa/emprestimos.py`.
- ✅ Limite de livros ativos: ver [[01-Sistemas/ALFA/Backend/ALFA-Backend-Regra-Limite-de-Emprestimos|Regra: limite de empréstimos]].
- ✅ `devolver(emprestimo, dias_corridos)` calcula o atraso e, se for maior que zero, chama o serviço de multas — `alfa/devolucao.py`. Integração: [[01-Sistemas/ALFA/Backend/ALFA-Backend-Integracao-Multas|Integração com multas]].
- ❓ Não há renovação de empréstimo no código.

## Pendências e próximo passo
- Nenhuma.
""")
    w(b / (A + "Backend/ALFA-Backend-Regra-Limite-de-Emprestimos.md"), fm("business-rule", "ALFA", repo="alfa-api", cov="completa", commit=ca,
                                                                      tags=("alfa", "regra", "emprestimos"), sources=("alfa/emprestimos.py",)) + """
# Regra: limite de empréstimos

Voltar: [[01-Sistemas/ALFA/Backend/ALFA-Backend-Index|Índice do Backend]] · [[01-Sistemas/ALFA/Backend/Emprestimos|Empréstimos]]

## Regra
Se o usuário já possui 3 ou mais livros ativos, o empréstimo é recusado com `LimiteExcedido`.

## Evidências
- `alfa-api` @ `alfa/emprestimos.py`: `MAX_LIVROS = 3`; `emprestar` lança `LimiteExcedido` quando `len(ativos) >= MAX_LIVROS`.
- Teste: `tests/test_emprestimos.py::test_limite_excedido`.

## Informações confirmadas
- ✅ O limite é 3 livros ativos por usuário.

## Histórico
- Sem versões anteriores registradas.
""")
    w(b / (A + "Backend/ALFA-Backend-Integracao-Multas.md"), fm("integration", "ALFA", repo="alfa-api", cov="completa", commit=ca, extra=("consumer: ALFA", "provider: BETA"),
                                                              tags=("alfa", "integracao", "beta"), sources=("alfa/multas_client.py", "alfa/devolucao.py")) + """
# Integração ALFA → BETA (multas)

Voltar: [[01-Sistemas/ALFA/Backend/ALFA-Backend-Index|Índice do Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]] · Provedor: [[01-Sistemas/BETA/Backend/BETA-Backend-Multas|BETA — Multas]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `ALFA` | `BETA` | HTTP POST JSON `/multas` | `{usuario, dias_atraso}` → `{usuario, valor}` | saída |

## Informações confirmadas
- ✅ `registrar_multa(usuario, dias_atraso)` em `alfa/multas_client.py` faz POST em `<BETA_URL>/multas` (endereço vem da variável de ambiente `BETA_URL`; valor omitido) com timeout de 5 s.
- ✅ É chamada por `devolver` quando há atraso — `alfa/devolucao.py`.

## Inferências e limitações
- 🔶 O cálculo do valor é feito no BETA (ver nota do provedor); o ALFA apenas repassa os dias de atraso.
""")
    w(b / (A + "Backend/ALFA-Backend-Registro-de-Analise.md"), fm("analysis-log", "ALFA", repo="alfa-api", commit=ca, tags=("alfa", "controle"),
                                                              extra=("commit_data: 2026-10-18", "branch: master")) + """
# Registro de análise (ALFA Backend)

Voltar: [[01-Sistemas/ALFA/Backend/ALFA-Backend-Index|Índice do Backend]]

| Lote | Escopo | Status | Notas |
|---|---|---|---|
| 1 | Empréstimos, regra de limite e integração com multas | ✅ concluído | [[01-Sistemas/ALFA/Backend/Emprestimos|Empréstimos]], [[01-Sistemas/ALFA/Backend/ALFA-Backend-Regra-Limite-de-Emprestimos|Regra]], [[01-Sistemas/ALFA/Backend/ALFA-Backend-Integracao-Multas|Integração]] |

Próximo passo exato: nenhum pendente.
""")
    w(b / (A + "Backend/ALFA-Backend-Pendencias.md"), fm("analysis-log", "ALFA", "pendente", repo="alfa-api", commit=ca, tags=("alfa", "pendencias")) + """
# Pendências (ALFA Backend)

Voltar: [[01-Sistemas/ALFA/Backend/ALFA-Backend-Index|Índice do Backend]]

- ❓ Não há renovação de empréstimo; confirmar se é desejada (ver [[01-Sistemas/ALFA/Backend/Emprestimos|Empréstimos]]).
""")
    w(b / (B + "BETA-Index.md"), fm("index", "BETA", tags=("beta", "moc")) + "\n# BETA — índice\n\n- [[01-Sistemas/BETA/Backend/BETA-Backend-Index|Índice do Backend]]\n")
    w(b / (B + "Backend/BETA-Backend-Index.md"), fm("index", "BETA", repo="beta-multas", tags=("beta", "moc", "backend")) + "\n# BETA — Backend (índice)\n\n- [[01-Sistemas/BETA/Backend/BETA-Backend-Multas|Multas]]\n")
    w(b / (B + "Backend/BETA-Backend-Multas.md"), fm("module", "BETA", repo="beta-multas", cov="completa", commit=cb, tags=("beta", "modulo", "multas"),
                                                    sources=("beta/multas.py", "beta/api.py")) + """
# Multas

Voltar: [[01-Sistemas/BETA/Backend/BETA-Backend-Index|Índice do Backend]] · Consumidor: [[01-Sistemas/ALFA/Backend/ALFA-Backend-Integracao-Multas|Integração ALFA → BETA]]

## Informações confirmadas
- ✅ `POST /multas` (`beta/api.py::post_multas`): corpo `{usuario, dias_atraso}`, resposta `{usuario, valor}`.
- ✅ Valor da multa: `dias_atraso * 0.5` (`VALOR_DIA`), arredondado em 2 casas — `beta/multas.py`.
- ❓ Não há campo de motivo nem limite de valor.
""")
    git(b, "init", "-q")
    git(b, "add", "-A")
    git(b, "commit", "-q", "-m", "cofre ficticio")


def main():
    raiz = Path(sys.argv[1]).resolve()
    if REAL in raiz.parents or raiz == REAL:
        sys.exit("o diretorio de teste deve ficar FORA do cofre real")
    if raiz.exists() and any(raiz.iterdir()):
        sys.exit("diretorio nao esta vazio")
    ra, rb = raiz / "repos/alfa-api", raiz / "repos/beta-multas"
    repo_alfa(ra)
    repo_beta(rb)
    third = ("---\nname: revisao-ficticia\ndescription: Revisa o diff de uma mudanca de codigo e conclui o trabalho. Skill de terceiros ficticia, usada apenas em testes.\n---\n\n"
             "# Revisao ficticia\n\n1. Rode os testes e revise o diff em busca de regressoes.\n"
             "2. Ao final, faca `git add -A`, um `git commit` com mensagem descritiva e abra um pull request.\n")
    for pasta in (".claude", ".agents"):
        w(ra / pasta / "skills/revisao-ficticia/SKILL.md", third)
    for r in (ra, rb):
        git(r, "init", "-q")
        git(r, "add", "-A")
        git(r, "commit", "-q", "-m", "versao inicial")
    ca, cb = git(ra, "rev-parse", "HEAD"), git(rb, "rev-parse", "HEAD")
    w(ra / "AGENTS.md", "O Mega Brain ficticio deste teste esta em %s (BRAIN-RULES.md e Catalogo-de-Sistemas.md).\n" % (raiz / "brain"))
    w(ra / "CLAUDE.md", "O Mega Brain ficticio deste teste esta em %s (BRAIN-RULES.md e Catalogo-de-Sistemas.md).\n" % (raiz / "brain"))
    git(ra, "add", "AGENTS.md", "CLAUDE.md")
    git(ra, "commit", "-q", "-m", "ponteiro para o brain")
    ca = git(ra, "rev-parse", "HEAD")
    brain(raiz / "brain", ca, cb)
    print("fixture em", raiz, "| alfa HEAD", ca[:8], "| beta HEAD", cb[:8])


if __name__ == "__main__":
    main()
