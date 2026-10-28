---
type: module
aliases:
  - "Frontend — módulo Super Busca"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
tags:
  - dados-pessoais
  - busca
sources:
  - src/app/components/super-busca
  - src/app/components/compartilhado/directives/super-buscar-bar.directive.js
  - src/app/components/compartilhado/services/util.service.js
---

# Frontend — módulo Super Busca

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Busca textual única (`/busca`) sobre conjuntos de dados do portal, por nome, CPF, CNPJ ou código de credor.

## Evidências
Commit `dca3e933`. Rota `/busca` → `SuperBuscaController`; `super-busca.service.js`, `super-buscar-bar.directive.js`, `Util` (validadores `validarCPF`, `validarCNPJ`, `hasCpfFormat`, `extractDigits`).

## Informações confirmadas
- ✅ `SuperBuscaService.buscar(valor, pagina)` escolhe os serviços do índice: texto → `/indice`; CPF válido → `/indice-cpf` + `/indice-cod-credor`; CNPJ válido → `/indice-cod-credor`. Cada serviço é chamado em paralelo (`$q.all`), com `GET {apisuperbusca}{serviço}/{pagina}/{termo}`; o total vem do cabeçalho `x-count`.
- ✅ O resultado é classificado por conjunto de dados (`REMUNERACAO`, `SERVIDOR-ORGAO`, `DESPESA-CREDOR`, `BENEFICIARIOS-SOCIAIS`, `DIARIAS-PASSAGENS`, …) em `ResultCategoria` (`getCategoriaId`); 🔶 o destino de cada resultado nas telas do portal não foi conferido.
- ✅ O termo é codificado apenas na barra (`/` → `%252F`); CPF/CNPJ são enviados **somente com dígitos** no caminho da URL.
- ✅ O host é `apisuperbusca` (não o `api`), portanto sem `x-client-id`.

## Inferências e limitações
- 🔶 CPF no caminho da URL pode ficar registrado em logs de proxy/servidor do serviço de busca; avaliado em [[01-Sistemas/Portal-Transparencia/Frontend/08-Seguranca/Portal-Transparencia-Frontend-Seguranca-e-Privacidade|Segurança e privacidade]].
- ❓ O provedor do serviço (índice) e seu contrato estão fora deste repositório.
- Cobertura parcial: a lista completa de categorias e templates não foi enumerada.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|Integrações externas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
