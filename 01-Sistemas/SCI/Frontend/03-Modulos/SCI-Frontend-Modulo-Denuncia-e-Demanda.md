---
type: module
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - frontend
  - modulo
  - denuncia
  - demanda
sources:
  - src/app/pages/denuncias
  - src/app/pages/demanda
  - src/app/components/layout/tratar-demanda
  - src/app/store/services/denuncia.service.ts
  - src/app/store/services/demanda.service.ts
  - src/app/core/enums/status-denuncia-enum.ts
  - src/app/core/enums/status-demanda-enum.ts
  - src/app/core/enums/tipo-tratamento-demanda.enum.ts
---
# SCI Frontend — módulo Denúncia e Demanda

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Documentar as telas de denúncias recebidas e de demandas (cadastro, anexos e tratamento).

## Evidências
- `pages/denuncias` (lista com filtros, `analisar-denuncia` de 328 linhas), `pages/demanda` (caixas de entrada da autoridade e do apoio, lista, edição, tratamento, visualização), `components/layout/tratar-demanda`, serviços `denuncia.service.ts` e `demanda.service.ts`.

## Informações confirmadas
### Denúncias (`/pages/denuncias`)
- ✅ Lista paginada com filtros (`GET denuncia/get-all`) e tela `analisar/:id` (`GET denuncia/{id}`).
- ✅ Status do cliente: `AguardandoAnalise` (0), `Aceita` (1), `Recusada` (2). A tela considera "aguardando análise" quando `status.id` é falso (zero).
- ✅ Só o perfil `Apoio Correcional` pode aceitar ou recusar (`podeAnalisar`); aceitar chama `POST denuncia/aceitar` com `{ denuncia: { id } }`; recusar exige motivo não vazio e chama `POST denuncia/recusar` com `{ denuncia: { id }, motivoRecusa }`. Após sucesso volta à lista.
- ✅ Anexos: baixar ou visualizar por `GET denuncia/{identificadorExterno}/download?nomeArquivo=` como blob. Visualização inline para PDF, imagens (jpg, jpeg, png), áudio (mp3) e vídeo (mp4); DOCX e XLSX só por download.
- 🔶 No backend, `POST denuncia/aceitar` e `recusar` exigem a política da autoridade correcional ([[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]); o cliente restringe ao Apoio. Conflito não resolvido (ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]]).

### Demandas (`/pages/demanda`, Autoridade e Apoio)
- ✅ Caixas de entrada `caixa-entrada-autoridade` e `caixa-entrada-apoio`, lista, `editar/:id`, `visualizar/:id` e `tratar/:id`. Consultas: `GET demanda/get-all`, `GET demanda/{id}`, `GET demanda/por-admissibilidade`.
- ✅ Criar e atualizar: `POST demanda` e `PUT demanda`; anexos: `POST demanda/{id}/adicionar-anexo` e `DELETE demanda/{id}/remover-anexo/{anexoId}`.
- ✅ Status do cliente: `AA` Aguardando análise (1), `EA` Em análise (2), `CPA` Concluída — Processo Admissibilidade (3), `CM` Concluída — MPTCE (4), `CPAM` Concluída — Processo Admissibilidade e MPTCE (5), `CR` Criada (6).
- ✅ Tratar demanda (`POST demanda/tratar`, modal `tratar-demanda`): tipos `encaminharProcessoAdmissibilidade`, `encaminharMptce`, `encaminharAmbos`, `encaminharProcessoAdmissibilidadeEDistribuir` e `encaminharAmbosEDistribuir`. Distribuir exige escolher um relator; a opção de distribuir depende de a unidade ter gestor (`GET unidade/has-gestor`).
- ✅ Tipos de documento, assuntos, origens de denúncia e tipificações são carregados para os formulários (ver [[01-Sistemas/SCI/Frontend/04-API-e-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]]).

## Inferências e limitações
- 🔶 "MPTCE" é tratado como destino alternativo ao processo de admissibilidade; a expansão da sigla e o que acontece após o encaminhamento ao MPTCE não aparecem no cliente.
- ❓ O vínculo denúncia aceita → demanda não é feito pelo cliente (o backend também não o faz; ver Pendências do backend, item 3).
- Formulários de demanda e templates HTML lidos por amostragem; regras de validação dos campos não detalhadas.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Módulo do backend]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-JAD-Admissibilidade|JAD]] · [[01-Sistemas/SCI/Frontend/02-Fluxos/SCI-Frontend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo denúncia até admissibilidade]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
