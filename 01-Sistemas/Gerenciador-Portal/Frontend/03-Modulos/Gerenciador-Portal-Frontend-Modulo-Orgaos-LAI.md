---
type: module
aliases:
  - "Módulo Órgãos LAI — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/app/components/paginas-lai/orgaoCtrl.js
  - src/app/components/paginas-lai/orgaoApi.js
  - src/app/index.route.js
---
# Módulo Órgãos LAI — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Tela `/orgaos-lai` (`OrgaoController`, `orgaoAPI`): cadastro, edição e exclusão dos órgãos da Lei de Acesso à Informação exibidos no Portal. Backend: [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Conteúdo do portal]].

## Evidências
`orgaoCtrl.js` (107 linhas) e `orgaoApi.js` lidos integralmente; HTML não lido.

## Informações confirmadas
- ✅ CRUD em `/orgao`: `POST` (novo), `GET` (lista), `PUT` (editar), `DELETE ?id`. O objeto `orgao` é o do formulário `formOrgao`; seus campos estão no HTML, **não** no controller.
- ✅ **Edição na mesma tela**: `pegarOrgaoParaEdicao` copia o órgão para o formulário (`Object.assign`) e liga `vm.editando`; ao concluir, `limparFormulario` zera o formulário (`$setPristine`, `$setUntouched`) e recarrega a lista.
- ✅ Exclusão com `confirm()`. Editar verifica o corpo `"OK"`; salvar e excluir só mostram sucesso quando a requisição não é rejeitada.
- ✅ Paginação no cliente.

## Falhas e dependências
- `vm.orgaos` é iniciado como `{}` e depois recebe um array; `totalDeOrgaos` só existe após `listar`.
- Sem tratamento de erro nas chamadas (aviso de falha só em `editar` com corpo diferente de `"OK"`).

## Inferências e limitações
- ❓ Campos de `OrgaoLAI` e regras de validação (vêm do HTML e do backend; ver módulo do backend).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Backend: Conteúdo do portal]] · [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Nenhum específico.
