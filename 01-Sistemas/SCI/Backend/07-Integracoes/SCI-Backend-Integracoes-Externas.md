---
type: index
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - integracoes
  - moc
sources:
  - src/SCI.Api/Program.cs
---
# SCI Backend — integrações externas (índice)

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Objetivo
Índice das integrações do `sci-backend`. Cada integração tem uma única nota canônica.

## Evidências
- Registro dos clientes e consumidores em `src/SCI.Api/Program.cs`.

## Informações confirmadas
| Consumidor → Provedor | Tecnologia | Nota canônica |
|---|---|---|
| `SCI` → `PARTICIPA-DF` | HTTP POST JSON (autenticação) | [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Autenticacao|Autenticação]] |
| `SCI` ⇄ `RabbitMQ` (eventos de denúncia com o `PARTICIPA-DF`) | mensageria | [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Eventos]] |
| `SCI` → `BCadastro` | HTTP POST JSON, Basic | [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-BCadastro|BCadastro]] |
| `SCI` → `Servico-HtmlToPdf` | HTTP POST JSON | [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-HtmlToPdf|HtmlToPdf]] |

Outras dependências (não são integrações com outros sistemas de negócio): SQL Server, armazenamento em disco compartilhado, destino de logs Grafana Loki (pacote `Serilog.Sinks.Grafana.Loki`; configuração de `LoggerSettings` não lida) e métricas Prometheus (endpoint de scraping).

## Inferências e limitações
- ❓ **SEI**: o SCI guarda apenas o número do processo (`NumeroProcessoSei`); **não há cliente** do SEI no código.
- ❓ **MPTCE**: aparece só como status da demanda.
- A POC de SSO (Keycloak) não commitada está fora do escopo.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações do PARTICIPA-DF Backend]]

## Pendências e próximo passo
- Ler `LoggerSettings` (somente nomes de chaves) para confirmar o destino de logs.
