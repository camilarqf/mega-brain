---
type: reference
system: SICI
repository: sici-backend
status: confirmado
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tipo: referencia
sistema: SICI
commit: 1871e32
atualizado: 2026-10-16
cobertura: completa
fontes: [pom.xml, src/main/resources/application*.properties, .docker/Dockerfile, .jenkins-pipelines/]
tags: [sici, configuracao, ambientes, profiles]
---

# Perfis e ambientes

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/01-Visao-Geral/Stack-e-Dependencias|Stack-e-Dependencias]], [[01-Sistemas/SICI/Backend/06-Seguranca/Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

> Esta nota registra **apenas nomes de chaves e valores não sensíveis**. URLs, usuários, senhas, segredos e listas de usuários foram omitidos de propósito.

## Mapeamento de profiles ✅
| Profile Maven (`pom.xml`) | `spring.profiles.active` | Arquivo |
|---|---|---|
| `local` | `local` | `application-local.properties` |
| `desenvolvimento` (**activeByDefault**) | `dev` | `application-dev.properties` |
| `homologacao` | `hom` | `application-hom.properties` |
| `producao` | `prod` | `application-prod.properties` |

O `application.properties` usa `spring.profiles.active=@spring.profiles.active@` (filtragem de recursos do Maven).

## Comparativo de comportamento ✅
| Configuração | base | local | dev | hom | prod |
|---|---|---|---|---|---|
| Banco | — | SQL Server | SQL Server | SQL Server | SQL Server |
| Flyway habilitado | não | **sim** | **sim** | não | não |
| `ddl-auto` | `validate` | (herda) | (herda) | `validate` | (herda) |
| Log `br.gov.df.cg.sici` | `DEBUG` | (herda) | (herda) | (herda) | `WARN` |
| Keycloak (resource server) | sim | — | — | sim | sim |
| Super-usuários (`security.super-users`) | — | — | — | — | **definido** |

🔶 Flyway só roda em local/dev; em hom/prod as migrations provavelmente são aplicadas por outro processo (DBA/pipeline). Ver [[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendencias]].

## Grupos de chaves ✅
| Grupo | Chaves | Uso no código |
|---|---|---|
| Actuator | `management.endpoints.web.exposure.include=health,prometheus`, `base-path=/`, `health` mapeado para `/healthcheck`, `show-details=always` | Healthcheck do Docker/Jenkins; `KeycloakHealthIndicator` |
| HikariCP | pool `SICIHikariCP`, min 5 / max 30 conexões, leak detection 120 s | — |
| Thymeleaf | prefixo/sufixo/encoding, `cache=false` | Templates de OS em `src/main/resources/templates` |
| PDF | `pdf.api.url` | `PdfService` (OkHttp) |
| Assinatura | `assinatura.url.validacao`, `assinatura.qr-size=180` | `AssinaturaProperties`, `ImagemUtils.gerarQrBase64` |
| Verificador | `integra.verify.secret` | `VerifyCodeProperties` → `VerifyCode.setSecret` (HMAC-SHA256) |
| Imagens | `integra.imagens.base-path` | `ImagemUtils` |
| OAuth2/JWT | `spring.security.oauth2.resourceserver.jwt.issuer-uri`, registro/provider `keycloak`, `jwt.auth.converter.principal-attribute=preferred_username` | `SecurityConfig`, `JwtAuthenticationConverterCustom` |
| Login Keycloak | `keycloak.auth.token-uri`, `userinfo-uri`, `client-id`, `client-secret`, `grant-type=password`, timeouts 5 s / 10 s | `KeycloakAuthProperties`, `KeycloakAuthAdapter` |
| Bypass | `security.super-users` | `JwtAuthenticationConverterCustom.isSuperUsuario` |
| Spring | `spring.main.allow-bean-definition-overriding=true` | — |

## Pontos de atenção
- ✅ Arquivos de properties de todos os ambientes estão **versionados** e contêm credenciais e segredos em texto puro. Ver [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Debitos-Tecnicos]].
- ✅ O valor de `integra.verify.secret` no profile local é o SHA-256 de uma string vazia, um valor publicamente conhecido.
- ✅ `grant-type=password` (Resource Owner Password Credentials) — fluxo desaconselhado pelo OAuth 2.1.
- ✅ `show-details=always` com `/healthcheck` público expõe detalhes de saúde (banco, Keycloak) sem autenticação.
- ✅ `spring.thymeleaf.cache=false` vale também para produção (não é sobrescrito em `application-prod.properties`).
- 🔶 Profile efetivo no container: ver observação sobre `-P SPRING_PROFILES_ACTIVE` em [[01-Sistemas/SICI/Backend/01-Visao-Geral/Stack-e-Dependencias|Stack-e-Dependencias]].
