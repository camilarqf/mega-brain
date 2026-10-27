---
type: module
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - frontend
  - modulo
  - cargas
sources:
  - src/app/components/carga-portal/cargaCtrl.js
  - src/app/components/carga-portal/cargaApi.js
  - src/app/components/carga-portal/carga.html
---
# Módulo Cargas — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Tela `/carga-portal` (`CargaController`, `cargaAPI`): consulta **somente leitura** ao controle de cargas do Portal, com filtros e cartões de contagem por status. Backend: [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Cargas|Cargas]].

## Evidências
`cargaCtrl.js` (106 linhas) e `cargaApi.js` lidos integralmente; `carga.html` não foi lido.

## Informações confirmadas
- ✅ Ao abrir, a tela busca **todas as cargas sem filtro** (`recuperarCarga()`) e as quantidades por status.
- ✅ **Filtros**: data, status, esquema e tabela, enviados como `dataCarga`, `statusCarga`, `esquemaCarga`, `tabelaCarga` em `GET /carga/listar-cargas`. Com algum filtro, `mostrarBtnExcluirFiltro` fica `true`; o resultado vazio mostra "Ops! Nenhum resultado encontrado :(".
- ✅ **Cartões**: quatro, montados **por posição** do vetor de `listar-quantidade-status`: `[0]` Atualizado, `[1]` Erro, `[2]` Sem Alteração (nome `SEM ALTER.`), `[3]` Realizado. Se o backend mudar a ordem ou o tamanho, os cartões ficam trocados ou `undefined`.
- ✅ Listas de status e de esquemas vêm de `listar-status` e `listar-esquema`; paginação no cliente (`dirPagination`, `pagination.current`).
- ✅ Nenhuma operação de escrita neste módulo; não usa o usuário logado.

## Falhas e dependências
- `vm.retornarListaDeCargas` chama `cargaAPI.retornarListaDeCargas`, **inexistente** (defeito latente; a função não é usada pelo controller).
- Filtro e paginação no cliente: a tela carrega a lista completa de cargas na abertura (volume desconhecido).

## Inferências e limitações
- 🔶 O significado de `SEM ALTER.`/`REALIZADO` depende do backend (pendência 9 do backend).
- ❓ Quais funções (`listarStatus`, `listarEsquema`) são disparadas pelo HTML (não há `ng-init` no código; o HTML não foi lido).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Cargas|Backend: Cargas]] · [[01-Sistemas/Gerenciador-Portal/Frontend/05-API-e-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Ler `carga.html` para confirmar quais chamadas o HTML dispara.
