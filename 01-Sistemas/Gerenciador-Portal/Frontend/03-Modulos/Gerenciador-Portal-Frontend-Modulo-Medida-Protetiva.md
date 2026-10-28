---
type: module
aliases:
  - "Módulo Medida Protetiva — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/app/components/exclusoes-medida-protetiva/exclusoesMedidaProtetivaCtrl.js
  - src/app/components/exclusoes-medida-protetiva/exclusoesMedidaProtetivaApi.js
  - src/app/components/exclusoes-medida-protetiva/exclusoes-medida-protetiva.html
---
# Módulo Medida Protetiva — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Tela `/exclusoes-medida-protetiva` (`ExclusoesMedidaProtetivaController`, `exclusoesAPI`; módulo `gerenciadorPortal.exclusoes`): pesquisar um servidor pelo nome em seis consultas do Portal e **ocultá-lo** delas (medida protetiva), ou remover o registro de ocultação. Backend: [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Medida protetiva]].

## Evidências
`exclusoesMedidaProtetivaCtrl.js` (206 linhas) e `exclusoesMedidaProtetivaApi.js` lidos integralmente; início do HTML (título e campo de busca).

## Informações confirmadas
- ✅ **Seis consultas** (configuração em `vm.consultas`), cada uma com seu sufixo de endpoint: Remuneração dos Servidores (`/remuneracao`), Servidores por Órgão (`/por-orgao`), Despesas (`/despesas`), Cadastro de Expulsões (`/cadastro-expulsoes`), Conselheiros (`/conselheiros`) e Conselhos (`/conselhos`). Cada uma guarda a lista pesquisada, a lista já oculta, a paginação e flags de busca.
- ✅ **Carga inicial** (`init`): lista os servidores já ocultos de cada consulta (`GET /servidores-medida-protetiva{consulta}`).
- ✅ **Pesquisa**: um campo de nome (obrigatório) dispara `GET /servidores{consulta}?nomeServidor` **nas seis consultas ao mesmo tempo**; a consulta "Conselhos" pesquisa em `/conselheiros` (`endPointPesquisarServidores`), mas oculta em `/conselhos`. Falha em uma consulta mostra aviso `warning` com o título da consulta.
- ✅ **Ocultar**: `confirm()` e `POST /servidores-medida-protetiva{consulta}` com `{identificador, nome}` e `usuarioAutenticado` (login em `$localStorage.usuario.login`); em sucesso recarrega a lista, chama `expirar-cache` e mostra a mensagem devolvida pelo servidor.
- ✅ **Remover registro**: `confirm()` e `DELETE /servidores-medida-protetiva/{id}?usuarioAutenticado`; recarrega **as seis** listas e chama `expirar-cache`.
- ✅ **`expirar-cache`** é um `GET` disparado pelo cliente depois de cada alteração (sem tratar resultado; só `console.log` no erro). O backend, por sua vez, publica a expiração no RabbitMQ ([[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Expirar-Cache-Medida-Protetiva|fluxo no Backend]]); isso responde em parte à pendência 7 do backend: **é o cliente web que dispara** a expiração.

## Falhas e dependências
- `vm.bloquearBotaoPesquisar` usa campos que não existem (`pesquisandoRemuneracao`, `pesquisandoServidoresPorOrgao`, `pesquisarServidoresDespesas`) e o único uso no HTML (indicador de carregamento do botão) está comentado: o botão só depende da validade do formulário e não há bloqueio contra pesquisas repetidas.
- Se o usuário não estiver em `$localStorage`, `ocultarServidor` e `deletarServidorMedidaProtetiva` lançam `TypeError` (acesso a `.login`).
- A mensagem de erro exibida é `error.data` (pode ser um objeto, e não texto).
- Dados sensíveis (identificação de servidores em medida protetiva) trafegam em `GET`/`POST` por `api.url`; ver [[01-Sistemas/Gerenciador-Portal/Frontend/08-Seguranca/Gerenciador-Portal-Frontend-Seguranca-e-Sessao|Segurança e sessão]].

## Inferências e limitações
- 🔶 `identificador` é o CPF/matrícula do servidor (o backend usa o mesmo nome); o frontend só repassa o valor devolvido pela pesquisa.
- ❓ Campos exibidos nas tabelas (HTML restante não lido).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Backend: Medida protetiva]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-RabbitMQ-Expirar-Cache|Integração com o RabbitMQ]] · [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Confirmar se o `GET /expirar-cache` do backend publica no RabbitMQ a partir dessa chamada (pendência 7 do backend, parte cliente respondida).
