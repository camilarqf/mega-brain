---
type: module
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - modulo
  - unidade
  - configuracao
sources:
  - src/SCI.Domain/Organizacional/Entities/Unidade.cs
  - src/SCI.Domain/Organizacional/Rules
  - src/SCI.Application/UseCases/GestaoUnidade
  - src/SCI.Api/Controllers/UnidadeController.cs
---
# SCI Backend — módulo Unidade e configuração de processos

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar a unidade organizacional, seus vínculos com outros sistemas e a configuração de processos (admissibilidade e PIP) e de revisões.

## Evidências
- `Unidade.{GetNumeroPorTipoVinculo, Desabilitar, CriarConfiguracao, Atualizar, ObterConfiguracaoProcesso, DesabilitarConfiguracoes}`, regras `Organizacional/Rules/*`, use cases `GestaoUnidade/*`, testes `FluxoCriarUnidadeTests`, `FluxoAtualizarUnidadeTests`, `FluxoDesabilitarUnidadeTests`, `FluxoAtualizarRevisoesTests`.

## Informações confirmadas
- ✅ `Unidade`: id textual, descrição, sigla, `PossuiEstruturaCorrecional`, cargos, vínculos (`UnidadeVinculada`: SEI, SIGRH, SIGGO, PARTICIPA_DF) e configurações de processo.
- ✅ **Regra de vínculo** (`VinculoAptoParaUnidade`): não pode repetir o mesmo tipo de vínculo na unidade ("Não é permitido informar o mesmo tipo de vínculo mais de uma vez para a unidade.").
- ✅ **Criar configuração** (`POST /unidade/configuracao`, Administrador): a unidade deve estar ativa (`UnidadeAtiva`) e o tipo de processo ainda não configurado (`TipoProcessoNaoConfigurado`). Há regras para atualizar configuração (`UnidadeAptaParaAtualizarConfiguracao`) e `ConfiguracaoPertenceAUnidadeAtiva`.
- ✅ **Revisões**: `ConfiguracaoRevisaoProcesso` define quais tipos de revisão estão ativos e o perfil responsável; `PUT /unidade/configuracao/revisoes` as atualiza. O fluxo de assinatura do processo segue as revisões ativas ([[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Admissibilidade]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]]).
- ✅ **Desabilitar configuração** (`POST /unidade/configuracao/desabilitar`) e **desabilitar unidade** (`DELETE /unidade/{id}`: `DesabilitarUnidadeHandler` chama `Unidade.Desabilitar()`; o efeito sobre as configurações não foi lido).
- ✅ O número de vínculo `PARTICIPA_DF` é usado para numerar denúncias e para resolver a unidade destino de uma denúncia recebida (`IUnidadeRepository.GetByUnidadeVinculadaAsync`).
- ✅ Consultas: `GET /unidade`, `/por-tipo/{id}`, `/has-gestor`, `/configuracao/{id}`.

## Inferências e limitações
- ⚠️ `DELETE /unidade/{id}` não declara política; vale só `[Authorize]` do controller ([[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]]). A política `unidade.CriarUnidadePolicy` existe e não encontrei uso.
- 🔶 Não achei endpoint de criação de unidade; as unidades vêm de seed (`04-Insert-TB_UNIDADE.sql`, não lido) e do `UnidadeAtualizada`.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denúncia e Demanda]] · [[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança]] · [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Testes-e-Cobertura|Testes]]

## Pendências e próximo passo
- Confirmar como unidades novas são cadastradas em produção.
