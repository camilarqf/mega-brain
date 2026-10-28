---
type: index
aliases:
  - "IBS — índice do sistema"
system: IBS
status: confirmado
updated: 2026-10-18
---
# IBS — índice do sistema

## Objetivo
Ponto de entrada do sistema **IBS** (Identity Broker Service): serviço de autenticação corporativa chamado pelo Keycloak da CGDF.

## Evidências
- Composição: [[Catalogo-de-Sistemas|Catálogo de sistemas]] e [[01-Sistemas/IBS/IBS-Repositorios|Repositórios]].
- Repositório `identity-broker-service`, commit `cf0959a` (ver [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Registro-de-Analise|Registro de análise]]).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `identity-broker-service` (componente `Backend`) | analisado (lotes 0 a 4 concluídos; cobertura parcial) | [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice do IBS Backend]] |

Notas do sistema:
- [[01-Sistemas/IBS/IBS-Contexto-do-Sistema|Contexto do sistema]]
- [[01-Sistemas/IBS/IBS-Repositorios|Repositórios]]

## Inferências e limitações
- Não há front-end conhecido. A visão de negócio depende de confirmar dono e consumidores do serviço.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integração Keycloak → IBS]]

## Pendências e próximo passo
- Próximo passo exato: ver [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Registro-de-Analise|Registro de análise]].
