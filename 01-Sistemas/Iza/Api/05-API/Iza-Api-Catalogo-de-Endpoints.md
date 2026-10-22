---
type: api
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - api
  - endpoints
sources:
  - src/main.py
  - src/internal/manifestacao.py
  - src/Queries
  - src/internal/description.py
---
# Iza Api — catálogo de endpoints

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Documentar o contrato HTTP exposto. Nenhum endpoint exige autenticação.

## Evidências
- `src/main.py` (decoradores `@app.post` / `@app.get`), `src/internal/manifestacao.py`, classes em `src/Queries/`. Respostas não foram executadas (leitura estática); os formatos abaixo vêm do código.

## Informações confirmadas
**Corpo das requisições `POST`** (`Manifestacao`, JSON): `relato` (string, **único campo obrigatório**), `assunto_id` (int, opcional), `classificacao_id` (int, opcional), `n_assuntos` (int, opcional e **não utilizado**). Campos desconhecidos são ignorados (padrão do Pydantic).

| Método | Caminho | Entrada usada | Resposta (formato no código) |
|---|---|---|---|
| POST | `/predict-assunto-by-relato?n_assuntos=10` | `relato`; `n_assuntos` vem da **query string** (padrão 10) | `{"assuntos": [ids], "probabilidades": [p…]}` em ordem decrescente |
| POST | `/predict-classificacao-by-relato-assunto` | `relato`, `assunto_id` | `{"response": <classificacao_id previsto>}` (0 se o modelo não devolver valor) |
| POST | `/predict-is-denuncia-by-relato-assunto` | `relato`, `assunto_id` | `{"response": 0 ou 1}` (resultado direto do `predict`, **sem limiar**) |
| POST | `/predict-unidade-by-relato-assunto-classificacao` | `relato`, `assunto_id`, `classificacao_id` | `{"response": <unidade>}`; `-1` se `assunto_id` ∈ {1694, 1695} |
| POST | `/predict-permite-anonimato-novo` | `relato`, `assunto_id` | `{"response": 0 ou 1}`; ver regra abaixo |
| POST | `/prob_classificacao_by_relato_and_assunto` | `relato`, `assunto_id` | `{"response": {"tipologias": [...], "probabilidades": [...]}}` em ordem **crescente** |
| POST | `/prob_denuncia_by_relato_and_assunto` | `relato`, `assunto_id` | `{"response": {"denuncia": [0,1 ordenados], "probabilidades": [...]}}` em ordem crescente |
| POST | `/prob_unidade_by_relato_and_assunto` | `relato`, `assunto_id`, `classificacao_id` | `{"response": {"unidades": [...], "probabilidades": [...]}}` em ordem crescente |
| GET | `/assuntos` | — | `{"assuntos": [ids conhecidos pelo modelo]}` |
| GET | `/hash_modelo_assunto` · `/hash_modelo_classificacao` · `/hash_modelo_denuncia` · `/hash_modelo_unidade` | — | `{"hash": "<md5 do arquivo .joblib>"}` |
| GET | `/health-check` | — | `true` (200) |
| GET | `/prometheus` | — | métricas Prometheus |
| GET | `/docs` (e `/openapi.json`) | — | Swagger do FastAPI (gerado automaticamente; coberto por teste) |

**Regra de `/predict-permite-anonimato-novo`** (✅ `query_permite_anonimato_by_relato_and_assunto`, limiar `0.05` fixo em `main.py`): devolve `1` se P(denúncia) ≥ 0,05; senão `1` se a classificação prevista for `2`; senão `0`. A docstring a descreve como indicador de "reclamação ou denúncia".

**Erros:** a validação do Pydantic devolve `422` quando falta `relato` ou há tipo inválido (coberto por testes). ✅ `404` para rotas inexistentes. Não há tratamento de exceções próprio: uma falha do modelo resulta em `500` padrão.

## Inferências e limitações
- ✅ Só `relato` é obrigatório. Se `assunto_id` ou `classificacao_id` forem omitidos, as consultas ainda são executadas com `None`; 🔶 o resultado depende do modelo (possível erro `500`), sem validação explícita (não executado).
- 🔶 As consultas montam o `DataFrame` a partir de `np.array([relato, assunto_id])`, o que converte os valores para texto (`assunto_id` vira `str`); o comportamento correto assume que o pipeline do modelo trata isso. Não verificável sem os modelos.
- 🔶 O consumidor `PARTICIPA-DF` documenta o campo como `classificao_id` (sem o segundo "c"); esta API só reconhece `classificacao_id` e ignora o outro silenciosamente (`classificacao_id` ficaria `None`). Verificar no cliente; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
- ❓ Quais endpoints são de fato usados: o vault só registra 4 operações do `PARTICIPA-DF` (assunto, classificação, é-denúncia, unidade). Os de probabilidade, anonimato e `hash_modelo_*` não têm consumidor identificado.
- ❓ A descrição do Swagger afirma limiar `0.05` para `is-denuncia`, mas o código não aplica limiar e o `CHANGELOG.md` (2.10.0) cita `0.15`; ver [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]].

## Relacionamentos
- [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] · [[01-Sistemas/Iza/Api/04-Fluxos/Iza-Api-Fluxo-Triagem-de-Manifestacao|Fluxo de triagem]] · [[01-Sistemas/Iza/Api/06-Seguranca/Iza-Api-Seguranca|Segurança]] · [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Integrações]]

## Pendências e próximo passo
- Confirmar o nome do campo no cliente e os endpoints realmente consumidos.
