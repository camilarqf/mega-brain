---
type: integration
aliases:
  - "Iza Api — integrações (lado provedor)"
system: Iza
component: Api
repository: cgdf-iza
status: inferido
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
provider: Iza
sources:
  - src/main.py
  - .jenkins-pipelines/deployment.params.yml
---
# Iza Api — integrações (lado provedor)

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Visão geral
O serviço é **somente provedor**: não há clientes HTTP, filas nem banco no código. As notas canônicas ficam no lado do consumidor; esta nota só aponta para elas (BRAIN-RULES, seção 7).

| Consumidor | Provedor | Tecnologia | Direção (do ponto de vista do consumidor) | Nota canônica |
|---|---|---|---|---|
| `PARTICIPA-DF` (`participa-df-backend`) | `Iza` | HTTP POST JSON (4 operações `predict-*`) | saída | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |

## Evidências
- Contrato do provedor: 4 endpoints `predict-*` com `relato`, `assunto_id` e `classificacao_id` (`src/main.py`, `src/internal/manifestacao.py`).
- Lado do consumidor (vault): `OuvDF.Iza.Client` chama `predict-assunto-by-relato`, `predict-classificacao-by-relato-assunto`, `predict-is-denuncia-by-relato-assunto` e `predict-unidade-by-relato-assunto-classificacao`; os nomes coincidem com os deste repositório.
- Roteamento: o ingress da CGDF encaminha o serviço `cgdf-iza` para `iza-api:8000`, igual ao nome do contêiner e à porta interna do pipeline; ver [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Integracoes-com-Upstreams|Integrações com upstreams do ingress]].

## Informações confirmadas
- ✅ Os nomes das 4 operações chamadas pelo `PARTICIPA-DF` existem neste repositório com método `POST`.
- ✅ Este repositório não faz chamadas a outros sistemas.
- ✅ O vínculo "o serviço `Iza` do `PARTICIPA-DF` é este repositório" foi aceito pelo usuário em 2026-10-22 (aprovação do plano de documentação).

## Inferências e limitações
- 🔶 O código não mostra os chamadores nem a URL implantada; o vínculo se apoia em correspondência de nomes/contrato, no roteamento do ingress e na confirmação do usuário.
- 🔶 Campo `classificao_id` (grafia no vault) × `classificacao_id` (aceito pela API): possível divergência no cliente; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
- ❓ Consumidores além do `PARTICIPA-DF`, e uso dos endpoints `prob_*`, `predict-permite-anonimato-novo` e `hash_modelo_*`.
- ❓ O `PARTICIPA-DF` envia o relato do cidadão a este serviço; se o serviço é institucional (dono não identificado) é relevante para a LGPD.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Iza/Api/06-API/Iza-Api-Catalogo-de-Endpoints|Catálogo de endpoints]] · [[01-Sistemas/Iza/Api/05-Fluxos/Iza-Api-Fluxo-Triagem-de-Manifestacao|Fluxo de triagem]]

## Pendências e próximo passo
- Registrar o dono e as URLs por ambiente quando informados.
