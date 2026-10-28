---
type: module
aliases:
  - Atribuicao-e-Bloqueio-Externo
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-23
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
  - src/OuvDF.IntegrationServices/Consumers
  - src/OuvDF.ServicoOuvidoria/Domain/Entities/Manifestacao.cs
---

# Atribuição, bloqueio externo e conta LGPD

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestacao]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]]

## Objetivo
Documentar três mecanismos de apoio: atribuição da manifestação a um operador, bloqueio externo disparado por outro sistema (denúncia) e a transferência de manifestações para uma conta institucional (LGPD).

## Evidências
Handlers de `AtribuirParaOperador`, `AplicarBloqueioExterno`, `RemoverBloqueioExterno`, `MoverManifestacoesParaContaLGPD` (leitura parcial) e `DenunciaAceitaConsumer`; commit `4901ad5`. Atualizado em 2026-10-23 (`820666c`): consumidores de denúncia relidos em `OuvDF.IntegrationServices/Consumers`.

## Informações confirmadas

### Atribuição
- ✅ `AtribuirParaOperador`: exige a permissão de detalhar (`DTL_MNF`); se a manifestação está na unidade do operador e sem operador, atribui; `Recebida` → `EmAnálise`; marca como visualizada; registra a primeira visualização daquela unidade.
- ✅ Existe `POST …/manifestacao/remover-atribuicao-operador` (papel `OperadorSO`, comando `RemoverAtribuicaoOperador`, handler não lido) e `Manifestacao.RemoveOperadorCorrente()` zera o operador; 🔶 o efeito é devolver a manifestação à caixa de entrada. A ação `DVL_MNF` permite ao operador corrente, ou a quem tem `DevolverParaCaixaDeEntrada`.

### Bloqueio externo
- ✅ `Manifestacao.BloqueadaExternamente` (bool) é ligado por `AplicarBloqueioExterno` e desligado por `RemoverBloqueioExterno`.
- ✅ Aplicar: cria uma `Providencia` automática com o texto "A manifestação está sob avaliação do sistema correcional", em nome do **operador de sistema** (`SharedSettings.IdOperadorSistema`) na unidade atual, e liga o bloqueio.
- ✅ Remover: cria `Providencia` com a justificativa recebida (ex.: "Denúncia aceita pela COACI (identificador processual)") e desliga o bloqueio.
- ✅ Efeito: com o bloqueio ligado, nenhuma das ações de operador de resposta, tramitação, complementação, anexo e reclassificação é permitida ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestacao]]).
- ✅ Gatilho conhecido: os consumidores `DenunciaAceitaConsumer` (fila `denuncia-aceita`) e `DenunciaRecusadaConsumer` (`denuncia-recusada`, com o `MotivoRecusa` como justificativa) enviam `RemoverBloqueioExterno` e, em seguida, apagam os objetos da denúncia no bucket S3 (ver [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas]]). **Nada neste repositório dispara `AplicarBloqueioExterno`** (verificado em 2026-10-23, `820666c`, por busca em todo o código, configuração e testes: só aparecem a definição do comando e o handler; não há controller, consumidor, workflow nem job que o envie). Sem outra origem, o envio da denúncia ao SCI **não bloqueia** a manifestação neste código; quem liga `BloqueadaExternamente` é ❓ (outro sistema por acesso direto ao banco, rota fora do repositório ou funcionalidade incompleta). Histórico (commit `4901ad5`): "Quem dispara `AplicarBloqueioExterno` não foi identificado no código lido (🔶 pode ser outro comando, endpoint ou o fluxo do `IAController`/`ServicosExternosController`)."

### Conta LGPD
- ✅ `MoverManifestacoesParaContaLGPD` localiza a pessoa jurídica de tipo `EntidadeEspecial` (a "conta LGPD") e move, para ela, os registros do manifestante atual: arquivos, complementações e históricos (as demais operações da fila de execução não foram lidas; 🔶 devem incluir as próprias manifestações).
- 🔶 Provável uso: exclusão de conta do cidadão, preservando manifestações sem manter os dados pessoais ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]], `excluir-conta`). Quem chama o comando não foi confirmado.

## Inferências e limitações
- 🔶 Se não houver pessoa jurídica `EntidadeEspecial`, o comando falha com "Conta LGPD não pode ser nula"; a existência desse registro é dado de ambiente.
- ✅ Resolvido em 2026-10-23 (`820666c`): a inferência anterior (recusa mantém o bloqueio) estava **errada**; `DenunciaRecusadaConsumer` também remove o bloqueio externo.
- Histórico (commit `4901ad5`): "🔶 `DenunciaRecusada` deveria manter o bloqueio; o consumidor não foi lido."
- ❓ Fluxo completo do correcional/COACI (aplicar → avaliar → aceitar ou recusar) e o sistema que publica os eventos (lote 7).
- ❓ Demais operações da fila de `MoverManifestacoesParaContaLGPD`.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio-de-Usuario]] (bloqueio de **usuário**, outro conceito)

## Pendências e próximo passo
- ✅ `DenunciaRecusadaConsumer` lido (2026-10-23). Busca por chamadores de `AplicarBloqueioExterno`: nenhum no repositório (ver acima). Falta confirmar com o time quem aplica o bloqueio externo.
- Confirmar o uso de `MoverManifestacoesParaContaLGPD`.
