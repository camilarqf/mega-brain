---
type: analysis-log
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
created: 2026-10-19
updated: 2026-10-23
commit_data: 2026-10-23
branch: master
tags:
  - sci
  - controle
  - cobertura
---

# Registro de análise

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendencias]]

## Base analisada
- Repositório: `sci-backend` (GitLab interno, endereço omitido). Branch `master`, commit `8e3c8648` (2026-10-18).
- Working tree: com arquivos não versionados (POC de SSO, `LEVANTAMENTO_TECNICO.md`, `docs/`, `tests/SCI.Application.Tests/`, `.idea/`). A POC de SSO foi **excluída por decisão do usuário**; `LEVANTAMENTO_TECNICO.md` serviu apenas de pista e foi confrontado com o código.
- Método: leitura estática. Testes não executados; aplicação não iniciada.

## Regras de proteção aplicadas
- Valores de `appsettings*.json`, `.jenkins-pipelines/*.env.yml` e scripts de seed **não registrados**.
- Lista de CPFs e senha de bypass encontrados no código **não reproduzidos**.
- Nenhum endereço de infraestrutura, usuário ou dado real registrado.

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Cadastro `SCI`, índices, controle, stack | ✅ concluído | 2026-10-19 | [[01-Sistemas/SCI/SCI-Index|SCI-Index]], [[01-Sistemas/SCI/SCI-Repositorios|Repositorios]], [[01-Sistemas/SCI/SCI-Contexto-do-Sistema|Contexto]], [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Backend-Index]], [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Stack-e-Dependencias|Stack]], Registro, Pendências |
| 1 | Arquitetura e domínio | ✅ concluído | 2026-10-19 | [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Arquitetura-CQRS-e-Event-Sourcing|Arquitetura]], [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Modelo-de-Dominio|Modelo-de-Dominio]], [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums-e-Estados]], [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Glossario|Glossario]] |
| 2 | Persistência | ✅ concluído (parcial: seeds e mappings não detalhados) | 2026-10-19 | [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco-e-Migrations]] |
| 3 | API e segurança | ✅ concluído (payloads não detalhados) | 2026-10-19 | [[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]], [[01-Sistemas/SCI/Backend/06-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] |
| 4 | Módulos e fluxos | ✅ concluído (parcial) | 2026-10-19 | [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denuncia-e-Demanda]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Processo-de-Admissibilidade]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Encaminhamento|Encaminhamento]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Documentos-e-Assinaturas|Documentos-e-Assinaturas]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Unidade-e-Configuracao|Unidade-e-Configuracao]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Identidade-e-Permissoes|Identidade-e-Permissoes]], [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Cadastros-de-Apoio|Cadastros-de-Apoio]], [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo-Denuncia]], [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|Fluxo-PIP]], [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]] |
| 5 | Integrações | ✅ concluído | 2026-10-19 | [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integracoes-Externas]], [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Autenticacao|Participa-DF-Autenticacao]], [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Participa-DF-Eventos]], [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-BCadastro|BCadastro]], [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-HtmlToPdf|HtmlToPdf]]; `Mapa-de-Integracoes` e `Catalogo-de-Sistemas` atualizados |
| 6 | Qualidade e débitos | ✅ concluído | 2026-10-19 | [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Debitos-Tecnicos]] |
| 7 | Atualização incremental `8e3c8648..29989114` (skill `atualizar-documentacao`): denúncia → demanda, anexos S3, `AnaliseDenuncia`, perfis, endpoints, testes | ✅ concluído (leitura estática, parcial) | 2026-10-23 | [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-S3-Anexos-de-Denuncia|Integracao-S3-Anexos-de-Denuncia]] (nova); atualizadas: Denuncia-e-Demanda, Fluxo-Denuncia, Participa-DF-Eventos, Integracoes-Externas, Modelo-de-Dominio, Enums-e-Estados, Banco-e-Migrations, Catalogo-de-Endpoints, Seguranca-e-Autorizacao, Stack, Arquitetura, Glossario, PIP, Encaminhamento, Processo-de-Admissibilidade, Testes-e-Cobertura, Debitos-Tecnicos, Index, Pendencias; `Mapa-de-Integracoes` |

## Resultado final
- **32 notas** do SCI (3 na raiz do sistema e as demais no backend) mais atualização de `Catalogo-de-Sistemas` e `Mapa-de-Integracoes`.
- Cobertura parcial declarada em quase todas as notas: não foram lidos os corpos de todos os handlers, as consultas SQL das visões, os seeds e os valores de configuração.
- A POC de SSO e os arquivos não versionados correspondentes foram **excluídos** por decisão do usuário.
- Itens ❓/🔶 abertos: ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendencias]].
- **Atualização de 2026-10-23**: HEAD `29989114` (branch `master`; 45 commits, 102 arquivos desde `8e3c8648`, quase todos da release `integracao-sci-participa`). Mudanças: aceite de denúncia cria demanda `CR`; `AnaliseDenuncia`/`AnexoDenuncia` substituem o status da denúncia; cliente S3 (`SCI.S3.Client`); evento `demanda-criada-por-denuncia`; aceitar/recusar passou ao ApoioCorrecional; endpoints novos de denúncia e `encaminhamento/recebido`; ajustes de PIP/JAD; 4 testes novos. A POC de SSO segue não versionada e **fora do escopo**. Notas não afetadas (sem alteração em `sources`): Fluxo-Autenticacao, BCadastro, HtmlToPdf, Participa-DF-Autenticacao, Documentos-e-Assinaturas, Identidade-e-Permissoes, Cadastros-de-Apoio, Unidade-e-Configuracao, Ciclo-do-PIP e todo o Frontend (cujo `analyzed_commit` próprio não foi tocado).
- Para atualizar após novos commits: `git diff 299891144fc8c08a314738782442772a8a98b913..HEAD --stat` e reabrir as notas cujos `sources` mudaram (skill `atualizar-documentacao`).

## Conflitos entre fontes
- `LEVANTAMENTO_TECNICO.md` (.NET 8, EF Core 8.0.8) × código (.NET 10, EF Core 10.0.5): prevalece o código.
- Cofre: o `Mapa-de-Integracoes` tinha o parceiro de eventos do `PARTICIPA-DF` como "não identificado"; agora aponta o SCI como contraparte provável.

## Cobertura por área do código
| Área | Lido integralmente | Lido parcialmente / amostragem | Não lido |
|---|---|---|---|
| `Program.cs`, csproj, `Directory.Packages.props` | ✅ | | |
| `SCI.Api/Controllers` | rotas, verbos e atributos de autorização de todos | corpo dos métodos | payloads e códigos |
| `SCI.Api/Identity/AuthorizationPolicies` | ✅ (todas as políticas) | | |
| `SCI.Domain` | enums, `Denuncia`, `Demanda`, `ProcessoAdmissibilidade`, `PIP`, regras selecionadas | demais entidades (propriedades) | maioria das regras de `Rules/` |
| `SCI.Application` | handlers de denúncia, demanda, autenticação, usuário, permissão e unidade (parcial); 9 `EventHandlers` | demais casos de uso (nomes) | corpo da maioria |
| `SCI.Infrastructure.Data` | `UnitOfWork`, `DatabaseOperation`, DI | mappings (nomes de tabela) | cardinalidades, seeds |
| `SCI.Infrastructure.Projections` | estrutura | | consultas SQL |
| Clientes HTTP, GED, consumidor | ✅ | | |
| `appsettings*.json` | só nomes de chaves e se estão preenchidas | | valores |
| `tests/` | contagem e estrutura | | corpo dos testes; resultado de execução |
| `Legacy/` | | | tudo |

## Próximo passo exato
0. (2026-10-23) Responder as perguntas 11 a 15 de [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendencias]].
1. Responder as perguntas de [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendencias]] (frontend, siglas, origem da demanda).
2. Lote 8 (opcional; antes planejado como lote 7): ler `Queries/*` do read model, seeds de configuração de fluxo (`23`, `24`, sem dados pessoais), `EnvolvidoBuilder`, regras restantes de `GestaoPIP/Rules` e `Legacy/`.
3. Rodar `sincronizar-brain` somente com autorização da categoria de conteúdo (b).
