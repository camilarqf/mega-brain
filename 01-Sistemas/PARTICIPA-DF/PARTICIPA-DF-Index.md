---
type: index
system: PARTICIPA-DF
status: pendente
updated: 2026-10-18
tags:
  - participa-df
  - moc
  - sistema
---
# PARTICIPA-DF — índice do sistema

## Objetivo
Ponto de entrada do sistema de negócio **Participa DF**. Cada repositório tem documentação técnica em subpasta própria.

## Evidências
- Nome do aplicativo `Participa-DF` em `.jenkins-pipelines/deployment.params.yml`; namespace do código `OuvDF` (`src/OuvDF.sln`). Repositório `participa-df-backend`, commit `4901ad5`.
- Composição: [[Catalogo-de-Sistemas|Catálogo de sistemas]] e [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]].

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `participa-df-backend` | analisado (lotes 0 a 8; cobertura parcial) | [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] |
| `participa-df-frontend` (Frontend Cidadão, rótulo provisório) | analisado (lotes 0 a 5; cobertura parcial) | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] |
| `participa-df-ouv-frontend` (Frontend Ouvidoria, rótulo provisório) | analisado (lotes 0 a 5; cobertura parcial) | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] |
| `participa-df-sic-frontend` (Frontend SIC, rótulo provisório) | analisado (lotes 0 a 5; cobertura parcial) | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] |

Notas do sistema:
- [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Contexto-do-Sistema|Contexto do sistema]]: visão de negócio derivada do backend.
- [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]]: repositórios, commit analisado e estado.

Atalhos do frontend:
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Rotas-e-Telas|Rotas e telas]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas de API]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]

Atalhos do frontend de Ouvidoria:
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]]

Atalhos do frontend SIC:
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]]

Atalhos do backend:
- [[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Débitos técnicos e riscos]]
- [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]
- [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas]] · [[Mapa-de-Integracoes|Mapa de integrações]]
- [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências]]

## Inferências e limitações
- 🔶 A visão de negócio vem só do backend; a finalidade legal e o dono do sistema não constam no código.
- A visão integrada de telas e fluxos cobre os 3 front-ends (Cidadão, Ouvidoria e SIC), analisados separadamente.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Home|Home]]

## Pendências e próximo passo
- Responder as perguntas de [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências]] com o time e tratar os débitos 🔴.
- Analisar o front-end SIC quando for identificado; para atualizar o backend após novos commits, usar `atualizar-documentacao`.
