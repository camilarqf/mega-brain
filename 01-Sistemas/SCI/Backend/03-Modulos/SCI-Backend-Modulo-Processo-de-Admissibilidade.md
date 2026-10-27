---
type: module
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
updated: 2026-10-23
tags:
  - sci
  - backend
  - modulo
  - admissibilidade
  - nota-tecnica
sources:
  - src/SCI.Domain/GestaoAdmissibilidade/Entities/ProcessoAdmissibilidade.cs
  - src/SCI.Domain/GestaoAdmissibilidade/Entities/AnaliseAdmissibilidade.cs
  - src/SCI.Domain/GestaoAdmissibilidade/Rules
  - src/SCI.Application/EventHandlers/CadastroAdmissibilidadeConcluidoEventHandler.cs
  - src/SCI.Application/EventHandlers/AnaliseAdmissibilidadeConcluidaEventHandler.cs
  - src/SCI.Application/EventHandlers/ProcessoAdmissibilidadeConcluidoEventHandler.cs
  - src/SCI.Api/Controllers/ProcessoAdmissibilidadeController.cs
  - src/SCI.Api/Controllers/AnaliseAdmissibilidadeController.cs
  - src/SCI.Domain/GestaoProcessual/Entities
---
# SCI Backend — módulo Processo de Admissibilidade

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar o processo de admissibilidade, sua análise, revisões, nota técnica e conclusão.

## Evidências
- Entidades, regras (`Rules/*`) e handlers listados em `sources`. Símbolos principais: `ProcessoAdmissibilidade.{DistribuirParaAnalista, ConcluirCadastro, IniciarRevisaoPorTipo, OrquestrarAssinatura, SincronizarFluxoAssinatura, ConcluirProcesso, AtualizarProcessoSei}`, `AnaliseAdmissibilidade.{EnvolvidosRecomendadosParaPIP, Aprovar}`.

## Informações confirmadas
### Estados e transições (domínio)
| Passo | Efeito | Condição / regra |
|---|---|---|
| Criação | `AD` (sem relator) ou `AC` (com relator) | `ProcessoAdmissibilidade.Criar` |
| Distribuir para analista | `AC` | perfil Gestor/Autoridade ([[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|políticas]]) |
| Redistribuir | mantém o estado, evento com justificativa | `ProcessoAdmissibilidadeAptoParaRedistribuir`: recusa se já está com o analista informado |
| Atualizar cadastro | `AC` → `EC` (em cadastro) | só muda o estado se o processo tem fatos e está em `AC`; analista |
| Concluir cadastro | `AA` | só se `EC` ("Não foi possível concluir o cadastro") |
| Reabrir | `EC` | não reabre se o estado é `Unknown`, `AD`, `AC` ou `EC` ("Não foi possível reabrir o processo.") |
| Iniciar análise | `EA` | |
| Revisão por tipo | `ERR` (Preliminar), `ERG` (Técnica), `ERA` (Admissibilidade) | outro tipo → `InvalidSciOperationException` |
| Fim da revisão | análise `Aprovar()` e processo vai para assinatura do Analista (`AAAN`) | `FinalizarRevisaoAdmissibilidade` |
| Assinatura da nota técnica | `AAAN` → `AARE` → `AAG` → `AAAU` conforme as revisões **ativas** da configuração, depois `AF` | `OrquestrarAssinatura`: só o perfil do estado atual assina ("Usuário não é o próximo revisor a assinar") |
| Invalidar nota técnica | evento `NotaTecnicaInvalidada` | não permitido se `PC` ou `FES` |
| Concluir | `PC` + evento `ProcessoAdmissibilidadeConcluido` | `ProcessoAdmissibilidadeAptoParaConclusao`: estar em `AF` e possuir nota técnica |
| Atualizar dados do SEI | `FES` (+ `NumeroProcessoSei`) | número informado por usuário |

### Análise
- ✅ Ao concluir o cadastro, `CadastroAdmissibilidadeConcluidoEventHandler` cria a `AnaliseAdmissibilidade` (ou sincroniza a análise em andamento).
- ✅ **Regra de conclusão da análise** (`AnaliseAdmissibilidadeAptaParaConclusao`): estar `EA` e ter **ao menos uma recomendação para cada envolvido**.
- ✅ Ao concluir a análise (`AnaliseAdmissibilidadeConcluida`), o handler dispara `CriarRevisaoAdmissibilidadeCommand` com a configuração do processo; sem configuração lança `InvalidOperationException` ("Configuração não definida para este processo de admissibilidade.").
- ✅ Notas da análise (`StatusNotaAdmissibilidadeEnum`: Criada, Aceita, Recusada) criadas/atualizadas/concluídas pelo AssessorAutoridade; regras `NotaAdmissibilidadeApta*`.
- ✅ Revisões: `RevisaoAdmissibilidade` com tipo e status (`EmAndamento`, `Reprovada`, `NaoAdmitida`, `Admitida`); reprovação gera `RevisaoAdmissibilidadeReprovada`.

### Geração do PIP
- ✅ Ao concluir o processo, `ProcessoAdmissibilidadeConcluidoEventHandler`: se já existe PIP, só registra aviso; usa a análise aprovada; **se algum envolvido tem recomendação `PIP` ou `IPF`** e a unidade de origem tem configuração ativa para PIP, cria o PIP com os fatos desses envolvidos; sem configuração, não cria e registra aviso. Ver [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]].

### Consultas
- ✅ Visões por perfil (gestor, autoridade, assessor, analista, apoio, revisor), por unidade e nota técnica — [[01-Sistemas/SCI/Backend/06-API/SCI-Backend-Catalogo-de-Endpoints|Endpoints]].

### Atualizações de 2026-10-23 (`29989114`)
- ✅ O clone do processo (correção "clonar JAD", `4e004181`) passou a manter as evidências ligadas aos envolvidos e os anexos de evidência (`Fato.Clonar`, `Evidencia.Clonar`).
- ✅ A demanda que origina o processo pode ter vindo de denúncia ([[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denúncia e Demanda]]); a consulta de demanda por processo foi ajustada (`QueryByProcessoAdmissibilidade`).

## Inferências e limitações
- 🔶 As regras de `ConfiguracaoProcesso` (revisões ativas) foram lidas pelo uso, não integralmente.
- 🔶 Fluxo de revisão detalhado por tipo (quem revisa em cada etapa) depende da configuração em banco (seeds `23-Insert-FLUXO_CONFIGURACAO` e `24-Insert-FLUXO_JAD`, não lidos).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Encaminhamento|Encaminhamento]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Documentos-e-Assinaturas|Documentos e assinaturas]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Unidade-e-Configuracao|Unidade e configuração]] · [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo]]

## Pendências e próximo passo
- Ler os seeds de configuração de fluxo (sem dados pessoais) para documentar a sequência de revisões por unidade.
