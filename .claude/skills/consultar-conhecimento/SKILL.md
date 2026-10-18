---
name: consultar-conhecimento
description: Responde perguntas com consultas progressivas ao Mega Brain, citando fontes, validade, lacunas e contradições. Somente leitura; use para entender regras, módulos, APIs, fluxos ou integrações já documentados.
---

# Consultar conhecimento

Regras e definições estão em `BRAIN-RULES.md` (seções citadas abaixo); não repeti-las aqui.

1. **Acesso.** Confirmar o acesso ao vault. Sem acesso, informar a limitação e pedir acesso; nunca responder como se o Brain tivesse sido consultado.
2. **Delimitar.** Identificar o sistema e o tipo de conhecimento (módulo, regra, API, fluxo, integração, segurança etc.) e o `type` provável (seção 2).
3. **Recuperar progressivamente** (seção 6): catálogo, índice, notas-alvo por `type`, `tags` e títulos, e só então vizinhas por link. Outro sistema apenas via `Mapa-de-Integracoes` e se for relevante. Não carregar o sistema inteiro; ler frontmatter e títulos antes das seções.
4. **Validar cada nota usada** (seção 5): comparar `analyzed_commit` com o `HEAD` e checar `sources` alterados; classificar como válida, desatualizada ou de validade desconhecida. Para afirmações importantes, confirmar no código atual, testes ou contratos quando acessíveis; se não for possível, dizer.
5. **Responder** com: a resposta direta; as **fontes** (nota, commit, validade, ✅/🔶/❓); as **contradições e lacunas**; e, se útil, o próximo passo sugerido (por exemplo `atualizar-documentacao`), sem executá-lo.
6. **Somente leitura.** Não modificar notas nem o Git sem pedido. Propor novas análises ou links apenas como sugestão. Respeitar a confidencialidade (seção 10).
