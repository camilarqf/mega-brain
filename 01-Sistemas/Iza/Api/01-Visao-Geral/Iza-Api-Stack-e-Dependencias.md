---
type: reference
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: completa
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - stack
  - dependencias
sources:
  - requirements.txt
  - pyproject.toml
  - Dockerfile
  - pyrightconfig.json
---
# Iza Api — stack e dependências

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Registrar linguagem, framework e bibliotecas efetivamente declaradas.

## Evidências
- `requirements.txt` (36 dependências fixadas com `==`), `Dockerfile` (`FROM python:3.12`), `pyproject.toml`.

## Informações confirmadas
| Camada | Item | Versão declarada |
|---|---|---|
| Linguagem / imagem | Python (`python:3.12`, sem fixar o patch) | 3.12 |
| Web | FastAPI · Starlette · Uvicorn · Gunicorn | 0.128.0 · 0.50.0 · 0.40.0 · 23.0.0 |
| Validação | Pydantic | 2.12.5 |
| Modelos | scikit-learn · LightGBM · imbalanced-learn (e o pacote `imblearn`) | 1.5.1 · 4.6.0 · 0.14.1 (`imblearn` 0.0) |
| Dados | pandas · NumPy · SciPy · joblib | 3.0.0 · 2.4.1 · 1.17.0 · 1.5.3 |
| Métricas | prometheus-fastapi-instrumentator · prometheus_client | 7.1.0 · 0.24.1 |
| Testes | pytest · httpx (usado pelo `TestClient`) | 9.0.2 · 0.28.1 |

- ✅ Um único `requirements.txt` serve produção e testes: `pytest` e `httpx` entram na imagem.
- ✅ `pyproject.toml` contém apenas uma tabela `[pytest]` com `pythonpath`; `pyrightconfig.json` aponta `venvPath` para `.venv/`.
- ✅ O histórico recente tem o commit "DOWNGRADE: scikit-learn 1.5.1" (2026-03-26) e o `CHANGELOG.md` menciona a atualização dos modelos para scikit-learn 1.5 (2.10.0).

## Inferências e limitações
- 🔶 Modelos serializados com `joblib` dependem de versões compatíveis de scikit-learn/NumPy/pandas entre treino e execução; o downgrade para 1.5.1 sugere que a versão precisa coincidir com a do treino. Não verificável sem os arquivos de modelo.
- 🔶 O cabeçalho `[pytest]` em `pyproject.toml` não é a tabela reconhecida pelo pytest nesse arquivo (`[tool.pytest.ini_options]`); o `pythonpath` provavelmente não tem efeito (não executado).
- ❓ `NEW_RELIC_APP_NAME` é definido nos arquivos de ambiente, mas nenhuma dependência de agente New Relic consta aqui; ver [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Observabilidade-e-Logs|Observabilidade]].

## Relacionamentos
- [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Arquitetura|Arquitetura]] · [[01-Sistemas/Iza/Api/09-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Confirmar a versão de scikit-learn usada no treino dos modelos em produção (ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]]).
