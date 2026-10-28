---
type: integration
aliases:
  - "Integrações externas"
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-23
consumer: PARTICIPA-DF
tags:
  - armazenamento-objetos
  - mensageria
sources:
  - src/OuvDF.DefaultHttpClient
  - src/OuvDF.Iza.Client
  - src/OuvDF.MailService.Client
  - src/OuvDF.PeoplesCheck.Client
  - src/OuvDF.IntegrationServices
  - src/OuvDF.S3.Client
  - src/OuvDF.ServicoOuvidoria/Domain/Contracts
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/ExportarDadosDenuncia
  - src/OuvDF.Api/Startup.cs
  - src/OuvDF.Api/Program.cs
  - src/OuvDF.Api/Controllers/ServicoOuvidoria/ServicosExternosController.cs
  - src/OuvDF.Api/Controllers/ServicoOuvidoria/ApiMetroController.cs
  - src/OuvDF.Api/Controllers/ServicoOuvidoria/IntegracaoController.cs
  - src/OuvDF.Api/Controllers/Shared/IntegracaoController.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/RegistrarManifestacao/SharedSteps/RecuperarDadosIA.cs
  - src/OuvDF.ServicoOuvidoria/Domain/EventHandlers
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands/VincularPedidoSei
  - src/OuvDF.Shared/Infra/Services/ConvertHtmlToPDF
  - src/OuvDF.Shared/Api/HealthChecks
  - src/Dockerfile
  - .jenkins-pipelines/deployment.params.yml
---

# Integrações externas

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[Mapa-de-Integracoes|Mapa de integrações]], [[Catalogo-de-Sistemas|Catálogo (serviços externos)]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]


Provedor: [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Servico-HtmlToPdf]] (✅ confirmado pelo usuário).

> Endereços, chaves e nomes de cabeçalho de segredo **omitidos** de propósito; só os nomes das seções de configuração são registrados.

## Visão geral

| Provedor (ID do catálogo) | Direção | Tecnologia | Cliente no código | Configuração | Confirmação |
|---|---|---|---|---|---|
| `Iza` | saída | HTTP POST JSON | `OuvDF.Iza.Client` (4 operações) | `IzaClientSettings` | ✅ |
| `MailService` | saída | HTTP POST JSON e multipart | `OuvDF.MailService.Client` | `MailServiceClientSettings`, `MailServiceApiSettings` | ✅ |
| `PeoplesCheck` | saída | HTTP GET/POST | `OuvDF.PeoplesCheck.Client` | `PeoplesCheckClientSettings` | ✅ |
| `SEI` | saída | web service via SDK `CGDF.SEI.DotNet.SDK` | passos de `VincularPedidoSei` | `SeiConnectionSettings`, `IntegracaoSicSeiSettings` | ✅ uso; 🔶 protocolo (SOAP) |
| `Servico-HtmlToPdf` | saída | HTTP POST JSON | `ConvertHtmlToPDFHandler` (RestSharp) | `HtmlToPdfConfiguration`, `url-service-html-to-pdf` | ✅ |
| `RabbitMQ` | saída e entrada | mensageria (SDK `CGDF.DotNet.SDK.PubSub`) | `ManifestacaoTramitadaEventHandler`, `DenunciaCriadaConsumer` e demais consumidores | `RabbitMqPubSubSettings`, `ConnectionStrings` | ✅ |
| Armazenamento de objetos S3 (🔶 `MinIO-CGDF`) | saída | API S3 via pacote `Minio` 4.0.7 | `OuvDF.S3.Client` (`S3Client`) | `S3ClientSettings` | ✅ uso; 🔶 provedor |
| `Servico-Geocodificacao` | saída (proxy) | HTTP GET (`WebClient`) | `ServicosExternosController` | host fixo no código (omitido) | ✅ |
| `Grafana-Loki` | saída | sink do Serilog | `Program.cs` | `LoggerSettings` | ✅ |
| `NewRelic` | saída | agente .NET no container | `Dockerfile` | variáveis do profiler | ✅ |
| Sistemas integrados (`OperadorWS`) | entrada | REST `v1/*` | `IntegracaoController` (Ouvidoria e Shared) | operador WS cadastrado | ✅ endpoints; ❓ consumidores |

## Evidências
Projetos de cliente e arquivos em `sources`; configuração apenas por nome. Commit `4901ad5`; seções 6 e 10 atualizadas até o commit `820666c` (2026-10-23).

## Informações confirmadas

### 1. Iza (IA de triagem)
- ✅ Operações (todas `POST` JSON com o **relato** do cidadão): `predict-assunto-by-relato`, `predict-classificacao-by-relato-assunto`, `predict-is-denuncia-by-relato-assunto`, `predict-unidade-by-relato-assunto-classificacao`. Campos: `relato`, `assunto_id`, `classificao_id`.
- ✅ Usadas pelo passo `RecuperarDadosIA` do registro de manifestação e por `IAController` (`servico-ouvidoria/ia/assunto` e `/classificacao`, anônimos): decide se é **denúncia**, a classificação sugerida, a unidade de tramitação inicial e assuntos prováveis.
- ✅ Se é denúncia, a classificação passa a `Denúncia` e a unidade inicial vira a unidade de triagem de denúncias (código fixo no código, `01007`).
- ✅ Resiliência: cada cliente tem *fallback* em `HttpRequestException` que devolve **200** com valor padrão: denúncia = `false`, classificação = `999` (Indefinida), unidade = `01005`, assunto vazio. Não há retry nem circuit breaker; timeout vem de `IzaClientSettings.Timeout`.
- ✅ Health check e URL de saúde: `IzaClientSettings.HealthCheckEndpoint` (configurado; uso 🔶 no health do deploy).
- ✅ Agente de usuário: `Participa-DF`.

### 2. MailService
- ✅ Operações: `GET /health`, `POST /mail/send` (JSON), `POST /mail/send-with-attachments` (multipart). Autenticação por cabeçalho de chave de API (nome e valor vêm de `MailServiceClientSettings`; omitidos).
- ✅ Remetente fixo no contrato (`MailMessageRequest.From`, caixa institucional do Participa-DF); corpo HTML vindo de templates (`IMailTemplateBuilder`, 34 modelos em `HtmlTemplates/Email`).
- ✅ Resiliência: *retry* (contagem e intervalo de `MailServiceClientSettings`), *circuit breaker*, *fallback* (resposta **400** com mensagem configurada quando o circuito abre) e *timeout* de 5 s fixo. Há `HttpLoggingHandler` que registra método, URI, status e tempo (sem corpo).
- ✅ Health check do MailService (estado *Degraded* se falhar).
- ✅ Uso: notificações de manifestações, pedidos, recursos, prorrogações, omissões, cadastro e recuperação de senha, exclusão de conta.

### 3. PeoplesCheck
Provedor: [[01-Sistemas/PeoplesCheck/Servico/06-API/PeoplesCheck-Servico-Catalogo-de-Endpoints|PeoplesCheck]] (✅ confirmado pelo usuário em 2026-10-19; contrato e regras do lado servidor em [[01-Sistemas/PeoplesCheck/PeoplesCheck-Index|PeoplesCheck-Index]]).
- ✅ Operações: `Check` (GET, parâmetro `data`), `CountTry` (GET), `Challenge` (POST JSON), `CheckPJ` (GET `…/{cnpj}?data=cpf`, exige o aceite de responsabilidade). Cabeçalho `X-API-KEY` (valor omitido). Os endpoints expostos em `SecurityController` (`check`, `count-try`, `challenge`, `check-cpf-vinculado-pj`) são **anônimos** e repassam os dados do chamador.
- ✅ Se `Challenge` retorna 200, a resposta é gravada em cache (`GravarDesafioEmCache`).
- ✅ Resiliência igual à do MailService (retry, breaker, fallback 400, timeout de 5 s).
- ✅ **A validação do certificado TLS do PeoplesCheck está desligada** (`ServerCertificateCustomValidationCallback` devolvendo `true`, aplicado com `ConfigurePrimaryHttpMessageHandler`).
- 🔶 Finalidade: validar identidade de pessoa (CPF e vínculo CPF–CNPJ) no cadastro; o contrato de resposta não está no repositório.

### 4. SEI (recurso de 3ª instância)
- ✅ Via SDK `CGDF.SEI.DotNet.SDK` (`AddSeiConnection`): cria o processo (`SeiProcedimento`, tipo e unidade em `IntegracaoSicSeiSettings`, nível de acesso **público**) e junta o PDF do pedido (`SeiDocumento`, tipo "R", com remetente configurado). Detalhes em [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]].
- ✅ O vínculo (id do processo, número, documento) é gravado em `TB_VINCULO_PEDIDO_SEI`.
- 🔶 `SeiConnectionSettings.WsURL` e a sigla de sistema indicam web service SEI (SOAP).

### 5. Serviço de PDF
- ✅ `ConvertHtmlToPDFHandler`: `POST html-to-pdf/generate` com `{"HtmlString": "..."}`; falha de status → notificação "Ocorreu um erro ao tentar gerar o arquivo PDF". Usado nos PDFs de manifestação e pedido.
- ✅ O contrato (`HtmlString`) é o mesmo do SICI e do SCI; o usuário informou em 2026-10-19 que é o mesmo serviço (ID único `Servico-HtmlToPdf`; ver [[Mapa-de-Integracoes|Mapa]]).

### 6. Mensageria (RabbitMQ)
*Atualizado em 2026-10-23 (commit `820666c`). A versão anterior está em "Histórico" abaixo.*

| Canal | Papel do Participa-DF | Evento | Tratamento |
|---|---|---|---|
| `denuncia-criada` | **publica e consome** | `DenunciaCriada` (só `DenunciaId`) | publicado por `ManifestacaoTramitadaEventHandler` quando uma **denúncia** sai da COACI para uma unidade de ouvidoria; consumido por `DenunciaCriadaConsumer` na própria API, que envia `ExportarDadosDenuncia` |
| `denuncia-registrada` | **publica** | `DenunciaRegistrada` (`DenunciaId`, unidades de origem e destino, protocolo, `Identificada`, `ArquivoReferencia`, `Anexos[]`) | publicado por `DenunciaCriadaConsumer` depois de os arquivos estarem no bucket (`produtor: participa-df`); se a manifestação não existe, o consumidor registra erro e não publica |
| `denuncia-aceita` | **consome** | `DenunciaAceita` | `RemoverBloqueioExterno` com justificativa "Denúncia aceita pela COACI (…)" e remoção dos objetos do prefixo `{DenunciaId}/` |
| `denuncia-recusada` | **consome** | `DenunciaRecusada` | `RemoverBloqueioExterno` com o `MotivoRecusa` e remoção dos objetos do prefixo `{DenunciaId}/` |
- ✅ Regra de disparo: `JaTramitouDaCoaciParaOuvidoria` conta os trâmites da manifestação com **o mesmo destino** e origem do tipo COACI; mais de 1 impede novo evento (o filtro por destino foi acrescentado no commit `7cd80da`).
- ✅ Configuração do consumo: `RabbitMqPubSubSettings.ConsumerSettings` (`MaxProcessingAttempts`, `PrefetchCount`); health check `RabbitMQ` (estado *Degraded*).
- ✅ Os contratos (`DenunciaCriada`, `DenunciaRegistrada`, `DenunciaAceita`, `DenunciaRecusada`) ficam em `OuvDF.ServicoOuvidoria/Domain/Contracts`; os três consumidores, em `OuvDF.IntegrationServices/Consumers`, registrados em `Startup.ConfigurePubSub`.
- 🔶 Contraparte (SCI): ver [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|SCI → eventos do Participa-DF]]; o payload esperado pelo SCI não foi conferido contra o contrato atual (o histórico do git tem um revert do ajuste de payload de arquivos, `2be9deb`).
- ✅ Também há publicação interna de `ExclusaoContaUsuarioSolicitada` (`IPublisher`) ao solicitar exclusão de conta; 🔶 é notificação em processo (MediatR), não mensageria externa.

### 7. Serviços de localização (proxy)
- ✅ `ServicosExternosController` (classe `[AllowAnonymous]`) devolve JSON de serviços externos de **geocodificação/endereço**: `localidade/pesquisa/{chave}` e `localidade/posicao?url=` (host fixo mais um caminho vindo do chamador), `siturb?url=` e `ra?url=` (**a URL inteira vem do chamador**). Usa `WebClient.DownloadString` e, em qualquer exceção, devolve `200` vazio.
- ✅ `ApiMetroController`: `metro/classificacao`, `metro/assunto` (lista fixa de ids de assunto no código), `metro/ra` (🔶 executa `ConsultarManifestacaoResumidaPorId`, nome não corresponde), `metro/manifestacao/cidadao` (autenticado). Consumidor "metro" ❓ (aplicativo ou parceiro).

### 8. API de integração (entrada)
- ✅ `v1/manifestacao` (registrar, consultar por id, por manifestante) e `v1/usuario/pessoa-fisica` (consultar por CPF, gravar cidadão) exigem o papel `OperadorWS`. O `OperadorWS` é um usuário de sistema com perfil, unidade e validade de 1 ano.

### 9. Observabilidade
- ✅ Logs: Serilog com Console e `Grafana-Loki` (rótulos `appName` e `environment`).
- ✅ New Relic: agente .NET instalado e ativado por variáveis do profiler no `Dockerfile`; pacotes de sinks New Relic, Discord e File referenciados em `OuvDF.Api.csproj` (🔶 uso por configuração não verificado).

### 10. Armazenamento de objetos (S3 / MinIO)
- ✅ `OuvDF.S3.Client` (`IS3Client`/`S3Client`, `AddS3Client` em `Startup`): cliente `Minio` sobre `HttpClient` nomeado com resiliência (retry e circuit breaker de `ResilienceSettings`) e `HttpLoggingHandler`. Operações: `UploadAsync`, `ExistsAsync` (considera existente só se o tamanho for > 0), `DeleteAsync`, `DeleteByPrefixAsync` (lista recursivamente e remove um a um), `GetObjectKey` e `GetReference` (`bucket/chave`).
- ✅ Configuração `S3ClientSettings`: `Uri`, `AccessKey`, `SecretKey`, `BucketName`, `ObjectPrefix`, `Timeout`, `UserAgent`, retry e circuit breaker, `FallbackMessage`. As chaves de acesso vêm de Swarm Secrets (`S3ClientSettings__AccessKey` e `__SecretKey`) nas três regiões. Valores omitidos.
- ✅ Ciclo de vida do objeto (chave `{prefixo}/{DenunciaId}/…`): `ExportarDadosDenunciaHandler` gera o PDF do relatório (comando `ExportarManifestacaoOperadorPDF`, visão `ManifestacaoDetalhadaOperador`, nome `{protocolo}.pdf`) e envia os anexos **ativos** (`{anexoId}-{nome}`, lidos do diretório de arquivos da manifestação); se o objeto já existe, reutiliza a referência (idempotência). Os consumidores de `denuncia-aceita` e `denuncia-recusada` apagam tudo do prefixo.
- ✅ Anexo ausente no disco gera `InvalidOperationException` e interrompe a preparação (nada é publicado).
- 🔶 Provedor provável: o `MinIO-CGDF` (só por mensagens de commit; o endereço não foi lido). Entra no Mapa como hipótese.

## Falhas e dependências
| Integração | Se falhar | Efeito observado |
|---|---|---|
| Iza | fallback 200 com valores padrão | registro continua; denúncia não detectada (`false`), classificação 999, unidade `01005` |
| MailService | retry, circuito aberto → 400 | e-mails perdidos silenciosamente na maioria dos handlers (só alguns chamam `EnsureSuccessStatusCode`) |
| PeoplesCheck | circuito aberto → 400 com mensagem | cadastro/validação falha ao cidadão |
| SEI | exceção do SDK | vínculo não criado (tratamento de erro no workflow não lido) |
| Serviço de PDF | notificação de erro | geração de PDF falha |
| RabbitMQ | health *Degraded* | eventos de denúncia não trafegam |
| S3 / MinIO | retry e circuito (mensagem de fallback configurada); exceção no consumidor | `denuncia-registrada` não é publicado; ou aceite/recusa já aplicou o desbloqueio e a limpeza falha depois |
| Geocodificação | `200` vazio | mapa sem resultados |

## Inferências e limitações
- 🔴 **Relato do cidadão enviado a um serviço externo (Iza) sem consentimento visível** e em quatro chamadas por registro; a natureza do Iza (institucional ou terceiro) é ❓. Rever com o time (LGPD).
- 🔴 **TLS desligado no PeoplesCheck** e, em intenção, também no Iza e MailService (`ConfigureServerCertificateCustomValidationCallbackHandler` e `ConfigureDefaultPrimaryHttpMessageHandler` criam o handler, mas **não o atribuem** ao cliente; o resultado é validação normal nesses dois, ao contrário do PeoplesCheck).
- 🔴 **`servicos/siturb?url=` e `servicos/ra?url=` são anônimos e fazem uma requisição ao endereço informado pelo chamador** (`WebClient.DownloadString(url)`): possível SSRF (requisições a recursos internos). `localidade/posicao?url=` concatena o parâmetro ao host fixo (injeção de caminho).
- 🔶 O fallback do Iza esconde indisponibilidade: denúncias passam como não denúncia sem aviso.
- 🔶 `Iza` usa `HttpClient.Send` (síncrono) dentro de métodos `async`.
- 🔶 `PeoplesCheck`/`MailService` repetem a configuração de resiliência (código duplicado entre os dois).
- 🔶 `unidade 01005` e `01007` são códigos de unidade fixos no código; dependem de dados do banco.
- ❓ Contratos de resposta do PeoplesCheck, do MailService (`/mail/send`) e do SEI. 🔶 O provedor dos eventos `denuncia-aceita/recusada` é provavelmente o `SCI` (ver Mapa); semântica de retry/DLQ do SDK de PubSub não lida.
- 🔶 (2026-10-23) Em `DenunciaAceitaConsumer`/`DenunciaRecusadaConsumer` o desbloqueio ocorre **antes** da limpeza do bucket e sem tratamento de erro: falha no S3 deixa os arquivos (com dados do cidadão) no armazenamento temporário. Ver [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Débitos técnicos]].
- ❓ Quem consome a API `v1` e o serviço "metro".

## Relacionamentos
- Provedor Iza (sistema documentado em 2026-10-22): [[01-Sistemas/Iza/Api/07-Integracoes/Iza-Api-Integracoes|Iza → lado provedor]]
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Atribuicao-e-Bloqueio-Externo|Atribuicao-e-Bloqueio-Externo]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Fluxo-Registro-de-Manifestacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Confirmar com o time: natureza do Iza, consentimento do cidadão, quem é o sistema correcional e os consumidores da API `v1` e "metro".
- Lote 8: registrar como débitos o TLS desligado, o SSRF potencial, o fallback silencioso e o duplicado de resiliência. (✅ feito no lote 8)
- Atualização 2026-10-23: confirmar o provedor do S3, a política de expiração do bucket e o payload que o SCI espera; ler o SDK de PubSub.

## Histórico
### 2026-10-23: substituído o quadro de mensageria do commit `4901ad5`
- Regra anterior (commit `4901ad5`): `denuncia-registrada` era publicado **direto** por `ManifestacaoTramitadaEventHandler` (sem arquivos; campos `DenunciaId`, unidades, protocolo, `Identificada`), só na primeira tramitação COACI→ouvidoria; `denuncia-aceita`/`denuncia-recusada` apenas executavam `RemoverBloqueioExterno`; o contrato ficava em `OuvDF.IntegrationServices`. Não havia armazenamento de objetos.
- Pendência resolvida em 2026-10-23 (`820666c`): `DenunciaRecusadaConsumer` foi lido (faz `RemoverBloqueioExterno` com o motivo e limpa o bucket).
