---
type: analysis-log
system: Iza
component: Api
repository: cgdf-iza
status: pendente
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - pendencias
---
# Iza Api — pendências

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Listar lacunas e confirmações pendentes.

## Evidências
- Origem: lotes 0 a 3 em [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Registro-de-Analise|Registro de análise]].

## Informações confirmadas
- Vínculo `cgdf-iza` = serviço `Iza`: aceito pelo usuário em 2026-10-22 ao aprovar o plano (o código não mostra os chamadores).
- ID `Iza`, componente `Api`, dono não informado: definidos na aprovação de 2026-10-22.

## Inferências e limitações
| # | Pendência | Tipo | Nota afetada |
|---|---|---|---|
| 1 | Qual é o limiar vigente de denúncia (0,05 / 0,15 / sem limiar) | ❓ | [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] |
| 2 | O cliente do `PARTICIPA-DF` envia `classificao_id` ou `classificacao_id`? (a API ignora o primeiro) | 🔶 | [[01-Sistemas/Iza/Api/05-API/Iza-Api-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Integrações]] |
| 3 | Dono do serviço, SLA e URLs por ambiente | ❓ | [[01-Sistemas/Iza/Iza-Contexto-do-Sistema|Contexto]] |
| 4 | Webhook do Discord escrito no `Jenkinsfile`: ainda válido? foi rotacionado? | 🔴 ❓ | [[01-Sistemas/Iza/Api/06-Seguranca/Iza-Api-Seguranca|Segurança]] |
| 5 | Mecanismo de deploy ativo (Swarm × Jenkinsfile legado) e processo de publicação dos modelos | ❓ | [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Deploy-e-Ambientes|Deploy]] · [[01-Sistemas/Iza/Api/02-Dominio/Iza-Api-Modelos-e-Artefatos|Modelos]] |
| 6 | Versão de scikit-learn usada no treino dos modelos em produção | 🔶 | [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Stack-e-Dependencias|Stack]] |
| 7 | Há agente New Relic ativo? (variável definida sem dependência) | ❓ | [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Observabilidade-e-Logs|Observabilidade]] |
| 8 | Consumidores além do `PARTICIPA-DF` e uso dos endpoints `prob_*`, anonimato e `hash_modelo_*` | ❓ | [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Integrações]] |
| 9 | Significado de negócio de `classificacao_id` 2 e dos assuntos 1694/1695 | ❓ | [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]] |
| 10 | Executar os testes com os modelos e medir cobertura | ❓ | [[01-Sistemas/Iza/Api/08-Qualidade/Iza-Api-Testes-e-Cobertura|Testes]] |
| 11 | Base legal/consentimento para enviar o relato a este serviço (LGPD) | ❓ | [[01-Sistemas/Iza/Api/06-Seguranca/Iza-Api-Seguranca|Segurança]] |

## Relacionamentos
- [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Pendências e próximo passo
- Próximo passo: itens 1 a 4 (dependem do dono/time); depois 5 a 11.
