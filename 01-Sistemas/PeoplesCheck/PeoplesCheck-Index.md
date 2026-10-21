---
type: index
system: PeoplesCheck
status: confirmado
updated: 2026-10-19
tags:
  - peoplescheck
  - moc
  - sistema
---
# PeoplesCheck — índice do sistema

## Objetivo
Ponto de entrada do sistema **PeoplesCheck**: API REST que valida CPF e CNPJ contra bases cadastrais e conduz um desafio de identidade (perguntas sobre nome, nome da mãe e data de nascimento). É o provedor consumido pelo backend do `PARTICIPA-DF`.

## Evidências
- Composição: [[Catalogo-de-Sistemas|Catálogo de sistemas]] e [[01-Sistemas/PeoplesCheck/PeoplesCheck-Repositorios|Repositórios]].
- Repositório `cgdf-peoples-check-api`, commit `21dbf0b` (ver [[01-Sistemas/PeoplesCheck/Servico/99-Controle/PeoplesCheck-Servico-Registro-de-Analise|Registro de análise]]).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `cgdf-peoples-check-api` (componente `Servico`) | analisado (lotes 0 a 6 concluídos; leitura estática; cobertura completa do código da aplicação, testes não executados) | [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]] |

Notas do sistema:
- [[01-Sistemas/PeoplesCheck/PeoplesCheck-Contexto-do-Sistema|Contexto do sistema]]
- [[01-Sistemas/PeoplesCheck/PeoplesCheck-Repositorios|Repositórios]]

## Inferências e limitações
- A correspondência entre este repositório e o serviço `PeoplesCheck` consumido pelo `PARTICIPA-DF` foi confirmada pelo usuário em 2026-10-19 (os endpoints e o cabeçalho de chave de API também coincidem com o cliente documentado).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Próximo passo exato: ver [[01-Sistemas/PeoplesCheck/Servico/99-Controle/PeoplesCheck-Servico-Registro-de-Analise|Registro de análise]].
