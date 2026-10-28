---
type: quality
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-23
tags:
  - participa-df
  - backend
  - testes
  - qualidade
sources:
  - tests/OuvDF.UnitTests
  - tests/OuvDF.IntegrationTests
  - tests/OuvDF.Iza.Client.Tests
  - tests/OuvDF.MailService.Client.Tests
  - tests/OuvDF.PeoplesCheck.Client.Tests
  - tests/OuvDF.TestHelpers
  - src/Dockerfile
---

# Testes e cobertura

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Debitos-Tecnicos]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Stack-e-Dependencias|Stack-e-Dependencias]]

## Objetivo
Descrever a estratégia de testes do repositório, o que ela cobre e o que não cobre. **Os testes não foram executados** (exigem banco, RabbitMQ e serviços externos) e não há relatório de cobertura no repositório.

## Evidências
Estrutura e conteúdo de `tests/**` (contagem por busca de `[Fact]`/`[Theory]`), `tests/OuvDF.IntegrationTests/Configuration`, nomes das chaves dos `appsettings.json` de teste (sem valores), `src/Dockerfile`. Commit `4901ad5`.

## Informações confirmadas

### Projetos de teste
| Projeto | Arquivos `.cs` | `[Fact]` | `[Theory]` | Natureza |
|---|---|---|---|---|
| `OuvDF.UnitTests` | 5 | 5 | 1 | unitários com Moq e `*Stub` (vencimento de manifestação, prorrogação) |
| `OuvDF.IntegrationTests` | 151 | 155 | 2 | integração ponta a ponta de comandos e consultas com o contêiner de DI real |
| `OuvDF.Iza.Client.Tests` | 6 | 10 | 0 | integração com o serviço Iza (+ 1 teste unitário de extensão) |
| `OuvDF.MailService.Client.Tests` | 2 | 3 | 0 | integração com o MailService |
| `OuvDF.PeoplesCheck.Client.Tests` | 4 | 5 | 0 | integração com o PeoplesCheck |
| `OuvDF.TestHelpers` | 2 | — | — | apoio (`DependencyResolverHelper`, `ServiceProviderHelper`) |
- ✅ Total aproximado: **178 `[Fact]` e 3 `[Theory]`**, dos quais 155 em `IntegrationTests`.
- ✅ Frameworks: xUnit, Moq, Shouldly, AutoFixture, coverlet (coleta de cobertura), `StructureMap` e `CGDF.DotNet.SDK.Services.Generators` nos testes de integração; `net5.0`.

### Testes de integração do domínio
- ✅ Organizados por módulo: `ServicoOuvidoriaTests` (31 de comandos e 39 de consultas, em arquivos `*Test.cs`), `ServicoInformacaoCidadaoTests` (26 de comandos e 29 de consultas), `SharedTests` (21 de comandos e 2 de consultas).
- ✅ Montam o provedor de serviços real (`ServiceInjector`/`Startup` de teste), com `TokenServiceMock` como única simulação de serviço e usam as dependências reais: **banco SQL Server** (`ConnectionStrings.DefaultConnection`), Redis (`RedisConnectionString`), RabbitMQ, serviço de PDF, SEI, Iza, PeoplesCheck e MailService, conforme as chaves do `appsettings.json` de teste.
- ✅ O `appsettings.json` de teste tem valores preenchidos para a conexão do banco, a chave de assinatura JWT e a senha do RabbitMQ (**versionados**; valores não reproduzidos aqui).

### Cobertura por nome (heurística)
Comparei as pastas de `Domain/Commands` com os nomes dos arquivos de teste (um comando conta como coberto se algum arquivo de teste contém o nome da pasta). É uma **estimativa**, não cobertura de linhas.
| Módulo | Comandos | Com teste (por nome) | Sem teste identificado |
|---|---|---|---|
| Ouvidoria | 36 | 27 | `AplicarBloqueioExterno`, `RemoverBloqueioExterno`, `AtualizarManifestacaoParaVencida` e `…AposProrrogacao` (só têm teste unitário), `EfetuarDownloadManifestante`, `MoverManifestacoesParaContaLGPD`, `RegistrarReclassificacaoSeccional`, `TramitarManifestacaoSeccional`, `ValidarAtributoComplementar` |
| SIC | 34 | 24 | `ProrrogarPrazoPedido`, `ProrrogarPrazoPedidosVencidos`, `ProrrogarPrazoRecursoNaoRespondido`, `ConcluirPedidosRespondidosComPrazoDeRecursoExpirado`, `SolicitarVinculoSei`, `VincularPedidoSei`, `ExcluirArquivoPorOperador`, `ExportarPedidoEmHtml`, `MoverPedidosParaContaLGPD`, `ResponderPesquisa` |
| Shared | 36 | 15 | `CadastrarPessoaFisica/Juridica`, `Atualizar*`, `ConcluirRecuperacaoSenha`, `CancelarToken`, `GravarCidadao`, `GravarUnidadeSO`, `AtivarUnidadeSIC`, `DesativarUnidadeSIC`, `AlterarUnidadeAtual`, `DesbloquearUsuarioDadosInconsistentes`, `GravarLogAuditoria`, `NotificarAutenticacao`, `DesabilitarOperador*`, `AceitarPoliticaDeSeguranca` e outros |
- ✅ Sem testes por nome: **todos os jobs** de prazo do SIC (prorrogação, conclusão, omissão de resposta), o vínculo SEI, o cadastro de pessoa física e jurídica e a recuperação de senha.
- ✅ Não há testes dos controllers, dos filtros (`LogAudit`, `ValidateTokenFilter`), de autenticação (`AutenticarUsuario`), nem de `CalculadoraPrazoService`/`CalcularPrazoHandler` (cálculo de prazo).

### Execução e integração contínua
- ✅ O `Dockerfile` restaura e publica (`dotnet restore`, `dotnet publish`); **não executa `dotnet test`**. O `.jenkins-pipelines/` contém só parâmetros de implantação.
- ✅ Há `coverlet.collector` nos projetos de teste, mas nenhum relatório ou limite de cobertura no repositório.

- ✅ (2026-10-23, `820666c`) O diff `4901ad5..820666c` **não toca `tests/`** e uma busca por `S3Client`, `ExportarDadosDenuncia`, `DenunciaCriada`, `DenunciaAceita`, `DenunciaRecusada` e `ManifestacaoTramitadaEventHandler` em `tests` não retorna nada: o código novo (cliente S3, exportação da denúncia, consumidores e a regra da COACI) está **sem teste**. Contagens de `[Fact]`/`[Theory]` acima não foram refeitas.

## Inferências e limitações
- 🔶 Sem banco isolado: os testes de integração gravam no banco apontado por `DefaultConnection` (não há *rollback* ou uso de `TransactionScope` nos testes que busquei); a limpeza dos dados é ❓.
- 🔶 Os testes dos clientes (Iza, MailService, PeoplesCheck) chamam os **serviços reais** (nome da pasta `IntegrationTests`), então falham sem a rede ou as chaves.
- 🔶 `OuvDF.UnitTests` cobre apenas os jobs de vencimento e a prorrogação de manifestação.
- ❓ Última execução, resultado, tempo e percentual de cobertura real.
- ❓ Quem executa os testes e quando (pipeline fora do repositório).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-do-SIC|Regras-de-Prazo-do-SIC]]

## Pendências e próximo passo
- Executar a suíte em um ambiente isolado para obter resultado e cobertura (sob autorização).
- Priorizar testes para cálculo de prazo, jobs do SIC, autenticação e cadastro (ver débitos).
