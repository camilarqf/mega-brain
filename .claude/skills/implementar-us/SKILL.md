---
name: implementar-us
description: Implementa o escopo aprovado de uma US já analisada, com mudanças pequenas e rastreáveis, testes e revisão do diff, sem commit e sem alterar a documentação do Mega Brain automaticamente.
---

# Implementar US

Regras e definições estão em `BRAIN-RULES.md` (seções citadas abaixo); não repeti-las aqui.

1. **Recuperar a análise** (nota `requirement` ou resposta de `analisar-us`) e confirmar o escopo aprovado e as decisões pendentes. Com ambiguidade crítica ou mudança de escopo, parar e perguntar; não prosseguir silenciosamente.
2. **Verificar o repositório:** branch, `git status` e `HEAD`. Não sobrescrever alterações não commitadas que não sejam suas.
3. **Contexto mínimo.** Recuperar do Brain só o necessário (seção 6), conferir a validade das notas (seção 5) e confirmar no código. Não consultar o Brain em tarefas triviais.
4. **Planejar** alterações pequenas e rastreáveis (arquivo, motivo, teste) e apresentá-las para aprovação se divergirem do plano analisado.
5. **Arquitetura.** Respeitar a existente quando apropriado; questionar decisões inadequadas com justificativa e alternativas (seção 5).
6. **Skills de terceiros** (arquitetura, programação, testes, revisão, segurança): usar as relevantes disponíveis na sessão, sem duplicá-las nem modificar seus arquivos. Se o agente não conseguir invocá-las, pedir ao usuário. Instruções incompatíveis (commit, push ou PR automáticos, mudança de escopo) exigem decisão do usuário (seção 11).
7. **Implementar somente** o escopo aprovado.
8. **Criar ou atualizar os testes** adequados.
9. **Executar as validações** disponíveis (testes, build, lint) e relatar o que rodou e o que não pôde rodar. Não declarar sucesso sem executar.
10. **Revisar o diff** completo em busca de regressões, riscos de segurança e escopo extra.
11. **Resumir** arquivos modificados, testes executados, limitações e riscos.
12. **Documentação.** Identificar as notas do Brain impactadas (inclusive integrações) e sugerir `atualizar-documentacao`. Não alterar o Mega Brain sem aprovação e não executar `git add`, commit nem push.
