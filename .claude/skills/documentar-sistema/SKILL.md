---
name: documentar-sistema
description: Analisa um repositório e documenta o sistema de negócio correspondente no Mega Brain, por lotes rastreáveis.
---

# Documentar sistema

1. Identificar o repositório e confirmar o caminho absoluto do vault Mega Brain. Se não houver acesso, pedir que o usuário use `/add-dir` ou `claude --add-dir`.
2. Ler `Catalogo-de-Sistemas.md`, `BRAIN-RULES.md` e o índice pertinente. Confirmar se o repositório pertence a sistema existente ou novo; não inferir associação apenas pelo nome.
3. Ler notas existentes, `Registro-de-Analise.md` e `Pendencias.md` antes de analisar. Conferir `git rev-parse HEAD` do projeto e registrar se mudou desde a análise anterior.
4. Fazer inventário: stack, módulos, controllers, rotas, serviços, entidades, persistência, integrações, autenticação, validações, testes e fluxos. Nunca reproduzir segredos, credenciais ou dados reais.
5. Apresentar **plano de lotes** e destino de cada nota. Obter aprovação antes de escrever.
6. Documentar por lotes pequenos, com evidências (repositório + commit + arquivo + símbolos), distinguindo confirmado, inferido e não identificado. Não confundir regra de negócio com hipótese baseada em nomes.
7. Gerar Markdown para Obsidian com frontmatter e links. Preservar material existente e não alterar o código.
8. Após cada lote aprovado: atualizar índice, `Registro-de-Analise.md`, `Pendencias.md`, cobertura e próximo passo exato.
9. Se backend/frontend compõem o mesmo sistema, documentar cada repositório em pasta própria; integrar fluxos somente após verificar ambos.
10. Nunca fazer Git push/commit automático. Se conteúdo institucional não estiver autorizado a sair, interromper qualquer escrita/sync no vault pessoal e propor ambiente institucional.
