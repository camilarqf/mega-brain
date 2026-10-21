---
type: integration
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: inferido
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
consumer: INGRESS-CGDF
tags:
  - ingress
  - nginx
  - upstreams
sources:
  - locations/prod/
  - locations/nonprod/
---
# INGRESS-CGDF — integrações com os upstreams HTTP

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `INGRESS-CGDF` | serviços Swarm listados abaixo | HTTP (proxy reverso) | prefixo de path → serviço:porta ([[01-Sistemas/INGRESS-CGDF/Nginx/05-API/INGRESS-CGDF-Nginx-Catalogo-de-Rotas|Catálogo de rotas]]) | saída do ingress; entrada de clientes |

## Evidências
- `locations/**/*.conf`: `set $upstream` e `proxy_pass` de cada rota.

## Informações confirmadas
- ✅ O ingress encaminha para os 19 serviços do catálogo de rotas.
- 🔶 **Correspondência com sistemas do cofre**, deduzida só pelo nome do serviço (as stacks não foram lidas); `status: inferido` desta nota:

| Rotas | Sistema do catálogo (provável) |
|---|---|
| `keycloak` | `KEYCLOAK-CGDF` — [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Index|índice]] |
| `identity-broker-service` | `IBS` — [[01-Sistemas/IBS/IBS-Index|índice]] (o nome coincide com o repositório `identity-broker-service`) |
| `participa-df`, `painel-ouvidoria` | `PARTICIPA-DF` — [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|índice]] (`painel-ouvidoria` 🔶 mais fraco) |
| `sci` | `SCI` — [[01-Sistemas/SCI/SCI-Index|índice]] |
| `html-to-pdf` | `Servico-HtmlToPdf` — [[01-Sistemas/Servico-HtmlToPdf/Servico-HtmlToPdf-Index|índice]] |
| `peoples-check-api` | `PeoplesCheck` — [[01-Sistemas/PeoplesCheck/PeoplesCheck-Index|índice]] |
| `portal-transparencia`, `app-transparencia`, `gerenciador-portal-transparencia` | `Portal-Transparencia` — [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Index|índice]] (🔶 só `portal-transparencia` é direto; o catálogo cita um backend "gerenciador" fora do cofre) |
| `minio` | `MinIO-CGDF` — [[01-Sistemas/MinIO-CGDF/MinIO-CGDF-Index|índice]] (✅ a rede `nginx-ingress-network` consta nas stacks do MinIO; ver [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Deploy-e-Ambientes|Deploy do MinIO-CGDF]]) |
| `api-super-busca`, `integra`, `sedoc`, `sisconep-client`, `cgdf-localization`, `cgdf-email-legacy`, `mail-service`, `cgdf-iza` | sem sistema no cofre; `cgdf-iza` pode ser o serviço externo `Iza` e `mail-service` o `MailService` (ambos 🔶 só pelo nome; ver [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|integrações externas do PARTICIPA-DF]]). Os demais, ainda não documentados, estão listados na seção abaixo, sem link por enquanto |

**Sistemas ainda não documentados no cofre** (sem link por enquanto; viram link quando forem cadastrados no catálogo): `api-super-busca`, `integra`, `sedoc`, `sisconep-client`, `cgdf-localization`, `cgdf-email-legacy`, `mail-service`, `cgdf-iza`, `painel-ouvidoria`, `gerenciador-portal-transparencia`.

## Falhas e dependências
- ✅ Sem timeouts, tentativas nem upstream de reserva: cada rota tem um único destino.
- Cada rota depende de o serviço existir na rede Swarm; ausente, a requisição falha por DNS (🔶 `502`).

## Inferências e limitações
- Os provedores acima são hipóteses até confrontar com as stacks e os repositórios dos serviços.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Proxy-TCP-RabbitMQ|Proxy TCP RabbitMQ]]

## Pendências e próximo passo
- Confirmar as correspondências; ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
