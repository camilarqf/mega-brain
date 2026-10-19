---
type: technical-debt
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
  - debitos
  - riscos
  - seguranca
sources:
  - src/SCI.Application/UseCases/AutenticarUsuario/AutenticarUsuarioHandler.cs
  - src/SCI.Api/Controllers/SupportController.cs
  - src/SCI.Api/Controllers/UnidadeController.cs
  - src/SCI.Api/Controllers/ArquivoController.cs
  - src/SCI.Api/appsettings.json
  - src/SCI.Api/Program.cs
  - src/SCI.Api/Extensions/CorsPolicyExtensions.cs
---
# SCI Backend — débitos técnicos e riscos

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Separar **fatos verificados no código** de **riscos e recomendações**. Valores sensíveis não são reproduzidos.

## Evidências
- Arquivos listados em `sources`. Para segredos, verifiquei apenas se a chave está preenchida (sem ler o valor).

## Informações confirmadas (fatos)
| # | Fato | Onde |
|---|---|---|
| 1 | O login tem uma **lista fixa de 12 CPFs** que, com uma **senha fixa** escrita no código, dispensa a validação no `PARTICIPA-DF` | `AutenticarUsuarioHandler` |
| 2 | `POST /support/generate-database` é `[AllowAnonymous]`; apaga **todas as tabelas do schema `dbo`** e recria; só é barrado pela feature flag `Support.GenerateDatabase` (`false` em `appsettings.json`; o usuário informou em 2026-10-19 que só funciona em dev e local, mecanismo não verificado no código). A política `RedefinirBancoDeDados` existe e não é usada | `SupportController`, `DatabaseOperation` |
| 3 | `DELETE /unidade/{id}` não tem política: qualquer usuário autenticado pode desabilitar uma unidade | `UnidadeController` |
| 4 | Arquivos versionados `appsettings.json`, `.Development`, `.Homolog` e `.Production` têm `JwtSettings:Secret` preenchido; `appsettings.json` e `.Production` têm `BCadastroClientSettings:Password` preenchida; `appsettings.Development.json` tem a string de conexão do RabbitMQ preenchida | `src/SCI.Api/appsettings*.json` |
| 5 | CORS aceita qualquer origem, método e cabeçalho | `CorsPolicyExtensions` |
| 6 | Swagger é habilitado sem condição de ambiente (UI na raiz) | `Program.cs` |
| 7 | `GET /arquivo/download/{nomeArquivo}` valida só "não vazio" e concatena ao diretório de armazenamento; `IsValidGuid` existe e não é usado | `ArquivoController`, `DownloadRequestValidator` |
| 8 | `POST /pip/assinar-minuta`, `/assinar-relatorio`, `/atualizar-dados-sei` e as rotas de diligência exigem só autenticação; o perfil é checado no domínio nas assinaturas; para diligências e dados do SEI a checagem nos handlers não foi verificada | `PipController`, `DiligenciaController` |
| 9 | Eventos de domínio são tratados depois do `SaveChanges`, fora da mesma transação | `UnitOfWork` |
| 10 | Políticas definidas e sem uso: `jad.ListarProcessosPorRelator`, `unidade.CriarUnidadePolicy`, `RedefinirBancoDeDados`; flag `Pip.Criar` sem uso; `SecurityId` registrado e sem uso em DTOs; `SecurityIdKey` vazio em `appsettings.json` | `AuthorizationPolicies`, `FeatureManagement`, `DataSecurity` |
| 11 | `RequestResponseLoggingMiddleware` e `ValidationExceptionMiddleware` existem e não vêm registrados | `src/SCI.Api/Middlewares` |
| 12 | Projeto de cliente HTML→PDF duplicado e fora da solução (`SCI.HtmlToPdfClient`); `Legacy/` com outra solução | `src/`, `Legacy/` |
| 13 | Sem migrations EF; o esquema é gerado e populado por scripts | [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco]] |
| 14 | Só 7 métodos de teste; 7 pastas de teste sem projeto; `SCI.Application.Tests` sem `.csproj` | [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Testes-e-Cobertura|Testes]] |
| 15 | `LEVANTAMENTO_TECNICO.md` (não versionado) diverge do código (.NET 8 × .NET 10) | [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Stack-e-Dependencias|Stack]] |
| 16 | `GET /processo-admissibilidade/por-relator` está `[Obsolete]` | `ProcessoAdmissibilidadeController` |

## Inferências e riscos (🔶)
- 🔴 **Alto**: fatos 1 e 4. Quem conhecer a lista/senha fixa autentica-se como esses CPFs; segredos versionados permitem forjar tokens JWT (a chave é simétrica) e usar as credenciais do BCadastro.
- 🟡 **Baixo/médio**: fato 2. Segundo o usuário só funciona em dev e local, o que reduz o risco; permanece anônimo e destrutivo onde a flag estiver ligada.
- 🟠 **Médio**: fatos 3, 7 e 8 (autorização insuficiente; impacto da rota de download não testado).
- 🟡 **Baixo/médio**: fatos 5, 6, 9, 10 e 11.
- 🟡 Organização/qualidade: fatos 12 a 16.

## Recomendações (não implementadas)
1. Remover o bypass de autenticação; se for necessário para testes, restringi-lo a ambiente de desenvolvimento por configuração.
2. Retirar segredos de `appsettings*.json` (variáveis de ambiente/cofre de segredos) e **rotacionar** a chave JWT e a senha do BCadastro.
3. Manter `generate-database` restrito a dev/local e, se possível, proteger com a política `Administrador`.
4. Aplicar política em `DELETE /unidade/{id}` e revisar rotas apenas autenticadas do PIP.
5. Validar `nomeArquivo` (GUID/nome simples) e restringir CORS e Swagger por ambiente.
6. Adicionar testes de domínio (regras de assinatura, encaminhamento e transições) e criar o `.csproj` de `SCI.Application.Tests`.
7. Decidir sobre a duplicata `SCI.HtmlToPdfClient`, o `Legacy/` e os itens sem uso do fato 10.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/06-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização]] · [[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Verificar valores de flags e segredos por ambiente **fora do cofre** e planejar a rotação.
