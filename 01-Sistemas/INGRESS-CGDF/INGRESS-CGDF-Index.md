---
type: index
aliases:
  - "INGRESS-CGDF — índice do sistema"
system: INGRESS-CGDF
status: confirmado
updated: 2026-10-21
---
# INGRESS-CGDF — índice do sistema

## Objetivo
Ponto de entrada do sistema **INGRESS-CGDF**: o Nginx que roteia por path as requisições HTTP para os serviços Swarm da CGDF e repassa o tráfego TCP do RabbitMQ, em produção, staging e sandbox.

## Evidências
- Composição: [[Catalogo-de-Sistemas|Catálogo de sistemas]] e [[01-Sistemas/INGRESS-CGDF/INGRESS-CGDF-Repositorios|Repositórios]].
- Repositório `ingress-controller`, commit `a51459e` (ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Registro-de-Analise|Registro de análise]]).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `ingress-controller` (componente `Nginx`) | analisado (lotes 0 a 3 concluídos; leitura estática, cobertura completa do conteúdo versionado) | [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]] |

Notas do sistema:
- [[01-Sistemas/INGRESS-CGDF/INGRESS-CGDF-Contexto-do-Sistema|Contexto do sistema]]
- [[01-Sistemas/INGRESS-CGDF/INGRESS-CGDF-Repositorios|Repositórios]]

## Inferências e limitações
- Dono, SLA, domínios públicos e a camada à frente do Nginx (TLS, balanceador) não constam no repositório.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Registro-de-Analise|Registro de análise]].
