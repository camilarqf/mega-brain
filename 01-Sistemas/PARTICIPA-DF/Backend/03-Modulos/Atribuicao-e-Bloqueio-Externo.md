---
type: module
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - backend
  - ouvidoria
  - bloqueio-externo
  - lgpd
sources:
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/AtribuirParaOperador
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/AplicarBloqueioExterno
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/RemoverBloqueioExterno
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/MoverManifestacoesParaContaLGPD
  - src/OuvDF.ServicoOuvidoria/Domain/EventHandlers/DenunciaAceitaConsumer.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Entities/Manifestacao.cs
---

# Atribuição, bloqueio externo e conta LGPD

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Manifestacao|Manifestacao]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]]

## Objetivo
Documentar três mecanismos de apoio: atribuição da manifestação a um operador, bloqueio externo disparado por outro sistema (denúncia) e a transferência de manifestações para uma conta institucional (LGPD).

## Evidências
Handlers de `AtribuirParaOperador`, `AplicarBloqueioExterno`, `RemoverBloqueioExterno`, `MoverManifestacoesParaContaLGPD` (leitura parcial) e `DenunciaAceitaConsumer`; commit `4901ad5`.

## Informações confirmadas

### Atribuição
- ✅ `AtribuirParaOperador`: exige a permissão de detalhar (`DTL_MNF`); se a manifestação está na unidade do operador e sem operador, atribui; `Recebida` → `EmAnálise`; marca como visualizada; registra a primeira visualização daquela unidade.
- ✅ Existe `POST …/manifestacao/remover-atribuicao-operador` (papel `OperadorSO`, comando `RemoverAtribuicaoOperador`, handler não lido) e `Manifestacao.RemoveOperadorCorrente()` zera o operador; 🔶 o efeito é devolver a manifestação à caixa de entrada. A ação `DVL_MNF` permite ao operador corrente, ou a quem tem `DevolverParaCaixaDeEntrada`.

### Bloqueio externo
- ✅ `Manifestacao.BloqueadaExternamente` (bool) é ligado por `AplicarBloqueioExterno` e desligado por `RemoverBloqueioExterno`.
- ✅ Aplicar: cria uma `Providencia` automática com o texto "A manifestação está sob avaliação do sistema correcional", em nome do **operador de sistema** (`SharedSettings.IdOperadorSistema`) na unidade atual, e liga o bloqueio.
- ✅ Remover: cria `Providencia` com a justificativa recebida (ex.: "Denúncia aceita pela COACI (identificador processual)") e desliga o bloqueio.
- ✅ Efeito: com o bloqueio ligado, nenhuma das ações de operador de resposta, tramitação, complementação, anexo e reclassificação é permitida ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Manifestacao|Manifestacao]]).
- ✅ Gatilho conhecido: o consumidor `DenunciaAceitaConsumer` (fila `denuncia-aceita`) envia `RemoverBloqueioExterno`. Quem dispara `AplicarBloqueioExterno` não foi identificado no código lido (🔶 pode ser outro comando, endpoint ou o fluxo do `IAController`/`ServicosExternosController`).

### Conta LGPD
- ✅ `MoverManifestacoesParaContaLGPD` localiza a pessoa jurídica de tipo `EntidadeEspecial` (a "conta LGPD") e move, para ela, os registros do manifestante atual: arquivos, complementações e históricos (as demais operações da fila de execução não foram lidas; 🔶 devem incluir as próprias manifestações).
- 🔶 Provável uso: exclusão de conta do cidadão, preservando manifestações sem manter os dados pessoais ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]], `excluir-conta`). Quem chama o comando não foi confirmado.

## Inferências e limitações
- 🔶 Se não houver pessoa jurídica `EntidadeEspecial`, o comando falha com "Conta LGPD não pode ser nula"; a existência desse registro é dado de ambiente.
- 🔶 `DenunciaRecusada` (fila `denuncia-recusada`) deveria manter o bloqueio; o consumidor não foi lido.
- ❓ Fluxo completo do correcional/COACI (aplicar → avaliar → aceitar ou recusar) e o sistema que publica os eventos (lote 7).
- ❓ Demais operações da fila de `MoverManifestacoesParaContaLGPD`.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Bloqueio-de-Usuario|Bloqueio-de-Usuario]] (bloqueio de **usuário**, outro conceito)

## Pendências e próximo passo
- Lote 7: ler `DenunciaRecusadaConsumer` e identificar quem aplica o bloqueio externo.
- Confirmar o uso de `MoverManifestacoesParaContaLGPD`.
