---
type: technical-debt
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - debitos
  - riscos
sources:
  - README.md
  - .docker/Dockerfile
  - .jenkins-pipelines/deployment.params.yml
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsApiClient.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsRestClient.java
---
# Débitos técnicos e riscos

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]]

## Objetivo
Separar **fatos** (✅ verificados) de **recomendações**. Nada aqui foi corrigido no código.

## Evidências
- Arquivos em `sources` e notas citadas em cada item.

## Informações confirmadas (fatos)
1. ✅ **README ≠ código no 403:** README diz "401/403 → `invalid_grant`"; o cliente só trata 401 assim, e 403 vira `server_error` (teste `loginMapeia403ComoErroTecnico`). Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]].
2. ✅ **Versões divergentes:** README cita Keycloak 26.3.2 e jar `1.0-SNAPSHOT`; `pom.xml` compila contra 26.3.2 (jar `1.0.0`); a imagem de runtime é `keycloak:25.0.2`. Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Stack-e-Dependencias|Stack-e-Dependencias]].
3. ✅ **Nome do jar fixo no Dockerfile** (`ibs-keycloak-extension-1.0.0.jar`): mudar a versão do `pom.xml` quebra o build da imagem.
4. ✅ **Testes pulados na imagem** (`-DskipTests`).
5. ✅ **Tema não copiado pelo Dockerfile** e sem código-fonte no repositório. Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Modulos/KEYCLOAK-CGDF-Servico-Tema-Integra-Login|Tema-Integra-Login]].
6. ✅ **Código morto:** `IbsRestClient` não é usado; `IbsRestClientTest` testa `IbsApiClient`. Metadados duplicados entre `IbsAuthenticator` e `IbsAuthenticatorFactory`. Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Arquitetura-SPI|Arquitetura-SPI]].
7. ✅ **Logs com identificadores pessoais:** `login`, `idOrgao`, `correlationKey` e hash de usuário em nível INFO, a cada login e a cada emissão de token.
8. ✅ **Usuário desabilitado é reabilitado** a cada login aprovado pelo IBS (`enabled=true`). Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Normalizacao-do-Usuario|Regra-Normalizacao-do-Usuario]].
9. ✅ **Sem retry/circuit breaker** na chamada ao IBS; timeout único de 3 s por padrão.
10. ✅ **Higiene do repositório:** `.idea/` versionado; sem `.gitignore` na raiz (o log `hs_err_pid*.log` aparece como não rastreado); `node_modules` do PatternFly/jQuery versionados em `resources-common`.
11. ✅ **Testes sem medição de cobertura** e sem testes de configuração (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Qualidade/KEYCLOAK-CGDF-Servico-Testes-e-Cobertura|Testes-e-Cobertura]]).

## Inferências e limitações
- 🔶 `KC_CACHE=local` com 2 réplicas em produção pode quebrar sessões entre réplicas (não verificado).
- ❓ `health_check_endpoint: healthcheck` pode não existir no Keycloak.

## Recomendações (não são fatos)
- Alinhar README, `pom.xml` e `Dockerfile` (versões e tratamento do 403); parametrizar o nome do jar com `ARG`.
- Executar os testes no pipeline; remover `IbsRestClient` ou passar a usá-lo; reduzir o nível de log de dados pessoais.
- Documentar/automatizar a implantação do tema e adicionar `.gitignore`.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/06-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Priorizar com o time; itens 1, 2 e 5 também estão em [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]].
