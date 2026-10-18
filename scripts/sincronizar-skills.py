#!/usr/bin/env python3
"""Distribui as Skills oficiais do cofre (.claude/skills) sem criar copias divergentes.

Fonte unica: <vault>/.claude/skills (versionada). Destinos, sem copias:
  - ~/.claude/skills/<skill>         junction para o cofre (Claude Code, global)
  - ~/.codex/skills/<skill>          junction para o cofre (Codex, global)
  - --agents-dir <dir>               opcional: copia para um diretorio .agents/skills de outro repositorio
Rodar uma vez em cada maquina nova.

Por padrao so VERIFICA (nada e alterado). Com --aplicar: antes de substituir qualquer
diretorio existente, move-o para ~/.mega-brain-backups/<data-hora>/ e grava um manifest.json.
So toca nas Skills cujo nome existe em <vault>/.claude/skills; Skills de terceiros nunca
sao lidas nem alteradas. --desfazer <data-hora> restaura o estado anterior.
Apenas biblioteca padrao.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def e_juncao(p):
    f = getattr(os.path, "isjunction", None)
    return bool(f and f(p)) or os.path.islink(p)


def arvore(d):
    saida = {}
    for f in sorted(Path(d).rglob("*")):
        if f.is_file():
            b = f.read_bytes()
            saida[str(f.relative_to(d)).replace("\\", "/")] = hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()
    return saida


def destino_juncao(p):
    return Path(os.path.realpath(p))


def criar_juncao(link, alvo):
    link, alvo = Path(link), Path(alvo)
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(alvo)], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("mklink falhou: " + (r.stdout + r.stderr).strip())
    else:
        os.symlink(alvo, link, target_is_directory=True)


def remover_juncao(link):
    os.rmdir(link) if os.name == "nt" else os.unlink(link)


def estado(alvo, origem, tipo):
    """Retorna (codigo, texto). Codigos: ok, criar, atualizar, conflito, bloqueado."""
    if not os.path.lexists(alvo):
        return "criar", "ausente"
    if tipo == "juncao":
        if e_juncao(alvo):
            if destino_juncao(alvo) == Path(os.path.realpath(origem)):
                return "ok", "junction correta"
            return "conflito", "junction aponta para outro lugar: " + str(destino_juncao(alvo))
        if Path(alvo).is_dir():
            if arvore(alvo) == arvore(origem):
                return "atualizar", "copia identica (sera trocada por junction)"
            return "conflito", "diretorio com conteudo diferente (versao antiga ou divergente)"
        return "bloqueado", "existe um arquivo com esse nome"
    if Path(alvo).is_dir() and not e_juncao(alvo):
        return ("ok", "copia identica") if arvore(alvo) == arvore(origem) else ("atualizar", "copia divergente")
    return "bloqueado", "destino inesperado"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--claude-dir", default=str(Path.home() / ".claude" / "skills"))
    ap.add_argument("--codex-dir", default=str(Path.home() / ".codex" / "skills"))
    ap.add_argument("--agents-dir", default=None, help="opcional: copia para outro .agents/skills")
    ap.add_argument("--backup-dir", default=str(Path.home() / ".mega-brain-backups"))
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--desfazer", metavar="DATA-HORA")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    vault = Path(a.vault).resolve()
    fonte = vault / ".claude" / "skills"
    alvos = [("claude", Path(a.claude_dir), "juncao"), ("codex", Path(a.codex_dir), "juncao")]
    if a.agents_dir:
        alvos.insert(0, ("agents", Path(a.agents_dir), "copia"))

    if a.desfazer:
        pasta = Path(a.backup_dir) / a.desfazer
        man = json.loads((pasta / "manifest.json").read_text(encoding="utf-8"))
        for ac in reversed(man["acoes"]):
            alvo = Path(ac["alvo"])
            if os.path.lexists(alvo):
                if e_juncao(alvo):
                    remover_juncao(alvo)
                else:
                    shutil.rmtree(alvo)
            if ac.get("backup"):
                shutil.move(ac["backup"], alvo)
            elif ac.get("juncao_anterior"):
                criar_juncao(alvo, ac["juncao_anterior"])
            print("restaurado:", alvo)
        return 0

    nomes = sorted(d.name for d in fonte.iterdir() if d.is_dir() and (d / "SKILL.md").exists())
    if not nomes:
        print("nenhuma Skill em", fonte)
        return 2
    plano = []
    for rotulo, base, tipo in alvos:
        terceiros = [d.name for d in base.iterdir() if d.is_dir() and d.name not in nomes] if base.exists() else []
        print("\n[%s] %s (%s) - %d Skills de terceiros/outras preservadas" % (rotulo, base, tipo, len(terceiros)))
        for n in nomes:
            cod, txt = estado(base / n, fonte / n, tipo)
            print("  %-24s %-10s %s" % (n, cod, txt))
            plano.append((rotulo, base / n, fonte / n, tipo, cod))
    pendentes = [p for p in plano if p[4] != "ok"]
    bloqueados = [p for p in plano if p[4] == "bloqueado"]
    if not a.aplicar:
        print("\nverificacao: %d de %d destinos precisam de acao (nada foi alterado)." % (len(pendentes), len(plano)))
        return 0 if not pendentes else 1
    if bloqueados:
        print("\nabortado: destinos bloqueados, nada foi alterado.")
        return 2

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    raiz_bk, k = Path(a.backup_dir) / ts, 1
    while raiz_bk.exists():
        k += 1
        raiz_bk = Path(a.backup_dir) / ("%s-%d" % (ts, k))
    ts = raiz_bk.name
    acoes = []
    for rotulo, alvo, origem, tipo, cod in pendentes:
        ac = {"alvo": str(alvo), "rotulo": rotulo}
        if os.path.lexists(alvo):
            if e_juncao(alvo):
                ac["juncao_anterior"] = str(destino_juncao(alvo))
                remover_juncao(alvo)
            else:
                bk = raiz_bk / rotulo / alvo.name
                bk.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(alvo), str(bk))
                if not bk.exists():
                    raise RuntimeError("backup nao confirmado: " + str(bk))
                ac["backup"] = str(bk)
        if tipo == "juncao":
            criar_juncao(alvo, origem)
        else:
            shutil.copytree(origem, alvo)
        acoes.append(ac)
        print("aplicado:", rotulo, alvo.name)
    if acoes:
        raiz_bk.mkdir(parents=True, exist_ok=True)
        (raiz_bk / "manifest.json").write_text(json.dumps({"vault": str(vault), "acoes": acoes}, ensure_ascii=False, indent=2), encoding="utf-8")
        print("\nbackup/manifest em", raiz_bk, "- desfazer: --desfazer", ts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
