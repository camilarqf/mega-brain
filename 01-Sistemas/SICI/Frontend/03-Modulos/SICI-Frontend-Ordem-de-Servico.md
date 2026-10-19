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
  - ordem-de-servico
  - prorrogacao
  - cancelamento
sources:
  - src/app/pages/ordem-servico/ordem-servico-listar/acao-controle-os.component.ts
  - src/app/pages/ordem-servico/ordem-servico-cadastrar/ordem-servico-cadastrar.component.ts
  - src/app/pages/ordem-servico/ordem-servico-atualizar/ordem-servico-atualizar.component.ts
  - src/app/pages/ordem-servico/ordens-servico-listagem/ordens-servico-listagem.component.ts
  - src/app/pages/ordem-servico/visualizar-pdf/visualizar-pdf.component.ts
  - src/app/pages/ordem-servico/ordem-servico-routing.module.ts
  - src/core/services/ordem-servico.service.ts
  - src/core/services/fase.service.ts
  - src/core/enums/status-ordem-servico.enum.ts
  - src/core/enums/tipo-ordem-servico.helper.ts
  - src/core/store/effects/ordem-servico-effects/ordem-servico.effects.ts
---

# Módulo — Ordem de Serviço (frontend)

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Backend: [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico (Backend)]], [[01-Sistemas/SICI/Backend/03-Modulos/Prorrogacao-e-Cancelamento|Prorrogacao-e-Cancelamento]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Enums-e-Estados|Enums-e-Estados]] · Fluxos: [[01-Sistemas/SICI/Frontend/02-Fluxos/SICI-Frontend-Fluxo-Ciclo-de-Vida-OS|Ciclo-de-Vida-OS]], [[01-Sistemas/SICI/Frontend/02-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Assinatura-OS]]

## Objetivo
Telas para emitir, editar, enviar, devolver, prorrogar, cancelar, excluir, visualizar em PDF e assinar **ordens de serviço** (OS) vinculadas a uma ação de controle.

## Evidências
Arquivos em `sources`. `ordem-servico-cadastrar` (1607 linhas) e `ordem-servico-atualizar` (790) foram lidos por trechos e por busca dirigida; `coverage: parcial`.

## Informações confirmadas ✅
### Enumerações no cliente
- `EStatusOrdemServico`: `CRIADA=1`, `ENVIADA=2`, `DEVOLVIDA=3`, `ASSINADA=4`, `CANCELADA=5`.
- `EModeloOrdemServico`: `ABERTURA=1`, `DESIGNACAO=2`, `EXCLUSAO=3`, `PRORROGACAO=4`, `CANCELAMENTO=5`, `SUBSTITUICAO=6`, `GENERICA=7`. `OrdemServicoEnums` compara status por nome e modelo por id.

### Telas
- **OS da ação** (`AcaoControleOsComponent`, `ordem-servico/listar/:acaoControleId`): carrega a ação e suas OS (estado NgRx), lista em ordem inversa e mostra selo de status (`criada`, `enviada`, `assinada`, `cancelada`). Botões por status e permissão:
  - **Enviar**: OS `DEVOLVIDA` ou `CRIADA` e `EMITIR_OS` (modal de confirmação).
  - **Editar**: `DEVOLVIDA`/`CRIADA`, tipo diferente de `CANCELAMENTO` e `EDITAR_OS`.
  - **Excluir**: `DEVOLVIDA`/`CRIADA` e permissão `CANCELAR_OS`.
  - **Solicitar cancelamento** (cria uma OS do tipo cancelamento para a ação inteira): permissão `SOLICITAR_CANCELAMENTO_OS`, só quando ainda não existe cancelamento para a ação.
  - **Editar justificativa** do cancelamento: OS de cancelamento em `CRIADA`.
  - **Prorrogar**: `EMITIR_OS`, só se existe OS de **abertura assinada**; sem prorrogação, a abertura assinada é a base; havendo prorrogações, só a **mais recente** e **assinada** exibe o botão (ordenação por data de criação/assinatura, com id como desempate).
  - **Motivo da devolução**: clique no selo `DEVOLVIDA` abre modal com `motivoDevolucao`.
  - **Visualizar PDF**.
- **Cadastro/edição/prorrogação** (`OrdemServicoCadastrarComponent`, mesma rota `cadastrar-ordem-servico/:acaoControleId`): o modo vem de *query params* — `idEdicao` (edição, exige `EDITAR_OS`), `idBase` + `modoProrrogacao` (prorrogação). Formulário com grupos; cada grupo tem `tipoAcao` (modelo) obrigatório e `observacao` (máx. 500, habilitada só para `ABERTURA` e `PRORROGACAO`). Modelos `ABERTURA` e `PRORROGACAO` exigem **fases**; `DESIGNACAO`, `EXCLUSAO`, `CANCELAMENTO`, `SUBSTITUICAO` e `GENERICA` só cadastram (sem edição). Ao escolher o modelo, a tela carrega a equipe da ação: `EXCLUSAO` carrega os auditores da ação; `DESIGNACAO`, os membros ainda não relacionados; `SUBSTITUICAO`, o coordenador atual, os coordenadores substitutos e os membros não relacionados, e **exige** `coordenadorSubstitutoId`. Descrições de fase vêm de `GET /fase/descricao-fase[/listar]` (por fase, tipo e natureza da ação), com editor rico (CKEditor) para o texto.
- **Edição** (`OrdemServicoAtualizarComponent`): reaproveita os componentes de fase; trata `ASSINADA` e `CRIADA` como estados de edição distintos.
- **Lista geral** (`OrdensServicoListagemComponent`, `ordens-servicos-lista`, `LISTAR_OS`, perfil SUBCI): carrega **todas** as OS e todas as genéricas (`page 0, size 10000`), agrupa por código da ação (e um grupo "Ordens Genéricas"), ordena OS por status (`ENVIADA`, `DEVOLVIDA`, `CRIADA`) e pagina no cliente. Ações: visualizar, **assinar** (popup, [[01-Sistemas/SICI/Frontend/02-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]]), **devolver** (modal de motivo) e validar assinatura. Ouve `postMessage` do popup para exibir toast e recarregar.
- **PDF** (`VisualizarPdfComponent`): baixa o PDF como *blob* (`GET /os-acao-controle/gerar-pdf?id=`), exibe com `ng2-pdf-viewer` e extrai o **código verificador** (32 caracteres hexadecimais) do texto do PDF. Botões conforme `origem` na URL: `ACAO_CONTROLE` mostra **Enviar** (para `DEVOLVIDA`/`CRIADA`); `LISTA_GERAL` mostra **Assinar** (para `ENVIADA`). Há ainda *Imprimir*, *Validar assinatura* e voltar para a origem.

### Chamadas (`OrdemServicoService`, `FaseService`)
`POST /os-acao-controle/salvar-os/{acaoControleId}`, `PUT .../atualizar/{id}`, `DELETE .../excluir/{id}`, `GET .../listar-os/{id}`, `GET .../listar?page&size`, `GET .../pesquisar?id=`, `POST|PUT .../{id}/prorrogacoes`, `GET .../gerar-pdf?id=`, `PUT .../alterarStatusOs/{id}`, `POST .../cancelar-os/{idAcaoControle}`, `PUT .../cancelamento/{idOS}/{idCancelamento}`, `GET /auditor/*`, `GET /coordenador/*`, `GET /fase/*`. Detalhe em [[01-Sistemas/SICI/Frontend/04-API-e-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]].

## Inferências e limitações
- 🔶 **Envio duplicado**: ao enviar, o componente (`acao-controle-os`, `visualizar-pdf`) despacha `enviarOrdemServico` (cujo efeito já chama `PUT /alterarStatusOs {status: ENVIADA}`) **e** chama o mesmo serviço em seguida: a mesma chamada sai duas vezes. Não executado; o comportamento do backend à segunda chamada não foi verificado. Ver [[01-Sistemas/SICI/Frontend/06-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]].
- 🔶 **URL sem barra**: `buscarOrdemServicoBase` e `getById` montam `${urlApi}os-acao-controle/pesquisar` (sem `/`); com `urlApi` = `/api` o resultado seria `/apios-acao-controle/pesquisar`. Esses métodos servem a prorrogação (OS base) e a `visualizarOrdemServicoPorId`. Efeito real não verificado.
- 🔶 `listarOrdemServicoById(id)` chama `listar-os/{id}`, que no backend recebe o id da **ação de controle**, mas `visualizar-pdf` e `validar-assinatura` o chamam com o id da **OS** (retorno é lista).
- 🔶 `GET /os-acao-controle/pesquisar` é restrito a SUBCI e DIRETOR no backend, enquanto o frontend o usa em telas liberadas a COORDENADOR e AUDITOR; possível `403` para esses perfis.
- 🔶 `buscarPorAcaoControle` usa `GET /ordem-servico/por-acao/{id}` e `listarDescricoesFase` usa `GET /fase/descricao-fase/listar`; **nenhum dos dois** consta no [[01-Sistemas/SICI/Backend/05-API/SICI-Backend-Catalogo-de-Endpoints|catálogo do backend]]. Confirmar se o catálogo está incompleto ou se são chamadas órfãs.
- 🔶 Código de interface sem referência em template: `abrirModalAssinar` e `AssinarOrdemServico` em `visualizar-pdf` (este usaria `assinarOs`, que assina **sem reautenticação**); o botão de assinar usa o popup.
- Regras de transição de estado e de prazo/prorrogação **pertencem ao backend**; o frontend apenas habilita/oculta botões por status e permissão.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Acao-de-Controle|Acao-de-Controle]] · [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-OS-Generica|OS-Generica]] · [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]] · [[01-Sistemas/SICI/Frontend/05-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
