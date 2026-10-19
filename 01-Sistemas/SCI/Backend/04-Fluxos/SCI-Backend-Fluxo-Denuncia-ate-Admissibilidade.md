---
type: flow
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
  - fluxo
  - denuncia
  - admissibilidade
sources:
  - src/SCI.IntegrationServices/EventConsumers/DenunciaRegistradaConsumer.cs
  - src/SCI.Application/UseCases/GestaoIntegracao
  - src/SCI.Application/EventHandlers
  - src/SCI.Domain/GestaoAdmissibilidade/Entities/ProcessoAdmissibilidade.cs
---
# SCI Backend — fluxo da denúncia até a conclusão da admissibilidade

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Descrever, de ponta a ponta, os passos, estados e atores entre o recebimento da denúncia e a conclusão do processo de admissibilidade (e o possível PIP).

## Evidências
- Handlers e entidades em `sources`; detalhes por etapa nas notas de módulo linkadas.

## Informações confirmadas
| # | Passo | Ator | Efeito |
|---|---|---|---|
| 1 | Evento `denuncia-registrada` chega do `PARTICIPA-DF` | sistema | cria `Denuncia` (`AA`) ou publica `denuncia-recusada` se a unidade não está habilitada |
| 2 | Aceitar/recusar denúncia | AutoridadeCorrecional | `AC` ou `RE`; publica `denuncia-aceita` / `denuncia-recusada` |
| 3 | Cadastrar e tratar demanda | ApoioCorrecional (criar); AutoridadeCorrecional (tratar) | demanda `CPA`, `CM` ou `CPAM` |
| 4 | `DemandaTratada` cria o processo de admissibilidade | sistema | `AD` (sem relator) ou `AC` |
| 5 | Distribuir ao analista | Gestor / Autoridade | relator definido; `AC` |
| 6 | Cadastrar fatos, envolvidos e evidências | AnalistaAdmissibilidade | `EC` → concluir cadastro → `AA`; cria a análise |
| 7 | Analisar: itens por envolvido com tipificações e recomendações | AnalistaAdmissibilidade | `EA`; conclusão exige ≥1 recomendação por envolvido |
| 8 | Revisões conforme a configuração (Preliminar `ERR`, Técnica `ERG`, Admissibilidade `ERA`) | RevisorJad, Gestor, Autoridade | aprovar ou reprovar (a reprovação gera `RevisaoAdmissibilidadeReprovada`; o efeito no processo não foi lido) |
| 9 | Assinar a nota técnica em cadeia | Analista → Revisor → Gestor → Autoridade | `AAAN`/`AARE`/`AAG`/`AAAU` → `AF` |
| 10a | Concluir | AnalistaAdmissibilidade | `PC`; se há recomendação `PIP`/`IPF` e a unidade tem configuração de PIP, cria o PIP |
| 10b | Encaminhar a outras unidades | Analista, Apoio, Autoridade | `AE`; aceite cria novo processo na unidade destino — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Encaminhamento|Encaminhamento]] |
| 11 | Registrar número do SEI | ApoioCorrecional | `FES` |

## Inferências e limitações
- ❓ **Lacuna**: a passagem de denúncia aceita para demanda não existe no backend lido; o usuário não sabe se a funcionalidade foi concluída. Os passos 2 e 3 podem estar desconectados no estado atual.
- 🔶 Sequência real de revisões depende da configuração por unidade (seeds não lidos).
- Falhas: eventos de domínio são tratados após a gravação; um erro no handler (ex.: sem configuração do processo) deixa o estado anterior gravado — [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Arquitetura-CQRS-e-Event-Sourcing|Arquitetura]].

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denúncia e Demanda]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Admissibilidade]] · [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|Ciclo do PIP]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Eventos com o PARTICIPA-DF]]

## Pendências e próximo passo
- Confirmar com o time se a conversão do passo 2 para o 3 está prevista.
