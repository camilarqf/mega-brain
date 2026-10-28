---
type: integration
aliases:
  - "Integrações externas"
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - autenticacao
  - geracao-pdf
sources:
  - application/service/comum/PdfService.java
  - infrastructure/external/adapter/KeycloakAuthAdapter.java
  - infrastructure/external/health/KeycloakHealthIndicator.java
---

# Integrações externas

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Assinatura-Digital|Assinatura-Digital]], [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

Provedor: [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Servico-HtmlToPdf]] (✅ confirmado pelo usuário).

> Endereços dos serviços **omitidos** de propósito; só os nomes das propriedades são registrados.

## Visão geral ✅
| Integração | Direção | Protocolo | Propriedade | Cliente |
|---|---|---|---|---|
| Serviço de geração de PDF | saída | HTTP POST JSON | `pdf.api.url` | `PdfService` (OkHttp) |
| Keycloak: validação de JWT | entrada (tokens) | OIDC / JWKS | `spring.security.oauth2.resourceserver.jwt.issuer-uri` | Spring Security Resource Server |
| Keycloak: login e userinfo | saída | HTTP (token endpoint, userinfo) | `keycloak.auth.*` | `KeycloakAuthAdapter` (RestTemplate) |
| Frontend de validação | link no QR Code | — | `assinatura.url.validacao` | — |

Não foram encontrados mensageria, e-mail, jobs agendados nem outras APIs.

## Serviço de PDF ✅
`application/service/comum/PdfService.gerarPdf(String htmlTemplate)`:
- Corpo: `{"HtmlString": "<html escapado>"}`, montado por **concatenação de strings**. Só escapa `"`, `\n` e `\r`.
- Resposta: bytes do PDF; status não-2xx ou corpo vazio → `PdfServiceException`; `IOException` → `PdfServiceException`.
- Cliente: `new OkHttpClient()` com timeouts padrão do OkHttp (10 s connect/read/write), sem retry configurado e sem autenticação no request.
- Usado em: assinatura de OS (`AssinarOrdemServico.gerarPdfDaOS`), assinatura de OS genérica, minuta (`OrdemServicoController.gerarRelatorioPdf`, `GerarPdfOrdemServicoGenerica`).

Pontos de atenção:
- ⚠️ **JSON montado à mão**: barras invertidas (`\`), tabulações e outros caracteres de controle no HTML (vindos de campos livres como observação, justificativa ou artigos) não são escapados. 🔶 Podem gerar JSON inválido e falha na geração do PDF.
- 🔶 Sem timeout explícito nem circuit breaker: a lentidão do serviço externo prende a transação de assinatura (ver [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]]).
- ❓ O serviço de PDF (tecnologia, dono, SLA) não aparece no repositório — ver [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]].

## Keycloak ✅
| Uso | Classe | Detalhe |
|---|---|---|
| Validação de JWT | Spring Resource Server (`SecurityConfig`) | `issuer-uri`; claim de usuário `preferred_username` |
| Login (ROPC) | `KeycloakAuthAdapter.autenticar` | `RestTemplate`; form `grant_type`, `client_id`, `client_secret` opcional, `username`, `password`, `scope`; 400/401 → `BadCredentialsException` (401), outros → `AuthenticationServiceException` (502) |
| Dados da conta | `KeycloakAuthAdapter.buscarDadosConta` | GET userinfo com Bearer; 401/403 → token inválido |
| Health | `KeycloakHealthIndicator` | GET `/.well-known/openid-configuration` derivado do token-uri |

Timeouts: connect 5 s, read 10 s (`keycloak.auth.connect-timeout-ms`, `read-timeout-ms`). Testado por `KeycloakAuthAdapterTest` (5 testes).
Fluxo completo e riscos: [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]], [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]].
