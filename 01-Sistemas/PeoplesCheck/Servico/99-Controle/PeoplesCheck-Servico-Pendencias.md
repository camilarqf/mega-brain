---
type: analysis-log
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: pendente
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - pendencias
---
# PeoplesCheck Serviço — pendências

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Listar lacunas e confirmações pendentes.

## Evidências
- Origem: lotes 0 a 6 em [[01-Sistemas/PeoplesCheck/Servico/99-Controle/PeoplesCheck-Servico-Registro-de-Analise|Registro de análise]].

## Informações confirmadas
- Correspondência com o serviço consumido pelo `PARTICIPA-DF`: confirmada pelo usuário em 2026-10-19.
- Dono: CGDF (informado pelo usuário em 2026-10-19).

## Inferências e limitações
| # | Pendência | Tipo | Nota afetada |
|---|---|---|---|
| 1 | ~~Quem agenda o job `DELETE /jobs/limpar-base-desafio`~~ — resolvido (Jenkins, informado pelo usuário em 2026-10-19); frequência/horário e valor de `jobName` seguem ❓ (baixa prioridade) | ✅ | [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio]] · [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Limite-de-Tentativas|Limite de tentativas]] |
| 2 | URLs, DNS e exposição de rede por ambiente; SLA | ❓ | [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Deploy-e-Ambientes|Deploy]] |
| 3 | Perfil Spring efetivo no JAR (`@activatedProperties@` e `-P SPRING_PROFILES_ACTIVE`) e uso do agente New Relic | 🔶 | [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Deploy-e-Ambientes|Deploy]] |
| 4 | Dono, origem e atualização das réplicas CouchDB; dono, índices/TTL e topologia do MongoDB | ❓ | [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-CouchDB|CouchDB]] · [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-MongoDB|MongoDB]] |
| 5 | Origem das regras resolvida (Ouvidoria, dona do negócio do PARTICIPA-DF, informado em 2026-10-19). Pendente: documento do requisito e o motivo de aceitar CNPJ suspenso/inapto | ❓ | [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Elegibilidade-Cadastral|Elegibilidade]] |
| 6 | Explorabilidade da injeção no seletor CouchDB (A1) e rotação das credenciais versionadas (A3) | 🔶 | [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos]] |
| 7 | Uso do desafio de CNPJ avulso e do `POST /challenge` por algum consumidor | 🔶 | [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio]] |
| 8 | Executar os testes e medir cobertura | ❓ | [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Testes-e-Cobertura|Testes]] |
| 9 | Comparar os DTOs do cliente do `PARTICIPA-DF` com os contratos deste serviço, campo a campo | ❓ | [[01-Sistemas/PeoplesCheck/Servico/06-API/PeoplesCheck-Servico-Catalogo-de-Endpoints|Endpoints]] |

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Pendências e próximo passo
- Próximo passo: itens 1, 2 e 5 (respondíveis pelo dono) e 8 (execução dos testes).
