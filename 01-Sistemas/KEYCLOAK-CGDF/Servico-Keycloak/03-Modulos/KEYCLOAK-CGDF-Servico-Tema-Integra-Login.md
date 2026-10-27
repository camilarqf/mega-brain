---
type: module
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - tema
  - keycloakify
  - login
sources:
  - integra-login/login/theme.properties
  - integra-login/login/login.ftl
  - integra-login/login/resources/dist/index.html
  - integra-login/login/messages/messages_pt_BR.properties
---
# Tema de login `integra-login`

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Build-e-Deploy|Build-e-Deploy]]

## Objetivo
Documentar o tema de login versionado em `integra-login/login/` (194 arquivos rastreados). Análise por inventário e leitura de amostras; o código compilado não foi lido em detalhe.

## Evidências
- `theme.properties`, `login.ftl` (cabeçalho), `resources/dist/index.html`, histórico git de `integra-login`.

## Informações confirmadas
- ✅ Tema gerado pelo **Keycloakify 11.9.2** (`login.ftl`: `themeName` `integra-login`, `themeVersion` `0.0.0`), com interface Angular compilada em `resources/dist/` (ponto de entrada `<kc-root>`, módulo `index-*.js`, páginas `keycloakify-angular-login-pages-*`).
- ✅ `theme.properties`: `parent=keycloak`, `darkMode=true`, 30 locales (`ar` … `zh-TW`, inclui `pt` e `pt-BR`).
- ✅ Cada página do Keycloak tem um `.ftl` que injeta o `kcContext` e carrega o bundle; recursos padrão (PatternFly, jQuery, JS de WebAuthn/OTP) ficam em `resources/` e `resources-common/`.
- ✅ Personalização identificável: logotipo `logo-integra-*.png` e mensagem `reauthenticate` em `pt_BR`/`pt` — "Para efetivar a assinatura do documento, é necessária a reautenticação por senha." (commit `b21d1f8`, 2026-01-15).
- ✅ Histórico: tela de login ajustada para a versão 25 do Keycloak (`5699742`, 2025-08-14).

## Inferências e limitações
- ❓ O `Dockerfile` não copia `integra-login/`; não há evidência de como o tema chega ao Keycloak nem se está ativo em algum realm.
- ❓ Código-fonte do Keycloakify (Angular) não está neste repositório; só o `dist` minificado.
- 🔶 A mensagem de reautenticação sugere uso na assinatura de documentos por algum sistema (talvez o SICI), sem evidência da relação.
- Páginas e componentes não foram lidos individualmente (cobertura parcial).

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/09-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Localizar o repositório-fonte do tema e como ele é implantado.
