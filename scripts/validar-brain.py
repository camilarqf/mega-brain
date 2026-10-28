#!/usr/bin/env python3
"""Valida o Mega Brain (somente leitura, apenas biblioteca padrao).

Uso: python scripts/validar-brain.py [caminho-do-vault] [--json]

Os valores validos (tipos, cores, campos, status, coverage, lifecycle) sao lidos de
BRAIN-RULES.md (secoes 2 e 4); nada e duplicado aqui. Codigo de saida: 0 sem erros,
1 com erros, 2 uso incorreto.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

EXCLUIDOS = {".git", ".obsidian", ".claude", ".agents", "scripts", "node_modules"}
MD_RAIZ_SEM_FRONTMATTER = {"Home.md", "Catalogo-de-Sistemas.md", "BRAIN-RULES.md", "CLAUDE.md", "AGENTS.md"}
LEGADO_PT = {"tipo", "sistema", "cobertura", "fontes", "commit", "atualizado", "componente"}

SENSIVEIS = [
    ("erro", "chave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("erro", "chave de acesso AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("erro", "token JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("erro", "credencial em URL", re.compile(r"://[^/\s:@]+:[^/\s@]+@")),
    ("aviso", "possivel segredo (chave = valor)",
     re.compile(r"(?i)\b(password|passwd|senha|secret|token|api[_-]?key)\b\s*[:=]\s*[\"']?[^\s\"'`,;|]{6,}")),
    ("aviso", "possivel CPF", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
    ("aviso", "endereco de e-mail", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("aviso", "endereco IPv4", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
]


def ler(p):
    return p.read_bytes().decode("utf-8").replace("\r\n", "\n")


def tabelas(trecho):
    """Linhas de dados de cada tabela Markdown, uma lista por tabela (ignora cabecalho e separador)."""
    saida, atual, vistos_sep = [], None, False
    for ln in trecho.split("\n"):
        if not ln.startswith("|"):
            vistos_sep, atual = False, None
            continue
        celulas = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in celulas):
            vistos_sep, atual = True, []
            saida.append(atual)
            continue
        if vistos_sep:
            atual.append(celulas)
    return saida


def linhas_tabela(trecho, n=0):
    """Linhas de dados da n-esima tabela do trecho."""
    t = tabelas(trecho)
    return t[n] if len(t) > n else []


def secao(texto, numero):
    m = re.search(r"^## %s\. .*$" % numero, texto, re.M)
    if not m:
        return ""
    prox = re.search(r"^## ", texto[m.end():], re.M)
    return texto[m.end(): m.end() + prox.start()] if prox else texto[m.end():]


def carregar_regras(vault):
    texto = ler(vault / "BRAIN-RULES.md")
    tipos, cores = [], {}
    for c in linhas_tabela(secao(texto, 2)):
        m = re.fullmatch(r"`([a-z-]+)`", c[0])
        if m:
            tipos.append(m.group(1))
            r = re.fullmatch(r"(\d+), (\d+), (\d+)", c[-1])
            h = re.search(r"#([0-9A-Fa-f]{6})\b", c[-1])
            if r:
                cores[m.group(1)] = tuple(int(x) for x in r.groups())
            elif h:
                cores[m.group(1)] = tuple(int(h.group(1)[i:i + 2], 16) for i in (0, 2, 4))
    campos, restritos, valores, obrigatorios = [], {}, {}, set()
    linhas = linhas_tabela(secao(texto, 4))
    todos = [n for c in linhas for n in re.findall(r"`([a-z_]+)`", c[0])]
    for c in linhas:
        nomes = re.findall(r"`([a-z_]+)`", c[0])
        for n in nomes:
            campos.append(n)
            if "somente" in c[1]:
                restritos[n] = set(re.findall(r"`([a-z-]+)`", c[1]))
            if c[1].startswith("todas"):
                obrigatorios.add(n)
            if n in ("status", "coverage", "lifecycle"):
                valores[n] = {t for t in re.findall(r"`([a-z-]+)`", c[3]) if t not in todos}
    tags = {m.group(1) for c in linhas_tabela(secao(texto, 4), 1)
            for m in [re.fullmatch(r"`([a-z0-9-]+)`", c[0])] if m}
    pastas = {m.group(1) for c in linhas_tabela(secao(texto, 1))
              for m in [re.fullmatch(r"`(\d\d-[A-Za-z-]+)`", c[0])] if m}
    return {"tipos": tipos, "cores": cores, "campos": campos, "restritos": restritos,
            "valores": valores, "obrigatorios": obrigatorios, "tags": tags, "pastas": pastas}


def frontmatter(texto):
    """Retorna (dados, ordem, erros, corpo) ou None se nao houver frontmatter."""
    if not texto.startswith("---\n"):
        return None
    fim = texto.find("\n---", 4)
    if fim == -1:
        return {}, [], ["frontmatter sem fechamento"], texto
    dados, ordem, erros, chave = {}, [], [], None
    for ln in texto[4:fim].split("\n"):
        if not ln.strip():
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):(?:[ \t]+(.*))?$", ln)
        it = re.match(r"^[ \t]+-[ \t]+(.*)$", ln)
        if m:
            chave, val = m.group(1), (m.group(2) or "").strip()
            if chave in dados:
                erros.append("chave duplicada: " + chave)
            ordem.append(chave)
            if val == "":
                dados[chave] = None
            elif val.startswith("[") and val.endswith("]"):
                dados[chave] = [x.strip() for x in val[1:-1].split(",") if x.strip()]
            else:
                dados[chave] = val
        elif it and chave is not None:
            if dados.get(chave) is None:
                dados[chave] = []
            if isinstance(dados[chave], list):
                dados[chave].append(it.group(1).strip())
            else:
                erros.append("item de lista em chave escalar: " + chave)
        else:
            erros.append("linha nao reconhecida: " + ln.strip()[:40])
    return dados, ordem, erros, texto[fim + 4:]


def sem_codigo(texto):
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", texto)


def data_valida(v):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v or ""):
        return False
    try:
        datetime.date.fromisoformat(v)
        return True
    except ValueError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    vault = Path(a.vault).resolve()
    if not (vault / "BRAIN-RULES.md").exists():
        print("BRAIN-RULES.md nao encontrado em " + str(vault), file=sys.stderr)
        return 2
    achados = []

    def add(nivel, onde, msg):
        achados.append({"nivel": nivel, "onde": onde, "msg": msg})

    regras = carregar_regras(vault)
    notas = [p for p in sorted(vault.rglob("*.md")) if not (EXCLUIDOS & set(p.relative_to(vault).parts[:-1]))]
    rel = lambda p: str(p.relative_to(vault)).replace("\\", "/")
    cat = vault / "Catalogo-de-Sistemas.md"
    ids = set(re.findall(r"^\| `([^`]+)` \|", ler(cat), re.M)) if cat.exists() else set()

    # nomes duplicados
    por_nome = {}
    for p in notas:
        por_nome.setdefault(p.stem, []).append(rel(p))
    for nome, ps in por_nome.items():
        if len(ps) > 1:
            add("erro", nome, "nome de arquivo duplicado: " + ", ".join(ps))
    caminhos = {rel(p)[:-3] for p in notas}

    # pastas de componente fora da numeracao da secao 1
    if regras["pastas"]:
        fora = set()
        for p in notas:
            for parte in p.relative_to(vault).parts[3:-1]:
                if re.match(r"\d\d-", parte) and parte not in regras["pastas"]:
                    fora.add(str(p.parent.relative_to(vault)).replace("\\", "/"))
        for d in sorted(fora):
            add("aviso", d, "pasta fora da numeracao da secao 1")

    # prefixo do sistema (secao 3)
    for p in notas:
        partes = p.relative_to(vault).parts
        if partes[0] == "01-Sistemas" and len(partes) > 2 and not p.stem.startswith(partes[1] + "-"):
            add("aviso", rel(p), "nota sem o prefixo do sistema: " + partes[1] + "-")

    entrantes = set()
    for p in notas:
        r = rel(p)
        texto = ler(p)
        raiz = len(p.relative_to(vault).parts) == 1 or r.startswith("02-Temas/")
        modelo = r.startswith("99-Templates/")
        fm = frontmatter(texto)
        if fm is None:
            if not raiz or p.name not in MD_RAIZ_SEM_FRONTMATTER:
                add("erro", r, "nota sem frontmatter")
            corpo = texto
        else:
            dados, ordem, erros, corpo = fm
            for e in erros:
                add("erro", r, e)
            t = dados.get("type")
            if t not in regras["tipos"]:
                add("erro", r, "type invalido ou ausente: %s" % t)
            for k in ordem:
                if k in LEGADO_PT:
                    add("erro", r, "campo legado em portugues: " + k)
                elif k not in regras["campos"]:
                    add("erro", r, "campo fora do schema: " + k)
                elif k in regras["restritos"] and t not in regras["restritos"][k]:
                    add("erro", r, "campo %s nao se aplica ao type %s" % (k, t))
            idx = [regras["campos"].index(k) for k in ordem if k in regras["campos"]]
            if idx != sorted(idx):
                add("erro", r, "chaves fora da ordem do schema")
            if not modelo:
                for k in regras["obrigatorios"]:
                    if k == "system" and raiz:
                        continue
                    if dados.get(k) in (None, [], ""):
                        add("erro", r, "campo obrigatorio ausente ou vazio: " + k)
                if t == "requirement" and not dados.get("lifecycle"):
                    add("erro", r, "requirement sem lifecycle")
                for k, v in dados.items():
                    if v in ('""', "''"):
                        add("erro", r, 'valor "" proibido em ' + k)
                for k in ("status", "coverage", "lifecycle"):
                    v = dados.get(k)
                    if v and v not in regras["valores"].get(k, set()):
                        add("erro", r, "valor invalido em %s: %s" % (k, v))
                for k in ("created", "updated", "commit_data"):
                    if k in dados and not data_valida(dados[k]):
                        add("erro", r, "data invalida em %s: %s" % (k, dados[k]))
                c = dados.get("analyzed_commit")
                if c and not re.fullmatch(r"[0-9a-f]{40}", c):
                    add("erro", r, "analyzed_commit deve ter 40 caracteres hexadecimais")
                for lst in ("aliases", "tags", "sources"):
                    if lst in dados and not isinstance(dados[lst], list):
                        add("erro", r, lst + " deve ser lista")
                for tg in dados.get("tags") or []:
                    if tg != tg.lower() or tg.startswith("#"):
                        add("erro", r, "tag fora do padrao: " + tg)
                    elif regras["tags"] and tg not in regras["tags"]:
                        add("aviso", r, "tag fora do vocabulario controlado: " + tg)
                if ids:
                    sist = dados.get("system")
                    if sist and sist not in ids:
                        add("erro", r, "system fora do catalogo: " + sist)
                    for k in ("consumer", "provider"):
                        if dados.get(k) and dados[k] not in ids:
                            add("erro", r, "%s fora do catalogo: %s" % (k, dados[k]))
        # links
        for alvo in re.findall(r"!?\[\[([^\]|#\n]+)(?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\]", sem_codigo(corpo)):
            alvo = alvo.strip().rstrip("\\")
            if re.search(r"\.[A-Za-z0-9]{2,4}$", alvo) and not alvo.endswith(".md"):
                if not (vault / alvo).exists():
                    add("erro", r, "anexo inexistente: " + alvo)
                continue
            alvo = alvo[:-3] if alvo.endswith(".md") else alvo
            if "/" in alvo:
                ok = alvo in caminhos
                dest = alvo
            else:
                cand = [c for c in caminhos if c.split("/")[-1] == alvo]
                ok, dest = len(cand) >= 1, (cand[0] if cand else alvo)
            if not ok:
                add("erro", r, "link quebrado: [[%s]]" % alvo)
            elif dest != r[:-3]:
                entrantes.add(dest)
    for p in notas:
        r = rel(p)
        if len(p.relative_to(vault).parts) > 1 and not r.startswith("99-Templates/") and r[:-3] not in entrantes:
            add("aviso", r, "nota orfa (nenhum link entrante)")

    # sensiveis
    for p in notas:
        for n, ln in enumerate(ler(p).split("\n"), 1):
            for nivel, nome, rx in SENSIVEIS:
                if rx.search(ln):
                    add(nivel, "%s:%d" % (rel(p), n), "conteudo sensivel? " + nome)

    # grafo
    g = vault / ".obsidian" / "graph.json"
    if g.exists():
        grupos = {}
        for x in json.loads(g.read_bytes().decode("utf-8")).get("colorGroups", []):
            c = x["color"]["rgb"]
            for t in re.findall(r"type:([a-z-]+)", x["query"]):
                grupos[t] = ((c >> 16) & 255, (c >> 8) & 255, c & 255)
        for t in regras["tipos"]:
            if t not in grupos:
                add("erro", ".obsidian/graph.json", "tipo sem grupo de cor: " + t)
            elif regras["cores"].get(t) != grupos[t]:
                add("erro", ".obsidian/graph.json", "cor de %s difere de BRAIN-RULES.md: %s" % (t, grupos[t]))
        for t in grupos:
            if t not in regras["tipos"]:
                add("erro", ".obsidian/graph.json", "grupo para tipo inexistente: " + t)
    else:
        add("aviso", ".obsidian/graph.json", "arquivo ausente")

    # skills
    origem = vault / ".claude" / "skills"
    for d in sorted(x for x in origem.glob("*") if x.is_dir()) if origem.exists() else []:
        s = d / "SKILL.md"
        r = rel(s)
        if not s.exists():
            add("erro", rel(d), "SKILL.md ausente")
            continue
        fm = frontmatter(ler(s))
        if fm is None or fm[0].get("name") != d.name or not fm[0].get("description"):
            add("erro", r, "frontmatter deve ter name igual ao diretorio e description")
        elif len(fm[0]["description"]) > 1024:
            add("aviso", r, "description com mais de 1024 caracteres")
        if "BRAIN-RULES.md" not in ler(s):
            add("aviso", r, "Skill nao referencia BRAIN-RULES.md")
        if sum(1 for t in regras["tipos"] if "`%s`" % t in ler(s)) >= 6:
            add("aviso", r, "possivel lista de tipos duplicada na Skill")

    erros = sum(1 for x in achados if x["nivel"] == "erro")
    avisos = len(achados) - erros
    if a.json:
        print(json.dumps({"erros": erros, "avisos": avisos, "achados": achados}, ensure_ascii=False, indent=2))
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        for x in achados:
            print("%-5s %s: %s" % (x["nivel"].upper(), x["onde"], x["msg"]))
        print("\nnotas verificadas: %d | tipos oficiais: %d | erros: %d | avisos: %d"
              % (len(notas), len(regras["tipos"]), erros, avisos))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
