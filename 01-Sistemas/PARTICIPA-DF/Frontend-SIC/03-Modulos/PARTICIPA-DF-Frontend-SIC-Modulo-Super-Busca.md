---
type: module
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - modulo
  - busca
sources:
  - app/super-busca/super-busca.ctrl.js
  - app/super-busca/super-busca.html
---

# Frontend SIC — super-busca

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Detalhe do pedido: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Caixa-de-Entrada-e-Detalhamento|Caixa de entrada e detalhamento]]

## Objetivo
Documentar a busca livre por pedidos e solicitantes (`/super-busca`), com item de menu visível a todo usuário autenticado (a rota não tem guarda).

## Evidências
`superBuscaCtrl` e `super-busca.html` (102 linhas), commit `5518a81`.

## Informações confirmadas
1. ✅ `buscar()`: se há termo, `POST acesso-informacao/pedido/consultar-por-termo` (`{termo}`); a resposta (`Rows`) é exibida como resultado. Sem termo, não faz nada. O controller chama `buscar()` ao carregar.
2. ✅ `detalhar(identificador)`: repete a busca usando o `Id` do identificador clicado.
3. ✅ `detalharPedido(pedido)`: para **cada linha** de `response.Rows`, chama `POST acesso-informacao/pedido/permite-detalhar` com o pedido clicado; se a resposta for `true`, navega para `/detalhar-pedido/{Id}`.
4. ✅ `atualizarUsuario(item)`: escolhe PF ou PJ pelo tamanho de `Identificador` (14 caracteres → PF, o CPF formatado; outro → PJ) e navega para `/atualizar-<tipo>/{Id}/<returnRoute>`.
5. ✅ `limpar()` zera termo e resultado.

## Inferências e limitações
- ✅ **Defeito**: `detalharPedido` percorre `response.Rows` com `forEach` e dispara `permite-detalhar` **uma vez por linha**, sempre para o mesmo `pedido`; o número de chamadas é igual ao de resultados da página.
- 🔶 A decisão PF/PJ pelo tamanho depende de o identificador vir **com máscara**; sem máscara (CPF 11, CNPJ 14) o CNPJ seria tratado como PF.
- ❓ O que `consultar-por-termo` pesquisa (protocolo, nome, CPF/CNPJ, texto) está no backend.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Conta-por-Operador|Conta-por-Operador]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Confirmar no backend o escopo de `consultar-por-termo`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
