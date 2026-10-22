---
type: quality
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: completa
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - testes
  - qualidade
sources:
  - src/test_main.py
  - pyproject.toml
  - requirements.txt
---
# Iza Api — testes e cobertura

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Descrever a estratégia de testes existente e suas lacunas. Os testes **não foram executados** (leitura estática).

## Evidências
- `src/test_main.py` (227 linhas, 26 funções `test_*`), `pyproject.toml`, `requirements.txt` (`pytest`, `httpx`).

## Informações confirmadas
- ✅ Todos os testes usam `fastapi.testclient.TestClient(app)` dentro de um `with` no nível do módulo, o que dispara o `lifespan` e carrega os **modelos reais**: sem `models_path` e sem os `.joblib`, o módulo falha na importação. São testes de integração, não unitários.
- ✅ Cobertura por endpoint: sucesso (200) e falha de validação (422 com `{}`) para assunto, classificação, é-denúncia, unidade, anonimato e as 3 rotas `prob_*`; sucesso para `/assuntos` e os 4 `hash_modelo_*`; `/`, `/invalid` (404) e `/docs` (200).
- ✅ `test_excecao_unidade` verifica a regra `assunto_id` 1694 → `{'response': -1}`.
- ✅ Entradas de teste genéricas ("bla bla bla", `assunto_id` 1); as asserções verificam quase só o status HTTP.
- ✅ Não há medição de cobertura, fixtures, mocks, testes de carga nem etapa de teste nos Jenkinsfiles.

## Inferências e limitações
- ✅ Lacunas: assunto 1695 (regra de exceção), limiar do anonimato (0,05), formato e ordenação das respostas, `n_assuntos`, campos opcionais ausentes, falha de modelo ausente.
- ✅ `test_predict_is_denuncia_by_relato_and_assunto_falha` chama `/predict-classificacao-by-relato-assunto` (rota errada): o caso de falha de `is-denuncia` não é de fato testado.
- ✅ `test_predict_assunto_by_relato_sucesso_unequal` compara os objetos `Response` (`response1 != response2`), que são sempre distintos; o teste não prova que os resultados diferem.
- 🔶 O `pythonpath` do `pyproject.toml` provavelmente não é lido (cabeçalho `[pytest]`); os imports `src.*` funcionam pelo pacote `src/__init__.py` e pelo diretório de execução.
- ❓ Se os testes rodam em algum pipeline e com quais modelos.

## Relacionamentos
- [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] · [[01-Sistemas/Iza/Api/08-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Executar os testes em ambiente com os modelos e medir cobertura; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
