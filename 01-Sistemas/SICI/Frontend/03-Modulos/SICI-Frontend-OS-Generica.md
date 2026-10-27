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
  - os-generica
sources:
  - src/app/pages/ordem-servico/ordem-servico-generica-listar/ordem-servico-generica-listar.component.ts
  - src/app/pages/ordem-servico/ordem-servico-generica-cadastrar/ordem-servico-generica-cadastrar.component.ts
  - src/app/pages/ordem-servico/visualizar-pdf-generica/visualizar-pdf-generica.component.ts
  - src/core/services/ordem-servico-generica-service/ordem-servico-generica.service.ts
  - src/core/services/ordem-servico-generica-service/assinatura-generica.service.ts
  - src/core/store/effects/ordem-servico-generica-effects/ordem-servico-generica.effects.ts
  - src/core/models/ordem-servico-generica/ordem-generica-payload.models.ts
---

# Módulo — OS Genérica (frontend)

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Backend: [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica (Backend)]] · Relacionado: [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]]

## Objetivo
Telas da **OS genérica**: ordem de serviço que não nasce de uma ação de controle (modelo `GENERICA`), com listagem própria, cadastro, PDF, envio e assinatura.

## Evidências
Arquivos em `sources`; cadastro lido por estrutura de formulário (cobertura `parcial`).

## Informações confirmadas ✅
- **Listagem** (`ordem-generica-lista`, `CONSULTAR_OS_POR_AC`): paginação **no servidor** (`GET /ordem-servico-generica/listar?page&size&search`, 10 por página; filtro global enviado como `search`); reordena a página por prioridade de status. Ações: visualizar o PDF (se `ASSINADA` com `idDocumentoAssinado`, abre o documento assinado), enviar (modal) e abrir o motivo de devolução.
- **Cadastro** (`ordem-generica-cadastrar`, `EDITAR_OS`): formulário com `areaExecutoraId` (obrigatório), `identificador`, `observacao`, `coordenadorId`, `ordemServicoAssociada`, lista de **artigos** (`descricao` obrigatória; o payload leva `numeroArtigo` e `descricao`), **fases** (`descricao`, `dataInicio`, `dataFim`, `duracao`) e um grupo com `arquivo` e `descricao` (máx. 1000). Auditores vêm de `listarAuditoresOrdemServico`. Depois de salvar volta à lista. Salva por `POST /ordem-servico-generica/salvar-os`, atualiza por `PUT /atualizar/{id}`.
- **PDF** (`visualizar-pdf-generica/:id`): `GET /ordem-servico-generica/gerar-pdf?id=`, mesmos botões da OS comum (enviar quando `CRIADA`/`DEVOLVIDA` e `exibirBotaoEnviar`; assinar quando `ENVIADA` e `exibirBotaoAssinar`, flags definidos pela `origem` da navegação).
- **Status**: `PUT /ordem-servico-generica/alterarStatusOs/{id}` (`ENVIADA`; devolução com motivo por *action* NgRx).
- **Assinatura**: `AssinaturaGenericaService` guarda no contexto do popup o **corpo completo** da OS (`areaExecutora`, `coordenador`, `auditores`, `artigos`, `fases`, `osVinculada`, `status = ASSINADA`) e o popup envia esse corpo em `POST /assinaturas/assinar-os-generica/{id}` ([[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]]).
- Na lista geral de OS, as genéricas entram num grupo "Ordens Genéricas".

## Inferências e limitações
- 🔶 O frontend não chama `DELETE /ordem-servico-generica/excluir/{id}` (busca textual): a exclusão de OS genérica existe no backend, sem tela correspondente neste commit.
- 🔶 Como a assinatura reenvia o corpo da OS gravado no popup, o conteúdo assinado depende do que o frontend monta; se o backend usa o corpo recebido em vez do registro salvo, divergências são possíveis. A regra do backend deve ser conferida em [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]].
- 🔶 `artigos` no formulário usa só `descricao` obrigatória, enquanto o payload leva também `numeroArtigo`; a origem desse número não foi lida.
- Anexo (`arquivo`): destino e envio não foram identificados no serviço lido.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]] · [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
