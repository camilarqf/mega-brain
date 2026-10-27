---
name: sincronizar-brain
description: Verifica o estado Git do cofre, valida metadados e conteúdo e conduz uma sincronização segura, com aprovação explícita para cada operação Git. Só roda quando o usuário a invoca.
---

# Sincronizar Brain

Regras e definições estão em `BRAIN-RULES.md` (seções 9 e 10); não repeti-las aqui. Esta Skill nunca é acionada automaticamente por outra.

1. **Estado.** Verificar o caminho do cofre, a branch, o remoto, `git status --short` e `git diff --stat`. Nada é alterado nesta etapa.
2. **Validar** com `python <vault>/scripts/validar-brain.py` (YAML, tipos, links, nomes duplicados, grupos do grafo, Skills e padrões sensíveis). Relatar as falhas; não corrigir sem pedido.
3. **Conteúdo.** Classificar as alterações por categoria (seção 10) e alertar sobre dados sensíveis, código interno, dumps, segredos, tokens, binários grandes, requisitos e documentação institucional. Conferir `.gitignore`, arquivos staged, unstaged e novos. Se o diff de `.obsidian/graph.json` mexer só em visualização (seção 9), apontar e propor descartá-lo.
4. **Resumo.** Exibir o resumo do diff e o plano de operações antes de qualquer operação Git.
5. **Remoto.** O remoto configurado não é, por si só, autorizado: pedir a confirmação da autorização para cada categoria de conteúdo presente. Sem autorização, parar e propor alternativa institucional.
6. **Aprovação por operação.** `git add` seletivo, commit, `fetch`, integração e `push` são aprovados separadamente. Nunca usar `reset --hard`, `push --force` ou comandos destrutivos. Fazer `fetch` antes do push e inspecionar divergências e conflitos.
7. **Verificar** o resultado de cada operação (por exemplo `git rev-list --left-right --count`) e informar o hash final, os arquivos enviados e as pendências. Não afirmar que a sincronização terminou sem checar.
