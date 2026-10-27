---
type: analysis-log
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: pendente
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
tags:
  - ingress
  - pendencias
---
# INGRESS-CGDF — pendências

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Listar o que a análise não conseguiu confirmar.

## Evidências
- Commit `a51459e`; ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Registro-de-Analise|Registro de análise]].

## Informações confirmadas
| # | Pendência | Estado |
|---|---|---|
| 1 | Dono do serviço e SLA | ❓ não informado (pergunta feita ao usuário, sem resposta) |
| 2 | Domínios/URLs por ambiente, terminação TLS e o que está à frente do Nginx | ❓ |
| 3 | Pipeline Jenkins e se valida a configuração (`nginx -t`) antes do deploy | ❓ fora do repositório |
| 4 | Correspondência das rotas com os sistemas do cofre (Keycloak, IBS, PARTICIPA-DF, SCI, etc.) | 🔶 só por nome; confrontar com as stacks dos serviços |
| 5 | Serviços sem sistema no cofre (`api-super-busca`, `integra`, `sedoc`, `sisconep-client`, `cgdf-localization`, `cgdf-email-legacy`, `mail-service`, `painel-ouvidoria`, `gerenciador-portal-transparencia`, `app-transparencia`) | ❓ não catalogados; ao cadastrar, trocar o texto por link em [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Integracoes-com-Upstreams|Integrações com upstreams]] e atualizar o `Mapa-de-Integracoes` |
| 6 | Clientes do proxy TCP RabbitMQ e se a porta 5672 é publicada | ❓ |
| 7 | Staging e Sandbox com o mesmo nome de contêiner: como as instâncias se distinguem | 🔶 label do nó |
| 8 | Exposição pública do health do Keycloak e do MinIO pelo ingress | ❓ |
| 9 | `sedoc` ausente em produção e rotas `-test` em produção: intencional? | ❓ |
| 10 | Resolução da pendência 2 do MinIO-CGDF (configuração do proxy `nginx-ingress-network`) | ✅ respondida em parte por este sistema; ver [[01-Sistemas/MinIO-CGDF/Infra/99-Controle/MinIO-CGDF-Infra-Pendencias|Pendências do MinIO-CGDF]] |

## Inferências e limitações
- As pendências 4 e 7 são hipóteses; as demais aguardam informação.

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/09-Qualidade/INGRESS-CGDF-Nginx-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Ver o próximo passo exato no [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Registro-de-Analise|Registro de análise]].
