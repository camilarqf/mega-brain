---
type: system
system: SICI
repository: ""
status: pendente
analyzed_commit: ""
updated: 2026-10-18
tags: [sici, moc, sistema]
---
# SICI — índice do sistema

## Objetivo
Ponto de entrada do sistema de negócio **SICI**. O sistema é composto por mais de um repositório; cada um tem sua própria documentação técnica em subpasta.

## Evidências
- Composição do sistema: [[Catalogo-de-Sistemas|Catálogo de sistemas]] e [[01-Sistemas/SICI/Repositorios|Repositórios]].
- Documentação técnica do backend: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] (commit `1871e32`).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `sici-backend` | analisado (6 lotes; cobertura parcial em 2 notas) | [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] |
| `sici-frontend` | **não analisado** | [[01-Sistemas/SICI/Repositorios|Repositórios]] |

Notas do sistema:
- [[01-Sistemas/SICI/Contexto-do-Sistema|Contexto do sistema]]: visão de negócio derivada do backend.
- [[01-Sistemas/SICI/Repositorios|Repositórios]]: repositórios, commits analisados e estado.

Atalhos do backend:
- [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Débitos técnicos e riscos]]
- [[01-Sistemas/SICI/Backend/05-API/Catalogo-de-Endpoints|Catálogo de endpoints]]
- [[01-Sistemas/SICI/Backend/99-Controle/Registro-de-Analise|Registro de análise]] · [[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendências]]

## Inferências e limitações
- A visão integrada (fluxos de tela → API) só será consolidada depois da análise do frontend.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Home|Home]]

## Pendências e próximo passo
- Analisar `sici-frontend` quando autorizado (skill `documentar-sistema`) e criar `01-Sistemas/SICI/Frontend/`.
- Responder as perguntas de [[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendências]].
