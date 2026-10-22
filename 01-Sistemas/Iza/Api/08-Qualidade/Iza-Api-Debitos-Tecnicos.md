---
type: technical-debt
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - debitos-tecnicos
sources:
  - src/main.py
  - src/classificador.py
  - src/helpers.py
  - src/resposta.py
  - src/Queries
  - src/test_main.py
  - deploy/Jenkinsfile
  - deploy/Jenkinsfile.hom
  - requirements.txt
  - pyproject.toml
  - CHANGELOG.md
  - README.md
---
# Iza Api — débitos técnicos

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Listar débitos e riscos, separados dos fatos documentados nas demais notas. Os itens são **recomendações**; nenhum código foi alterado.

## Evidências
- Cada item cita o arquivo; os fatos correspondentes estão em [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]], [[01-Sistemas/Iza/Api/06-Seguranca/Iza-Api-Seguranca|Segurança]] e [[01-Sistemas/Iza/Api/08-Qualidade/Iza-Api-Testes-e-Cobertura|Testes]].

## Informações confirmadas
| # | Débito | Evidência | Prioridade sugerida |
|---|---|---|---|
| 1 | 🔴 Webhook do Discord com token escrito em `deploy/Jenkinsfile` (e no histórico). Revogar e usar credencial do Jenkins | `deploy/Jenkinsfile` | alta |
| 2 | API sem autenticação, inclusive `/docs` e `/prometheus`; contato individual exposto no Swagger | `src/main.py` | alta (decidir com o dono) |
| 3 | Regra do limiar de denúncia ambígua (0,05 / 0,15 / sem limiar) entre código, Swagger e changelog | `src/main.py`, `CHANGELOG.md`, `src/internal/description.py` | alta |
| 4 | Entrada sem validação: `assunto_id`/`classificacao_id` opcionais nas rotas que os exigem; `relato` sem limite de tamanho | `src/internal/manifestacao.py` | média |
| 5 | Inferência síncrona dentro de `async def` bloqueia o laço de eventos; 2 workers × 4 modelos em memória | `src/main.py` | média |
| 6 | Modelo de denúncia carregado duas vezes (`model_denuncia` e `model_denuncia_assunto`) | `src/main.py` `load_models` | média |
| 7 | `GET /hash_modelo_*` recalcula MD5 do arquivo inteiro a cada chamada; `query_hash_modelo` exige `models_path` na importação | `src/Queries/query_hash_modelo.py` | média |
| 8 | Health check fixo (`true`), sem verificar modelos | `src/main.py` | média |
| 9 | Código morto: classe/instância `Classificador`, `resposta.py`, `helpers.any`, `query_permite_anonimato_by_relato`, `n_assuntos` em `Manifestacao`; `import *` nas consultas | `src/classificador.py`, `src/resposta.py`, `src/helpers.py`, `src/Queries` | baixa |
| 10 | Versão `2.11.1` no código sem entrada no `CHANGELOG.md` (termina em 2.10.2); `README.md` vazio | `src/main.py`, `CHANGELOG.md`, `README.md` | baixa |
| 11 | Testes dependem dos modelos reais; asserções fracas; teste de falha de `is-denuncia` aponta a rota errada; comparação de `Response` sem valor; sem teste do assunto 1695 | `src/test_main.py` | média |
| 12 | `requirements.txt` único mistura produção e testes; `pyproject.toml` com `[pytest]` possivelmente ignorado; `python:3.12` sem fixar o patch; imagem sem `USER` | `requirements.txt`, `pyproject.toml`, `Dockerfile` | baixa |
| 13 | Jenkinsfiles legados duplicados (prod e hom) com `allowAnyHosts`, registry HTTP e erro de digitação `--memory=4g--restart` | `deploy/Jenkinsfile.hom` | baixa (se o pipeline Swarm for o oficial, remover os legados) |
| 14 | Códigos fixos no código (assuntos 1694/1695, `classificacao == 2`, limiar 0,05) sem documentação de negócio | `src/Queries`, `src/main.py` | média |
| 15 | `NEW_RELIC_APP_NAME` definido sem agente New Relic nas dependências | `.jenkins-pipelines/*.env.yml`, `requirements.txt` | baixa |

## Inferências e limitações
- 🔶 A prioridade é uma sugestão da análise, não uma decisão do time.
- ❓ O item 5 (impacto em carga) não foi medido.

## Relacionamentos
- [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Arquitetura|Arquitetura]] · [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Deploy-e-Ambientes|Deploy e ambientes]]

## Pendências e próximo passo
- Os itens 1 e 3 dependem de confirmação com o dono do serviço; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
