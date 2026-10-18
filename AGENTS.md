# Mega Brain — instruções para Codex (GPT)

Este repositório contém conhecimento em Markdown para Obsidian e Agent Skills compartilhadas com Claude Code. **Todas as regras estão em `BRAIN-RULES.md`** (fonte única): ler apenas a seção necessária e não copiar definições para cá.

- Ponto de entrada: `Catalogo-de-Sistemas.md` e o índice do sistema pertinente (recuperação progressiva: `BRAIN-RULES.md`, seção 6).
- Skills oficiais em `.claude/skills/` (única fonte); o Codex as usa pela instalação global `~/.codex/skills/`, criada por `scripts/sincronizar-skills.py`: `documentar-sistema`, `consultar-conhecimento`, `atualizar-documentacao`, `sincronizar-brain`, `analisar-us`, `implementar-us`.
- Não presuma que o cofre Obsidian está montado: confira o caminho e as permissões na sessão e informe a limitação se não houver acesso.
- Nunca executar `git add`, `commit`, `push`, `reset` ou rebase automaticamente, nem escrever em notas sem plano aprovado (seções 9 e 10).
