---
type: business-rule
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - regra
  - erros
sources:
  - src/main/java/br/gov/df/cg/ibs/api/exceptions/GlobalExceptionHandler.java
  - src/main/java/br/gov/df/cg/ibs/domain/autenticacao/enums/MotivoFalhaAutenticacao.java
---
# IBS Backend — regra: mapeamento de falhas para HTTP

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar a tradução de falhas de domínio em status HTTP e mensagens (condição → efeito).

## Evidências
- `GlobalExceptionHandler`; `MotivoFalhaAutenticacao` e `TipoFalhaTecnica`.

## Informações confirmadas
| Condição | HTTP | Mensagem ao cliente |
|---|---|---|
| `CREDENCIAL_INVALIDA` | 401 | Usuário ou senha inválidos. |
| `USUARIO_SEM_VINCULO_NO_ORGAO` | 401 | Usuário não possui vínculo ativo com o órgão informado. |
| `USUARIO_SEM_MATRICULA` | 409 | Usuário sem matrícula cadastrada. Contate o administrador. |
| `SERVICO_INDISPONIVEL` | 503 | Serviço de autenticação indisponível no momento. |
| `FONTE_NAO_ENCONTRADA` (como `AutenticacaoException`) | 503 | Nenhuma fonte de autenticação encontrada para o órgão informado. |
| Falha de validação do body | 400 | primeira mensagem de campo, ou "Requisição inválida." |
| `IllegalArgumentException` | 400 | mensagem da exceção |
| `UsuarioNaoEncontradoException` | 404 | Usuário não encontrado. |

- ✅ O detalhe técnico (tipo da falha, servidor, código LDAP) vai apenas para o log, nunca para o cliente.
- ✅ Cliente consumidor: o `ibs-authenticator` do Keycloak trata 401 como autenticação negada e qualquer outro status como erro de servidor (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integração Keycloak → IBS]]). Logo, **409 e 503 viram `server_error` no Keycloak**.

## Inferências e limitações
- ✅ Sem handler (resulta em 500 pelo Spring): órgão sem fonte (`FonteAutenticacaoNaoEncontradaException`), `IdentidadeInstitucionalIndisponivelException`, `MediatorException` e falhas de banco. Ver [[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/IBS/Backend/06-API/IBS-Backend-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo de autenticação]]

## Pendências e próximo passo
- Nenhuma específica.
