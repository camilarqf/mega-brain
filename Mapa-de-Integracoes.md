---
type: index
status: pendente
updated: 2026-10-18
tags:
  - integracoes
  - moc
---

# Mapa de integrações

Voltar: [[Catalogo-de-Sistemas|Catálogo de sistemas]] · Regras: `BRAIN-RULES.md`, seção 7.

Índice de todas as integrações entre sistemas e serviços externos. Cada linha aponta para a **nota canônica** da integração; o detalhe não é repetido aqui. IDs conforme o catálogo.

## Integrações com evidência
| Consumidor | Provedor | Tecnologia | Direção | Confirmação | Nota canônica |
|---|---|---|---|---|---|
| `SICI` (`sici-backend`) | `Servico-de-PDF` | HTTP POST JSON | saída | ✅ cliente no código; ❓ provedor não identificado | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `SICI` (`sici-backend`) | `Keycloak` | OIDC / JWKS (validação de JWT) | entrada (tokens) | ✅ | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `SICI` (`sici-backend`) | `Keycloak` | HTTP (token endpoint e userinfo) | saída | ✅ | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `Iza` | HTTP POST JSON (4 operações `predict-*`) | saída | ✅ (natureza do provedor ❓) | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `MailService` | HTTP POST JSON e multipart | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `PeoplesCheck` | HTTP GET/POST, chave de API | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `SEI` | web service (SDK `CGDF.SEI.DotNet.SDK`) | saída | ✅ uso; 🔶 protocolo | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `Servico-HtmlToPdf` | HTTP POST JSON | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `RabbitMQ` | mensageria: publica `denuncia-registrada`; consome `denuncia-aceita` e `denuncia-recusada` | saída e entrada | ✅ (contraparte do evento ❓) | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `Servico-Geocodificacao` | HTTP GET (proxy) | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `Grafana-Loki` | sink do Serilog | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-backend`) | `NewRelic` | agente .NET | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PARTICIPA-DF` (`participa-df-frontend`) | `PARTICIPA-DF` (`participa-df-backend`) | HTTP JSON (REST), `Bearer` JWT; 66 caminhos | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas\|Integrações do Frontend Cidadão]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API\|Chamadas de API]] |
| `PARTICIPA-DF` (`participa-df-frontend`) | `Servico-Localizacao-CGDF` | HTTP POST JSON direto do navegador | saída | ✅ chamada; ❓ dono | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas\|Integrações do Frontend Cidadão]] |
| `PARTICIPA-DF` (`participa-df-frontend`) | `Google-Analytics` | `gtag.js` | saída | ✅ | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas\|Integrações do Frontend Cidadão]] |
| `PARTICIPA-DF` (`participa-df-frontend`) | `Perto-Digital` | plugin JS por CDN | entrada (script) | ✅ | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas\|Integrações do Frontend Cidadão]] |

## Relações não confirmadas (hipóteses)
- 🔶 O frontend `participa-df-frontend` redireciona o navegador, após `security/notify`, para os front-ends `SistemaOuvDF` e `SistemaSicDF` (login assistido por `sessionId`). Os repositórios desses destinos (dois dos 3 front-ends do Participa) não foram identificados nem analisados.
- 🔶 `Servico-Localizacao-CGDF` (chamado pelo frontend) pode ser o mesmo serviço que o backend consome por proxy como `Servico-Geocodificacao`; os caminhos chamados são diferentes. Manter IDs separados até haver evidência.
- 🔶 `Servico-HtmlToPdf` (PARTICIPA-DF) e `Servico-de-PDF` (SICI) usam o mesmo contrato (`POST` com `{"HtmlString": ...}`); podem ser o mesmo serviço. Não confirmado: manter os IDs separados até haver evidência de dono e endereço.
- 🔶 Os eventos `denuncia-registrada`, `denuncia-aceita` e `denuncia-recusada` indicam um sistema correcional/de denúncias (a mensagem cita a COACI) como contraparte do PARTICIPA-DF. Esse sistema não foi identificado e não está no catálogo.
- 🔶 O PARTICIPA-DF expõe `v1/*` (papel `OperadorWS`) e `metro/*` a consumidores externos ainda não identificados.
- 🔶 O backend do SICI grava no QR Code um link de validação (`assinatura.url.validacao`) que aponta para um frontend de validação. Não está confirmado se é o `sici-frontend`, que ainda não foi analisado.

## Como manter
- Toda integração nova ou alterada atualiza uma linha deste mapa e a nota canônica correspondente.
- Relação sem evidência entra apenas na seção de hipóteses.
