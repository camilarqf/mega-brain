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
  - palavras-chave
sources:
  - src/app/components/palavras-chave/palavraCtrl.js
  - src/app/components/palavras-chave/palavraApi.js
  - src/app/index.route.js
---
# Módulo Palavras-chave — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Telas `/palavras-chave` (lista e inclusão) e `/editar-palavra` (edição), ambas com `PalavraController` e `palavraAPI`: manter as palavras-chave de busca do Portal. Backend: [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Conteúdo do portal]] (grava no MongoDB; [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MongoDB|integração]]).

## Evidências
`palavraCtrl.js` (127 linhas) e `palavraApi.js` lidos integralmente; HTML não lido.

## Informações confirmadas
- ✅ **Campos** da palavra: `_id`, `palavraChave`, `urlConsulta`, `descricao` (identificador do MongoDB).
- ✅ **Operações**: listar (`GET /palavra/listar`), salvar, editar e excluir (`POST`; a exclusão envia a palavra inteira no corpo). A lista é recarregada ao fim.
- ✅ **Edição por query string**: `pegarPalavraParaEdicao` navega para `/editar-palavra/` e passa `_id`, `palavraChave`, `urlConsulta` e `descricao` em `$location.search()`; a tela de edição lê esses parâmetros (`definirPalavraParaEdicao`). Se a página de edição for aberta sem eles, os campos ficam vazios.
- ✅ **Salvar edição** só chama a API se `_.isEqual(editada, original)` for falso; depois volta para `/palavras-chave`. Sucesso = corpo `"OK"`.
- ✅ **Exclusão** pede `confirm()`; não verifica o corpo da resposta e sempre mostra "excluída com sucesso" quando a requisição não é rejeitada.
- ✅ Paginação no cliente (`dirPagination`).

## Falhas e dependências
- A navegação para `/palavras-chave` ocorre **antes** do retorno do `editar`, e o `listarPalavras` também; a lista pode mostrar o estado anterior.
- `editarPalavra` deixa `console.log` de depuração (inclui a frase "To indo pra API").
- Os dados da palavra viajam na URL de edição (sem dado pessoal esperado; não verificado).

## Inferências e limitações
- 🔶 A `urlConsulta` aponta para uma consulta do Portal; a relação com o serviço de busca (`apiSuperbusca`) não aparece no frontend (ver [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MongoDB|MongoDB]]).
- ❓ Validações do formulário (HTML não lido).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Backend: Conteúdo do portal]] · [[01-Sistemas/Gerenciador-Portal/Frontend/05-API-e-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Nenhum específico.
