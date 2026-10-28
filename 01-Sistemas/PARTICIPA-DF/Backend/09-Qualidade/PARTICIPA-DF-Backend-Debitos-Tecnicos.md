---
type: technical-debt
aliases:
  - "Débitos técnicos e riscos"
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-23
sources:
  - src/Dockerfile
  - src/OuvDF.Api
  - src/OuvDF.Shared
  - src/OuvDF.ServicoOuvidoria
  - src/OuvDF.ServicoInformacaoCidadao
  - src/OuvDF.IntegrationServices
  - src/OuvDF.S3.Client
  - .jenkins-pipelines/deployment.params.yml
  - tests
---

# Débitos técnicos e riscos

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendencias]]

## Objetivo
Consolidar, em um só lugar, os débitos e riscos registrados nas notas dos lotes 1 a 8. Cada item separa o **fato** (com a nota de origem) da **recomendação**. Nenhum valor sensível é reproduzido.

## Evidências
Notas linkadas em cada linha e, para os números, buscas no código no commit `4901ad5`. Itens com 🔶 dependem de confirmação (SDK interno não lido, execução não feita). A severidade é uma estimativa do analista, não uma decisão do time.

Legenda de severidade: 🔴 alta · 🟠 média · 🟡 baixa.

## Informações confirmadas

### A. Segurança e privacidade
| # | Fato (✅ ou 🔶) | Origem | Sev. | Recomendação |
|---|---|---|---|---|
| A1 | ✅ `appsettings*.json` versionados (4 em `src/OuvDF.Api` e 4 em `tests`) têm valores preenchidos em chaves sensíveis: chave de assinatura JWT, `SecuritySecret`, senha do RabbitMQ, chaves de API do MailService e PeoplesCheck, e a conexão do banco no teste. O `Dockerfile` define a licença do New Relic em texto. Só verifiquei o preenchimento e o tamanho, sem expor valores. | [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] | 🔴 | Tratar como comprometidos: rotacionar, mover para *secrets* (o entrypoint já lê `/run/secrets`), remover do histórico e usar valores fictícios nos testes. |
| A1.1 | ✅ **Atualização 2026-10-23 (`820666c`, parcialmente resolvido A1)**: `Jwt.Secret`, `SecuritySecret`, a chave de API do MailService e PeoplesCheck, `WsIdentificacaoServico` do SEI, o bloco `RabbitMQSettings` de Prod e a licença do New Relic (`Dockerfile` e `launchSettings`) foram **removidos** dos arquivos versionados e passaram a vir de Swarm Secrets (`deployment.params.yml`, 3 regiões). 🔶 Continuam abertos: os valores seguem no **histórico do git** e a rotação não é verificável; os `appsettings` de `tests` não mudaram; `appsettings.Development/Homolog` ainda podem ter outras chaves sensíveis (não reverificado). | [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] | 🟠 (era 🔴) | Rotacionar os valores que estiveram versionados e limpar o histórico. |
| A2 | ✅ 25 endpoints sem `[Authorize]` nem `[AllowAnonymous]` (inclui gravar/ativar/desativar unidade, `notificacao/*` do SIC, `jobs/*`, `arquivo/download` do SIC, `configuration/*`); 56 anônimos, vários que gravam. 🔶 O SDK pode impor autenticação global (não lido). | [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] | 🔴 | Verificar o SDK; adotar *fallback policy* de autorização e listar explicitamente os públicos. |
| A3 | ✅ `POST operador-so/operador-ws` é anônimo e cria operador de serviço; 🔶 o handler tende a sempre rejeitar (comparação com consulta nunca nula). | [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] | 🔴 | Exigir papel; corrigir a verificação de login existente. |
| A4 | ✅ `servicos/siturb?url=` e `servicos/ra?url=` anônimos fazem GET na URL informada pelo chamador (`WebClient`); `localidade/posicao?url=` concatena ao host fixo. 🔶 SSRF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]] | 🔴 | Permitir lista de hosts, validar o destino e exigir autenticação ou *rate limit*. |
| A5 | ✅ `ValidateTokenFilter` (token cancelado) sem uso no repositório; logout só grava o token. 🔶 pode não invalidar a sessão. | [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] | 🔴 | Ligar a checagem (ou confirmar o SDK) e testar o logout. |
| A6 | ✅ TLS do PeoplesCheck desligado (`ServerCertificateCustomValidationCallback` retorna `true`); no Iza e MailService o código equivalente não é aplicado (handler não atribuído). | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]] | 🔴 | Instalar a cadeia de certificados e remover o *bypass*; apagar os métodos que não fazem nada. |
| A7 | ✅ Relato do cidadão: registrado em log de aviso (`ValidarIdentificacao`) e enviado ao Iza em 4 chamadas por registro; `ExceptionHandlingFilter` (que mascara relato) não está ligado. | [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Fluxo-Registro-de-Manifestacao]] | 🔴 | Remover o relato dos logs; avaliar base legal/consentimento e minimização no envio ao Iza (LGPD). |
| A8 | ✅ Recuperação de senha: link reaproveitável por 30 min, resposta que diferencia login existente de inexistente, e-mail mascarado devolvido. Sem limite de tentativas de login. | [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]] | 🟠 | Token de uso único, resposta neutra e bloqueio progressivo. |
| A9 | ✅ Senha com `Salt` no banco; 🔶 `GravarOperadorWS` devolve `DecryptValue` (senha reversível); histórico de senhas desligado (`TODO`). | [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] | 🟠 | Confirmar no SDK; usar *hash* lento e remover retorno em claro. |
| A10 | ✅ CORS com `AllowAnyOrigin` mesmo lendo `CorsOrigins`; `configuration/cors-origins` e `front-end-urls` públicos; hub SignalR `/notification-auth` sem autorização visível e `token-retrieve/{sessionId}` anônimo. | [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]] | 🟠 | Aplicar a lista de origens; autorizar o hub; proteger o `sessionId`. |
| A11 | ✅ Processo SEI do recurso de 3ª instância criado com acesso **público** e PDF do pedido anexado. | [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]] | 🟠 | Respeitar o grau de sigilo do pedido e anonimato do autor. |
| A12 | ✅ `ReencaminharPedido` sem checar `RRE_PDD`/operador; `InvalidarManifestacao` sem as regras da ação; `indeferir` prorrogação sem papel; `PermiteRemoverOperadorAtual` sempre verdadeiro; `ResponderEsclarecimento` sem checar o dono. | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Pedido-e-Recurso|Pedido-e-Recurso]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Reclassificacao-e-Invalidacao|Reclassificacao-e-Invalidacao]] | 🟠 | Repetir a checagem de permissão nos comandos (não só na consulta de ações). |

### B. Defeitos prováveis de lógica
| # | Fato | Origem | Sev. | Recomendação |
|---|---|---|---|---|
| B1 | ✅ `RegistrarReclassificacaoSeccional`: `assuntoEhDiferenteDoOriginal` compara igualdade. | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Reclassificacao-e-Invalidacao|Reclassificacao-e-Invalidacao]] | 🟠 | Confirmar a regra e corrigir com teste. |
| B2 | ✅ `BloqueioUsuario.DesbloquearUsuario`: condição invertida e contrato não aplicado; "falecido não desbloqueia" sem efeito. | [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio-de-Usuario]] | 🟠 | Corrigir e testar. |
| B3 | ✅ `Usuario.IsBloqueado()` ignora `DataDesbloqueio` (usado nas permissões de detalhar). | [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Banco-e-Mapeamentos|Banco-e-Mapeamentos]] | 🟠 | Considerar só bloqueios ativos. |
| B4 | ✅ Duas ações `GET v1/manifestacao` na integração de Ouvidoria (rota ambígua) e `GET` com `[FromBody]`. | [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] | 🟠 | Remover a ação de exemplo (`Create`) e usar `POST`/query. |
| B5 | ✅ `ProrrogarPrazoPedido` (manual) atualiza o prazo vigente antes de verificar prorrogação anterior. | [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]] | 🟠 | Validar antes de alterar. |
| B6 | ✅ `metro/ra` executa `ConsultarManifestacaoResumidaPorId`; nome de rota e comando não conferem. `claims.First(Name)` quebra para `OperadorWS`. | [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Endpoints-Ouvidoria|Endpoints-Ouvidoria]] | 🟡 | Corrigir o comando; tratar usuário sem nome. |
| B7 | ✅ Datas: 80 usos de `DateTime.Now` e 1 de `DateTime.Today`, mais `IApplicationDateTime` configurável; jobs e consultas divergem. | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]] | 🟠 | Unificar no relógio da aplicação. |

### C. Robustez e operação
| # | Fato | Origem | Sev. | Recomendação |
|---|---|---|---|---|
| C1 | ✅ 10 métodos `async void`, 5 `.Result` e 1 `.Wait()`, 28 `catch (Exception)` e vários handlers de job que engolem exceções e só registram. | busca no código | 🟠 | Retornar `Task`, propagar falhas e alertar. |
| C2 | ✅ Fallback silencioso do Iza (denúncia = false, classificação 999, unidade `01005`) e e-mails perdidos sem erro. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]] | 🟠 | Métrica e alerta; fila de reenvio de e-mail. |
| C3 | ✅ Registro de pedido para N unidades grava em N transações; `Publish` sem `await`. | [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Fluxo-Registro-de-Pedido]] | 🟡 | Uma transação por lote ou compensação. |
| C4 | ✅ Jobs só rodam por `GET /jobs/v2/{nome}`; sem agendador no repositório; job inexistente gera exceção de referência nula; endpoint v1 com dicionário vazio. | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]] | 🟠 | Documentar o agendador, autenticar, validar o nome e remover a v1. |
| C5 | ✅ Estado em campos de handlers (`_pedido`, `manifestacao`, `_usuario`) usado no pós-execução. | notas de fluxo | 🟡 | Garantir handlers transientes ou usar contexto do comando. |
| C6 | ✅ `Wait()` sobre `Send` na consulta de permissões (19 ações em lote). | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestacao]] | 🟡 | Tornar assíncrono e evitar repetir a consulta. |

### D. Manutenção, plataforma e dados
| # | Fato | Origem | Sev. | Recomendação |
|---|---|---|---|---|
| D1 | ✅ .NET 5 em todos os projetos e imagem `dotnet/aspnet:5.0`. Conhecimento externo: o .NET 5 saiu de suporte em 2022. | [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] | 🔴 | Planejar migração para versão com suporte. |
| D2 | ✅ `Dockerfile` ajusta o `apt` para `archive.debian.org` e instala pacotes sem verificação de validade (`Check-Valid-Until false`). | `src/Dockerfile` | 🟠 | Atualizar a imagem base. |
| D3 | ✅ Sem migrations/DDL no repositório; tabelas em três convenções; esquema fora do código. | [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Banco-e-Mapeamentos|Banco-e-Mapeamentos]] | 🟠 | Versionar o esquema (ferramenta de migração). |
| D4 | ✅ Valores fixos no código: unidades `01005` e `01007`, 90 dias de inatividade, 100 usuários/execução, janela ±5 dias, 9 dias de tramitação seccional, lista de ids de assunto do "metro", 3 pró-ativas, timeout de 5 s dos clientes. | notas de regra | 🟡 | Mover para configuração ou tabelas. |
| D5 | ✅ 30 `TODO`, código comentado (12 endpoints de `Dashboard`, `GravarFeriado` com enums inexistentes), `RecursoOld`, valor 25 ausente em `SituacaoPedidoEnum`, pacote `Cronos` sem uso, `OuvDF.IntegrationServices` com 1 arquivo, `BCadastro.Client` e `GovBr.Client` sem código. | busca no código | 🟡 | Remover legado; abrir itens para os `TODO`. |
| D6 | ✅ Resiliência HTTP duplicada entre MailService e PeoplesCheck; `DefaultHttpClient` não usado por todos. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]] | 🟡 | Centralizar em `DefaultHttpClient`. |
| D7 | ✅ Pastas `artifacts/` dentro de `src/` em 9 projetos (ignoradas pelo Git) e `src/Directory.Build.props` não versionado. | `.gitignore`, git status | 🟡 | Mover artefatos para fora de `src` e versionar o `props` ou documentar. |
| D8 | ✅ Documentação inexistente no repositório (sem README). | [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositorios]] | 🟡 | Manter o Mega Brain e criar README mínimo. |

### E. Testes
| # | Fato | Origem | Sev. | Recomendação |
|---|---|---|---|---|
| E1 | ✅ Testes de integração usam banco, Redis, RabbitMQ e serviços reais; só um *mock* (token); os clientes testam serviços reais. | [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] | 🟠 | Isolar com contêineres e doubles; não usar dados reais. |
| E2 | ✅ Sem teste por nome para jobs do SIC, cadastro de PF/PJ, recuperação de senha, vínculo SEI e cálculo de prazo; só 5 `[Fact]` unitários. | idem | 🟠 | Começar por cálculo de prazo, autenticação e jobs. |
| E3 | ✅ Pipeline do `Dockerfile` não executa `dotnet test`; sem relatório de cobertura. | idem | 🟠 | Rodar os testes no CI com limite mínimo. |

### F. Integração de denúncias com o S3 (novo em 2026-10-23, `820666c`)
| # | Fato (✅ ou 🔶) | Origem | Sev. | Recomendação |
|---|---|---|---|---|
| F1 | ✅ `DenunciaAceitaConsumer` e `DenunciaRecusadaConsumer` enviam `RemoverBloqueioExterno` **antes** de `DeleteByPrefixAsync`, sem `try/catch`; se o S3 falhar, o bloqueio já foi removido e o consumidor lança exceção (reprocessamento 🔶 depende do SDK, não lido), e os arquivos (relatório e anexos do cidadão) podem permanecer no bucket. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]] | 🟠 | Tornar a limpeza idempotente e tolerante a falha; definir política de expiração do bucket. |
| F2 | ✅ `ExportarDadosDenunciaHandler` envia o PDF do relatório (dados da manifestação) e os anexos a um armazenamento temporário externo à API; 🔶 classificação de dados (LGPD), controle de acesso e criptografia do bucket não verificados. | idem | 🟠 | Confirmar com o time as regras do bucket (acesso, retenção, criptografia). |
| F3 | ✅ `ExistsAsync` considera inexistente um objeto de tamanho 0 e `UploadAsync` o sobrescreve; um upload interrompido que deixa objeto parcial não é detectado (só o tamanho > 0). 🔶 sem validação de integridade. | idem | 🟡 | Comparar tamanho/ETag ao reutilizar. |
| F4 | ✅ Anexo ausente em disco lança `InvalidOperationException` e a denúncia não é publicada ao SCI; sem *retry* explícito nem alerta no código lido. | idem | 🟠 | Tratar e registrar o caso, com reprocessamento. |
| F5 | ✅ Sem teste (unitário ou de integração) para `S3Client`, `ExportarDadosDenunciaHandler`, os três consumidores ou o filtro por destino em `JaTramitouDaCoaciParaOuvidoria` (busca em `tests` sem ocorrências). | [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] | 🟠 | Cobrir com testes (S3 simulado). |

## Inferências e limitações
- 🔶 A severidade é do analista. Os itens A2, A5, A9 e A10 dependem do SDK interno `CGDF.DotNet.SDK` (autenticação global, validação de token, hash de senha), que não foi lido.
- 🔶 Nenhum teste foi executado; a lista de defeitos (B) vem de leitura estática.
- ❓ Itens fora do escopo: frontend, infraestrutura (Swarm, Jenkins), banco de produção.
- Conhecimento externo (D1): a data de fim de suporte do .NET 5 não vem do repositório.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Registro-de-Analise|Registro-de-Analise]]

## Pendências e próximo passo
- Revisar a severidade com o time; abrir itens (ou US) para A1 a A7 e D1 primeiro.
- Usar `analisar-us` para detalhar a correção de cada item aprovado.
