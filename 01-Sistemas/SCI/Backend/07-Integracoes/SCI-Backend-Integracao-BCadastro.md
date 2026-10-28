---
type: integration
aliases:
  - "Integração SCI → BCadastro"
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
consumer: SCI
provider: BCadastro
tags:
  - dados-pessoais
sources:
  - src/SCI.BCadastro.Client/Services/BCadastroClient.cs
  - src/SCI.BCadastro.Client/BCadastroClientSettings.cs
  - src/SCI.BCadastro.Client/Extensions/ServicesCollectionExtensions.cs
  - src/SCI.Application/Builders/EnvolvidoBuilder.cs
---
# Integração SCI → BCadastro

Voltar: [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas do SCI Backend]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `SCI` (`sci-backend`) | `BCadastro` | HTTP `POST` JSON, Basic Auth | consulta por seletor `{"selector": {"_id": {"$eq": <documento>}}}`, resposta `{docs: [...]}` | saída |

## Evidências
- `BCadastroClient.GetPessoaFisicaByCPF` e `GetPessoaJuridicaByCNPJ`; chaves de `BCadastroClientSettings`: `Uri`, `Username`, `Password`, `Timeout`, `HealthCheckEndpoint`, `CnpjEndpoint`, `CpfEndpoint`, `RetryCount`, `RetryIntervalInSeconds`, `HandledEventsAllowedBeforeBreaking`, `DurationOfBreakInSeconds`, `FallbackMessage` (valores não lidos).

## Informações confirmadas
- ✅ **Por CPF**: uma consulta; sem resultado devolve objeto com `Erro = "CPF inválido ou nenhum registro encontrado."`.
- ✅ **Por CNPJ**: consulta o CNPJ completo (sem resultado → `Erro = "CNPJ inválido ou nenhum registro encontrado."`); depois consulta a **raiz do CNPJ** (8 primeiros dígitos) para obter razão social e CPF do responsável; se houver CPF do responsável, consulta a pessoa física e preenche `RepresentanteLegal`.
- ✅ A autenticação é Basic (usuário e senha vindos da configuração; `Authorization` definido em `DefaultRequestHeaders` a cada chamada).
- ✅ Resiliência: retry, circuit breaker e timeout de 5 s (Polly).
- ✅ Uso: `EnvolvidoBuilder` busca pessoas ao registrar envolvidos identificados.
- ✅ Estilo do contrato (seletor `_id` com `$eq`) lembra consultas do tipo Mango/CouchDB, mas isso é 🔶 (tecnologia do provedor não identificada).

## Falhas e dependências
- ✅ Status HTTP de erro lança exceção (`EnsureSuccessStatusCode`); resposta sem corpo lança `ApplicationException`.
- Dependência: disponibilidade do BCadastro para cadastrar envolvidos pessoa física/jurídica.

## Inferências e limitações
- ❓ Dono, SLA e ambiente do BCadastro não identificados.
- ⚠️ `DefaultRequestHeaders.Authorization` é reatribuído em cada chamada num `HttpClient` tipado (detalhe de implementação; sem impacto verificado).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Cadastros-de-Apoio|Cadastros de apoio]]

## Pendências e próximo passo
- Identificar o dono do BCadastro e confirmar a tecnologia.
