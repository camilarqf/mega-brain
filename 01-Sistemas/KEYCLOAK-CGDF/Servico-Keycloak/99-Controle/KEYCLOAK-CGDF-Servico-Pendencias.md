---
type: analysis-log
aliases:
  - "Pendências e pontos a confirmar — Serviço Keycloak"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: pendente
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
---
# Pendências e pontos a confirmar — Serviço Keycloak

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Registro-de-Analise|Registro-de-Analise]]

## Conflitos entre documentação e código (a resolver com o time)
- [ ] O `README.md` diz "401/403 → `invalid_grant`"; no código (`IbsApiClient.login`) só o 401 é tratado como falha de autenticação, e o 403 lança `IOException` (→ `server_error`). O teste `loginMapeia403ComoErroTecnico` confirma o código. Qual é o comportamento desejado?
- [ ] O `README.md` cita Keycloak 26.3.2 e jar `1.0-SNAPSHOT`; o `Dockerfile` usa a imagem `keycloak:25.0.2` e o jar `1.0.0`, enquanto o `pom.xml` compila contra 26.3.2. A versão de runtime é a 25.0.2?

## Perguntas técnicas
- [ ] Como o tema `integra-login` chega ao Keycloak? O `Dockerfile` não o copia.
- [ ] O `health_check_endpoint: healthcheck` do pipeline corresponde a algum endpoint real (o Keycloak expõe `/health`)?
- [ ] Os logs do SPI gravam `login`, `idOrgao` e `correlationKey` (não a senha). Isso é aceitável quanto a dados pessoais?

## Perguntas de negócio e integração
- [ ] Quem são os consumidores do fluxo Direct Grant com IBS (clients/realms)?
- [ ] Quem é o dono do IBS e qual o ambiente de cada `ibsBaseUrl`?
- [ ] Como é configurada a federação com o AD usada pelo SICI (fora deste repositório)?
- [ ] Onde está o código-fonte do tema Keycloakify?
- [ ] O tema `integra-login` está ativo em algum realm? A mensagem `reauthenticate` ("assinatura do documento") é usada por qual sistema?
- [ ] Usuários desabilitados no Keycloak devem continuar sendo reabilitados a cada login aprovado pelo IBS (`enabled=true` forçado)?
- [ ] Houve migração dos usuários criados antes de 2026-07-17 (username por hash) para o username `idUsuario`?
- [ ] O tráfego Keycloak → IBS usa TLS nos ambientes reais?
- [ ] `KC_CACHE=local` com 2 réplicas em produção é intencional?
- [x] Os testes (`mvn test`) passam? Sim: 20 testes, 0 falhas (2026-10-18, commit `1755591`).
