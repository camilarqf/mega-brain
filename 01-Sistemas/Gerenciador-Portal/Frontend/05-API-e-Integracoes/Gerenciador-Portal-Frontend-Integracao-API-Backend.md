---
type: integration
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
consumer: Gerenciador-Portal
provider: Gerenciador-Portal
tags:
  - gerenciador-portal
  - frontend
  - integracao
  - api-rest
sources:
  - src/app/token-interceptor.js
  - src/app/index.module.js
  - src/app/components/login/loginAPI.js
  - src/app/components/arquivos/arquivoApi.js
  - src/app/components/imagem-portal/imagemApi.js
  - src/app/components/exclusoes-medida-protetiva/exclusoesMedidaProtetivaApi.js
  - config.json
---
# Integração Gerenciador-Portal Frontend → Backend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Gerenciador-Portal` (`gerenciador-portal-frontend`) | `Gerenciador-Portal` (`gerenciador-portal-backend`, mesmo sistema) | HTTP/JSON e *multipart* (`$http`, `Upload.upload`), no navegador | [[01-Sistemas/Gerenciador-Portal/Backend/05-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Catálogo de endpoints do Backend]]; cabeçalho `x-client-id` | saída (navegador → API) |

Os dois lados pertencem ao mesmo sistema (`Gerenciador-Portal`); a nota fica no componente que contém o cliente (seção 7 do `BRAIN-RULES.md`).

## Evidências
`token-interceptor.js`, `index.module.js`, `*Api.js` de cada tela, `config.json` (chave `api`).

## Informações confirmadas
- ✅ **Base**: constante `api.url` do perfil (`/api` relativo em homologação e produção; endereço absoluto no `local`). Todo serviço de API monta `api.url + '/<caminho>'`.
- ✅ **Cabeçalho `x-client-id`**: o interceptor gera um UUID (`crypto.randomUUID` ou fallback com `Math.random`) **uma vez por carregamento da página** (variável em memória, não persistida) e o envia em toda requisição cuja URL começa por `api.url`. Também publica `window.GerenciadorPortalClient` (`getClientId`, `getHeaders`, `CLIENT_ID_HEADER`). O backend exige o cabeçalho (qualquer valor não vazio) e responde `400` sem ele ([[01-Sistemas/Gerenciador-Portal/Backend/05-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Backend]]); o frontend e o contrato **coincidem**.
- ✅ **Nenhum token de SSO é enviado**: não há `Authorization`, cookie nem `withCredentials` (a linha está comentada). A única credencial é o `POST /login` (`{login, senha}`), cuja resposta (`UsuarioDTO`) é guardada em `$localStorage.usuario`.
- ✅ **Identidade para auditoria**: o login do usuário é passado pelo cliente em cada operação de escrita, como `usuarioLogado` (arquivos e imagens; na URL ou na query) ou `usuarioAutenticado` (medida protetiva). O backend usa só para auditoria (🔶, nota do backend).
- ✅ **Erros**: sem tratamento global. Cada controller mostra um aviso genérico ou ignora; `401`/`403` não deslogam. O login exibe `error.data.mensagem` ou "Não foi possível realizar a autenticação.".
- ✅ **Sem `timeout`, retry ou cache** configurados.
- ✅ **Uploads**: arquivos e imagens vão como `multipart` ao backend (`/arquivo/salvar-arquivo/…`, `/imagem/salvar…`); o frontend **não** fala com o MinIO para gravar. Os caminhos `caminhoArquivos`/`caminhoImagens` servem para **exibir/baixar** os objetos já gravados (por exemplo links e miniaturas nas telas).
- ✅ **Expiração de cache**: após ocultar ou excluir servidor em medida protetiva, o frontend chama `GET /servidores-medida-protetiva/expirar-cache` e só registra erro no console.

## Falhas e dependências
- A indisponibilidade da API deixa as telas vazias, sem mensagem (várias chamadas `.then` sem tratamento de erro).
- Como o `x-client-id` é gerado no navegador, ele **não autentica** nada ([[01-Sistemas/Gerenciador-Portal/Frontend/06-Seguranca/Gerenciador-Portal-Frontend-Seguranca-e-Sessao|Segurança e sessão]]).
- O `api.url` precisa estar acessível pelo mesmo host (perfis relativos) ou liberar CORS (perfil `local`).

## Inferências e limitações
- 🔶 Em homologação e produção, `/api` e `/arquivos/<bucket>` relativos indicam um proxy reverso à frente (🔶 possivelmente o [[01-Sistemas/INGRESS-CGDF/INGRESS-CGDF-Index|INGRESS-CGDF]]); não confirmado.
- ❓ `apiPortal` e `apiSuperbusca` existem nos perfis e são injetadas em `exclusoesAPI`, mas **nenhuma chamada** a elas foi encontrada no código lido (ver pendências).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Frontend/05-API-e-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|Integração do Backend com o SSO]] · [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis]]

## Pendências e próximo passo
- Confirmar o proxy reverso e se `apiPortal`/`apiSuperbusca` são usadas fora do código lido.
