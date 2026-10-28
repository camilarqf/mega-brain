---
type: domain
aliases:
  - "Iza Api — modelos e artefatos"
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
sources:
  - src/main.py
  - src/Queries/query_hash_modelo.py
  - src/internal/manifestacao.py
  - Dockerfile
  - .gitignore
---
# Iza Api — modelos e artefatos

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Descrever os artefatos de modelo que a API carrega e as entidades conceituais da triagem. Não há entidades persistidas nem banco.

## Evidências
- `src/main.py` (`load_models`), `src/Queries/query_hash_modelo.py`, `src/internal/manifestacao.py`, `Dockerfile` (`models_path`), `.gitignore` (`models/`).

## Informações confirmadas
**Artefatos carregados** (`<models_path>/…`, `models_path` = variável de ambiente; `/mnt/iza-modelos` na imagem):
| Arquivo | Atributo em `clf` | Uso |
|---|---|---|
| `relato_assunto.joblib` | `model_assunto_id` | sugestão de assunto e lista de assuntos |
| `relato_assunto_classificacao.joblib` | `model_relato_assunto_classificacao` | classificação/tipologia e probabilidades; parte da regra de anonimato |
| `relato_assunto_denuncia.joblib` | `model_denuncia` **e** `model_denuncia_assunto` (duas cargas do mesmo arquivo) | indício de denúncia e probabilidades |
| `relato_assunto_classificacao_unidade.joblib` | `model_unidade` | unidade de trâmite inicial e probabilidades |

**Entradas conceituais** (`Manifestacao` e colunas dos modelos): `Relato` (texto livre), `Assunto_id`, `Classificacao_id`. **Saídas conceituais:** assunto (id), classificação/tipologia (id), denúncia (0/1), unidade (id), `-1` como "sem unidade sugerida" nos assuntos de exceção.

- ✅ A pasta `models/` está no `.gitignore`: os modelos e seus dados de treino não são versionados aqui.
- ✅ `query_hash_modelo` lê o arquivo inteiro e calcula MD5 a cada chamada; serve para conferir qual versão do modelo está em uso.
- ✅ `models_path` é lido por `query_hash_modelo` **na importação do módulo** e por `load_models` na inicialização; sem a variável, a aplicação nem importa.

## Inferências e limitações
- ❓ Estrutura interna dos pipelines (vetorização, algoritmo, classes), versão de treino, métricas e origem dos dados não são conhecidas. `lightgbm` e `imbalanced-learn` nas dependências sugerem pipelines que as usam (🔶).
- ❓ Quem treina, publica e versiona os `.joblib` e como o diretório do volume é atualizado.
- 🔶 Cada worker do Gunicorn carrega uma cópia dos 4 modelos (e a duplicata do de denúncia); o consumo de memória (limite de 4G no pipeline) depende do tamanho dos arquivos, que não é conhecido.
- ✅ Dados reais não são reproduzidos nesta nota.

## Relacionamentos
- [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] · [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Deploy-e-Ambientes|Deploy e ambientes]] · [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Stack-e-Dependencias|Stack e dependências]]

## Pendências e próximo passo
- Registrar o processo de treino/publicação dos modelos quando informado; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
