---
name: analisar-us
description: Analisa uma história de usuário ou solicitação de mudança em fases (análise independente, contexto, confronto crítico e entregáveis), sem implementar código e sem registrar comportamento como implementado.
---

# Analisar US

Regras e definições estão em `BRAIN-RULES.md` (seções citadas abaixo); não repeti-las aqui.

## Fase A — Análise independente
**Antes de qualquer outra ferramenta (além de ler esta Skill), escreva a Fase A completa como mensagem ao usuário.** Até essa mensagem existir, não ler nem listar o Mega Brain (catálogo, `BRAIN-RULES.md`, índices, notas, `Mapa-de-Integracoes`), nem o código nem os testes. Usar só o texto da US e o que o usuário informar; se faltar o nome do sistema, perguntar.
1. Interpretar a US e os critérios de aceite; identificar os objetivos de negócio.
2. Extrair regras novas e alterações de regras; ambiguidades e requisitos ausentes; cenários de erro e casos extremos; hipóteses iniciais.
3. Registrar a Fase A por escrito (na resposta e, se a nota for criada, na seção da Fase A) **antes** de seguir; depois ela não é reescrita, apenas confrontada.

## Fase B — Contextualização
4. Identificar sistema, componente e repositório no catálogo. Recuperar contexto progressivamente (seção 6) e conferir a validade das notas (seção 5). Examinar código, testes e contratos relevantes e as regras existentes; levantar integrações e sistemas potencialmente impactados pelo `Mapa-de-Integracoes` (seção 7). Ler notas de outro sistema só quando a US tocar a integração ou o contrato; não é padrão.

## Fase C — Confronto crítico
5. Comparar requisito, código atual e documentação. Relatar conflitos e restrições sem resolvê-los por suposição. Considerar alternativas e trade-offs, riscos, dependências e impactos arquiteturais e funcionais. A implementação atual não é presumida como a melhor solução, e documentação histórica não prevalece sobre o código atual (seção 5).

## Fase D — Entregáveis
6. Entregar: resumo da US; requisitos e regras; comportamento atual versus solicitado; impacto por módulo e sistema; arquivos ou componentes prováveis; dependências e integrações; critérios de aceite e cenários de teste; riscos, dúvidas e decisões pendentes; plano de implementação proposto.
7. Opcional, mediante aprovação: propor uma nota `requirement` (modelo `99-Templates/Historia-de-Usuario.md`, `lifecycle: proposed`, nome `<Sistema>-US-<ID>-<Resumo>`), verificando duplicidade (seção 8). Requisitos são conteúdo institucional (seção 10).

## Limites
Não implementar código, não documentar comportamento como implementado, não alterar notas existentes sem plano aprovado e não executar `git add`, commit nem push. O próximo passo é `implementar-us`, depois que as decisões pendentes forem resolvidas e o escopo aprovado.
