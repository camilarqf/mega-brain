---
type: security
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - seguranca
  - autorizacao
  - owasp
sources:
  - api/config/SecurityConfig.java
  - api/security/*
  - application/exception/GlobalExceptionHandler.java
  - todos os controllers em api/
  - src/main/resources/application*.properties (somente chaves)
---

# Segurança e autorização

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Fluxo: [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]] · Relacionado: [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]], [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]], [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Debitos-Tecnicos|Debitos-Tecnicos]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

> Análise **estática** do código. Não houve teste de intrusão nem execução da aplicação. Nenhum segredo foi lido ou registrado.

## Configuração (`SecurityConfig`) ✅
| Item | Valor |
|---|---|
| Modelo | OAuth2 Resource Server (JWT do Keycloak) + `@EnableMethodSecurity` |
| Sessão | stateless (Bearer) |
| CSRF | desabilitado (aceitável para API com Bearer) |
| CORS | `allowedOrigins = *`; métodos GET/POST/PUT/DELETE/OPTIONS; headers incluem `Authorization` |
| Rotas públicas | `/actuator/health/**`, `/actuator/prometheus`, `/prometheus`, `/healthcheck/**`, `/v3/api-docs/**`, `/swagger-ui/**`, `/public/**`, `/error/**`, `/auth/login` |
| Demais rotas | `authenticated()` |
| Handlers | `CustomAuthenticationEntryPoint` (401 JSON, distingue token expirado), `CustomAccessDeniedHandler` (403 JSON) |

## Matriz de autorização ✅
Totais: **61 endpoints** (`@*Mapping`). **14** têm restrição de role: 12 por `@PreAuthorize` no método e 2 por `@PreAuthorize` na classe (`AuditorPerfilController`, `AuditorPerfilConsultaController`). **1** é público (`/auth/login`). Os **46** restantes exigem só um token válido de auditor ativo (ou super-usuário). Lista completa em [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]].

| Role | Pode (exclusivo ou compartilhado) |
|---|---|
| SUBCI | tudo que tem role; exclusivo: listar todas as OS, listar SUBCI, consultar e vincular perfis de auditores |
| DIRETOR | criar/atualizar ação; criar, atualizar, excluir, cancelar e pesquisar OS |
| COORDENADOR | criar, atualizar e inativar ação; criar, atualizar, excluir e cancelar OS |
| AUDITOR | criar (exceto cancelamento), atualizar e mudar status de OS; listar OS da ação |
| SUPER_USUARIO | só endpoints **sem** role |
| (qualquer autenticado) | 46 endpoints sem role, incluindo escrita: cadastrar SUBCI e substituto, POAC, OS genérica (CRUD e status), prorrogações, fases, justificativa de cancelamento, assinatura*, downloads |

\* A assinatura tem checagem própria (titular ou substituto), contornável pelos endpoints de SUBCI.

## Achados de segurança
| # | Severidade | Achado | Evidência | Status |
|---|---|---|---|---|
| S1 | 🔴 Crítica | **Escalada para assinante**: qualquer auditor autenticado se cadastra como SUBCI titular ou substituto e passa a assinar OS oficiais | `SubciController` sem `@PreAuthorize`; `AssinarOrdemServico.resolverAssinanteAutorizado` — [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]] | ✅ |
| S2 | 🔴 Crítica | **Segredos versionados**: senha de banco, segredo do HMAC (`integra.verify.secret`) e lista de super-usuários em `application-*.properties` no Git, em todos os ambientes | `git ls-files`; classificação literal/placeholder feita sem exibir valores | ✅ |
| S3 | 🟠 Alta | Status **ASSINADA sem assinatura** via `PUT /alterarStatusOs` (OS e OS genérica) | `AlterarStatusOrdemServico`, `EStatusOrdemServico` — [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] | ✅ |
| S4 | 🟠 Alta | 46 endpoints sem controle de perfil, incluindo escrita e exclusão (ex.: excluir OS genérica assinada) | [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]], [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]] | ✅ |
| S5 | 🟠 Alta | Validação do QR Code sempre "válido"; não verifica integridade nem cancelamento | `AssinaturaServiceImpl.validarPorCodigo` — [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]] | ✅ |
| S6 | 🟡 Média | **IDOR** em downloads de PDF (`/assinaturas/{id}/download*`) e consultas por id: sem checagem de vínculo com a ação | `AssinaturaController` | ✅ |
| S7 | 🟡 Média | CORS `*` | `SecurityConfig.corsConfigurationSource` | ✅ (mitigado por Bearer, sem cookies) |
| S8 | 🟡 Média | Login por ROPC (`grant_type=password`): a API recebe a senha do usuário | `KeycloakAuthAdapter.autenticar` | ✅ |
| S9 | 🟡 Média | Bypass por lista de super-usuários em propriedade, sem cadastro nem auditoria | `JwtAuthenticationConverterCustom` | ✅ |
| S10 | 🟡 Média | `/healthcheck` com `show-details=always` público e `/actuator/prometheus` público: expõem estado de banco, Keycloak e métricas | `application.properties`, `SecurityConfig` | ✅ |
| S11 | 🟡 Média | Swagger UI e `/v3/api-docs` públicos em todos os ambientes | `SecurityConfig` | ✅ |
| S12 | 🟢 Baixa | Mensagens internas devolvidas ao cliente (`NullPointerException` → 400 com `ex.getMessage()`; `HttpMessageNotReadableException` com detalhes de desserialização) | `GlobalExceptionHandler` | ✅ |
| S13 | 🟢 Baixa | Sem trilha de auditoria (quem criou, alterou, assinou) além da própria assinatura | ausência de entidades/campos de auditoria | ✅ |
| S14 | 🟢 Baixa | Segredo do HMAC de `local` é valor público (SHA-256 de string vazia) | `application-local.properties` (não reproduzido) | ✅ |

## Tratamento de erros (`GlobalExceptionHandler`) ✅
| Exceção | HTTP |
|---|---|
| `IllegalArgumentException`, `NullPointerException`, `MethodArgumentNotValidException`, `HttpMessageNotReadableException`, `UnexpectedTypeException`, `MultiplasValidacoesException` | 400 |
| `ResourceNotFoundException` | 404 |
| `DocumentoException`, `OsAssinadaNaoPodeSerExcluidaException`, `OsAssinadaNaoPodeSerAtualizadaException`, `DuplicidadeAberturaException`, `RegraNegocioException`, `RegraCriacaoProrrogacaoException` | 409 |
| `AccessDeniedException` | 403 |
| `PdfServiceException` | 503 |
| `BadCredentialsException` / `AuthenticationServiceException` (só em `AuthController`) | 401 / 502 |

- ✅ **Sem handler genérico** (`Exception`/`RuntimeException`). `IllegalStateException`, `java.lang.module.ResolutionException` (usada em `OrdemServicoServiceImpl`), `RuntimeException` genérica e `DataIntegrityViolationException` caem no `/error` padrão do Spring, ou seja, **500**. Ex.: "OS não encontrada" em `alterarStatusOs` responde 500, não 404.
- ✅ Tratar `NullPointerException` como 400 esconde bugs como se fossem erro do cliente.
