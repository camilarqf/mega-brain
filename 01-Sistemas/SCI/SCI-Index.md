---
type: index
system: SCI
status: pendente
updated: 2026-10-19
tags:
  - sci
  - moc
  - sistema
---
# SCI — índice do sistema

## Objetivo
Ponto de entrada do sistema de negócio **SCI**. Só o backend foi analisado; o frontend é citado como `não analisado` em [[01-Sistemas/SCI/SCI-Repositorios|Repositórios]].

## Evidências
- Cadastro: [[Catalogo-de-Sistemas|Catálogo de sistemas]] (ID `SCI`, cadastrado em 2026-10-19 por autorização do usuário).
- Documentação técnica do backend: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] (commit `8e3c8648`).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `sci-backend` | analisado (lotes 0 a 6 concluídos; cobertura parcial) | [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] |
| frontend | não analisado (repositório não identificado) | — |

Notas do sistema:
- [[01-Sistemas/SCI/SCI-Contexto-do-Sistema|Contexto do sistema]]
- [[01-Sistemas/SCI/SCI-Repositorios|Repositórios]]

Atalhos do backend:
- [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos e riscos]]
- [[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]
- [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]]

## Inferências e limitações
- 🔶 O SCI é a contraparte dos eventos de denúncia do `PARTICIPA-DF` (mesmos nomes de canal nos dois lados; ver [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Integração por eventos]]).
- ❓ Não há relação verificada com o sistema `SICI` (stack e domínio diferentes).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]] · [[Home|Home]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]].
