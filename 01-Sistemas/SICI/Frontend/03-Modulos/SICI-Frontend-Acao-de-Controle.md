---
type: module
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - modulo
  - acao-de-controle
sources:
  - src/app/pages/acao-controle/acao-controle-listar/acao-controle-listar.component.ts
  - src/app/pages/acao-controle/acao-controle-cadastrar/acao-controle-cadastrar.component.ts
  - src/app/pages/acao-controle/acao-controle-visualizar/acao-controle-visualizar.component.ts
  - src/app/pages/acao-controle/acao-controle-atualizar/acao-controle-atualizar.component.ts
  - src/app/pages/acao-controle/acao-controle-routing.module.ts
  - src/core/services/acao-controle-services/acao-controle.service.ts
  - src/core/services/poac.service.ts
  - src/core/enums/tipo-acao.enum.ts
  - src/core/enums/natureza-acao.enum.ts
---

# Módulo — Ação de Controle (frontend)

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Backend: [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Acao-de-Controle|Acao-de-Controle (Backend)]], [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-POAC|POAC]], [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Cadastros-Auxiliares|Cadastros-Auxiliares]] · Relacionado: [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]]

## Objetivo
Telas de listagem, cadastro, consulta e edição de **ações de controle** (auditoria, consultoria, inspeção) e porta de entrada para as OS de cada ação.

## Evidências
Arquivos em `sources`. Listagem e cadastro lidos em detalhe; `visualizar` e `atualizar` apenas por estrutura (cobertura `parcial`).

## Informações confirmadas ✅
- **Listagem** (`AcaoControleListarComponent`, rota inicial de `pages/home`): carrega todas as ações (`loadAcoesControle`), **mantém só as com `status === true`** e monta textos de filtro (unidades auditadas, órgão, programa de governo, objetivo PPA, área executora). Filtro global na tabela (PrimeNG). Mostra até 3 unidades auditadas, com expansão.
- **Botões por permissão** (`PermissaoService`): editar (`EDITAR_ACAO`), excluir (`EXCLUIR_ACAO`, com modal de confirmação) e listar OS da ação (`CONSULTAR_OS_POR_AC`). Visualizar não consulta permissão no componente (a rota exige `CONSULTAR_ACAO`).
- **Ir para as OS**: `listarOsAcaoControle` converte tipo e naturezas da ação em ids (`AUDITORIA=1`, `CONSULTORIA=2`, `INSPECAO=3`; naturezas `CONFORMIDADE=1` a `PROGRAMA_INTEGRIDADE=5`), grava-os no estado (`definirDadosDaAcaoControle`) e navega para `ordem-servico/listar/:id` após um `setTimeout` de 300 ms. O estado é usado depois para buscar as descrições de fase.
- **Cadastro** (`AcaoControleCadastrarComponent`, formulário reativo). Campos obrigatórios: unidade de auditoria interna, área executora, tipo, classificação, programa de governo (código), objetivo PPA, naturezas, unidades auditadas, ano de programação, quantidade de membros, dias úteis, esforço total, descrição da ação (máx. 30 caracteres) e POAC (`idPoac`). Opcional: objetivo da ação (máx. 500). Cadastros dependentes em cascata: área executora depende da unidade de auditoria interna; objetivo PPA, do programa de governo (cada um carregado por *action*/efeito NgRx). Após salvar volta a `pages/home`.
- **POAC**: `PoacService.pesquisarPorAno` consulta `GET /poac/pesquisar-ano?anoPoac=`.
- **Chamadas** (`AcaoControleService`): `GET /acao-controle/listar`, `GET /acao-controle/pesquisar?id=`, `POST /acao-controle/cadastrar`, `PUT /acao-controle/atualizar/{id}`, `DELETE /acao-controle/inativar?id=`, `GET /acao-controle/validar/{id}`. Cadastros auxiliares: `GET /unidade-auditoria/listar`, `/area-executora/listar/{id}`, `/programa-governo/listar`, `/objetivo-ppa/listar/{codigo}`, `/unidade-auditada/listar`. Catálogo em [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]].
- **Rotas**: `visualizar/:id` (`CONSULTAR_ACAO`), `atualizar/:id` (`EDITAR_ACAO`), `cadastrar-acao-controle` (`CRIAR_ACAO` declarada **sem** `canActivate`).

## Regras de negócio
Nenhuma regra de negócio verificável foi extraída do frontend além das validações de formulário acima (campos obrigatórios e limites de tamanho). Regras de domínio da ação ficam no backend.

## Inferências e limitações
- 🔶 "Excluir" no frontend chama `inativar`; o backend bloqueia a inativação se houver OS ([[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Acao-de-Controle|Acao-de-Controle]]). O tratamento da mensagem de erro na tela não foi lido.
- 🔶 `GET /acao-controle/validar/{id}` existe no serviço, mas o uso na tela não foi localizado.
- 🔶 O padrão do ano da programação e do POAC (qual POAC é escolhido) não foi lido; o campo é obrigatório.
- Telas `visualizar` e `atualizar` e templates HTML lidos só por estrutura.

## Relacionamentos
- Ordens de serviço da ação: [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]] · Permissões: [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]] · Padrão de estado: [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
