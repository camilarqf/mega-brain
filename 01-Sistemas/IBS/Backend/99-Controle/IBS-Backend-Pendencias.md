---
type: analysis-log
aliases:
  - "Pendências — IBS Backend"
system: IBS
component: Backend
repository: identity-broker-service
status: pendente
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
---
# Pendências — IBS Backend

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]] · Relacionado: [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Registro-de-Analise|Registro de análise]]

## Objetivo
Listar lacunas, conflitos e riscos identificados, sem resolvê-los por suposição.

## Evidências
- Lotes 0 a 4, commit `cf0959ae140844926755b218a8452d34f3970ed3`.

## Informações confirmadas
- ✅ Credenciais em texto claro no arquivo local `src/main/resources/application-local.properties` (ignorado pelo Git), incluindo linhas comentadas de outros ambientes. Valores não registrados. Recomendação: rotacionar e remover.
- ✅ O cliente Keycloak envia `X-IBS-Secret` e `X-Correlation-ID`; o IBS não valida segredo, não há Spring Security e lê `X-Correlation-Key` ([[01-Sistemas/IBS/Backend/08-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Segurança]]).
- ✅ Cache de fonte recente sem limite; erros sem handler resultam em 500 ([[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Debitos-Tecnicos|Débitos técnicos]]).
- ✅ `UsuarioControllerTest` usa a rota `/usuarios/busca` (a real é `/usuarios/buscar`): 4 testes falham; `ResolverFontesPorOrgaoIntegrationTest` exige banco real ([[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Testes-e-Cobertura|Testes]]).

## Inferências e limitações
- ❓ Dono do IBS, SLA e consumidores além do Keycloak (inclusive de `/usuarios/*`, `ResolverFontesPorOrgaoHandler` e `ObterFontesPorSufixoHandler`).
- ❓ Dono e hosts dos ADs (`AD-LDAP`) e dono do banco `DB_SIP` (`SIP-SQLServer`).
- ❓ Como usuário e senha do banco chegam ao contêiner em dev, hom e prod.
- ❓ Se o pipeline executa os testes e se há proteção de rede (ingress, mTLS) para o IBS.
- 🔶 Intenção de negócio de continuar os binds após credencial inválida (o README diz "não realizar tentativa cega").
- 🔶 OpenAPI/Swagger publicados e coerção de `idOrgao` textual, não verificados em execução.
- 🔶 Cobertura parcial: `LoginContextualizado` e o `LoginUsuario` de `fonteautenticacao` não lidos; testes lidos por amostra.
- Arquivos não versionados `ANALISE_CLAIMS_E_DISPONIBILIDADE.md` e `docs/contratos-api-ibs.md`: ignorados por pedido do usuário; podem ser confrontados com o código se ele autorizar.

## Relacionamentos
- [[01-Sistemas/IBS/IBS-Index|IBS]]

## Pendências e próximo passo
- Próximo passo exato: ver [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Registro-de-Analise|Registro de análise]].
