---
type: analysis-log
aliases:
  - "Registro de análise — Serviço Keycloak"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: pendente
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-28
commit_data: 2026-09-03
branch: master
---
# Registro de análise — Serviço Keycloak

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]]

## Objetivo
Controlar os lotes de análise do repositório `keycloak` e permitir retomada sem repetir trabalho.

## Evidências
- Repositório `keycloak`, branch `master`, commit `1755591a3abfeee96a626cedd800187263967154`.
- Inventário (lote 0) cobriu: `README.md`, `providers/pom.xml`, as 9 classes de `providers/src/main`, os 2 arquivos `META-INF/services`, os 4 testes, `.docker/*`, `.jenkins-pipelines/*` e `integra-login/login/theme.properties`.
- O `dist` compilado e os `.ftl` do tema não foram lidos em detalhe.

## Informações confirmadas
| Lote | Escopo | Estado |
|---|---|---|
| 0 | Cadastro, inventário, esqueleto e notas de controle | ✅ concluído em 2026-10-18 |
| 1 | Stack, arquitetura SPI, build e deploy (3 notas) | ✅ concluído em 2026-10-18 |
| 2 | Fluxo Direct Grant, modelo de claims, segurança, 3 regras de negócio (6 notas) | ✅ concluído em 2026-10-18 |
| 3 | Integração IBS, contrato do token endpoint, tema, testes, débitos (5 notas) | ✅ concluído em 2026-10-18; tema e contrato com cobertura parcial |

Total: 14 notas técnicas + 2 de controle + 4 de sistema/índice. Cobertura do componente: **parcial** (tema `integra-login` só por inventário; `dist` e `.ftl` não lidos em detalhe; `mvn test` executado em 2026-10-18: 20 testes passando).

Correção durante o lote 1: `IbsRestClient` foi inicialmente descrito como usado nos testes; a verificação por busca mostrou que não é referenciado por ninguém (registrado como código morto).

Decisões do usuário (2026-10-18): ID do sistema `KEYCLOAK-CGDF`, componente `Servico-Keycloak`; este é o Keycloak usado pelo SICI, que não usa o componente IBS (usa o AD).

## Inferências e limitações
- Cobertura `parcial` até os lotes 1 a 3 serem concluídos.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Repositorios|Repositórios]] · [[Catalogo-de-Sistemas|Catálogo]]

## Pendências e próximo passo
- **Próximo passo exato:** (1) responder as perguntas de [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]]; (2) ler os `.ftl` e o `dist` do tema, se o tema for relevante; (3) com a exportação do realm (sem segredos), documentar clients e fluxos. Antes, conferir `git rev-parse HEAD` = `1755591`; se mudou, usar `atualizar-documentacao`.

## Histórico de estrutura
- 2026-10-27: pastas reorganizadas conforme a seção 1 do `BRAIN-RULES.md` (numeração fixa; melhorias do cofre, lote 3).
- 2026-10-28: frontmatter padronizado: título legível em `aliases` e tags reduzidas ao vocabulário controlado da seção 4 do `BRAIN-RULES.md` (melhorias do cofre, lote 5).
