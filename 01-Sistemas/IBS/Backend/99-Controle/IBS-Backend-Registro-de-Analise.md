---
type: analysis-log
system: IBS
component: Backend
repository: identity-broker-service
status: pendente
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
commit_data: 2026-08-31
branch: master
tags:
  - ibs
  - registro-de-analise
---
# Registro de análise — IBS Backend

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]] · Relacionado: [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Pendencias|Pendências]]

## Objetivo
Controlar os lotes de análise do repositório `identity-broker-service` e permitir retomada sem repetir trabalho.

## Evidências
- Repositório `identity-broker-service`, branch `master`, commit `cf0959ae140844926755b218a8452d34f3970ed3`.
- Total: 19 notas técnicas e 2 de controle no componente, mais 3 notas do sistema (índice, contexto, repositórios) e o índice do componente. Cobertura do componente: **parcial**.

`./mvnw test` (2026-10-18): 157 testes, 152 passando, 5 com erro (4 por rota errada no teste e 1 que exige banco real). Nenhum código foi alterado.

Alterações em notas existentes: `Catalogo-de-Sistemas` (sistema `IBS` e serviços externos `AD-LDAP` e `SIP-SQLServer`; a linha antiga do serviço externo `IBS` foi substituída pelo sistema), `Mapa-de-Integracoes` (2 linhas) e `KEYCLOAK-CGDF-Servico-Integracao-IBS` (link para o lado provedor).

Inventário do lote 0 leu: `README.md`, `pom.xml`, `.docker/Dockerfile`, `.jenkins-pipelines/deployment.params.yml`, `application*.properties`, o código de `api`, `application` e `infra` principal (auth, usuários, fontes, LDAP, identidade institucional, config) e parte do `domain`; testes só por contagem (157 `@Test`).
- Não lidos em detalhe: mappers, SQL completo de `UsuarioRepository`, entidades de domínio restantes, conteúdo dos testes.

## Informações confirmadas
| Lote | Escopo | Estado |
|---|---|---|
| 0 | Cadastro, inventário, índices, stack e notas de controle | ✅ concluído em 2026-10-18 |
| 1 | Arquitetura em camadas, catálogo de endpoints, perfis e ambientes (3 notas) | ✅ concluído em 2026-10-18 |
| 2 | Módulos (autenticação, fontes, usuários), fluxo, 3 regras, modelo de domínio e de claims (9 notas) | ✅ concluído em 2026-10-18 |
| 3 | Banco SIP, integrações AD/LDAP e SIP, mapa de integrações e catálogo (3 notas + 3 notas existentes atualizadas) | ✅ concluído em 2026-10-18 |
| 4 | Segurança, testes (com `mvn test`), débitos técnicos (3 notas) | ✅ concluído em 2026-10-18; segurança e testes com cobertura parcial |

Decisões do usuário (2026-10-18): ID do sistema `IBS`, componente `Backend`; confirmou que o repositório é o serviço chamado pelo Keycloak; pediu para **ignorar por enquanto** `ANALISE_CLAIMS_E_DISPONIBILIDADE.md` e `docs/contratos-api-ibs.md` (não versionados): não foram usados como fonte.

## Inferências e limitações
- Toda afirmação das notas vem do código do commit analisado e da execução dos testes. Não lidos em detalhe: `LoginContextualizado` e o segundo `LoginUsuario`, corpo da maioria dos testes, `*.env.yml` além do perfil. Nada foi verificado em execução contra AD ou banco reais.

## Relacionamentos
- [[01-Sistemas/IBS/IBS-Index|IBS]]

## Pendências e próximo passo
- **Próximo passo exato:** a análise inicial está concluída. Para refinar: (1) ler `LoginContextualizado`, o `LoginUsuario` de `fonteautenticacao` e o conteúdo dos testes de infra para elevar a cobertura de `Modelo-de-Dominio`, `Consulta-de-Usuarios` e `Testes`; (2) resolver as pendências de dono e consumidores. Para mudanças futuras no código, usar a skill `atualizar-documentacao` (`git diff cf0959a..HEAD`).
