---
type: analysis-log
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
commit_data: 2026-03-26
branch: main
tags:
  - iza
  - registro-de-analise
---
# Iza Api — registro de análise

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Controlar os lotes da análise de `cgdf-iza`.

## Evidências
- `git rev-parse HEAD` = `988360c5302bb0785f21c4c1bb9f04da02816b7c`, branch `main`, commit de 2026-03-26. Árvore de trabalho limpa.
- Análise por leitura estática; testes e aplicação não foram executados. Os modelos `.joblib` não estão no repositório e não foram analisados.

## Informações confirmadas
| Lote | Escopo | Notas | Estado |
|---|---|---|---|
| 0 | Identificação, cadastro e estrutura | [[01-Sistemas/Iza/Iza-Index|Index]], [[01-Sistemas/Iza/Iza-Contexto-do-Sistema|Contexto]], [[01-Sistemas/Iza/Iza-Repositorios|Repositórios]], [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]] | concluído |
| 1 | Visão geral | [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Stack-e-Dependencias|Stack]], [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Arquitetura|Arquitetura]], [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Deploy-e-Ambientes|Deploy]], [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Observabilidade-e-Logs|Observabilidade]] | concluído |
| 2 | Núcleo funcional | [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Módulo]], [[01-Sistemas/Iza/Api/05-API/Iza-Api-Catalogo-de-Endpoints|Endpoints]], [[01-Sistemas/Iza/Api/04-Fluxos/Iza-Api-Fluxo-Triagem-de-Manifestacao|Fluxo]], [[01-Sistemas/Iza/Api/02-Dominio/Iza-Api-Modelos-e-Artefatos|Modelos e artefatos]] | concluído |
| 3 | Integração, segurança e qualidade; catálogo e mapa | [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Integrações]], [[01-Sistemas/Iza/Api/06-Seguranca/Iza-Api-Seguranca|Segurança]], [[01-Sistemas/Iza/Api/08-Qualidade/Iza-Api-Testes-e-Cobertura|Testes]], [[01-Sistemas/Iza/Api/08-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos]]; edições em `Catalogo-de-Sistemas`, `Mapa-de-Integracoes`, na nota de integrações do `PARTICIPA-DF` e nas notas do ingress | concluído |

- Decisão de catálogo (aprovada pelo usuário em 2026-10-22): o ID `Iza` passa de serviço externo a sistema, sem renomear os `provider` existentes (mesmo tratamento de `Servico-HtmlToPdf` e `PeoplesCheck`). Componente `Api`; dono não informado; marca "validar permissão antes de publicar".
- Divergências entre fontes foram **registradas, não resolvidas**: limiar de denúncia, versão `2.11.1` × changelog, nome do campo `classificao_id` × `classificacao_id`.

## Inferências e limitações
- Não foram criadas notas de persistência (não há banco) nem de regras de negócio isoladas: as regras verificáveis (unidade `-1` para 1694/1695; anonimato por limiar) estão no módulo.
- Cobertura `parcial`: comportamento real das predições depende dos modelos, fora do repositório.

## Relacionamentos
- [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]]

## Pendências e próximo passo
- **Próximo passo exato:** o usuário deve responder as pendências 1 a 4 (limiar de denúncia, campo `classificao_id` no cliente, dono, webhook exposto). Se `HEAD` mudar, comparar `git diff --name-only 988360c..HEAD` com os `sources` das notas e acionar `atualizar-documentacao`. Depois, validar o vínculo com o `PARTICIPA-DF` no código do cliente.
- Sugestão: rodar `sincronizar-brain` para revisar o estado Git do cofre (nenhuma operação Git foi executada nesta análise).
