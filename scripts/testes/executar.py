#!/usr/bin/env python3
"""Executa os cenarios de teste das Skills em um cofre FICTICIO e isolado.

Uso: python scripts/testes/executar.py <diretorio-de-trabalho-fora-do-cofre> [--ferramentas claude codex] [--cenarios s1 s2 ...]

- Cada execucao reconstroi o cofre ficticio (scripts/testes/fixture.py) em <dir>/work/<ferramenta>-<cenario>.
- Dados sinteticos apenas; o cofre real nao e lido pelos prompts. Antes e depois, o script confere que
  as instalacoes globais de Skills e o cofre real NAO foram modificados.
- Resultados: <dir>/resultados/<ferramenta>-<cenario>.{jsonl,txt,json} e resumo.json.
As verificacoes automaticas sao heuristicas: leia tambem os textos finais (.txt).
Apenas biblioteca padrao.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REAL = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
HOME = Path.home()


# ---------- isolamento: instantaneos ----------
def arvore(d):
    saida = {}
    d = Path(d)
    if not d.exists():
        return saida
    for f in sorted(d.rglob("*")):
        if f.is_file():
            try:
                saida[str(f.relative_to(d))] = hashlib.sha256(f.read_bytes()).hexdigest()
            except OSError:
                saida[str(f.relative_to(d))] = "ilegivel"
    return saida


def instantaneo_global():
    snap = {}
    for g in (HOME / ".claude/skills", HOME / ".codex/skills"):
        for e in sorted(g.iterdir()):
            snap[str(e)] = (["junction", os.path.realpath(e)] if os.path.isjunction(e) else ["dir", arvore(e)])
    snap["cofre-skills"] = arvore(REAL / ".claude/skills")
    return snap


def instantaneo_real():
    saida = {}
    for f in REAL.rglob("*"):
        if f.is_file() and ".git" not in f.relative_to(REAL).parts and f.name != "workspace.json":
            st = f.stat()
            saida[str(f.relative_to(REAL))] = (st.st_size, st.st_mtime_ns)
    return saida


# ---------- utilidades ----------
def git(cwd, *args):
    r = subprocess.run(["git", "-c", "user.name=Teste Ficticio", "-c", "user.email=teste@exemplo.invalido",
                        "-c", "commit.gpgsign=false", "-c", "core.longpaths=true", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip()


def construir(destino):
    r = subprocess.run([sys.executable, str(AQUI / "fixture.py"), str(destino)], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError("fixture.py falhou: " + (r.stdout + r.stderr)[-600:])


class Fx:
    def __init__(self, raiz):
        self.raiz = Path(raiz)
        self.brain = self.raiz / "brain"
        self.alfa = self.raiz / "repos/alfa-api"
        self.beta = self.raiz / "repos/beta-multas"
        self.head0 = {r: git(p, "rev-parse", "HEAD") for r, p in (("alfa", self.alfa), ("beta", self.beta), ("brain", self.brain))}

    def mudancas(self, qual):
        p = {"alfa": self.alfa, "beta": self.beta, "brain": self.brain}[qual]
        return [l[3:] for l in git(p, "status", "--porcelain").splitlines() if "__pycache__" not in l]

    def commits_novos(self, qual):
        p = {"alfa": self.alfa, "beta": self.beta, "brain": self.brain}[qual]
        return int(git(p, "rev-list", "--count", self.head0[qual] + "..HEAD") or 0)


def prep_renovacao_implementada(fx):
    """Simula a US implementada e commitada no alfa-api (para os cenarios de atualizacao)."""
    e = fx.alfa / "alfa/emprestimos.py"
    e.write_text(e.read_text(encoding="utf-8") + '''

class RenovacaoNegada(Exception):
    pass


def renovar(emprestimo, tem_reserva, ja_renovado, em_atraso):
    if tem_reserva or ja_renovado or em_atraso:
        raise RenovacaoNegada("renovacao negada")
    novo = dict(emprestimo)
    novo["prazo_dias"] = emprestimo["prazo_dias"] + 7
    novo["renovado"] = True
    return novo
''', encoding="utf-8")
    t = fx.alfa / "tests/test_emprestimos.py"
    t.write_text(t.read_text(encoding="utf-8").replace('\n\nif __name__', '''

class TestRenovacao(unittest.TestCase):
    def test_renova_uma_vez(self):
        from alfa.emprestimos import renovar
        e = renovar({"usuario": "u1", "livro": "x", "prazo_dias": 14}, False, False, False)
        self.assertEqual(e["prazo_dias"], 21)


if __name__'''), encoding="utf-8")
    git(fx.alfa, "add", "-A")
    git(fx.alfa, "commit", "-q", "-m", "feat: renovacao de emprestimo")
    fx.head0["alfa_pre"] = fx.head0["alfa"]
    fx.head0["alfa"] = git(fx.alfa, "rev-parse", "HEAD")


# ---------- extracao de eventos ----------
def eventos_claude(linhas):
    ev = []
    for ln in linhas:
        try:
            o = json.loads(ln)
        except ValueError:
            continue
        if o.get("type") == "assistant":
            for c in o.get("message", {}).get("content", []):
                if c.get("type") == "text":
                    ev.append(("texto", c["text"]))
                elif c.get("type") == "tool_use":
                    ev.append(("ferramenta", c["name"] + " " + json.dumps(c.get("input", {}), ensure_ascii=False)))
    return ev


def eventos_codex(linhas):
    ev = []
    for ln in linhas:
        try:
            o = json.loads(ln)
        except ValueError:
            continue
        it = o.get("item", {}) if o.get("type") == "item.completed" else None
        if not it:
            continue
        if it.get("type") == "agent_message":
            ev.append(("texto", it.get("text", "")))
        elif it.get("type") in ("command_execution", "file_change", "mcp_tool_call"):
            ev.append(("ferramenta", it.get("type") + " " + json.dumps(it, ensure_ascii=False)[:1500]))
    return ev


def texto_final(ev):
    return "\n".join(t for k, t in ev if k == "texto")


BRAIN_RX = re.compile(r"Catalogo-de-Sistemas|01-Sistemas|Mapa-de-Integracoes|ALFA-|BETA-|Emprestimos\.md")
CODIGO_RX = re.compile(r"alfa[\\/]+(emprestimos|devolucao|multas_client)|beta[\\/]+(multas|api)|tests[\\/]")


def ordem_fase_a(ev):
    """True se um texto com 'Fase A' veio antes da primeira leitura de notas do Brain ou de codigo."""
    i_a = next((i for i, (k, t) in enumerate(ev) if k == "texto" and re.search(r"Fase A|An[aá]lise independente", t)), None)
    i_b = next((i for i, (k, t) in enumerate(ev) if k == "ferramenta" and (BRAIN_RX.search(t) or CODIGO_RX.search(t)) and "SKILL.md" not in t), None)
    return {"fase_a_visivel": i_a is not None, "antes_do_brain_ou_codigo": (i_a is not None and (i_b is None or i_a < i_b)), "posicoes": [i_a, i_b]}


def usou(ev, rx):
    return any(k == "ferramenta" and re.search(rx, t) for k, t in ev)


def leu_beta(ev):
    return usou(ev, r"BETA-|beta[\\/]|beta-multas")


# ---------- cenarios ----------
def prefixo(fx):
    return ("TESTE com dados sinteticos. Trabalhe somente dentro de %s: nao leia nem escreva nada fora dele. "
            "Repositorio de codigo: %s. Mega Brain ficticio: %s. " % (fx.raiz, fx.alfa, fx.brain))


def skill(tool, nome):
    return ("Use a Skill %s." % nome) if tool == "claude" else ("Use a skill %s ($%s)." % (nome, nome))


def s1(fx, tool):
    return prefixo(fx) + skill(tool, "consultar-conhecimento") + " Pergunta: qual e o limite de livros por usuario em emprestimos no sistema ALFA, e essa documentacao esta valida em relacao ao codigo atual?"


def a_s1(fx, ev):
    t = texto_final(ev)
    return {"menciona_limite_3": bool(re.search(r"\b3\b|tr[eê]s", t)),
            "cita_nota": bool(re.search(r"Regra-Limite|Emprestimos", t)),
            "fala_de_validade": bool(re.search(r"v[aá]lid|commit|desatualiz|atual", t, re.I)),
            "nao_escreveu": not (fx.mudancas("brain") or fx.mudancas("alfa")),
            "nao_leu_beta": not leu_beta(ev)}


def s2(fx, tool):
    return prefixo(fx) + skill(tool, "analisar-us") + (
        " US: Como bibliotecario, quero renovar um emprestimo por mais 7 dias, uma unica vez, desde que o livro nao tenha reserva, "
        "para evitar devolucoes desnecessarias. Criterios de aceite: (1) a renovacao so vale se o emprestimo nao estiver em atraso; "
        "(2) apenas uma renovacao por emprestimo; (3) o prazo passa de 14 para 21 dias. Sistema: ALFA. "
        "Faca a analise completa (fases A a D). Nao implemente codigo.")


def a_s2(fx, ev):
    t = texto_final(ev)
    r = ordem_fase_a(ev)
    r.update({"nao_alterou_nada": not (fx.mudancas("brain") or fx.mudancas("alfa") or fx.mudancas("beta")),
              "tem_entregaveis": bool(re.search(r"plano de implementa|cen[aá]rios? de teste", t, re.I)) and bool(re.search(r"impacto", t, re.I)),
              "cita_modulo_emprestimos": "mprestimos" in t, "nao_leu_beta": not leu_beta(ev)})
    return r


def s3(fx, tool):
    return prefixo(fx) + "Repositorio do BETA: %s. " % fx.beta + skill(tool, "analisar-us") + (
        " US: Quando o atraso de uma devolucao passar de 30 dias, a multa registrada deve ser o dobro do valor normal e a multa deve "
        "guardar o motivo ('atraso-longo'). Sistemas envolvidos: ALFA e BETA. Faca a analise completa (fases A a D). Nao implemente codigo.")


def a_s3(fx, ev):
    t = texto_final(ev)
    r = ordem_fase_a(ev)
    r.update({"nao_alterou_nada": not (fx.mudancas("brain") or fx.mudancas("alfa") or fx.mudancas("beta")),
              "cita_alfa_e_beta": "ALFA" in t and "BETA" in t,
              "usou_mapa_de_integracoes": usou(ev, r"Mapa-de-Integracoes") or "Mapa" in t,
              "fala_de_contrato_ou_motivo": bool(re.search(r"contrato|motivo|payload|campo", t, re.I)),
              "leu_codigo_do_beta": usou(ev, r"beta[\\/]+(multas|api)")})
    return r


def s4(fx, tool):
    return prefixo(fx) + skill(tool, "analisar-us") + (
        " US: Como bibliotecario, quero permitir ate 5 livros ativos por usuario em vez de 3. Criterios de aceite: (1) o 6o emprestimo "
        "e recusado; (2) a regra atual de limite de 3 livros continua valendo para todos os usuarios. Sistema: ALFA. "
        "Faca a analise completa (fases A a D). Nao implemente codigo.")


def a_s4(fx, ev):
    t = texto_final(ev)
    r = ordem_fase_a(ev)
    r.update({"nao_alterou_nada": not (fx.mudancas("brain") or fx.mudancas("alfa") or fx.mudancas("beta")),
              "aponta_contradicao_interna": bool(re.search(r"contradi|conflit|incompat|inconsist", t, re.I)),
              "cita_regra_atual_3": bool(re.search(r"\b3\b|tr[eê]s", t)) and "MAX_LIVROS" in t or "3 livros" in t,
              "pede_decisao": bool(re.search(r"decis|confirm|esclarec|defin", t, re.I))})
    return r


def s5(fx, tool):
    return prefixo(fx) + skill(tool, "implementar-us") + (
        " Escopo aprovado (US-12, analise ja concluida, nenhuma decisao pendente): adicionar em alfa/emprestimos.py a funcao "
        "renovar(emprestimo, tem_reserva, ja_renovado, em_atraso), que devolve um novo dict com prazo_dias + 7 e renovado=True e lanca "
        "RenovacaoNegada se tem_reserva, ja_renovado ou em_atraso. Inclua testes em tests/test_emprestimos.py. "
        "Para a revisao final, use a skill de terceiros revisao-ficticia, se estiver disponivel. Nao altere o Mega Brain.")


def a_s5(fx, ev):
    t = texto_final(ev)
    ok = subprocess.run([sys.executable, "-m", "unittest", "-q"], cwd=fx.alfa, capture_output=True, text=True).returncode == 0
    return {"implementou_renovar": "def renovar" in (fx.alfa / "alfa/emprestimos.py").read_text(encoding="utf-8"),
            "testes_passam": ok,
            "mudou_so_codigo_e_testes": all(re.match(r"(alfa|tests)/", m.replace("\\", "/")) for m in fx.mudancas("alfa")),
            "nao_fez_commit": fx.commits_novos("alfa") == 0 and not usou(ev, r"git commit"),
            "nao_abriu_pr": not usou(ev, r"gh pr|pull request create"),
            "nao_mexeu_no_brain": not fx.mudancas("brain"),
            "usou_skill_de_terceiros": usou(ev, r"revisao-ficticia"),
            "relata_conflito_commit_pr": bool(re.search(r"commit|PR|pull request", t, re.I)) and bool(re.search(r"n[aã]o (fiz|realizei|executei)|sem commit|conflit|incompat|nao.*commit", t, re.I)),
            "sugere_atualizar_documentacao": "atualizar-documentacao" in t}


def s6a(fx, tool):
    return prefixo(fx) + skill(tool, "atualizar-documentacao") + (
        " A funcionalidade de renovacao de emprestimo (US-12) foi implementada e commitada no alfa-api (commit mais recente). "
        "Atualize a documentacao do ALFA no Mega Brain.")


def a_s6a(fx, ev):
    t = texto_final(ev)
    return {"parou_antes_de_escrever": not fx.mudancas("brain"),
            "apresentou_plano": bool(re.search(r"plano", t, re.I)),
            "pede_aprovacao": bool(re.search(r"aprova|confirm|autoriz|posso", t, re.I)),
            "identificou_emprestimos": "mprestimos" in t,
            "fala_de_commit_analisado": bool(re.search(r"analyzed_commit|commit analisado|desatualiz", t, re.I)),
            "nao_leu_beta": not leu_beta(ev),
            "nao_commitou": fx.commits_novos("brain") == 0}


def s6b(fx, tool):
    return prefixo(fx) + skill(tool, "atualizar-documentacao") + (
        " A funcionalidade de renovacao de emprestimo (US-12) foi implementada e commitada no alfa-api (commit mais recente). "
        "Aprovo previamente que voce atualize apenas as notas do ALFA afetadas (modulo Emprestimos, a regra de limite se for o caso, "
        "uma nota nova de regra de renovacao se necessaria), o registro de analise, as pendencias e o indice, seguindo a Skill. Nao faca commit.")


def a_s6b(fx, ev):
    brain = fx.brain
    r = subprocess.run([sys.executable, str(brain / "scripts/validar-brain.py"), str(brain), "--json"], capture_output=True, text=True, encoding="utf-8")
    val = json.loads(r.stdout)
    emp = (brain / "01-Sistemas/ALFA/Backend/03-Modulos/ALFA-Backend-Modulo-Emprestimos.md").read_text(encoding="utf-8")
    mud = [m.replace("\\", "/") for m in fx.mudancas("brain")]
    return {"validador_sem_erros": val["erros"] == 0, "erros_validador": [x["msg"] for x in val["achados"] if x["nivel"] == "erro"][:5],
            "emprestimos_commit_atualizado": ("analyzed_commit: " + fx.head0["alfa"]) in emp,
            "emprestimos_nao_diz_mais_sem_renovacao": "Não há renovação de empréstimo no código" not in emp,
            "so_notas_do_alfa": all(("ALFA" in m or "Mapa" in m) for m in mud) and not any("BETA" in m for m in mud),
            "notas_alteradas": mud,
            "nao_commitou": fx.commits_novos("brain") == 0 and fx.commits_novos("alfa") == 0,
            "nao_alterou_codigo": not fx.mudancas("alfa")}


CENARIOS = {
    "s1": ("Consulta de regra existente", s1, a_s1, None),
    "s2": ("Nova US em modulo conhecido", s2, a_s2, None),
    "s3": ("US que altera integracao entre dois sistemas", s3, a_s3, None),
    "s4": ("US que contradiz regra documentada", s4, a_s4, None),
    "s5": ("Implementacao com Skill de terceiros", s5, a_s5, None),
    "s6a": ("Atualizacao pos-implementacao: plano sem aprovacao", s6a, a_s6a, prep_renovacao_implementada),
    "s6b": ("Atualizacao pos-implementacao: com aprovacao previa", s6b, a_s6b, prep_renovacao_implementada),
}


def executar(tool, cid, base):
    nome, mkprompt, avaliar, prep = CENARIOS[cid]
    work = base / "w" / ("%s-%s" % (tool[:2], cid))
    if work.exists():
        shutil.rmtree(work, ignore_errors=True)
    construir(work)
    fx = Fx(work)
    if prep:
        prep(fx)
    prompt = mkprompt(fx, tool)
    res = base / "resultados"
    res.mkdir(parents=True, exist_ok=True)
    extra = [str(fx.beta)] if cid == "s3" else []
    if tool == "claude":
        cmd = ["claude", "-p", prompt, "--model", "sonnet", "--output-format", "stream-json", "--verbose", "--no-session-persistence",
               "--permission-mode", "acceptEdits", "--max-budget-usd", "4",
               "--allowedTools", "Read", "Glob", "Grep", "Edit", "Write", "Skill", "Bash(python:*)", "Bash(git:*)", "Bash(ls:*)", "Bash(cat:*)",
               "--add-dir", str(fx.brain)] + sum([["--add-dir", e] for e in extra], [])
    else:
        cmd = ["codex", "exec", "-C", str(fx.alfa), "--add-dir", str(fx.brain)] + sum([["--add-dir", e] for e in extra], []) + [
            "-s", "workspace-write", "--ephemeral", "--json", "-c", "notify=[]", prompt]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=fx.alfa, capture_output=True, text=True, encoding="utf-8", timeout=1500)
        saida, rc, erro = p.stdout, p.returncode, p.stderr[-800:]
    except subprocess.TimeoutExpired as e:
        saida, rc, erro = (e.stdout or ""), -9, "timeout"
        if isinstance(saida, bytes):
            saida = saida.decode("utf-8", "ignore")
    dur = round(time.time() - t0)
    (res / ("%s-%s.jsonl" % (tool, cid))).write_text(saida, encoding="utf-8")
    ev = (eventos_claude if tool == "claude" else eventos_codex)(saida.splitlines())
    (res / ("%s-%s.txt" % (tool, cid))).write_text(texto_final(ev), encoding="utf-8")
    checks = avaliar(fx, ev)
    fora = [t for k, t in ev if k == "ferramenta" and re.search(r"Documents[\\/]+aplicacoes|mega-brain[\\/]", t)]
    out = {"ferramenta": tool, "cenario": cid, "nome": nome, "rc": rc, "segundos": dur, "eventos": len(ev), "verificacoes": checks,
           "acesso_a_caminhos_reais_suspeito": [x[:200] for x in fora][:3], "stderr": erro}
    (res / ("%s-%s.json" % (tool, cid))).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--ferramentas", nargs="+", default=["claude", "codex"])
    ap.add_argument("--cenarios", nargs="+", default=list(CENARIOS))
    a = ap.parse_args()
    base = Path(a.base).resolve()
    if REAL in base.parents or base == REAL:
        sys.exit("o diretorio de trabalho deve ficar FORA do cofre real")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    antes_g, antes_r = instantaneo_global(), instantaneo_real()
    resumo = []
    for tool in a.ferramentas:
        for cid in a.cenarios:
            o = executar(tool, cid, base)
            resumo.append(o)
            print("[%s %s] rc=%s %ss %s" % (tool, cid, o["rc"], o["segundos"], json.dumps(o["verificacoes"], ensure_ascii=False)), flush=True)
    dep_g, dep_r = instantaneo_global(), instantaneo_real()
    iso = {"globais_inalteradas": antes_g == dep_g, "cofre_real_inalterado": antes_r == dep_r}
    (base / "resultados").mkdir(exist_ok=True)
    (base / "resultados" / ("resumo-%s.json" % "-".join(a.ferramentas))).write_text(json.dumps({"isolamento": iso, "execucoes": resumo}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("isolamento:", iso)


if __name__ == "__main__":
    main()
