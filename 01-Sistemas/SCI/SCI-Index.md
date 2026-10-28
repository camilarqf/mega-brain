---
type: index
aliases:
  - "SCI — índice do sistema"
system: SCI
status: pendente
updated: 2026-10-19
---
# SCI — índice do sistema

## Objetivo
Ponto de entrada do sistema de negócio **SCI**. Backend e frontend foram analisados (ver [[01-Sistemas/SCI/SCI-Repositorios|Repositórios]]).

## Evidências
- Cadastro: [[Catalogo-de-Sistemas|Catálogo de sistemas]] (ID `SCI`, cadastrado em 2026-10-19 por autorização do usuário).
- Documentação técnica do backend: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] (commit `8e3c8648`).
- Documentação técnica do frontend: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] (commit `5e20fda1`; repositório `sci-frontend` confirmado pelo usuário em 2026-10-19).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `sci-backend` | analisado (lotes 0 a 6 concluídos; cobertura parcial) | [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] |
| `sci-frontend` | analisado (lotes 0 a 4 concluídos; leitura estática; cobertura parcial) | [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] |

Notas do sistema:
- [[01-Sistemas/SCI/SCI-Contexto-do-Sistema|Contexto do sistema]]
- [[01-Sistemas/SCI/SCI-Repositorios|Repositórios]]

Atalhos do frontend:
- [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Debitos-Tecnicos|Débitos técnicos e riscos]] · [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]]
- [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]]

Atalhos do backend:
- [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos e riscos]]
- [[01-Sistemas/SCI/Backend/06-API/SCI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]
- [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]]

## Inferências e limitações
- 🔶 O SCI é a contraparte dos eventos de denúncia do `PARTICIPA-DF` (mesmos nomes de canal nos dois lados; ver [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Integração por eventos]]).
- ❓ Não há relação verificada com o sistema `SICI` (stack e domínio diferentes).
- 🔶 8 chamadas do frontend não têm rota no backend analisado; ver [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]].

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]] · [[Home|Home]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]].
