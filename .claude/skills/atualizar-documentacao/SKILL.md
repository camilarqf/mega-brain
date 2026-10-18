---
name: atualizar-documentacao
description: Atualiza a documentação técnica do Mega Brain a partir de mudanças confirmadas no código desde o commit analisado.
---

# Atualizar documentação

1. Identificar o repositório e o sistema no catálogo; localizar o `Registro-de-Analise.md` correspondente e o commit de referência.
2. Comparar commit analisado com `HEAD` (`git log`, `git diff --name-status`, e diffs relevantes). Conferir renomes e arquivos removidos. Não tratar diff como prova suficiente de comportamento sem ler o contexto.
3. Identificar notas impactadas usando evidências e referências; apresentar plano e solicitar aprovação.
4. Atualizar somente notas afetadas; manter versões históricas de decisões e registrar mudanças de comportamento separadamente.
5. Corrigir links internos e conferir consistência dos índices.
6. Atualizar no frontmatter das notas afetadas `analyzed_commit`, `coverage`, `status` e `updated` (schema de `BRAIN-RULES.md`; manter `created` e não reintroduzir campos em português), além de pendências e próximo passo. Relatar notas verificadas e não verificadas.
7. Não modificar código-fonte, não executar push/commit automaticamente, não copiar material confidencial a ambiente não autorizado.
