---
type: analysis-log
system: PARTICIPA-DF
repository: participa-df-backend
status: pendente
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-23
tags:
  - participa-df
  - pendencias
  - duvidas
---

# Pendências e pontos a confirmar

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Registro-de-Analise|Registro-de-Analise]]

## Perguntas de negócio (confirmar com o time)
- [ ] Qual é o nome oficial do sistema? 🔶 Hipótese com evidência no código (lote 7): **Participa DF** é o nome do produto ao usuário (e-mails, agente HTTP, produtor de eventos) e **OuvDF** o nome histórico do código. Confirmar e, se aprovado, fechar este item.
- [x] Qual é o repositório do frontend consumidor? Resolvido em 2026-10-18: `participa-df-frontend` ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Frontend Cidadão]]). Restam os repositórios dos outros 2 front-ends (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências do Frontend]]).

## Perguntas técnicas
- [ ] `OuvDF.BCadastro.Client` e `OuvDF.GovBr.Client` (só `bin/obj`) foram removidos ou são trabalho futuro?
- [x] `OuvDF.IntegrationServices` (1 arquivo `.cs`) tem uso real? Resolvido em 2026-10-23 (`820666c`): o projeto agora contém os 3 consumidores de denúncia e é referenciado pela `OuvDF.Api`.

## Perguntas surgidas no lote 1
- [ ] Expansão oficial de SO, SIC, SEI, COACI, CQ e OGDF; finalidade de Iza e PeoplesCheck (ver [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Glossario|Glossário]]).
- [ ] Qual agendador dispara `GET /jobs/v2/{nome}`, com que periodicidade e com que credencial? `/jobs/*` exige autenticação? ([[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]])
- [ ] Os endpoints `GET /jobs/{nome}` (v1) ainda são usados? O dicionário de comandos está vazio.
- [ ] (2026-10-23: a licença do New Relic e os segredos de aplicação saíram dos arquivos versionados, `820666c`; a pergunta sobre rotação e histórico do git continua aberta) Os valores sensíveis em `appsettings*.json` e a licença do New Relic no `Dockerfile` são reais? Já foram rotacionados? ([[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]])
- [ ] A política de CORS deveria restringir às origens de `CorsOrigins`? Hoje aplica `AllowAnyOrigin`.
- [ ] Correspondência entre ambientes da aplicação (Development, Homolog, Prod) e do deploy (sandbox, staging, prod); origem da string de conexão do banco.
- [ ] `ExportarPedidosCaixaEntradaWorkFlow` (PDF) está desativado de propósito? Falta `AddWorkFlow` em `Startup`.
- [ ] `ValidateTokenFilter`, `ExceptionHandlingFilter` e `ExceptionHandlingMiddleware` estão em uso? ([[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]])
- [ ] Os jobs de pedidos devem comparar prazos com `IApplicationDateTime` (hoje usam `DateTime.Now` nas consultas)?
- [ ] Quem publica `denuncia-aceita` e `denuncia-recusada`? 🔶 Provavelmente o `SCI`. `DenunciaId` equivale ao id da manifestação? ✅ Sim no código (`CommandID<long>(DenunciaId)`; confirmado em 2026-10-23, `820666c`), falta confirmar no lado do SCI.

## Perguntas surgidas no lote 2
- [ ] O SDK (`UseCgdfSecurity`/`AddJwtSecurity`) verifica `TokenCancelado` ou impõe autenticação global? Sem isso, logout não invalida o token e `/jobs/*` e o hub SignalR ficam abertos ([[01-Sistemas/PARTICIPA-DF/Backend/06-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]).
- [ ] `POST /operador-so/operador-ws` precisa ser anônimo? A comparação `loginExistente != null` faz o comando sempre falhar?
- [ ] Como a senha é guardada (classe `Senha` do SDK)? Por que `GravarOperadorWS` devolve `DecryptValue`?
- [ ] O link de recuperação de senha deveria ser de uso único? O login inexistente deveria ter a mesma resposta que o existente?
- [ ] Existe bloqueio por tentativas de login? Para que serve `count-try` do PeoplesCheck?
- [ ] O login assistido por sessão (`notify`/`token-retrieve`) é usado por qual cliente? O hub `/notification-auth` precisa de autorização?
- [ ] Por que `AtualizarHistoricoDeSenha` está comentado (`TODO: Revisar`)? A regra das 3 últimas senhas está ativa?
- [ ] Regra "falecido não pode ser desbloqueado": está inativa por erro? ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Bloqueio-de-Usuario|Bloqueio-de-Usuario]])
- [ ] `BloquearUsuarioHandler` engole exceções: o operador de sistema tem a funcionalidade 36 (Bloquear/Desbloquear)?
- [ ] Os endpoints de `OperadorSICController` e `PerfilSICController` só com `[Authorize]` são protegidos por funcionalidade nos handlers?
- [ ] O token de login deve falhar para usuários sem PF/PJ (ex.: `OperadorWS`) por causa de `claims.First(Name)`?

## Perguntas surgidas no lote 3
- [ ] Qual a relação entre os nomes "Participa DF" e "OuvDF"? `TipoEntradaEnum` trata `OUVDF` e `PARTICIPADF` como canais distintos, e há tabela `TB_LISTA_OBITO_PARTICIPA_DF` ([[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]]).
- [ ] Onde está o DDL do banco (chaves, índices, constraints) e quem gerencia o esquema? Não há migrations no repositório ([[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Banco-e-Mapeamentos|Banco-e-Mapeamentos]]).
- [ ] Como e com que frequência `TB_LISTA_OBITO_PARTICIPA_DF` é alimentada, e a partir de qual fonte?
- [ ] O valor 25 de `SituacaoPedidoEnum` foi removido de propósito?
- [ ] `RecursoOld` ainda é usada ou é legado a remover?
- [ ] Por que `PessoaFisica` cria `Senha(senha, 3)` e `PessoaJuridica` `Senha(senha)`?
- [ ] `Usuario.IsBloqueado()` deveria considerar só bloqueios sem `DataDesbloqueio`?
- [ ] Qual a relação entre `Cidadao`, `Estrangeiro` e `PessoaFisica`?

## Perguntas surgidas no lote 4
- [ ] Qual é o valor de `PrazoManifestacaoPadrao` e a regra de negócio dos prazos (dias corridos com ajuste ao dia útil)? A janela de ±5 dias para solicitar prorrogação é regra oficial? ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Regras-de-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]])
- [ ] Na reclassificação seccional, `assuntoEhDiferenteDoOriginal` compara igualdade: erro? ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Reclassificacao-e-Invalidacao|Reclassificacao-e-Invalidacao]])
- [ ] `InvalidarManifestacao` deveria repetir as regras da ação `NVL_MNF` (operador corrente, unidade, estado)?
- [ ] O que devolve `POST manifestacao/resumo` (anônimo)? Há dados pessoais?
- [ ] `POST prorrogacao-prazo/indeferir` deve exigir o papel `OperadorSO` e a funcionalidade `GerenciarProrrogacoes`?
- [ ] Quem pode avaliar o atendimento (`avaliar`) e o que ocorre se o cidadão não avalia?
- [ ] O relato do cidadão pode ser registrado em log de aviso (`ValidarIdentificacao`)?
- [ ] Quem dispara `AplicarBloqueioExterno` e como funciona o fluxo com o sistema correcional/COACI?
- [ ] Quem chama `MoverManifestacoesParaContaLGPD`, e a conta LGPD (pessoa jurídica `EntidadeEspecial`) existe em todos os ambientes?
- [ ] Os handlers (Resposta, Prorrogação etc.) são transientes? Eles guardam estado em campo de instância.

## Perguntas surgidas no lote 5
- [ ] Qual o valor de cada prazo do SIC (`QtdDiadPrazoPedido`, `…Prorrogacao`, `…ParaResponder`, `…ParaRecorrer`, `…NotificacaoOrgao`, `…RecursoTerceiraInstancia`, `…NotificacaoCGDF`) e a base legal? ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Regras-de-Prazo-do-SIC|Regras-de-Prazo-do-SIC]])
- [ ] Os endpoints de `NotificacaoController` (omissão de resposta) precisam ser autenticados? Quem os usa manualmente? ([[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]])
- [ ] `ReencaminharPedido` deveria verificar a permissão `RRE_PDD` e o operador atual? `PermiteRemoverOperadorAtual` deve ser sempre `true`?
- [ ] O processo SEI de recurso de 3ª instância é criado com acesso **público** e com o PDF do pedido; isso é intencional? Como tratar pedidos com sigilo restrito ou dados pessoais? ([[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]])
- [ ] A prorrogação manual atualiza o prazo vigente antes de verificar se já houve prorrogação: a transação desfaz? 
- [ ] Um pedido registrado para N unidades é gravado em N transações; o que ocorre com falha parcial?
- [ ] O que o evento `PedidoRegistrado` dispara (quem consome)?
- [ ] Quais regras do recurso de 2ª/3ª (comentários `todo`) estão pendentes?
- [ ] Os trechos comentados e valores de `SituacaoPedidoEnum` ausentes (25; Deferido/Indeferido em `GravarFeriado`) são legado a remover?

## Perguntas surgidas no lote 6
- [ ] Há autenticação global? Se não, os 25 endpoints sem atributo (`Unidade`, `Notificacao`, `Job`, `Configuration`, SIC `arquivo/download` etc.) estão abertos ([[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]]).
- [ ] `pessoa-fisica/por-operador` deveria ser anônimo? 
- [ ] A rota `GET v1/manifestacao` duplicada na integração da Ouvidoria funciona? Quem consome a API `v1` (`OperadorWS`)?
- [ ] `EfetuarDownload` (SIC e Ouvidoria) confere o dono do anexo antes de devolver o arquivo?
- [ ] Os endpoints comentados de `Dashboard` foram migrados para outro serviço?
- [ ] `configuration/cors-origins` e `front-end-urls` precisam ser públicos?

## Perguntas surgidas no lote 7
- [ ] O Iza é um serviço institucional ou de terceiro? O cidadão consente o envio do relato? ([[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]])
- [ ] O fallback do Iza (denúncia = false, unidade `01005`) é desejado? Alguém monitora as falhas?
- [ ] Por que o TLS está desligado no PeoplesCheck? Há certificado interno não confiável?
- [ ] `servicos/siturb` e `servicos/ra` precisam aceitar uma URL completa do chamador? Quem usa `servicos/*` e `metro/*`?
- [ ] Qual é o sistema correcional/COACI que publica `denuncia-aceita/recusada` e consome `denuncia-registrada`?
- [ ] O processo SEI de 3ª instância precisa ser público com o PDF do pedido?
- [ ] Os e-mails perdidos (circuito aberto, 400) são reenviados? Há fila de reenvio?
- [x] Os serviços de PDF do PARTICIPA-DF e do SICI são o mesmo serviço? Sim, informado pelo usuário em 2026-10-19 (ID único `Servico-HtmlToPdf`). Falta identificar o dono.
- [ ] Os códigos de unidade fixos (`01005`, `01007`) estão documentados no banco?

## Perguntas surgidas no lote 8
- [ ] Os testes de integração rodam contra qual banco/ambiente? Há limpeza dos dados? Quem os executa e quando? ([[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Testes-e-Cobertura|Testes-e-Cobertura]])
- [ ] Os segredos versionados (A1) já foram rotacionados? Quem é o dono do ambiente? ([[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Debitos-Tecnicos]])
- [ ] Existe plano de migração do .NET 5?
- [ ] Qual é a ferramenta de CI/CD e ela executa testes e análise de dependências?

## Perguntas surgidas na atualização de 2026-10-23 (`820666c`)
- [ ] O bucket S3 de `integracao-sci-participa-df` é o `MinIO-CGDF`? Quem é o dono, qual a política de acesso, criptografia e expiração dos objetos?
- [ ] O `SCI` espera o payload atual de `denuncia-registrada` (`ArquivoReferencia` e `Anexos`) e o novo canal `denuncia-criada`? Por que o merge de `integracao-sci-ajustar-payload-arquivos` foi revertido (`2be9deb`)?
- [ ] Falha do S3 em `DenunciaAceitaConsumer`/`DenunciaRecusadaConsumer`: o SDK de PubSub reprocessa a mensagem (e a remoção do bloqueio roda de novo)? (débito F1)
- [ ] Os segredos que estiveram nos arquivos versionados foram rotacionados e o histórico do git foi limpo? (A1.1)
- [ ] Quem aplica `AplicarBloqueioExterno`? Em 2026-10-23 (`820666c`) confirmei que **nenhum código do repositório** envia esse comando; perguntar ao time se o bloqueio é ligado por outro sistema, por rota fora do repositório, ou se a funcionalidade está incompleta (sem ele, `denuncia-aceita`/`denuncia-recusada` só removem um bloqueio que não foi ligado aqui).

## Próximo passo
Análise inicial concluída (ver [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Registro-de-Analise|Registro-de-Analise]]).
