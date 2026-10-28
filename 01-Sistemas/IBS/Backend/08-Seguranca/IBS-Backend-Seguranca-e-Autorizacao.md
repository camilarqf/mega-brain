---
type: security
aliases:
  - "IBS Backend — segurança e autorização"
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
sources:
  - pom.xml
  - src/main/java/br/gov/df/cg/ibs/api
  - src/main/java/br/gov/df/cg/ibs/domain/_sharedkernel/valueobjects/SenhaUsuario.java
  - src/main/java/br/gov/df/cg/ibs/infra/ldap/LdapBindService.java
  - src/main/resources/application.properties
  - .docker/Dockerfile
---
# IBS Backend — segurança e autorização

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar os controles de segurança presentes e as lacunas verificáveis no código (sem segredos).

## Evidências
- `pom.xml` (sem `spring-security`), controllers, `SenhaUsuario`, `LdapBindService`, `application.properties`, `Dockerfile`, entrypoint de secrets.

## Informações confirmadas
- ✅ **Sem autenticação/autorização própria:** não há Spring Security, filtro, interceptador nem validação de chave/segredo; todas as rotas (`/auth`, `/usuarios/*`, `/healthcheck`, `/actuator/*` expostos) respondem a qualquer chamador que alcance o serviço. A proteção depende da rede/ingress (não verificada).
- ✅ **Cabeçalhos do cliente:** o cliente do Keycloak envia `X-IBS-Secret` (se configurado) e `X-Correlation-ID`; o IBS não lê nenhum dos dois e usa `X-Correlation-Key`. O segredo compartilhado, se existir, não é verificado aqui.
- ✅ **Tratamento da senha:** `SenhaUsuario` em `char[]` com `clear()`; zerada no handler e em cada bind; não é logada. Não é persistida (serviço só lê o banco).
- ✅ **Logs:** correlação, fonte, servidor, tipo de falha e código LDAP; o login não é logado nas rotas analisadas, mas `mensagem` da exceção JNDI é.
- ✅ **Canal LDAP:** `ldap://` com bind simples (ver [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-AD-LDAP|AD/LDAP]]).
- ✅ **Contêiner:** usuário não root; secrets via `/run/secrets` exportados como variáveis (o nome é impresso no log de inicialização).
- ✅ **Exposição de dados:** `GET /usuarios/buscar` e `/usuarios/{id}` devolvem nome, nome social, matrícula, login e lotação a qualquer chamador, sem autenticação.
- ✅ **Enumeração:** a checagem de vínculo antes da senha revela, sem credencial, se um login tem vínculo ativo no órgão (401 com mensagens diferentes).
- ✅ **Bloqueio de conta:** sem limitação de taxa/tentativas no IBS; uma senha errada gera um bind por servidor de cada fonte do órgão ([[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Ordem-de-Tentativa-LDAP|regra]]).
- ✅ **Credenciais em arquivo local:** `application-local.properties` (fora do Git) guarda credenciais de banco em texto claro, inclusive de outros ambientes em linhas comentadas; valores não registrados aqui.

## Inferências e limitações
- 🔶 `springdoc` provavelmente expõe `/swagger-ui.html` e `/v3/api-docs` sem autenticação (padrão da biblioteca; não verificado em execução).
- 🔶 `management.endpoint.health.show-details=when_authorized` sem segurança configurada tende a ocultar detalhes no `/actuator/health`, mas `/healthcheck` devolve o descritor do grupo readiness ao chamador.
- ❓ Controles de rede (ingress, firewall, mTLS) e política de rotação de segredos não estão no repositório.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/06-API/IBS-Backend-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Segurança do Keycloak]]

## Pendências e próximo passo
- Confirmar o desenho de proteção na rede e se o segredo compartilhado deveria ser validado no IBS.
