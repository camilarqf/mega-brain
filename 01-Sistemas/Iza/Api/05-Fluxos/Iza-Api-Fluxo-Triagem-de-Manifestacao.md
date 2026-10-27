---
type: flow
system: Iza
component: Api
repository: cgdf-iza
status: inferido
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - fluxo
  - triagem
sources:
  - src/main.py
  - src/internal/description.py
  - src/Queries
---
# Iza Api — fluxo de triagem de manifestação

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Descrever a sequência de chamadas que a API foi desenhada para atender e o que ocorre dentro dela em cada uma. A orquestração entre as chamadas é feita pelo **cliente**, não por este serviço.

## Evidências
- `src/internal/description.py` ("Novo fluxo": assunto → classificação → é denúncia → unidade) e as rotas correspondentes em `src/main.py`.
- Lado do consumidor (vault): passo `RecuperarDadosIA` do registro de manifestação do `PARTICIPA-DF`, em [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas do PARTICIPA-DF Backend]] (não verificado neste repositório).

## Informações confirmadas
| Passo | Chamada | Entrada | Saída usada no passo seguinte |
|---|---|---|---|
| 1 | `POST /predict-assunto-by-relato` | `relato` (e `n_assuntos` na query) | lista de assuntos prováveis e probabilidades |
| 2 | `POST /predict-classificacao-by-relato-assunto` | `relato`, `assunto_id` | `classificacao_id` previsto |
| 3 | `POST /predict-is-denuncia-by-relato-assunto` | `relato`, `assunto_id` | 0 ou 1 |
| 4 | `POST /predict-unidade-by-relato-assunto-classificacao` | `relato`, `assunto_id`, `classificacao_id` | unidade de trâmite inicial (`-1` para os assuntos de exceção) |

- ✅ Cada chamada é independente e sem estado: o serviço não guarda o relato, o assunto escolhido nem os resultados.
- ✅ Os endpoints `prob_*` e `predict-permite-anonimato-novo` oferecem consultas auxiliares fora dessa sequência; não há evidência de uso nesta cadeia.

## Inferências e limitações
- 🔶 O assunto do passo 2 em diante é escolhido pelo cliente (provavelmente o de maior probabilidade ou o informado pelo cidadão); este repositório não define essa escolha.
- 🔶 Segundo a documentação do consumidor no vault, falhas do serviço são tratadas no `PARTICIPA-DF` com valores padrão (denúncia `false`, classificação 999, unidade `01005`), o que não pode ser conferido aqui; o contrato da Iza não define códigos de erro próprios.
- ❓ Se o cliente chama o passo 3 antes ou depois do 2 e como trata o `-1` não é verificável neste repositório.

## Relacionamentos
- [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] · [[01-Sistemas/Iza/Api/06-API/Iza-Api-Catalogo-de-Endpoints|Catálogo de endpoints]] · [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Integrações]]

## Pendências e próximo passo
- Validar a sequência no código do consumidor quando o repositório do `PARTICIPA-DF` for revisitado.
