---
type: module
aliases:
  - "Iza Api — módulo de predição de triagem"
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
sources:
  - src/main.py
  - src/Queries
  - src/internal/manifestacao.py
  - CHANGELOG.md
---
# Iza Api — módulo de predição de triagem

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Documentar a capacidade única do serviço: transformar `relato` (e, em cadeia, `assunto_id` e `classificacao_id`) em sugestões de assunto, classificação, unidade e indício de denúncia.

## Evidências
- Rotas em `src/main.py` e uma classe `query_*` por consulta em `src/Queries/`.

## Informações confirmadas
| Consulta (`src/Queries/`) | Modelo usado | Entrada do modelo | Resultado |
|---|---|---|---|
| `query_assunto_by_relato` | assunto (`clf.model_assunto_id`) | `[relato]` | `predict_proba`; ordena por probabilidade decrescente e devolve os `n` primeiros (`classes_` e probabilidades) |
| `query_classificacao_by_relato_and_assunto` | classificação | `DataFrame[Relato, Assunto_id]` | `predict`; primeiro elemento, ou `0` |
| `query_is_denuncia_by_relato_and_assunto` | denúncia (`clf.model_denuncia_assunto`) | `DataFrame[Relato, Assunto_id]` | `predict`; primeiro elemento, ou `0` |
| `query_unidade_by_relato_and_assunto_and_classificacao` | unidade | `DataFrame[Relato, Classificacao_id, Assunto_id]` | `predict`; primeiro elemento, ou `0`; `-1` para `assunto_id` 1694 ou 1695 |
| `query_permite_anonimato_by_relato_and_assunto` | denúncia + classificação | `DataFrame[Relato, Assunto_id]` | `1` se P(denúncia) ≥ limiar (0,05) ou classificação prevista = 2; senão `0` |
| `query_prob_classificacao…` · `query_prob_denuncia…` · `query_prob_unidade…` | classificação · denúncia · unidade | como acima | `predict_proba`; classes e probabilidades ordenadas de forma crescente |
| `query_classes_assunto` | assunto | — | `classes_` do modelo |
| `query_hash_modelo` | (arquivo) | nome do modelo | MD5 do arquivo `.joblib` |

**Regras verificáveis (condição → efeito)**
- ✅ Unidade: `assunto_id` ∈ {1694, 1695} → resposta `-1` (o modelo ainda é executado antes; o `CHANGELOG.md` 2.9.0 registra "Inclui exceção no ponto de unidade"). Só o 1694 tem teste.
- ✅ Anonimato: P(denúncia) ≥ 0,05 **ou** classificação prevista = 2 → `1` (permite). Limiar `0.05` fixo em `main.py`.
- ✅ Valor `0` é devolvido quando o modelo retorna lista vazia/zero (testes de verdade `any(response)`).

**Cadeia esperada pelo desenho (descrição da API):** assunto → classificação → (é denúncia) → unidade, em que cada passo usa a saída do anterior. ✅ O serviço não encadeia as chamadas: o cliente envia os valores de cada etapa. Ver [[01-Sistemas/Iza/Api/05-Fluxos/Iza-Api-Fluxo-Triagem-de-Manifestacao|Fluxo de triagem]].

**Histórico de versões relevante (`CHANGELOG.md`)**: 2.7.0 adicionou os endpoints de hash; 2.9.0 a exceção de unidade; 2.10.0 atualizou os 4 modelos para scikit-learn 1.5 e "altera regra de probabilidade do modelo de denúncia para 0.15"; 2.10.2 reverteu o modelo de denúncia (NearMiss 2).

## Inferências e limitações
- ❓ **Conflito de limiar:** o `CHANGELOG.md` (2.10.0) fala em 0,15 para a denúncia, a descrição do Swagger diz "> 0.05" para `is-denuncia`, `permite-anonimato-novo` usa 0,05 e `is-denuncia` não aplica limiar (usa `predict`). Não é possível dizer qual é a regra vigente sem confirmar com o time; nenhuma foi alterada nesta análise.
- ✅ O `CHANGELOG.md` termina em 2.10.2 (2024-06-19); `main.py` declara `2.11.1` (commits até 2026-03-26 sem entrada no changelog).
- 🔶 `is-denuncia` e `prob_denuncia` usam o mesmo arquivo de modelo (`relato_assunto_denuncia.joblib`) carregado duas vezes (`clf.model_denuncia` e `clf.model_denuncia_assunto`).
- 🔶 `src/Queries/query_permite_anonimato_by_relato.py` (só `relato`) não é importado por `main.py`; é compatível com a remoção do endpoint `/predict-permite-anonimato` na 2.4.0 (`CHANGELOG.md`). Código morto.
- ❓ Significado de negócio de `classificacao_id == 2`, dos assuntos 1694/1695 e dos códigos de unidade não consta no repositório.

## Relacionamentos
- [[01-Sistemas/Iza/Api/06-API/Iza-Api-Catalogo-de-Endpoints|Catálogo de endpoints]] · [[01-Sistemas/Iza/Api/02-Dominio/Iza-Api-Modelos-e-Artefatos|Modelos e artefatos]] · [[01-Sistemas/Iza/Api/09-Qualidade/Iza-Api-Testes-e-Cobertura|Testes]] · [[01-Sistemas/Iza/Api/09-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Confirmar com o time o limiar de denúncia vigente e o significado dos códigos fixos; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
