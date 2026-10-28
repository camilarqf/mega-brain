---
type: index
aliases:
  - "Iza — índice do sistema"
system: Iza
status: confirmado
updated: 2026-10-22
---
# Iza — índice do sistema

## Objetivo
Ponto de entrada do sistema **Iza** ("Robô Iza", projeto OUV-IA): API de inferência que sugere assunto, classificação (tipologia), unidade de trâmite inicial e indício de denúncia a partir do relato de uma manifestação.

## Evidências
- Composição: [[Catalogo-de-Sistemas|Catálogo de sistemas]] e [[01-Sistemas/Iza/Iza-Repositorios|Repositórios]].
- Repositório `cgdf-iza`, commit `988360c` (ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Registro-de-Analise|Registro de análise]]).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `cgdf-iza` (componente `Api`) | analisado (lotes 0 a 3 concluídos; leitura estática; cobertura parcial: os modelos `.joblib` não fazem parte do repositório) | [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]] |

Notas do sistema:
- [[01-Sistemas/Iza/Iza-Contexto-do-Sistema|Contexto do sistema]]
- [[01-Sistemas/Iza/Iza-Repositorios|Repositórios]]

## Inferências e limitações
- Dono do serviço não identificado (o código traz apenas um contato individual, que não é reproduzido aqui).
- 🔶 O consumidor conhecido é o backend do `PARTICIPA-DF`, pela correspondência de nomes de operações; ver [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Integrações]].

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Próximo passo exato: ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Registro-de-Analise|Registro de análise]].
