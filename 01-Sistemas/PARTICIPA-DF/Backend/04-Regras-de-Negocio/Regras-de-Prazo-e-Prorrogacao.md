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
  - ouvidoria
  - prazo
  - prorrogacao
sources:
  - src/OuvDF.Shared/Domain/Services/CalculadoraPrazoService.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Entities/Manifestacao.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Entities/Prazo.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/RegistrarManifestacao/SharedSteps/CriarManifestacao.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/RegistrarManifestacao/SharedSteps/AtualizarPrazos.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/SolicitarProrrogacaoDePrazo
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/DeferirSolicitacaoDeProrrogacaoDePrazo
  - src/OuvDF.ServicoOuvidoria/Infra/Queries/ConsultarManifestacoesVencidas/ConsultarManifestacoesVencidasHandler.cs
  - src/OuvDF.ServicoOuvidoria/Jobs
---

# Regras de prazo e prorrogação (Ouvidoria)

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Manifestacao|Manifestacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]], [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]]

## Objetivo
Registrar, em condição → efeito, as regras de cálculo de prazo, vencimento, prazos de notificação e prorrogação das manifestações. Só regras verificadas no código; valores configuráveis aparecem como nome de chave.

## Evidências
Arquivos em `sources`, commit `4901ad5`. O valor de `ServicoOuvidoriaSettings:PrazoManifestacaoPadrao` não foi lido.

## Informações confirmadas

| # | Condição | Efeito | Evidência |
|---|---|---|---|
| P1 | Registro de uma manifestação | `DataInicio` = próximo **dia útil** depois do dia do registro; `DataTermino` = `DataInicio` + (`PrazoManifestacaoPadrao` − 1) dias corridos, ajustado para o próximo dia útil se cair em fim de semana ou feriado; esse término vira o `Vencimento` | `CalculadoraPrazoService.CalcularPrazoManifestacao`, `CriarManifestacao` |
| P2 | Dia a avaliar | é dia útil se não é sábado nem domingo e não consta nos feriados (`IFeriadoReadRepository`, carregados uma vez por instância) | `IsDiaUtil` |
| P3 | `PrazoManifestacaoPadrao` ≤ 0 | erro ("Quantidade de dias deve ser positiva") | `CalcularPrazoManifestacao` |
| P4 | Registro | cada `NotificacaoDePrazo` ativo e sem "marcar como vencida" gera um `Prazo` com `Data` = abertura + `QtdDias`; guarda se bloqueia a caixa de entrada, a ação que o remove e o texto | `AtualizarPrazos`, `Manifestacao.AddPrazos` |
| P5 | Resposta preliminar | baixa (`Pendente=false`) apenas os prazos pendentes cuja ação de remoção é "resposta preliminar" | `Manifestacao.BaixarPrazos` |
| P6 | Resposta definitiva | baixa todos os prazos pendentes e zera `MarcarManifestacaoComoVencida` | `RegistrarRespostaDefinitivaHandler` |
| P7 | Job de vencimento | manifestações em `Recebida`/`EmAnálise` cujo `Vencimento` (ou, se nulo, a maior data de prazo pendente que marca como vencida) é anterior a **hoje** passam a `Vencida` | `ConsultarManifestacoesVencidasHandler`, `AtualizarSituacaoManifestacaoParaVencidaJob` |
| P8 | Job de vencimento pós-prorrogação | idem para `Prorrogada` → `Vencida_após_prorrogação` | `AtualizarSituacaoManifestacaoParaVencidaAposProrrogacaoJob` |
| P9 | Solicitar prorrogação | exige ação `PRG_PRZ`: a classificação permite prorrogação, dentro da janela de ±5 dias em relação ao vencimento (`prazoRestante` entre −5 e +5), em atendimento, operador corrente, funcionalidade `ProrrogarPrazo` | `PermiteProrrogarPrazo`, `EstaNoPeriodoDeProrrogacao` |
| P10 | Solicitação | só uma prorrogação: recusa se já foi deferida ("O prazo desta manifestação já foi prorrogado") ou se há uma pendente | `SolicitarProrrogacaoDePrazoHandler` |
| P11 | Solicitação aceita | cria `ProrrogacaoDePrazo` (quantidade de dias, motivação, operador, situação `Solicitada`) e envia e-mail aos operadores com a funcionalidade `GerenciarProrrogacoes` | `OnPostExecutedAsync` |
| P12 | Deferir | só se `Solicitada` e o homologador tem `GerenciarProrrogacoes`; soma `QtdDias` ao `Vencimento` se houver; senão, baixa o prazo de vencimento e cria outro com `QtdDias` a partir da data do anterior; situação → `Prorrogada` | `DeferirSolicitacaoDeProrrogacaoDePrazoHandler` |
| P13 | Deferir sem `Vencimento` e sem prazo de vencimento | erro "Não é possível prorrogar o prazo desta manifestação" | idem |
| P14 | Tramitação seccional | só se faltam mais de **9** dias (`PrazoTramitacaoSeccionalDias`) para o vencimento | `Manifestacao.PrazoPermiteTramitacaoSeccional` |
| P15 | Manifestação vencida | tramitar só se o último trâmite foi `Apurar` ou `EncaminharRespostaApuracao` (ou o operador tem `TratarBloqueadas`) | `ManifestacaoPermiteTramiteAposVencimento` |
| P16 | Prazo com `BloquearCaixaDeEntrada` pendente | a manifestação "bloqueante" faz as demais da mesma unidade ficarem bloqueadas para operadores sem `TratarBloqueadas` | `ConsultarManifestacaoBloqueante` (🔶 a consulta não foi lida) |

## Inferências e limitações
- 🔶 A contagem é em **dias corridos** com ajuste do término ao próximo dia útil (não em dias úteis contados). O texto de negócio (ex.: "20 dias") não está no código.
- 🔶 A janela de ±5 dias aceita solicitar prorrogação até 5 dias **depois** do vencimento; o valor 5 é fixo no código.
- 🔶 `DateTime.Today`/`DateTime.Now` são usados nas consultas e na entidade, enquanto o registro usa `IApplicationDateTime` ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]]).
- 🔶 `IndeferirSolicitacaoDeProrrogacaoDePrazo` não foi lido; o endpoint `indeferir` não restringe papel (só `[Authorize]`).
- 🔶 `Deferir(...)` é chamado antes da verificação de `IsValid` do comando; se a entidade mudar de estado e a transação for confirmada apesar das notificações, haveria deferimento indevido (a confirmar no SDK).
- 🔶 O deferimento não valida o limite de dias solicitado nem a unidade do homologador.
- ❓ Valor de `PrazoManifestacaoPadrao` e dos `NotificacaoDePrazo` cadastrados (dados).
- ❓ Origem dos feriados (`FeriadoSic`, `FeriadoSicReadRepository`).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Fluxo-Registro]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Fluxo-Tramitacao-e-Resposta]]

## Pendências e próximo passo
- Ler `IndeferirSolicitacao…`, `ConsultarManifestacaoBloqueante` e `Feriado*`.
- Perguntar ao time o valor de negócio do prazo e da janela de prorrogação.
