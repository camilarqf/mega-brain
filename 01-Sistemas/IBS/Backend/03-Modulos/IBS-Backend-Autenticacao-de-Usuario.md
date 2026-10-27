---
type: module
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - modulo
  - autenticacao
sources:
  - src/main/java/br/gov/df/cg/ibs/api/auth
  - src/main/java/br/gov/df/cg/ibs/application/autenticacao
  - src/main/java/br/gov/df/cg/ibs/application/claims
  - src/main/java/br/gov/df/cg/ibs/domain/autenticacao
  - src/main/java/br/gov/df/cg/ibs/domain/_sharedkernel/valueobjects
  - src/main/java/br/gov/df/cg/ibs/infra/ldap/LdapBindService.java
---
# IBS Backend — módulo de autenticação de usuário

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Reunir as peças que implementam `POST /auth`: validar credencial por LDAP e montar as claims.

## Evidências
- Pacotes em `sources`; testes `LoginControllerTest` (5), `AutenticarUsuarioHandlerTest` (14), `MontarClaimsHandlerTest` (5), `LdapBindServiceTest` (11).

## Informações confirmadas
| Peça                                             | Papel                                                                                                                                          |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `LoginController` / `LoginApi`                   | Rota `POST /auth`, header de correlação, anotações OpenAPI                                                                                     |
| `AutenticarUsuarioCommand` / `Handler`           | Valida obrigatórios; garante que a senha é zerada (`finally`)                                                                                  |
| `AutenticacaoService`                            | Orquestra vínculo → fontes → binds → claims; mantém o cache de fonte recente                                                                   |
| `ClaimsService` + `MontarClaimsCommand/Handler`  | Monta `ClaimsUsuario` e exige matrícula; o handler de montagem existe como caso de uso separado, mas o fluxo de `/auth` chama o serviço direto |
| `LdapBindService`                                | Bind JNDI com o próprio usuário e classificação do resultado                                                                                   |
| `LoginUsuario`, `SenhaUsuario`, `CorrelationKey` | Value objects do núcleo compartilhado (`_sharedkernel`)                                                                                        |
| `ResultadoAutenticacao` (sealed)                 | `Sucesso`, `CredencialInvalida`, `FalhaTecnica`                                                                                                |

- ✅ `SenhaUsuario` guarda `char[]`, entrega cópias e permite `clear()`; `LoginUsuario` rejeita sufixo `@` (o sufixo vem da fonte) e oferece `mascararLogin()` (não usado no fluxo principal).
- ✅ O módulo não grava nada (sem escrita em banco, sem auditoria: `infra/data/auditoria` está vazio).

## Inferências e limitações
- 🔶 `MontarClaimsHandler` só é referenciado na configuração e nos testes.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo]] · [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Ordem-de-Tentativa-LDAP|Ordem de tentativa]] · [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Vinculo-Ativo-e-Matricula|Vínculo e matrícula]] · [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Mapeamento-de-Erros-HTTP|Erros HTTP]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Claims|Claims]]

## Pendências e próximo passo
- Nenhuma específica.
