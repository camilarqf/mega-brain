---
type: reference
system: PARTICIPA-DF
repository: participa-df-backend
status: inferido
coverage: parcial
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-23
tags:
  - participa-df
  - backend
  - glossario
sources:
  - src/OuvDF.Api/Startup.cs
  - src/OuvDF.Api/appsettings.json
  - src/OuvDF.IntegrationServices/Consumers
  - src/OuvDF.ServicoInformacaoCidadao/Jobs
  - src/OuvDF.Shared/Jobs
---

# Glossário

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]]

## Objetivo
Reunir os termos do código e seu significado. As definições vêm **de nomes de classes e configurações**; só viram fato após a confirmação do time ou da leitura do domínio nos lotes 3 a 5.

## Evidências
Nomes de classes, comandos, chaves de configuração e comentários de logs, no commit `4901ad5`. Cada linha indica o grau de confirmação.

## Informações confirmadas e inferências
| Termo | Significado | Confirmação / evidência |
|---|---|---|
| **OuvDF** | Prefixo do namespace e da solução; pasta e projetos `OuvDF.*` | ✅ nome no código. Relação com o nome "Participa DF" (pipeline): ❓ |
| **SO** (Serviço de Ouvidoria) | Módulo de manifestações | 🔶 `OuvDF.ServicoOuvidoria`, `OperadorSO`, `PerfilSO`; a expansão "SO" não está escrita no código |
| **SIC** (Serviço de Informação ao Cidadão) | Módulo de pedidos de acesso à informação | 🔶 `OuvDF.ServicoInformacaoCidadao`, `OperadorSIC`; "SIC" não está expandido no código |
| **Manifestação** | Registro feito por cidadão ou operador na Ouvidoria; tem situação, vencimento e prazos | ✅ entidade `Manifestacao` e comandos `RegistrarManifestacao*` |
| **Pedido** | Pedido de acesso à informação no SIC; tem prazo vigente, situação, recursos | ✅ entidade `Pedido`, `RegistrarPedido*` |
| **Recurso (1ª, 2ª, 3ª instância)** | Contestação de resposta a um pedido | ✅ situações `EmRecursoDePrimeiraInstancia` e `EmRecursoDeSegundaInstancia`; templates de e-mail de 3 instâncias e chaves de prazo de 3ª instância |
| **Prorrogação** | Extensão do prazo de manifestação ou pedido | ✅ situação `Prorrogada`/`Prorrogado`, comandos `Prorrogar*` |
| **Omissão de resposta** | Pedido sem resposta no prazo; gera notificação | ✅ comandos `RegistrarNotificacaoOmissaoResposta` e `…CGDF` |
| **Reclamação ao órgão** | Situação em que o pedido está em reclamação ao órgão | 🔶 `SituacaoPedidoEnum.ReclamacaoOrgao` (uso no job de omissão CGDF) |
| **Reclassificação** | Mudança de classificação de manifestação, parcial ou integral | ✅ workflow `ReclassificarManifestacaoWorkflow` |
| **Trâmite** | Encaminhamento/movimentação da manifestação entre unidades | 🔶 `TramiteController`, passo `CriarTramite` |
| **Operador** | Usuário interno que atende (SIC ou SO); tem acesso expirável | ✅ `OperadorSIC`, `OperadorSO`, jobs de desabilitação por 90 dias sem acesso |
| **Operador do sistema** | Operador técnico usado para ações automáticas | ✅ `SharedSettings.IdOperadorSistema` (usado em `BloquearUsuariosFalecidosJob`) |
| **Unidade** | Órgão/unidade que recebe e responde manifestações e pedidos | ✅ `UnidadeController`, `Pedido.Unidade` |
| **CGDF** | Controladoria-Geral do Distrito Federal | 🔶 prefixo do SDK `CGDF.*` e tipos `…CGDF`; usado nos jobs `…-omissao-resposta-cgdf` |
| **COACI / CQ / OGDF** | Unidades configuradas em `ServicoOuvidoriaSettings.UnidadeServicoOuvidoriaSettings`; COACI aparece na mensagem de denúncia aceita | ✅ nomes de chaves e texto do consumer; siglas ❓ sem expansão |
| **Zeladoria** | Tipo de solicitação de zeladoria urbana; há política `IsSolicitacaoZeladoria`, tema `IdTemaZeladoria` e passo `BloquearSolicitacaoZeladoria` | ✅ nomes; regra ❓ lote 4 |
| **Denúncia** | Manifestação classificada como denúncia, tramitada da COACI à ouvidoria; gera os eventos `denuncia-criada` e `denuncia-registrada` (com arquivos no S3), e os eventos externos aceita/recusada **liberam** o bloqueio externo (os dois) e limpam os arquivos | ✅ consumidores `DenunciaCriada`, `DenunciaAceita` e `DenunciaRecusada` (atualizado em 2026-10-23, `820666c`; antes: "evento externo aceito/recusado que libera ou mantém bloqueio", a parte "mantém" estava incorreta) |
| **Iza** | Serviço externo usado para classificação, assunto e denúncia | 🔶 `OuvDF.Iza.Client` (`ClassificationRequest`, `SubjectRequest`, `AccusationRequest`); tipo exato ❓ |
| **PeoplesCheck** | Serviço externo de validação de pessoas (CPF/PJ, desafio) | 🔶 chaves `CheckEndpoint`, `CheckPJEndpoint`, `ChallengeEndpoint`; ❓ finalidade |
| **MailService** | Serviço de envio de e-mail (por fila e API) | ✅ `MailServiceClientSettings`, `MailServiceApiSettings`, health check |
| **SEI** | Sistema de processos eletrônicos | 🔶 `CGDF.SEI.DotNet.SDK`, `SeiConnectionSettings`; sigla não expandida no código |
| **Workflow** | Sequência de passos de um caso de uso | ✅ `PipelineBehaviorWorkflow` + `AddStep` |
| **Job** | Rotina disparada por endpoint `/jobs/v2/{nome}` | ✅ `IJob` |
| **Usuário falecido** | Pessoa com CPF constante em `UsuarioFalecido`; é bloqueada por job | ✅ `BloquearUsuariosFalecidosJob` |

## Inferências e limitações
- Termos 🔶 e ❓ dependem de confirmação com o time (ver [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências]]).
- A nota será revisada nos lotes 3 a 5, quando o domínio for lido.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]] · [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]] · [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]]

## Pendências e próximo passo
- Pedir ao time a expansão oficial de SO, SIC, SEI, COACI, CQ, OGDF e a finalidade de Iza e PeoplesCheck.
