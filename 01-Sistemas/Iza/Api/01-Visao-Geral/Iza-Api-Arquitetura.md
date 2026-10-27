---
type: architecture
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: completa
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - arquitetura
sources:
  - src/main.py
  - src/classificador.py
  - src/Queries
  - src/internal
  - src/log_config.py
  - src/helpers.py
  - src/resposta.py
---
# Iza Api — arquitetura

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Descrever como o código está organizado e como os modelos chegam aos endpoints.

## Evidências
- `src/main.py` (rotas, `lifespan`, `load_models`), `src/Queries/*.py`, `src/classificador.py`, `src/internal/*.py`.

## Informações confirmadas
| Elemento | Papel |
|---|---|
| `src/main.py` | Aplicação `FastAPI` (versão declarada `2.11.1`), rotas, instrumentação Prometheus e carregamento dos modelos no `lifespan` |
| `src/classificador.py` | Módulo usado como **contêiner de estado**: `main.py` o importa como `clf` e atribui os modelos carregados a atributos de módulo (`clf.model_assunto_id`, `clf.model_relato_assunto_classificacao`, `clf.model_denuncia`, `clf.model_unidade`, `clf.model_denuncia_assunto`) |
| `src/Queries/` | Uma classe por consulta (`query_*`), cada uma com método `execute`; recebe o modelo por parâmetro, monta a entrada e devolve o resultado |
| `src/internal/manifestacao.py` | Modelo Pydantic `Manifestacao` (corpo das requisições) |
| `src/internal/description.py` | Descrição e `tags` exibidas no Swagger |
| `src/log_config.py` | `dictConfig` do log de acesso do Uvicorn |
| `src/resposta.py`, `src/helpers.py` | Classes `Denuncia`/`Anonimo` e função `any`; ver inferências |

**Camadas:** rota (`main.py`) → classe `query_*` → modelo `scikit-learn` em memória. Não há camada de serviço, repositório nem persistência.

**Ciclo de vida:** na inicialização (`lifespan`) o código lê `os.environ["models_path"]` e executa `joblib.load` de quatro arquivos; só então a aplicação atende. Os mesmos modelos são compartilhados por todas as requisições do processo (2 workers = 2 cópias). Ver [[01-Sistemas/Iza/Api/02-Dominio/Iza-Api-Modelos-e-Artefatos|Modelos e artefatos]].

## Inferências e limitações
- ✅ Todas as rotas são `async def`, mas as inferências (`predict`, `predict_proba`) são síncronas e CPU-bound; executam no laço de eventos. 🔶 Em carga, uma predição longa bloqueia o worker (não medido).
- ✅ `src/classificador.py` também define a classe `Classificador` com respostas fixas e a instância `clf`; como `main.py` importa o **módulo** (`from src import classificador as clf`), a classe e a instância não são usadas. 🔶 Código morto.
- ✅ `src/resposta.py` (`Denuncia`, `Anonimo`) não é importado por nenhum módulo. `src/helpers.py` define `any`, que as consultas não importam (usam o `any` embutido). 🔶 Código morto.
- ✅ `main.py` usa `from … import *` para todas as consultas.

## Relacionamentos
- [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] · [[01-Sistemas/Iza/Api/06-API/Iza-Api-Catalogo-de-Endpoints|Catálogo de endpoints]] · [[01-Sistemas/Iza/Api/09-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Confirmar se o código morto pode ser removido (débito); ver [[01-Sistemas/Iza/Api/09-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos técnicos]].
