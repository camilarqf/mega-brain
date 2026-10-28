---
type: analysis-log
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-28
commit_data: 2026-10-22
branch: master
tags:
  - participa-df
  - controle
  - cobertura
---

# Registro de análise

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendencias]]

## Base analisada
- Repositório: `participa-df-backend` (endereço omitido); branch `master`; commit `4901ad5` (2026-09-15).
- Working tree: só `src/Directory.Build.props` não versionado.
- Método: leitura estática. Testes não executados, aplicação não iniciada.

## Regras de proteção aplicadas
- Valores de `appsettings*.json`, `.jenkins-pipelines/*.env.yml` e `.docker/` não serão reproduzidos: só nomes de chaves.
- Nenhum endereço, usuário ou dado pessoal será registrado.

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Cadastro no catálogo, inventário e esqueleto | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|Index]], [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositorios]], [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Backend-Index]], este registro, [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendencias]] |
| 1 | Visão geral: stack, arquitetura, ambientes, glossário, jobs, workflows | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Stack-e-Dependencias|Stack-e-Dependencias]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] (parcial), [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Glossario|Glossario]] (inferido, parcial), [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]] |
| 2 | Segurança, usuários, operadores e perfis | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] (parcial), [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]] (parcial), [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio-de-Usuario]] (parcial) |
| 3 | Domínio e persistência (NHibernate) | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] (parcial), [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]] (parcial), [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Banco-e-Mapeamentos|Banco-e-Mapeamentos]] (parcial) + ajuste em [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio-de-Usuario]] |
| 4 | Módulo Ouvidoria | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestacao]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Fluxo-Registro-de-Manifestacao]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Fluxo-Tramitacao-e-Resposta]], [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Reclassificacao-e-Invalidacao|Reclassificacao-e-Invalidacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Atribuicao-e-Bloqueio-Externo|Atribuicao-e-Bloqueio-Externo]] (todas parciais) + máquina de estados em [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]] |
| 5 | Módulo SIC (pedidos e recursos) | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Pedido-e-Recurso|Pedido-e-Recurso]], [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-do-SIC|Regras-de-Prazo-do-SIC]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Fluxo-Registro-de-Pedido]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]] (todas parciais) + máquina de estados do pedido em [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]] e ajuste em [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]] |
| 6 | Catálogo de endpoints | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]], [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Endpoints-Ouvidoria|Endpoints-Ouvidoria]], [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Endpoints-SIC|Endpoints-SIC]] (parciais; 262 endpoints) |
| 7 | Integrações (Iza, MailService, PeoplesCheck, SEI, RabbitMQ, HtmlToPdf, JWT) e Mapa | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]] (parcial) + `Catalogo-de-Sistemas` (9 serviços externos) e `Mapa-de-Integracoes` (9 linhas e 3 hipóteses) |
| 8 | Testes e débitos técnicos | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Debitos-Tecnicos]] (parciais) + [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Contexto-do-Sistema|Contexto-do-Sistema]] (inferido) |

## Resultado do lote 0
- Sistema cadastrado no catálogo com o ID `PARTICIPA-DF` (aprovado no plano). Sem relação com o `SICI`: as menções a "participa" nas notas do SICI são só `participant` em diagramas Mermaid.
- Não há documentação preexistente no repositório nem no vault.

## Resultado do lote 1
- 6 notas em `01-Visao-Geral/` (a sexta, Workflows-e-Consumidores, foi acrescentada com aprovação).
- Lido: `Program.cs`, `Startup.cs`, `.csproj` e `Directory.Packages.props`, `Dockerfile`, entrypoint de secrets, `JobController`, os 10 jobs e as consultas deles, 3 de 13 workflows, `DenunciaAceitaConsumer`, filtros e middlewares da Api, e só os **nomes** de chaves de `appsettings*.json` e dos YAML de pipeline.
- Não lido: valores de configuração, `*.env.yml`, `nuget_sources.config`, passos de 9 workflows, `DenunciaRecusadaConsumer`, predicados `NaoRespondido`/`EmSituacaoDeConclusao`/`NoPrazo()`, handler dos operadores SO.
- Riscos observados para o lote 8 (sem reproduzir valores): variável de licença literal no Dockerfile; chaves sensíveis em `appsettings*.json` versionados; CORS com `AllowAnyOrigin`; `/jobs/*` sem `[Authorize]` visível; uso de `DateTime.Now`/`Today` junto de `IApplicationDateTime`.

## Resultado do lote 2
- 4 notas: segurança (`security`), fluxo de autenticação (`flow`), módulo de usuários/operadores/perfis (`module`) e regra de bloqueio (`business-rule`).
- Lido: controllers `Security`, `Usuario` (v1/v2), `OperadorSIC/SO`, `PerfilSIC/SO`, `PessoaFisica/Juridica` (rotas e atributos), `Unidade`, `Politica`, `Integracao`, `Job`; entidades `Usuario`, `Perfil`, `Funcionalidade`, `OperadorSO/SIC/WS`, `BloqueioUsuario`; handlers de autenticação, token, notificação, recuperação e alteração de senha, bloqueio e desbloqueio, `GravarOperadorWS`, complexidade de senha; enums de funcionalidade, módulo, motivo e tipo de bloqueio.
- Não lido: SDK `CGDF.DotNet.SDK.*` (`UseCgdfSecurity`, `AddJwtSecurity`, `ITokenService`, `Senha`), cadastros de PF/PJ, `Unidade`, `ConsultarBloqueioUsuario`, `ConsultarUsuarioEstaBloqueado`, handlers dos operadores, `PeoplesCheck.Client`.
- Auto-correção: a regra "falecido não é desbloqueado" foi registrada como 🔶 (não aplicada no código lido), após reler o handler.
- Riscos para o lote 8: token cancelado sem verificação visível; `operador-ws` anônimo; senha reversível (indício); link de recuperação reaproveitável; enumeração de usuários; sem limite de tentativas; histórico de senhas desligado; `/jobs/*` sem `[Authorize]`; hub SignalR sem autorização visível.

## Resultado do lote 3
- 3 notas em `02-Dominio/` (todas `parcial`) e ajuste em `Bloqueio-de-Usuario` (continua `parcial`).
- Lido: `Usuario`, `PessoaFisica`, `PessoaJuridica`, `Unidade`, `Perfil`, operadores, `BloqueioUsuario`, `Prazo` (Shared e Ouvidoria), `SituacaoManifestacao`, `SituacaoPedido`, campos de `Manifestacao` e `Pedido`, todos os enums de Ouvidoria, SIC e Shared relevantes, mapas `Usuario`, `PessoaFisica`, `PessoaJuridica`, `Operador*`, `OperadorWS`, `BloqueioUsuario`, `UsuarioFalecido` e as relações de `ManifestacaoMap`/`PedidoMap` (nomes de tabelas dos 3 projetos via busca), duas consultas de bloqueio.
- Não lido: corpo de `Manifestacao` e `Pedido`, os outros ~100 mapas, DDL/chaves/índices (inexistentes no repositório), conexão com o banco.
- Achados: não há migrations; 3 convenções de nome de tabela; `PARTICIPADF` e `OUVDF` são canais de entrada na Ouvidoria (`TipoEntradaEnum`); tabela de óbitos chamada `TB_LISTA_OBITO_PARTICIPA_DF`; `SituacaoPedidoEnum` sem o valor 25; `Usuario.IsBloqueado()` ignora `DataDesbloqueio`.

## Resultado do lote 4
- 6 notas novas (todas `parcial`) + máquina de estados da manifestação em `Enums-e-Estados`.
- Autorização da usuária (2026-10-18): "pode aprovar esse e os próximos planos". Os lotes seguintes seguem o mesmo ritual (plano resumido no registro, escrita, validação), sem git e sem alterar código.
- Lido: controllers de Ouvidoria (rotas e acesso), `Manifestacao` inteira, passos do registro (4 de 15), 4 passos da reclassificação, handlers de tramitação (comum e seccional), respostas (3), prorrogação (solicitar, deferir), invalidação, avaliação, esclarecimentos, complementação pró-ativa, atribuição, bloqueio externo, `CalculadoraPrazoService`, e toda a consulta de permissões.
- Não lido: `Dashboard`, `Colecoes`, cadastros (assunto, classificação, formulário), exportações, variantes operador/integrada do registro, `IndeferirSolicitacao…`, `RegistrarProvidencia`, solicitação de avaliação e pesquisa de satisfação, `ConsultarManifestacaoBloqueante`, `RemoverAtribuicaoOperador`, política de zeladoria.
- Riscos para o lote 8: relato do cidadão em log; reclassificação seccional com comparação invertida; `InvalidarManifestacao` sem a regra de unidade/estado; `resumo` anônimo; `indeferir` sem papel; `Wait()` sobre `Send` nas permissões; mediador sem `await` em `ValidarPermissao`; `ResponderEsclarecimento` sem checar o dono; `Usuario.IsBloqueado()` ignorando desbloqueio afeta o detalhamento.

## Resultado do lote 5
- 5 notas novas (parciais), máquina de estados do pedido em `Enums-e-Estados` e correção do diagrama de omissão; ajuste em `Jobs-Agendados`.
- Lido: controllers do SIC (rotas e acessos), `Pedido` completo, `ConsultarPermissaoPedido` (21 ações), passos `SetContext`, `CriarPedido`, `GravarPedido`, handlers de resposta do pedido, prorrogação (manual, automática, de recurso), recursos 1ª e 3ª, resposta de recurso 1ª, resposta preliminar e decisão da 3ª, omissão (unidade e CGDF, decisão), reencaminhamento, conclusão por prazo, passos `CriarProcessoSei` e `CriarDocumento`, `CalcularPrazoHandler`, `ConsultarSituacaoResposta`; grep de todas as situações por comando.
- Não lido: `Validar`, `ValidarArquivos`, `NotificarAutor`, `AtribuirPedidoParaOperador`, 2ª instância (registro e resposta), `RegistrarRespostaPreliminarNotificacaoOmissaoResposta`, `SolicitarVinculoSei`, `RegistrarRespostaDefinitivaPedido`, `GerarPedidoPDFSei`, cadastros (formulário, assunto, feriado), questionário, exportações e `MoverPedidosParaContaLGPD`.
- Riscos para o lote 8: `NotificacaoController` sem `[Authorize]`; `Reencaminhar` sem checagem de permissão; `PermiteRemoverOperadorAtual` sempre verdadeiro; prorrogação manual altera o prazo antes de validar a prorrogação já feita; transações por unidade no registro; processo SEI público com PDF do pedido; `todo` nas regras de recurso; exceções engolidas nos handlers de job; `Publish` sem `await`.

## Resultado do lote 6
- 3 notas `api` (catálogo geral com matriz, Ouvidoria e SIC) geradas por **script** a partir dos atributos dos controllers: 262 endpoints (180 POST, 82 GET), conferidos contra a contagem de `[Http*]` do código sem trechos comentados. O script ficou na área temporária da sessão, não no repositório nem no vault.
- Achados: 25 endpoints sem atributo de autorização (inclui `Unidade` gravar/ativar/desativar, `Notificacao` do SIC, `Job`, `Configuration`, `arquivo/download` do SIC); 56 anônimos (vários gravam dados, inclusive `pessoa-fisica/por-operador` e `operador-so/operador-ws`); duas ações `GET v1/manifestacao` na integração de Ouvidoria; 12 endpoints do `Dashboard` comentados; nenhum PUT/DELETE.
- Não lido: contratos dos comandos (campos), códigos de resposta, `EfetuarDownload`.

## Resultado do lote 7
- 1 nota canônica de integrações (`integration`, parcial) com 10 integrações; catálogo e mapa atualizados (IDs: `Iza`, `MailService`, `PeoplesCheck`, `SEI`, `Servico-HtmlToPdf`, `RabbitMQ`, `Servico-Geocodificacao`, `Grafana-Loki`, `NewRelic`).
- Lido: todos os arquivos dos clientes `DefaultHttpClient`, `Iza.Client`, `MailService.Client`, `PeoplesCheck.Client`, `IntegrationServices`; controllers `IA`, `ApiMetro`, `ServicosExternos`, `Integracao` (Ouvidoria e Shared); `ManifestacaoTramitadaEventHandler`, os dois consumidores de denúncia, `ConvertHtmlToPDFHandler`, health checks, `ExcluirContaUsuario`, passos do vínculo SEI (2 de 6).
- Não lido: valores de configuração, o SDK `CGDF.SEI.DotNet.SDK` e `CGDF.DotNet.SDK.PubSub`, passos `GerarPedidoPDFSei`/`NotificarSolicitante`, contratos de resposta de MailService e PeoplesCheck.
- Achado de nome (🔶): "Participa DF" é o nome do produto para o usuário (texto de e-mail, agente HTTP `Participa-DF`, produtor `participa-df` nos eventos, mensagem de zeladoria); `OuvDF` é o nome histórico do código (mensagem "OUV-DF"). Confirmar com o time.
- Riscos para o lote 8: SSRF potencial em `servicos/siturb` e `servicos/ra` (anônimos, `WebClient` com URL do chamador); TLS desligado no PeoplesCheck; relato do cidadão enviado ao Iza (4 chamadas por registro); fallback silencioso do Iza (denúncia = false, unidade `01005`); e-mails perdidos sem erro; processo SEI público; códigos de unidade fixos (`01005`, `01007`); resiliência duplicada; `HttpClient.Send` síncrono.

## Resultado do lote 8
- 2 notas (`quality` e `technical-debt`, parciais) + `PARTICIPA-DF-Contexto-do-Sistema` (`system`, inferido).
- Lido: estrutura e contagem de todos os projetos de `tests/`, `Configuration/Startup` de teste, nomes de chaves dos `appsettings.json` de teste, cobertura por nome de comando; buscas de contagem (`async void`, `.Result`, `.Wait()`, `catch (Exception)`, `DateTime.Now`, `TODO`); verificação do preenchimento (apenas tamanho) de chaves sensíveis nos `appsettings*.json` versionados; `Dockerfile`.
- Não feito: execução dos testes (exigem banco e serviços externos), cobertura de linhas, leitura do corpo dos testes.
- Débitos consolidados: 12 de segurança/privacidade (A), 7 de lógica (B), 6 de robustez (C), 8 de manutenção/plataforma (D), 3 de testes (E).

## Resultado final da análise (lotes 0 a 8)
- **Notas**: 33 no backend (30 técnicas + índice + 2 de controle) e 3 de sistema (índice, repositórios, contexto); catálogo, mapa de integrações e 9 serviços externos atualizados.
- **Cobertura**: `parcial` em quase todas as notas. Lacunas principais: SDK interno `CGDF.DotNet.SDK.*` (autenticação, senha, pipeline de comandos, PubSub, SEI), valores de configuração e `*.env.yml`, ~100 mapas NHibernate, cadastros e consultas auxiliares, exportações, contratos de payload, frontend, execução dos testes.
- **Itens abertos**: ver [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências]] (cerca de 70 perguntas por lote).
- **Para atualizar após novos commits**: `git diff 4901ad5..HEAD --stat` e a skill `atualizar-documentacao`; o campo `sources` de cada nota indica os arquivos cobertos.

## Atualização de 2026-10-23 (`4901ad5..820666c`)
- Base: HEAD `820666cb28ee23b239e5ad033034c3e8413a10ed` (branch `master`, 2026-10-22); 13 commits sem merges, 31 arquivos; classificação: mudança funcional e de contrato/integração, mais configuração e segurança. Working tree: `Directory.Build.props` e dois `.md` de caso (`case-participa-df-*`) não versionados (não analisados).
- Notas atualizadas: Integracoes-Externas (mensageria reescrita, nova seção S3, histórico), Workflows-e-Consumidores, Atribuicao-e-Bloqueio-Externo, Perfis-e-Ambientes, Stack-e-Dependencias, Arquitetura, Glossario, Debitos-Tecnicos (A1.1 e F1–F5), Testes-e-Cobertura, Index e Pendencias; fora do backend: `Mapa-de-Integracoes` e `PARTICIPA-DF-Repositorios`. Nenhuma nota nova.
- Lido: `S3Client`, `S3ClientSettings`, `AddS3Client`, `ExportarDadosDenuncia` e o handler, contratos de denúncia, os 3 consumidores, o diff do `ManifestacaoTramitadaEventHandler`, `Startup`, csproj, `Dockerfile`, `deployment.params.yml` e os diffs dos `appsettings` (só nomes de chaves).
- Não lido: SDK `CGDF.DotNet.SDK.PubSub` (retry e DLQ), `ExportarManifestacaoOperadorPDF` e o template do relatório, `UploadObjectRequest`, `IS3Client`, o conteúdo do bucket, `appsettings` de teste, o SCI atual contra o payload.
- Corrigido: a inferência anterior de que a recusa mantém o bloqueio (agora ✅ remove). Notas fora do escopo e não reverificadas: Seguranca-e-Autorizacao, Catálogo de endpoints, módulos de Ouvidoria/SIC (o diff não toca controllers).
- Contagens do Index ("Números rápidos") e dos testes não foram refeitas.

## Próximo passo exato
0. (2026-10-23) Responder as perguntas da seção "atualização de 2026-10-23" em [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendencias]], conferir o payload com a documentação do `SCI` e rotacionar os segredos que estiveram versionados.
1. Revisar com o time as pendências e os débitos 🔴 (A1 a A7, D1) e confirmar o contexto do sistema.
2. Ler o SDK `CGDF.DotNet.SDK.*` (se acessível) para fechar A2, A5, A9 e A10, e subir a cobertura das notas de segurança.
3. Identificar e analisar o frontend (nova pasta `Frontend/`) e consolidar os fluxos ponta a ponta.
4. Quando autorizado, executar a suíte de testes em ambiente isolado e registrar o resultado.
5. Sincronizar o vault com a skill `sincronizar-brain` (aprovação explícita; conteúdo é documentação derivada de código institucional, categoria (b), e contém riscos de segurança: confirmar a autorização antes de qualquer publicação).

## Histórico de estrutura
- 2026-10-27: pastas reorganizadas conforme a seção 1 do `BRAIN-RULES.md` (numeração fixa; melhorias do cofre, lote 3).
- 2026-10-28: notas renomeadas com o prefixo do sistema (seção 3 do `BRAIN-RULES.md`; melhorias do cofre, lote 4). O nome antigo ficou em `aliases`:
  - `Atribuicao-e-Bloqueio-Externo` → `PARTICIPA-DF-Backend-Modulo-Atribuicao-e-Bloqueio-Externo`
  - `Bloqueio-de-Usuario` → `PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario`
  - `Manifestacao` → `PARTICIPA-DF-Backend-Modulo-Manifestacao`
  - `Pedido-e-Recurso` → `PARTICIPA-DF-Backend-Modulo-Pedido-e-Recurso`
  - `Reclassificacao-e-Invalidacao` → `PARTICIPA-DF-Backend-Modulo-Reclassificacao-e-Invalidacao`
  - `Regras-de-Prazo-do-SIC` → `PARTICIPA-DF-Backend-Regra-Prazo-do-SIC`
  - `Regras-de-Prazo-e-Prorrogacao` → `PARTICIPA-DF-Backend-Regra-Prazo-e-Prorrogacao`
  - `Usuarios-Operadores-Perfis` → `PARTICIPA-DF-Backend-Modulo-Usuarios-Operadores-Perfis`
