---
type: integration
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
consumer: SCI
provider: Servico-HtmlToPdf
tags:
  - sci
  - integracao
  - pdf
sources:
  - src/SCI.HtmlToPdf.Client/Services/HtmlToPdfApiClient.cs
  - src/SCI.HtmlToPdf.Client/Settings/HtmlToPdfClientSettings.cs
  - src/SCI.GED/UseCases
---
# Integração SCI → serviço HtmlToPdf

Voltar: [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas do SCI Backend]]


Provedor: [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Servico-HtmlToPdf]] (✅ confirmado pelo usuário).

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `SCI` (`sci-backend`) | `Servico-HtmlToPdf` | HTTP `POST` JSON | corpo `{"HtmlString": "<html>"}`, resposta binária (PDF) | saída |

## Evidências
- `HtmlToPdfApiClient.ConvertToPdfAsync`: `POST {Uri}/{ConvertToPdfEndpoint}`, `EnsureSuccessStatusCode`, devolve `byte[]`. Chaves de configuração: `Uri`, `Timeout`, `UserAgent`, `ConvertToPdfEndpoint`, `HealthCheckEndpoint` e as de resiliência (valores não lidos).
- Uso: `SCI.GED` (nota técnica, minuta e relatório do PIP).

## Informações confirmadas
- ✅ O contrato é o mesmo já documentado para o `PARTICIPA-DF` e o `SICI`; ver [[Mapa-de-Integracoes|Mapa de integrações]].
- ✅ O projeto está duplicado no repositório: `SCI.HtmlToPdf.Client` (na solução, usado em `Program.cs`) e `SCI.HtmlToPdfClient` (idêntico, fora da solução).
- ✅ Falha HTTP lança exceção; não há fallback de conteúdo no cliente além do configurado.

## Falhas e dependências
- Sem o serviço, não é possível gerar nota técnica, minuta e relatório em PDF.

## Inferências e limitações
- ✅ Informado pelo usuário em 2026-10-19: é o **mesmo serviço** usado pelo `PARTICIPA-DF` (ID `Servico-HtmlToPdf`). O usuário confirmou, também em 2026-10-19, que o serviço do `SICI` é o mesmo; o ID passou a ser único (`Servico-HtmlToPdf`). Dono: ❓.
- Resiliência (retry/circuit breaker) herda `ResilienceSettings`; aplicação no `HttpClient` deste cliente não foi lida.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Documentos-e-Assinaturas|Documentos e assinaturas]]

## Pendências e próximo passo
- Identificar o dono do serviço.
