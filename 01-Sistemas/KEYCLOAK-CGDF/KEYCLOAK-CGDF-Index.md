---
type: index
aliases:
  - "KEYCLOAK-CGDF — índice do sistema"
system: KEYCLOAK-CGDF
status: pendente
updated: 2026-10-18
---
# KEYCLOAK-CGDF — índice do sistema

## Objetivo
Ponto de entrada do sistema **KEYCLOAK-CGDF**: a instância de Keycloak customizada da CGDF (imagem Docker, extensão Java e tema de login). O ID do sistema foi escolhido pelo usuário em 2026-10-18; `Keycloak` (sem sufixo) continua sendo o ID do serviço externo no catálogo.

## Evidências
- Composição: [[Catalogo-de-Sistemas|Catálogo de sistemas]] e [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Repositorios|Repositórios]].
- Repositório `keycloak`, commit `1755591` (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Registro-de-Analise|Registro de análise]]).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `keycloak` (componente `Servico-Keycloak`) | analisado (lotes 0 a 3; cobertura parcial) | [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice do Serviço Keycloak]] |

Notas do sistema:
- [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Contexto-do-Sistema|Contexto do sistema]]
- [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Repositorios|Repositórios]]

## Inferências e limitações
- A visão de negócio compartilhada só será consolidada com mais evidências (configuração de realms e clients não está no repositório).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]] · [[Home|Home]]

## Pendências e próximo passo
- Próximo passo exato: ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Registro-de-Analise|Registro de análise]].
