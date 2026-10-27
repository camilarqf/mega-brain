---
type: business-rule
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
  - sic
  - prazo
  - regras
sources:
  - src/OuvDF.ServicoInformacaoCidadao/Infra/Queries/CalcularPrazo/CalcularPrazoHandler.cs
  - src/OuvDF.ServicoInformacaoCidadao/Infra/Queries/_Extensions/PedidoQueryExtensions.cs
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/RegistrarPedido/SharedSteps/SetContext.cs
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/RegistrarRespostaPedido/RegistrarRespostaPedidoHandler.cs
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/RegistrarRecursoPrimeiraInstancia
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/RegistrarRecursoTerceiraInstancia
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/ProrrogarPrazoPedido
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/ProrrogarPrazoRecursoNaoRespondido
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/RegistrarNotificacaoOmissaoRespostaCGDF
  - src/OuvDF.ServicoInformacaoCidadao/Jobs
---

# Regras de prazo do SIC

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Pedido-e-Recurso|Pedido-e-Recurso]], [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Regras-de-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]] (Ouvidoria), [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Objetivo
Reunir, em condição → efeito, todas as regras de prazo do pedido e dos recursos. As durações vêm de configuração (`ServicoInformacaoCidadaoSettings`); os valores **não foram lidos**.

## Evidências
Arquivos em `sources`, commit `4901ad5`.

## Informações confirmadas

### Cálculo
| # | Condição | Efeito | Evidência |
|---|---|---|---|
| S1 | `CalcularPrazo(DataInicio, N)` | início = próximo **dia útil** depois da `DataInicio` (início do dia); término = início + (N − 1) dias corridos (fim do dia), ajustado ao próximo dia útil; dias não úteis: fins de semana e feriados cadastrados (`Feriado`) | `CalcularPrazoHandler` |
| S2 | Pedido vigente | `IsInPrazoVigente(hoje)`: existe `PrazoVigente` e a data está no prazo (`Prazo.Vigente`) | `Pedido` |
| S3 | "Fora do prazo vigente" nas consultas | `PrazoVigente.DataTermino < DateTime.Now` | `PedidoQueryExtensions.ForaDoPrazoVigente` |

### Durações por etapa (chave de configuração)
| Etapa | Chave | Prazo calculado a partir de |
|---|---|---|
| Resposta ao pedido (prazo inicial do pedido) | `QtdDiadPrazoPedido` | data do registro |
| Prorrogação | `QtdDiasPrazoProrrogacao` | término do prazo **original** do pedido |
| Prazo para o cidadão recorrer (após resposta ao pedido ou ao recurso) | `QtdDiasPrazoParaRecorrer` | data da resposta |
| Prazo para o órgão responder o recurso (1ª e 2ª) | `QtdDiasPrazoParaResponder` | data do recurso |
| Prazo do recurso de 3ª instância | `QtdDiasPrazoRecursoTerceiraInstancia` | data do recurso |
| Notificação à CGDF (reclamação) | `QtdDiasPrazoNotificacaoCGDF` | véspera da data atual (para contar a partir de hoje) |
| Notificação ao órgão | `QtdDiasPrazoNotificacaoOrgao` | usada nas notificações à unidade (🔶 handler não lido) |

### Regras de efeito
| # | Condição | Efeito |
|---|---|---|
| S4 | Pedido registrado | `Prazo` = `PrazoVigente` = `QtdDiadPrazoPedido` dias, situação `Recebido` (cada unidade ganha o mesmo prazo) |
| S5 | Resposta ao pedido | `PrazoVigente` passa a ser o prazo de recorrer; `Respondido` |
| S6 | Recurso de 1ª ou 2ª registrado | `PrazoVigente` = prazo para o órgão responder |
| S7 | Resposta de recurso 1ª ou 2ª | `PrazoVigente` = prazo de recorrer (`QtdDiasPrazoParaRecorrer`) |
| S8 | Resposta preliminar da 3ª instância | `PrazoVigente = null` (sem prazo corrente) |
| S9 | Prorrogação (manual) | permitida uma única vez, enquanto no prazo vigente, em `EmAnalise`/`Recebido`, por operador atual da unidade |
| S10 | Pedido com prazo vigente expirado e não respondido (job) | prorrogação automática única, pelo operador automático, justificativa configurada |
| S11 | Recurso 1ª/2ª sem resposta até o fim do prazo vigente (job) | situação "não respondido" da instância |
| S12 | Pedido concluído por prazo (job) | situação concluída/vencida e `PrazoVigente = null` |
| S13 | Pedido `Prorrogado` com prazo final vencido (job) | notificação de omissão à unidade e situação `ReclamacaoOrgao` |
| S14 | Pedido `ReclamacaoOrgao` com prazo final vencido (job) | notificação à CGDF, situação `ReclamacaoCgdf`, prazo `QtdDiasPrazoNotificacaoCGDF` |

## Inferências e limitações
- 🔶 As consultas dos jobs comparam com `DateTime.Now` (e `PrazoFinalMenorQue(Data)` com `IApplicationDateTime`); com a data configurável da aplicação podem divergir.
- 🔶 O cálculo conta dias corridos e ajusta o término ao dia útil: não é "N dias úteis".
- 🔶 `RegistrarNotificacaoOmissaoRespostaCGDF` calcula o prazo a partir de `hoje − 1` para que o primeiro dia contado seja hoje; qualquer outra chamada usa o dia seguinte.
- ❓ Valores reais de todas as chaves (dias) e feriados cadastrados.
- ❓ `PrazoFinalMenorQue` e `NaoRespondido`/`EmSituacaoDeConclusao`: definições não lidas.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]]

## Pendências e próximo passo
- Perguntar ao time o significado de negócio de cada prazo (dias) e a base legal; ler `PrazoFinalMenorQue`.
