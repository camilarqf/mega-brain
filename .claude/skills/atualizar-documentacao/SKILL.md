---
name: atualizar-documentacao
description: Atualiza de forma incremental as notas do Mega Brain afetadas por mudanças no código, commits ou requisitos implementados, com plano aprovado antes de escrever.
---

# Atualizar documentação

Regras e definições estão em `BRAIN-RULES.md` (seções citadas abaixo); não repeti-las aqui.

1. **Contexto.** Confirmar o acesso ao vault, o sistema e o componente no catálogo, o registro de análise e o commit de referência (seção 6, N0–N1).
2. **Identificar a mudança** por diffs e commits (`git log`, `git diff --name-status <analyzed_commit>..HEAD`), pelo código atual e, se houver, pela US implementada. Conferir renomes e remoções. Diff não prova comportamento: ler o contexto. Uma US aprovada não é funcionalidade implementada sem evidência no código (seção 5).
3. **Classificar:** refatoração interna (sem efeito funcional), mudança funcional, mudança de contrato ou integração, ou remoção.
4. **Impacto.** Notas cujo `sources` casa com os arquivos alterados e suas vizinhas por link; integração alterada leva à nota canônica e ao `Mapa-de-Integracoes` (seção 7). Procurar nota existente antes de criar outra (seção 8).
5. **Plano e aprovação.** Apresentar notas afetadas, o que muda, o que permanece e novos links; **obter aprovação antes de escrever.**
6. **Atualizar incrementalmente** só o conhecimento afetado. Preservar o histórico de regras e decisões (seção 5) e não duplicar regras, módulos ou fluxos. Atualizar `analyzed_commit`, `coverage`, `status` e `updated`, mantendo `created`. Pendências resolvidas permanecem na nota marcadas como resolvidas (data e commit), sem serem apagadas. Se a mudança for um requisito, `lifecycle` só avança com evidência.
7. **Validar** metadados, links, nomes e índices com `python <vault>/scripts/validar-brain.py` (ou manualmente); atualizar o registro de análise e as pendências, com o próximo passo.
8. **Relatar** notas verificadas e não verificadas. Não alterar código, não executar `git add`, commit nem push; ao final, sugerir `sincronizar-brain`.
