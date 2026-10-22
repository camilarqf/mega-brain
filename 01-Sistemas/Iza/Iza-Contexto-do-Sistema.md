---
type: system
system: Iza
repository: cgdf-iza
status: confirmado
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - contexto
sources:
  - src/main.py
  - src/internal/description.py
  - CHANGELOG.md
  - .jenkins-pipelines/deployment.params.yml
---
# Iza — contexto do sistema

Voltar: [[01-Sistemas/Iza/Iza-Index|Índice do sistema]]

## Objetivo
Servir, por HTTP, modelos de aprendizado de máquina treinados para apoiar a triagem de manifestações: dado o texto do relato (`relato`), sugerir o assunto, a classificação/tipologia, a unidade de trâmite inicial e se há indício de denúncia.

## Evidências
- `src/internal/description.py`: "API Robô Iza 🤖 endpoints para o projeto OUV-IA".
- `src/main.py`: 8 endpoints `POST` de predição/probabilidade e 6 `GET` de metadados; ver [[01-Sistemas/Iza/Api/05-API/Iza-Api-Catalogo-de-Endpoints|Catálogo de endpoints]].
- `CHANGELOG.md`: histórico de versões desde 2.4.0 (2023), com demandas SIGEDEM citadas nas atualizações de modelo.
- `.jenkins-pipelines/deployment.params.yml`: nome da aplicação `Iza Api`, serviço `iza-api`.

## Informações confirmadas
- ✅ Serviço **sem estado e sem banco**: cada chamada executa um modelo carregado em memória na inicialização. Ver [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] e [[01-Sistemas/Iza/Api/02-Dominio/Iza-Api-Modelos-e-Artefatos|Modelos e artefatos]].
- ✅ Quatro modelos serializados (`.joblib`) lidos de um diretório configurado por variável de ambiente; os arquivos **não** estão no repositório.
- ✅ Não há autenticação, autorização, banco, fila nem chamadas de saída no código. Ver [[01-Sistemas/Iza/Api/06-Seguranca/Iza-Api-Seguranca|Segurança]].
- ✅ Implantação por Jenkins em Docker/Swarm; ver [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Deploy-e-Ambientes|Deploy e ambientes]].

## Inferências e limitações
- 🔶 Consumidor: o backend do `PARTICIPA-DF` chama operações com os mesmos nomes (`predict-*`) e o ingress roteia `cgdf-iza` para `iza-api:8000`; o vínculo entre este repositório e o serviço `Iza` do `PARTICIPA-DF` foi **confirmado pelo usuário em 2026-10-22** (aprovação do plano de documentação), mas o código deste repositório não mostra os chamadores.
- ❓ Dono do serviço, SLA e URLs por ambiente não identificados.
- ❓ Origem, dados de treino e métricas dos modelos não estão no repositório.

## Relacionamentos
- [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Integrações (lado provedor)]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
