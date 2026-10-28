---
type: security
aliases:
  - "Segurança e sessão — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
tags:
  - autenticacao
sources:
  - src/app/token-interceptor.js
  - src/app/index.route.js
  - src/app/index.module.js
  - src/app/components/login/loginCtrl.js
  - src/app/components/navbar.controller.js
  - src/app/components/exclusoes-medida-protetiva/exclusoesMedidaProtetivaApi.js
  - .bowerrc
  - config.json
---
# Segurança e sessão — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar como o frontend autentica, guarda a sessão e protege (ou não) as telas, separando fatos de recomendações. Sem segredos.

## Evidências
Os arquivos de `sources`. Leitura estática; HTML e estilos não foram lidos em detalhe. Contraparte: [[01-Sistemas/Gerenciador-Portal/Backend/08-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Segurança do Backend]].

## Informações confirmadas
- ✅ **Autenticação**: formulário próprio → `POST /login` ([[01-Sistemas/Gerenciador-Portal/Frontend/05-Fluxos/Gerenciador-Portal-Frontend-Fluxo-Login-e-Sessao|fluxo]]). A senha é enviada apenas nessa chamada e **não** é guardada pelo frontend.
- ✅ **Sessão**: a resposta do login fica em `$localStorage.usuario` (`localStorage`, sem expiração, legível por qualquer script da origem). Não há token, cookie de sessão nem renovação.
- ✅ **Sem guarda de rota**: todas as rotas abrem sem login; só o logout apaga a sessão local.
- ✅ **Sem `Authorization`**: a API é chamada com `x-client-id` (UUID gerado no navegador a cada carregamento). Isso **não é autenticação**: qualquer cliente pode enviar qualquer valor.
- ✅ **Identidade nas operações**: o frontend envia o login como `usuarioLogado`/`usuarioAutenticado` (URL ou query) e o backend o aceita sem conferir (🔶 só auditoria). Quem altera o `localStorage` ou chama a API direto escolhe o nome que fica registrado.
- ✅ **Autorização**: o frontend não esconde nem desabilita telas por perfil; o único filtro de acesso (órgão e unidades) está no login do backend.
- ✅ **Sem tratamento de `401`/`403`**: o interceptor só rejeita; a UI não redireciona ao login.
- ✅ **Dados sensíveis na tela de medida protetiva**: nome e identificador de servidores ocultos trafegam e aparecem sem controle de perfil no frontend.
- ✅ Dados pessoais/segredos no código: nenhum segredo lido; `config.json` e `src/app/config.js` (versionado) contêm **endereços internos** de ambientes (omitidos nestas notas).
- ✅ `.bowerrc` com `strict-ssl: false` desliga a verificação de TLS na instalação das dependências do build.
- ✅ Chamadas a `console.log`/`console.error` expõem dados da lista de arquivos (`filtroInicial`) e o objeto de erro do login no console do navegador.
- ✅ Proteção contra XSS: `ngSanitize` está carregado; a tela de textos usa `textAngular` (editor HTML), mas não foi lido como o HTML é renderizado (❓).

## Falhas e dependências
Consequência conjunta com o backend: sem validação de token no servidor, **qualquer pessoa com acesso de rede** à API (e um `x-client-id` qualquer) executa as operações de escrita; o frontend não acrescenta nenhuma barreira ([[01-Sistemas/Gerenciador-Portal/Backend/08-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|ver Backend]]). Mitigação depende de rede restrita/gateway (pendência 3 do backend).

## Inferências e limitações
- 🔶 **Recomendações** (não são fatos): validar token no backend e enviá-lo pelo frontend (`Authorization: Bearer`), guarda de rota e tratamento de `401`, expiração de sessão, `sessionStorage` ou cookie `HttpOnly`, remover `console.log`, tirar `config.js` do controle de versão, restabelecer o TLS no Bower.
- ❓ Cabeçalhos de segurança (CSP, HSTS) dependem do servidor web, que não está no repositório.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|SSO (Backend)]] · [[01-Sistemas/Gerenciador-Portal/Frontend/09-Qualidade/Gerenciador-Portal-Frontend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Integracao-API-Backend|Integração com o Backend]]

## Pendências e próximo passo
- Confirmar com o time o desenho pretendido da autenticação (a refatoração `sessaoSso` não versionada) e a proteção de rede da API.
