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
  - arquivos
sources:
  - src/app/components/arquivos/arquivoCtrl.js
  - src/app/components/arquivos/arquivoApi.js
  - src/app/components/arquivos/arquivo.html
  - src/app/index.route.js
---
# Módulo Arquivos — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Tela `/arquivo` (`ArquivoController`, `arquivoAPI`): enviar, completar, filtrar, ativar, inativar e excluir os arquivos/relatórios publicados no Portal. É a tela inicial após o login. Backend correspondente: [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Arquivos e relatórios]].

## Evidências
`arquivoCtrl.js` (504 linhas, lido integralmente), `arquivoApi.js`, trecho de `arquivo.html` (link de download). Chamadas em [[01-Sistemas/Gerenciador-Portal/Frontend/05-API-e-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]].

## Informações confirmadas
- ✅ **Carga inicial** (`main`): anos de referência, contagem de arquivos incompletos e completos, categorias, tipos de referência e lista de arquivos. Ao abrir, a tela mostra o modal `#filtrarInicial` para escolher a categoria.
- ✅ **Envio em duas etapas**: (1) `Upload.upload` para `/arquivo/salvar-arquivo/{login}/{categoria}/{ano}`, um pedido por arquivo selecionado (o `$watch('files')` dispara o envio assim que há arquivos); (2) o arquivo volta **incompleto** e o usuário preenche os metadados no modal (`recuperarArquivo` com `status == false` usa `recuperar-arquivo-incompleto`), que grava com `salvar-informacoes-arquivo` (categoria, prefixo da categoria, tipo e valor de referência, nome original).
- ✅ **Referência**: o valor depende do tipo escolhido (`dataReferencia`, `diaReferencia` ou `periodoReferencia`); o tipo vem de `/arquivo/listar-periodo` e a lista de opções de `/arquivo/listar-referencia?idReferencia`. Ao reabrir um arquivo sem `referencia`, a tela decide pelo texto `dsReferencia`: com `-` é período (tipo posição 7, id 8), senão dia (posição 0, id 1) — **índices e ids fixos no código**.
- ✅ **Filtro**: `POST /arquivo/filtrar-arquivos` com `nome`, `descricao`, `codigoCategoria`, `ano`, `dataReferencia`; o filtro da categoria e do ano também alimenta a URL do próximo upload.
- ✅ **Operações**: ativar, inativar e excluir (um arquivo ou vários marcados) por `POST`; sucesso = corpo `"OK"` (qualquer outro valor mostra erro). Excluir pede confirmação por modal (nome e id guardados em `pegarArquivoParaExcluir`).
- ✅ **Regras de tela por código de categoria** (valores fixos): categorias `43` a `47` ("saibaMais") dispensam o ano (`anoVazio` devolve `false`); `50` a `54` e `56` a `59` usam URL única (`verificarUrlUnico`, sem período). O significado de negócio está na pendência 10 do backend.
- ✅ **Download/abertura**: o link usa `caminhoArquivos.url + '/' + file.url` (`target="_blank"`).
- ✅ Usuário: o login vem de `$localStorage.usuario.login`; `$scope.nomeUsuario = vm.usuario.nome`.

## Falhas e dependências
- Se o usuário não estiver em `$localStorage`, o construtor do controller lança `TypeError` (`vm.usuario.nome`), e a tela fica em branco (sem guarda de rota).
- Se não houver categoria ou ano filtrados, a URL de upload leva `null` no caminho (`/null/null`); o comportamento do backend nesse caso não foi verificado.
- Há `console.log` com a lista retornada por `filtroInicial` (volume de dados no console) e código morto (`$("#modal").click(...)` sem efeito; bloco `vm.arquivos.length = 0` comentado).
- `qtdArquivosCompletos(vm.filtroCategoria)` é chamada com argumento que o serviço ignora.

## Inferências e limitações
- 🔶 "Incompleto" significa arquivo já enviado, sem metadados; coerente com o backend, mas o estado exato não foi validado.
- ❓ HTML do formulário (campos obrigatórios, máscaras) não foi lido; não se sabe quais validações a tela aplica antes de salvar.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Backend: Arquivos e relatórios]] · [[01-Sistemas/Gerenciador-Portal/Backend/04-Fluxos/Gerenciador-Portal-Backend-Fluxo-Cadastro-de-Arquivo|Backend: fluxo de cadastro]] · [[01-Sistemas/Gerenciador-Portal/Frontend/04-Fluxos/Gerenciador-Portal-Frontend-Fluxo-Login-e-Sessao|Fluxo de login e sessão]]

## Pendências e próximo passo
- Ler `arquivo.html` para as validações do formulário (pendência 6 do [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Pendencias|controle]]).
