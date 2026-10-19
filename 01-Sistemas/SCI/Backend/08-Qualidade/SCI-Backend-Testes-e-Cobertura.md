---
type: quality
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - testes
  - qualidade
sources:
  - tests/SCI.Integration.Tests
  - tests/SCI.Tests.Helpers
  - tests/SCI.Application.Tests
  - SCI.sln
---
# SCI Backend — testes e cobertura

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Registrar o que existe de testes automatizados e o que não existe.

## Evidências
- Listagem de `tests/*`, contagem de `[Fact]`/`[Theory]`, `SCI.sln`, `*.csproj` de testes. **Testes não foram executados.**

## Informações confirmadas
- ✅ Projetos de teste com `.csproj`: `SCI.Integration.Tests` (xUnit, Shouldly, `Microsoft.AspNetCore.Mvc.Testing`, coverlet; referencia `SCI.Api`, CQRS, Data, Projections e `SCI.Tests.Helpers`) e `SCI.Tests.Helpers`. Ambos estão na solução.
- ✅ Total: **7** métodos `[Fact]`/`[Theory]` no repositório.
  - Integração (`tests/SCI.Integration.Tests`): `FluxoCriarUnidadeTests`, `FluxoAtualizarUnidadeTests`, `FluxoDesabilitarUnidadeTests`, `FluxoAtualizarRevisoesTests` (comandos de unidade) e `ProcessoAdmissibilidadeQueryTests`, `RevisorPipQueryTests` (consultas).
  - Unitário: `tests/SCI.Application.Tests/UseCases/DesvincularDiligenciaMatrizHandlerTests.cs` (1 teste).
- ⚠️ `SCI.Application.Tests` **não tem `.csproj`** e está fora do controle de versão (pasta não rastreada): não é executável como está.
- ✅ As pastas `SCI.Api.Tests`, `SCI.BCadastro.Client.Tests`, `SCI.Domain.Tests`, `SCI.GED.Tests`, `SCI.Infrastructure.Integration.Tests`, `SCI.Infrastructure.Projections.Tests` e `SCI.ParticipaDF.Client.Tests` não têm `.cs` nem `.csproj` (apenas artefatos de build).
- ✅ A API expõe `public partial class Program` para os testes de integração (`WebApplicationFactory`).

## Inferências e limitações
- 🔶 Cobertura estimada **muito baixa** para a lógica de domínio (regras de admissibilidade, PIP, assinatura e encaminhamento sem teste).
- ❓ Não verifiquei se os testes de integração precisam de banco/RabbitMQ (`appsettings.Tests.json` não lido) nem se passam.
- Há ainda testes no `Legacy/` (`APITests`), não analisados.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Unidade-e-Configuracao|Unidade e configuração]]

## Pendências e próximo passo
- Executar a suíte localmente e registrar o resultado; decidir o destino de `SCI.Application.Tests`.
