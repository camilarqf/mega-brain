---
type: integration
aliases:
  - "Frontend — integrações externas"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: inferido
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
consumer: Portal-Transparencia
sources:
  - src/app/config.js
  - config.json
  - src/index.html
  - src/app/index.module.js
  - src/app/components/super-busca/super-busca.service.js
  - src/app/components/url-arquivos/arquivo.url.service.js
  - src/app/components/quadros-tematicos/quadros-tematicos.controller.js
  - src/app/components/compartilhado/services/setor-desejado/setor-desejado.service.js
---

# Frontend — integrações externas

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

> Endereços, hosts e chaves **não** são reproduzidos (regra do cofre).

## Visão geral
| Consumidor | Provedor (ID) | Tecnologia | Contrato | Direção | Confirmação |
|---|---|---|---|---|---|
| frontend | serviço de busca (`apisuperbusca`) — provedor ❓ | HTTP GET JSON (direto do navegador) | `/indice/{pagina}/{termo}`, `/indice-cpf/…`, `/indice-cod-credor/…`; cabeçalho de resposta `x-count` | saída | ✅ cliente; ❓ provedor |
| frontend | objetos em armazenamento (`caminhoImagens`, `caminhoArquivos`, `caminhoDadosAbertos`) — 🔶 `MinIO-CGDF` | HTTP GET de URL composto | `{prefixo}{caminho}` onde o caminho vem da API | saída (navegador baixa objetos) | ✅ cliente; 🔶 provedor |
| frontend | "gerenciador" (`apiGerenciador`) — ❓ | URL base de links/imagens | Quadros Temáticos e Setor Desejado | saída | ✅ uso; ❓ provedor |
| frontend | `Google-Analytics` | `gtag.js` + `angulartics.google.analytics` | evento de página | saída | ✅ |

## Evidências
Commit `dca3e933`. `config.json`/`config.js` (constantes), `super-busca.service.js`, `arquivo.url.service.js`, `quadros-tematicos.controller.js`, `setor-desejado.service.js`, `src/index.html` (script `gtag`, fontes e *scripts* de terceiros por CDN).

## Informações confirmadas
- ✅ **Super busca**: `SuperBuscaService.buscar` decide o endpoint pelo formato do termo: texto livre → `/indice`; CPF válido → `/indice-cpf` e `/indice-cod-credor`; CNPJ válido → `/indice-cod-credor`; os dígitos do CPF/CNPJ vão **no caminho da URL**. O cabeçalho `x-count` soma o total. O `x-client-id` não é enviado a este host.
- ✅ **Objetos**: `ArquivoUrlService` expõe `IMAGENS`, `ARQUIVOS` e `DADOS_ABERTOS` a partir das constantes. `ArquivoUrlController` (`/url-arquivo?query=…[&exercicio=…]`) mapeia 9 consultas para `codCategoria`, chama `GET /arquivos/url-ultimo-arquivo-categoria[-exercicio]/…` na API e **redireciona o navegador** para `ARQUIVOS + urlArquivo`. Quadros Temáticos monta `IMAGENS + caminhoImagem`.
- ✅ **Google**: `index.html` carrega `gtag.js` (ID de medição omitido) e `angulartics`; também há `google-site-verification`/arquivo de verificação na raiz. O Backend tem consulta própria à API de relatórios do Google ([[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integrações do Backend]]), consumida aqui via `/analytics/*` (ver [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo]]).
- ✅ **Mapas**: Leaflet com arquivos locais (`src/assets/scriptsleaflet`, `delimitacao_ras.json`, `localizacoes_ras.json`); sem chamada a provedor de *tiles* identificada nos serviços lidos (❓ não verificado na diretiva do mapa).
- ✅ **Ativos de terceiros por CDN** no `index.html` (fontes e scripts); lista completa não transcrita.

## Falhas e dependências
- Falha do serviço de busca derruba só a tela de busca; falha do armazenamento quebra downloads e imagens; não há *fallback*.
- Chamadas diretas do navegador exigem CORS nesses hosts; no perfil `homologacao` elas passam por caminhos relativos (`/api-super-busca`, `/arquivos/...`), o que sugere proxy (🔶).

## Inferências e limitações
- 🔶 O armazenamento dos objetos é o MinIO tratado em [[01-Sistemas/MinIO-CGDF/MinIO-CGDF-Index|MinIO-CGDF]] e no Backend (`/storage/url`, `feature/refatoracao-acesso-minio`); só os nomes dos *buckets* (`portal-imagens`, `portal-arquivos`, `portal-dados-abertos`) no sufixo das URLs sugerem isso. Os commits recentes do frontend (`cc44e3f1`, `21068a92`) alteraram apenas `src/app/config.js`.
- ❓ Dono do serviço `apisuperbusca` e do "gerenciador" (o usuário informou em 2026-10-21, sem evidência no código, que o `gerenciador` consome endpoints de armazenamento do Backend; aqui ele aparece como destino de links/imagens).
- Esta nota registra integrações do **frontend com terceiros**; a integração principal está em [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API do Backend]].

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis]] · [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]] (#2 a #5).
