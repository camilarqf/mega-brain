---
type: analysis-log
system: SICI
repository: sici-backend
status: confirmado
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
created: 2026-10-16
updated: 2026-10-18
commit_data: 2026-10-05
branch: master
tags:
  - sici
  - controle
  - cobertura
---

# Registro de análise

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]]

## Base analisada
- Repositório: `sici-backend` (GitLab interno — endereço omitido)
- Branch: `master`
- Commit: `1871e32` (2026-10-05); histórico de 468 commits desde 2024-06-13
- Working tree: limpo, exceto um log de crash da JVM não versionado (`hs_err_pid*.log`)
- Método: leitura estática do código. **Testes não executados**, aplicação não iniciada.

## Regras de proteção aplicadas
- Valores de `application*.properties`, `.jenkins-pipelines/*.env.yml` e `.idea/dataSources` **não lidos**: só nomes de chaves e valores técnicos não sensíveis.
- Conteúdo dos seeders (`V2__seeders.sql`, `V55__seeders_unidade_auditada.sql`) **não lido**.
- Nenhum endereço de infraestrutura, usuário ou nome de pessoa registrado.

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Descoberta geral (estrutura, pom, endpoints, segurança, enums, use cases principais por amostragem) | ✅ concluído | 2026-10-16 | — (resultado no chat) |
| 1 | Base: stack, arquitetura, ambientes, glossário, controle | ✅ concluído | 2026-10-16 | [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Stack-e-Dependencias|Stack-e-Dependencias]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Arquitetura-Hexagonal|Arquitetura-Hexagonal]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Glossario|Glossario]], [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]] |
| 2 | Domínio: models, enums, entidades JPA, migrations | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Modelo-de-Dominio|Modelo-de-Dominio]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Enums-e-Estados|Enums-e-Estados]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Banco-e-Migrations|Banco-e-Migrations]] (+ correção em [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Glossario|Glossario]]) |
| 3 | Ordem de Serviço completa | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Backend/03-Modulos/Prorrogacao-e-Cancelamento|Prorrogacao-e-Cancelamento]], [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Ciclo-de-Vida-OS|Fluxo-Ciclo-de-Vida-OS]] |
| 4 | Assinatura, numeração, PDF, templates | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]], [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]], [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integracoes-Externas]] (parcial: Keycloak no lote 6) |
| 5 | Ação de Controle, POAC, OS Genérica, SUBCI, auditores, cadastros | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]], [[01-Sistemas/SICI/Backend/03-Modulos/POAC|POAC]], [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]] (parcial), [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]], [[01-Sistemas/SICI/Backend/03-Modulos/Auditores-Coordenadores-Perfis|Auditores-Coordenadores-Perfis]], [[01-Sistemas/SICI/Backend/03-Modulos/Cadastros-Auxiliares|Cadastros-Auxiliares]] |
| 6 | Segurança, API, testes, débitos técnicos | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Backend/04-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]], [[01-Sistemas/SICI/Backend/06-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]], [[01-Sistemas/SICI/Backend/05-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]], [[01-Sistemas/SICI/Backend/08-Qualidade/SICI-Backend-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/SICI/Backend/08-Qualidade/SICI-Backend-Debitos-Tecnicos|Debitos-Tecnicos]] (+ Keycloak em [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integracoes-Externas]]) |

## Resultado final
- **27 notas** em 10 pastas; todas as notas previstas no plano foram criadas.
- Cobertura parcial declarada em: [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Banco-e-Migrations|Banco-e-Migrations]] (seeders não lidos, de propósito) e [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]] (ramos internos de criação/atualização).
- Itens ❓/🔶 abertos: ver [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]].
- Para atualizar esta base depois de novos commits: `git diff 1871e32..HEAD --stat` e reabrir as notas dos módulos afetados (os campos `fontes` do frontmatter indicam quais arquivos cada nota cobre).

## Cobertura por área do código
| Área | Lido integralmente | Lido parcialmente / amostragem | Não lido |
|---|---|---|---|
| `pom.xml`, `Dockerfile` | ✅ | | |
| `application*.properties` | | só chaves + valores não sensíveis | valores sensíveis |
| `api/*` | `SecurityConfig`, `api/security/*`, `AuthController`, `OpenSwagger`, `HealthCheckController` | mapeamentos de todos os controllers | corpo dos demais |
| `infrastructure/external` | `KeycloakAuthAdapter`, `KeycloakHealthIndicator`, `VerifyCodeProperties` | | `KeycloakAuthProperties`, contratos |
| `application/exception/GlobalExceptionHandler` | mapeamento exceção → HTTP | | corpo das respostas |
| `src/test` + `target/surefire-reports` | contagem, tipos, resultado da última execução (.txt) | causas das falhas (primeiras linhas) | corpo dos testes; XMLs (contêm propriedades do ambiente) |
| `domain/enums` | ✅ todos (7) | | |
| `domain/model` (+ `valueObjects`) | campos e métodos de todas as 32 classes; corpo de `OrdemServico`, `AcaoControle` (validações), `Assinatura`, `ProrrogacaoOrdemServico` | corpo das demais | |
| `application/usecase/ordemServico` (+ `coordenador/SubstituirCoordenador`) | `SalvarOrdemServico`, `AtualizarOrdemServico`, `AlterarStatusOrdemServico`, `ExcluirOrdemServico`, `CancelarOrdemServico`, `CriarProrrogacaoOrdemServico`, `SubstituirCoordenador` | `AtualizarProrrogacaoOrdemServico`, `AtualizarDatasAuditorOrdemServico`, `ObterSubciVigenteParaDocumento`, `fase/SalvarFaseOrdemServico` | `GerarOrdemServico`, `Listar…`, `Pesquisar…` |
| `api/ordemServico/OrdemServicoController` | endpoints e `validarDataProrrogacao` | `gerarRelatorioPdf` | |
| `application/service/ordemServico/OrdemServicoServiceImpl` | `alterarStatusOs`, `salvarOsi`, `cancelarOrdemServico`, `atualizarJustificativaCancelamento` | lista de métodos | `toResponseEnriquecido` e auxiliares |
| `application/usecase/assinatura` | `AssinarDocumento`, `AssinarOrdemServico` | `AssinarOrdemServicoGenerica` (diferenças) | |
| `application/service/assinatura` | `AssinaturaServiceImpl`, `AssinaturaDocumentoServiceImpl`, `NumeracaoServiceImpl` | | |
| `api/assinatura/AssinaturaController` | ✅ | | |
| `application/usecase` (acaoControle, poac, subci, auditor) | `CriarAcaoControle`, `AtualizarAcaoControle`, `InativarAcaoControle`, `CriarPoac`, `CriarSubci`, `AtualizarPerfisAuditorUseCase` | `ListarSubci`, `PesquisarSubci`, `ListarAuditor`, `ListarAuditoresComPerfilUseCase`, `ListarCoordenador` | `ListarAcaoControle`, `PesquisarAcaoControle` |
| `application/usecase/ordemServicoGenerica` | | `Criar`, `Atualizar`, `AlterarStatus`, `Excluir` (regras e guardas) | `Listar`, `Pesquisar`, `GerarPdf` |
| `application/usecase` (cadastros auxiliares) | | todas as listagens (chamada à porta) | queries dos adapters |
| `application/service` (AcaoControle, subci) | `SubciSubstitutoServiceImpl` | `AcaoControleServiceImpl` | demais services do lote |
| `api/*` restantes | anotações `@*Mapping`/`@PreAuthorize` de todos os controllers | | corpo dos métodos simples |
| `application/utils` + `service/comum` | `HashUtils`, `VerifyCode`, `ImagemUtils`, `QRCodeGenerator`, `PdfService`, `AssinaturaProperties`, `VerifyCodeProperties` | | `RomanUtils` |
| `templates/*.html` | | variáveis e uso de `th:text`/`th:utext` (contagem) | texto institucional (de propósito) |
| `infrastructure/persistence/entity` | tabelas, relacionamentos e enums de todas as 32 entidades | colunas simples | |
| `infrastructure/persistence` (adapter/repository) | `NumeracaoRepositoryAdapter`, `NumeracaoRepository` | `AcaoControleRepositoryAdapter` (dependências) | demais |
| `infrastructure/mapper` | | | todos |
| `db/migrations` | DDL de V1 e V3–V57 (exceto seeders) | | V2 e V55 (seeders, de propósito) |
| `templates` | | nomes dos 8 arquivos | conteúdo |
| `src/test` | | lista de classes e contagem de `@Test` | conteúdo |

## Reorganização da base — 2026-10-18
- **Motivo**: adequação a `BRAIN-RULES.md`: sistema em `01-Sistemas/<Sistema>/`, uma subpasta por repositório.
- **Movido**: `02-Projetos/SICI/` → `01-Sistemas/SICI/Backend/`, com subpastas e nomes preservados. Única renomeação: `00-SICI-Index.md` → `00-Backend-Index.md`.
- **Links**: os 274 links internos foram convertidos para caminho completo (`[[01-Sistemas/SICI/Backend/...|Título]]`) para evitar colisão com notas futuras do frontend.
- **Frontmatter**: acrescentadas as chaves `type`, `system`, `repository`, `status`, `analyzed_commit`, `updated`; as chaves originais (`tipo`, `commit`, `atualizado`, `fontes`…) foram mantidas. `status`: `confirmado` para notas de cobertura completa, `pendente` para cobertura parcial e para [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]].
- **Removidos**: 7 arquivos vazios (0 bytes) na raiz do cofre, com nomes iguais a notas do SICI (provavelmente criados ao clicar em links ainda não resolvidos).
- **Criado na raiz do sistema**: [[01-Sistemas/SICI/SICI-Index|SICI-Index]], [[01-Sistemas/SICI/SICI-Contexto-do-Sistema|Contexto-do-Sistema]], [[01-Sistemas/SICI/SICI-Repositorios|Repositorios]].
- **Conteúdo técnico**: inalterado. O commit analisado continua `1871e32`, e o HEAD do `sici-backend` em 2026-10-18 é o mesmo commit.
- **Próximo passo exato**: (a) responder as perguntas de [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]] com o time; (b) quando autorizado, analisar `sici-frontend` com a skill `documentar-sistema`, criando `01-Sistemas/SICI/Frontend/`.

## Revisão de taxonomia — 2026-10-18
- **Tipos**: `BRAIN-RULES.md` passou a ser a fonte única dos valores de `type` (17 tipos), com os novos `domain`, `persistence` e `quality`; paleta aplicada nos grupos nativos do grafo (`.obsidian/graph.json`).
- **Reclassificadas (somente o `type`)**: `SICI-Index` → `index`; `Modelo-de-Dominio` e `Enums-e-Estados` → `domain`; `Banco-e-Migrations` → `persistence`; `Testes-e-Cobertura` → `quality`; `Catalogo-de-Endpoints` → `api`; `Debitos-Tecnicos` → `technical-debt`.
- **Conteúdo técnico**: inalterado; nenhuma nota criada, movida ou removida.

## Padronização de nomes de arquivo — 2026-10-18
- **Renomeadas (18, via `git mv`, mesmas pastas)**: `00-Backend-Index` → `SICI-Backend-Index` · `Contexto-do-Sistema` → `SICI-Contexto-do-Sistema` · `Repositorios` → `SICI-Repositorios` · `Pendencias` → `SICI-Backend-Pendencias` · `Registro-de-Analise` → `SICI-Backend-Registro-de-Analise` · `Glossario` → `SICI-Backend-Glossario` · `Arquitetura-Hexagonal` → `SICI-Backend-Arquitetura-Hexagonal` · `Perfis-e-Ambientes` → `SICI-Backend-Perfis-e-Ambientes` · `Stack-e-Dependencias` → `SICI-Backend-Stack-e-Dependencias` · `Modelo-de-Dominio` → `SICI-Backend-Modelo-de-Dominio` · `Enums-e-Estados` → `SICI-Backend-Enums-e-Estados` · `Banco-e-Migrations` → `SICI-Backend-Banco-e-Migrations` · `Fluxo-Autenticacao` → `SICI-Backend-Fluxo-Autenticacao` · `Catalogo-de-Endpoints` → `SICI-Backend-Catalogo-de-Endpoints` · `Seguranca-e-Autorizacao` → `SICI-Backend-Seguranca-e-Autorizacao` · `Integracoes-Externas` → `SICI-Backend-Integracoes-Externas` · `Debitos-Tecnicos` → `SICI-Backend-Debitos-Tecnicos` · `Testes-e-Cobertura` → `SICI-Backend-Testes-e-Cobertura`.
- **Histórico**: os links `[[…]]` foram redirecionados para os novos nomes; o texto das seções anteriores (que cita os nomes antigos) foi mantido como registro da época. Módulos e fluxos de negócio mantêm nomes curtos.
- **Convenção**: ver "Nomenclatura de arquivos" em `BRAIN-RULES.md`.
