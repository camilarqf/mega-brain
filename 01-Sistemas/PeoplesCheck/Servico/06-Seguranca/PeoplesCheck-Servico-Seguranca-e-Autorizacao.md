---
type: security
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - seguranca
  - api-key
sources:
  - src/main/java/br/gov/df/peoplescheckapi/api/security/SecurityConfig.java
  - src/main/java/br/gov/df/peoplescheckapi/api/security/AuthenticationFilter.java
  - src/main/java/br/gov/df/peoplescheckapi/api/security/AuthenticationServiceImpl.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/couchdb/HttClientFactory.java
  - src/main/resources/application.properties
---
# PeoplesCheck Serviço — segurança e autorização

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar autenticação, autorização, proteção de dados e controles. Nenhum segredo é reproduzido.

## Evidências
- `SecurityConfig`, `AuthenticationFilter`, `AuthenticationServiceImpl`, `HttClientFactory`.

## Informações confirmadas
- ✅ **Autenticação por chave de API compartilhada:** o cabeçalho (nome em `security.api.key.header`) é comparado com `security.api.key` (um valor por perfil) por `String.equals`. Divergente ou ausente → `BadCredentialsException("Invalid API Key")`.
- ✅ **Autorização:** nenhuma. A autenticação criada (`ApiKeyAuthentication`) não tem papéis (`NO_AUTHORITIES`); toda rota autenticada vale para qualquer portador da chave, inclusive as administrativas (`DELETE /challenge`, `DELETE /challenge/old`, `DELETE /jobs/...`, `GET /challenge`).
- ✅ **Liberados sem chave:** `GET /healthcheck` e `GET /prometheus` (`permitAll` e exceção no filtro).
- ✅ Sessão `STATELESS`; CSRF desabilitado; `httpBasic()` habilitado (sem usuários configurados; as auto-configurações de usuário foram excluídas).
- ✅ **Proteção de dados:** o serviço só devolve nome, data de nascimento, nome da mãe e CPF (ou dados da empresa) depois de o desafio ser respondido corretamente; antes disso devolve apenas o comprimento do primeiro nome e do primeiro nome da mãe (mascaramento por `_`).
- ✅ Tentativas erradas limitadas a 3 por pessoa ([[01-Sistemas/PeoplesCheck/Servico/09-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Limite-de-Tentativas|regra]]).
- ✅ Comunicação com o CouchDB por HTTP(S) com usuário e senha de configuração; **sem validação de certificado nem de nome do host** ([[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-CouchDB|CouchDB]]).

## Inferências e limitações
- 🔴 ✅ Uma única chave por ambiente, sem identificação do consumidor, rotação ou expiração; vazamento dá acesso total (inclusive a consulta de dados pessoais por desafio e à remoção de desafios).
- 🔴 ✅ Valores de chave de API, URI do MongoDB e credenciais estão em arquivos versionados (`application-*.properties`, `*.env.yml`); uma chave de API também aparece em teste (`ApiKeyControllerTests`). Valores não reproduzidos aqui; rotacionar e mover para secrets do cluster.
- 🔶 `AuthenticationFilter` escreve a resposta 401 e, no `finally`, ainda chama `filterChain.doFilter`; o efeito exato em resposta já confirmada não foi verificado (o `anyRequest().authenticated()` deve barrar a rota, mas há tentativa de segunda escrita).
- 🔶 A comparação da chave não é de tempo constante.
- 🔶 `/healthcheck` com `show-details=always` expõe a versão do CouchDB; `/prometheus` é público.
- 🔶 CPF e CNPJ trafegam em query string (`data`, `cnpj`), que costuma ser registrada por proxies e balanceadores.
- 🔴 Possível injeção no seletor do CouchDB: ver [[01-Sistemas/PeoplesCheck/Servico/08-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]] (A1).
- LGPD: o serviço trata dados pessoais (nome, mãe, nascimento, CPF) de forma transitória; sem trilha de auditoria de quem consultou quem (🔶 não há log de consulta no código).

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/05-API/PeoplesCheck-Servico-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Observabilidade-e-Logs|Observabilidade]]

## Pendências e próximo passo
- Confirmar a exposição de rede por ambiente (o serviço deve ficar acessível apenas aos consumidores).
