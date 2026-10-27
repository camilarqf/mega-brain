---
type: security
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - backend
  - seguranca
  - autenticacao
  - autorizacao
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/services/LoginService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/SsoAuthClient.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/JwtService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/AutorizacaoService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/config/ClientIdFilter.java
  - src/main/java/br/gov/df/cgdf/gerenciador/config/CorsFilter.java
---
# Segurança e autorização

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

> Nenhum valor de credencial é registrado aqui; só nomes de chaves.

## Objetivo
Documentar como o operador é autenticado e autorizado e quais controles existem (ou faltam) na API.

## Evidências
`LoginService`, `SsoAuthClient`, `JwtService`, `AutorizacaoService`, `ClientIdFilter`, `CorsFilter`, `ResourceExceptionHandler`, `pom.xml` (apenas `spring-security-jwt`, sem `spring-boot-starter-security`).

## Informações confirmadas
**Login (`POST /login`)** — fluxo completo em [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Login-e-Autorizacao|Fluxo de login]]:
1. ✅ Se `login`/`senha` coincidem com `dev.usuario.cpf`/`dev.usuario.senha`, devolve um usuário "DEVELOPER" (`servidorSUTCS=true`) **sem consultar o SSO**.
2. ✅ Senão, `SsoAuthClient` faz `POST` ao endpoint de token OIDC (`so.auth.url`, `grant_type=password`, `client_id`, `client_secret`, `idOrgao`).
3. ✅ `JwtService` decodifica o `access_token` com `JwtHelper.decode` (lê as claims `nomePessoa`, `login`, `matricula`, `siglaOrgao`, `idOrgao`, `nomeOrgao`, `autenticado`, `unidades`) — **sem verificar assinatura**.
4. ✅ `AutorizacaoService.possuiAcesso`: exige `idOrgao` igual a `autorizacao.id-orgao` e ao menos uma unidade do usuário em `autorizacao.id-unidades` (lista separada por vírgula); falha → `AcessoNegadoException`.
5. ✅ O corpo devolvido é o `UsuarioDTO`; **nenhum token ou sessão é emitido** pelo gerenciador.

**Demais rotas**
- ✅ Só o filtro `ClientIdFilter` age: exige o cabeçalho `x-client-id` com qualquer valor; isenta `OPTIONS`, `*/healthcheck` e `*/prometheus`.
- ✅ `CorsFilter`: `Access-Control-Allow-Origin: *`, métodos `POST, GET, PUT, OPTIONS, DELETE`, cabeçalhos incluindo `Authorization` e `x-client-id`.
- ✅ Nenhum controller valida identidade ou perfil. A identidade do autor (`usuarioLogado`/`usuarioAutenticado`) vem do cliente.

**Tratamento de erros de login**: `SsoAuthClient` lança `AutenticacaoException` com status `401` (usuário/senha inválidos), `400` (outra falha 4xx do SSO) ou `503` (SSO indisponível), mas o handler em `ResourceExceptionHandler` **ignora esse status e responde sempre `401`** ("Não autorizado"); `AcessoNegadoException` responde `403`. A `RuntimeException` de "token não retornado"/"erro ao converter JWT" não tem handler e vira `500`.

## Falhas e dependências
Riscos (recomendações separadas dos fatos em [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos técnicos]]):
- ✅ A API de escrita (upload, exclusão, ativação, medida protetiva) é alcançável por quem enviar `x-client-id` qualquer; a autorização por órgão/unidade só vale no `/login`.
- ✅ O JWT não tem a assinatura verificada, mas também não é usado depois do login (o `UsuarioDTO` é só devolvido).
- ✅ O usuário "DEVELOPER" está habilitado em todos os perfis versionados (as chaves `dev.usuario.*` existem inclusive em `prod`).
- ✅ O endpoint do SSO configurado usa `http` (sem TLS) nos perfis `homolog` e `prod` (verificado no esquema da URL; host omitido).
- ✅ O `/healthcheck` público devolve nomes de buckets e mensagem de erro do S3.

## Inferências e limitações
- 🔶 O provedor de identidade é o Keycloak (caminho `.../realms/<realm>/protocol/openid-connect/token`; as claims `idOrgao` e `unidades` coincidem com o [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|modelo de claims do KEYCLOAK-CGDF]]); a instância exata não consta no código.
- ❓ Se há proteção por gateway/ingress (WAF, autenticação, rede restrita) na frente do serviço.
- ❓ Quais órgãos e unidades correspondem aos valores configurados (`autorizacao.*`).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|Integração com o SSO]] · [[01-Sistemas/Gerenciador-Portal/Backend/06-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Confirmar com o time se a API é acessível só por rede interna e se o frontend repassa o token ao backend.
