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
  - imagens
sources:
  - src/app/components/imagem-portal/imagemCtrl.js
  - src/app/components/imagem-portal/imagemApi.js
  - src/app/components/imagem-portal/imagem.html
  - src/app/components/imagem-portal/modal-imagem-slideshow.html
  - src/app/components/imagem-portal/modal-imagem-painelSetores.html
---
# Módulo Imagens do Portal — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Tela `/imagem-portal` (`ImagemController`, `imagemAPI`): gerenciar as imagens do slideshow e dos painéis de setores do Portal, com ordem de exibição, ativação e imagem de fundo do painel. Backend: [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Imagens-do-Portal|Imagens do portal]].

## Evidências
`imagemCtrl.js` (406 linhas, lido integralmente), `imagemApi.js`, e as linhas de `imagem.html`/modal que montam `<img>` com `caminhoImagens`. Os demais trechos de HTML dos modais não foram lidos.

## Informações confirmadas
- ✅ **Duas categorias com códigos fixos**: `55` = slideshow, `56` = painéis de setores (`COD_IMAGEM_SLIDESHOW`, `COD_IMAGEM_PAINEIS`); os botões da tela só trocam `vm.categoriaImagem` antes do upload.
- ✅ **Envio**: vários arquivos de uma vez usam `POST /imagem/salvar-sem-ordenar/{login}/{categoria}` por arquivo e, quando todos terminam, `PUT /imagem/ordenar-prioridades-imagens/{categoria}`; um arquivo só usa `POST /imagem/salvar/{login}/{categoria}`. O contador `uploadedImages` só chega ao total se **todos** os envios tiverem sucesso: com uma falha a reordenação não ocorre.
- ✅ **Limite de tamanho**: o aviso informa "máx. 1MB" por imagem (`$scope.imagensInvalidas` com `$error == 'maxSize'`); o valor do limite está no HTML do campo (não lido), não neste controller.
- ✅ **Edição** em modal (`salvar-imagem`, `PUT`): descrição, e `codFuncao` quando é painel de setor (lista de `listar-funcoes-paineis`). Após salvar, recarrega a imagem e as listas.
- ✅ **Imagem de fundo** do painel: `POST /imagem/salvar-imagem-background/{login}/{idImagem}`, depois salva as informações com a função escolhida; exclusão por `DELETE /imagem/excluir-background`.
- ✅ **Ordem**: `mover-prioridade-acima` e `mover-prioridade-abaixo` (corpo = a imagem) e recarga das listas.
- ✅ **Ativar, desativar e excluir** por `POST`/`DELETE`; sucesso = corpo `"OK"` (exceto ordenar, que não verifica). O estilo da miniatura muda por classe CSS `grid-item-ativo`/`grid-item-inativo`.
- ✅ **Exibição**: `src = caminhoImagens.url + '/' + imagem.url`.
- ✅ Modais do `angular-strap` (`$modal`): slideshow, painel de setores, exclusão de imagem e exclusão de fundo, com `backdrop: 'static'`; o controller guarda o modal atual para voltar depois da exclusão.

## Falhas e dependências
- `recuperarImagem` decide o modal por `vm.categoriaImagem == 55` (valor fixo); abrir uma imagem sem ter escolhido a categoria cai no modal de painel.
- `$watch('imagens')` dispara `salvarImagens` a cada mudança do modelo, inclusive na inicialização (a função ignora `null`).
- O ramo `salvar-sem-ordenar` + `ordenar-prioridades` não é atômico (a pendência 6 do backend questiona o uso de `salvar-sem-ordenar`).
- O serviço expõe `recuperarImagemBackgroundPorPainelId`, que nenhum controller usa.

## Inferências e limitações
- 🔶 Os códigos 55/56 coincidem com as categorias de imagem do módulo de arquivos do backend (pendência 10); não confirmado.
- ❓ Como o Portal usa a `prioridade` e `codFuncao` ao exibir.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Imagens-do-Portal|Backend: Imagens]] · [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Ler os HTML dos modais para validações e limites ([[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Pendencias|controle]]).
