---
type: integration
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
consumer: Portal-Transparencia
tags:
  - portal-transparencia
  - backend
  - integracoes
sources:
  - src/main/java/br/gov/df/transparencia/servico/comum/SendMailService.java
  - src/main/java/br/gov/df/transparencia/api/comum/SendMailController.java
  - src/main/java/br/gov/df/transparencia/externalServices
  - src/main/java/br/gov/df/transparencia/api/comum/PortalAnalyticsController.java
  - src/main/java/br/gov/df/transparencia/api/comum/PortalAnalyticsService.java
  - src/main/java/br/gov/df/transparencia/api/comum/GoogleAnalyticsConstantes.java
  - src/main/java/br/gov/df/transparencia/servico/mascaramento/MascaramentoAMQService.java
  - src/main/java/br/gov/df/transparencia/api/comum/IntegracaoSistemasController.java
  - src/main/resources/application-prod.properties
  - pom.xml
  - src/main/java/br/gov/df/transparencia/api/comum/StorageController.java
  - src/main/java/br/gov/df/transparencia/servico/comum/storage
  - src/main/resources/application-hom.properties
---
# Integrações externas do backend

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Índice geral: [[Mapa-de-Integracoes|Mapa de integrações]]

> Endereços, chaves, contas e senhas **não** são registrados; só nomes de configuração.

## Objetivo
Registrar as comunicações do `portal-transparencia-backend` com outros sistemas e serviços (nota canônica; consumidor = `Portal-Transparencia`).

## Evidências
Leitura de `StorageController`, `StorageService` e `StorageUrlService` (atualização para `e98fcc38`), `SendMailService`/`SendMailController`/`externalServices`, `PortalAnalyticsController`/`PortalAnalyticsService`/`GoogleAnalyticsConstantes`, `MascaramentoAMQService`, `IntegracaoSistemasController`, dos `application-*.properties` e do `pom.xml`.

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Portal-Transparencia` | `MailService` (🔶) | HTTP POST JSON (OkHttp) | `EmailRequest` (`from`, `to[]`, `subject`, `content`) | saída |
| `Portal-Transparencia` | `Google-Analytics-API` | HTTPS, Google Analytics Core Reporting API v3, conta de serviço (`.p12`) | métricas `ga:*` dos últimos 7 dias | saída |
| `Portal-Transparencia` | `RabbitMQ` | AMQP; exchange fanout `medida-protetiva-topic` | JSON com `expirePortal` | entrada (consumo) |
| consumidores não identificados | `Portal-Transparencia` | HTTP GET JSON, `/integracao/*` | 8 rotas | entrada (o backend é provedor) |
| `Portal-Transparencia` | `MinIO-CGDF` (🔶 instância não confirmada) | HTTP GET (`RestTemplate`), sem autenticação no código | `{storage.url}/minio/health/live` | saída |
| `gerenciador` (🔶 informado pelo usuário; sistema não identificado) | `Portal-Transparencia` | HTTP GET, `/storage/health` e `/storage/url` | 2 rotas | entrada (o backend é provedor) |

## Informações confirmadas
### 1. Envio de e-mail → serviço de e-mail
- ✅ `SendMailService.sendEmail` faz `POST` JSON para a URL da propriedade `email.service.url`, com dois cabeçalhos configuráveis (`security.api.key.header` + valor `security.api.key.value`, e `security.api.user.agent.header` + valor). Timeout padrão do OkHttp; sem retentativa.
- ✅ Chamado por `GET /send-email` (corpo `SendMailRequest`: `emailDestinatario`, `emailCidadao`, `assuntoMensagem`, `conteudoMensagem`), que mapeia `from = emailDestinatario` e `to = [emailCidadao]`.
- ✅ `SendMailRequest` valida os campos (`@Valid`) e traz valores padrão institucionais para `emailCidadao` e `emailDestinatario` (não reproduzidos). O mesmo `SendMailService` é usado pela pesquisa de satisfação quando a resposta é *Insatisfeito*/*Muito Insatisfeito* ([[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados|Apoio]]).
- ✅ Resultado: 2xx → `200` com mensagem de enviado; outro status → mesmo status com mensagem de erro; `IOException` → `500`. A mensagem de sucesso é registrada em nível `WARN`.
- ✅ Valores por ambiente: a URL em `dev` e `hom` termina em `/mail/send` e em `prod` em `/mail-service/mail/send` (hosts omitidos).

### 2. Google Analytics (Core Reporting API v3)
- ✅ `PortalAnalyticsService` autentica com **conta de serviço** (identificador em constante e chave privada de arquivo `.p12` copiado para `/home/PortalFiles/ChavePortal/`) e consulta os últimos 7 dias do perfil configurado: páginas populares (`pageviews`, `uniquePageviews`, `timeOnPage`, `bounces`, `entrances`, `exits`, até 15), usuários, visualizações, sessões e sessões por categoria de dispositivo.
- ✅ Expostos por `/analytics/*` (6 rotas GET em `PortalAnalyticsController`); cada chamada reinicializa o cliente e consulta o Google (sem cache).
- ✅ Defeito de código: `recuperarPaginasMaisPopulares` itera sempre 15 posições; com menos linhas lança `IndexOutOfBoundsException`, que o `ResourceExceptionHandler` converte em `204`.

### 3. RabbitMQ (entrada)
- ✅ O backend consome mensagens de uma fila anônima ligada à exchange fanout `medida-protetiva-topic`; ver [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Fluxo]]. Chaves: `spring.rabbitmq.host/port/username/password/virtual-host` (virtual hosts `development`, `homolog`, `prod`).

### 4. API para outros sistemas (backend como provedor)
- ✅ `/integracao/*` (8 rotas GET): `funcao-servidor`, `verificar-sutcs`, `consultar-servidor`, `nome-servidor`, `consultar-servidor-ativo`, `pesquisar-servidor` (por CPF, matrícula, órgão ou nome), `nota-empenho/{gestão}/{unidade}/{número}` e `listar-nl-ob/{ug}/{gestão}/{empenho}`. Sem autenticação além do cabeçalho `x-client-id`.
- ✅ Os modelos `ServidorSciIntegracao`, `NotaEmpenhoIntegracao` e `OrdemBancariaIntegracao` e o método `recuperarServidorAtivoSci` indicam o uso por sistemas externos.

### 4b. Storage de objetos (MinIO-CGDF), adicionado na `feat/servico-minio` (commits até `e98fcc38`)
- ✅ `GET /storage/health` (`StorageController` → `StorageService.health`): faz `GET` em `{storage.url}/minio/health/live` com `RestTemplate` e devolve `true` se o status for 2xx; qualquer exceção vira `false` e é impressa com `printStackTrace`. Sem timeout configurado.
- ✅ `GET /storage/url?arquivo=` (`StorageUrlService.gerarUrlPublica`): devolve a **string** `{storage.url}/{storage.bucket}/{arquivo}`. Não consulta o MinIO, não confere se o arquivo existe e não valida nem normaliza o nome.
- 🔶 Provedor: o serviço MinIO documentado no cofre é [[01-Sistemas/MinIO-CGDF/MinIO-CGDF-Index|MinIO-CGDF]] (`minio-infra`); o código só traz o endereço configurado, então é provável, mas não confirmado, que seja essa instância (pendência 19).
- ✅ Configuração: `storage.url` e `storage.bucket` em `hom` e `prod`; `storage.endpoint` (só em `hom`) não é lida. A biblioteca `io.minio:minio 8.5.7` está no `pom.xml` e não é usada. Ver [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]].
- ✅ Em `prod`, `storage.url` aponta para um host interno do cluster, e `/storage/url` o devolve ao chamador (⚠️ host omitido aqui).
- 🔶 **Consumidor:** o usuário informou, em 2026-10-21, que quem consome essas rotas é o **gerenciador**. Não há evidência no código deste repositório, e o sistema não está identificado no catálogo (pendência 18).
- 🔶 Fluxo provável (inferência): o gerenciador pede ao backend a URL pública de um arquivo e usa `health` para saber se o storage está no ar. O backend **não grava** arquivos no MinIO neste código; quem envia os objetos é ❓.
- ❓ Se o bucket é de leitura pública (a rota se chama "url pública") e se o `x-client-id` obrigatório é suficiente para o gerenciador (pendência 19).

### 5. Banco e observabilidade (não são integrações com outro sistema)
- ✅ SQL Server do próprio portal (ver [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]]); métricas Prometheus em `GET /prometheus` (modelo *pull*).
- ✅ O arquivo `newrelic/newrelic.yml` e o agente `newrelic.jar` estão no repositório, mas o `CMD` do `Dockerfile` (`java -jar`) **não** passa `-javaagent`: não há evidência de ativação na imagem (⚠️ `newrelic.yml` não foi lido por poder conter chave).

## Falhas e dependências
- E-mail: falha do serviço não é tratada com retentativa; depende de o `MailService` aceitar o remetente informado.
- Analytics: depende do arquivo `.p12` no caminho fixo, de rede de saída para o Google e de a API continuar existindo (ver inferências).
- RabbitMQ: `management.health.rabbit` desligado em `hom`/`prod`, e o `Healthcheck` sempre responde UP; queda do broker não é percebida pelo healthcheck.

## Inferências e limitações
- 🔶 O provedor de e-mail provavelmente é o mesmo `MailService` usado pelo `PARTICIPA-DF` (mesmo padrão de API com cabeçalhos de chave e de agente), mas **não há evidência** de que seja o mesmo serviço; o ID `MailService` foi usado como hipótese.
- 🔶 A Core Reporting API v3 pertence ao Universal Analytics, que o Google encerrou (coleta em 2023 e API depois). É provável que os 6 endpoints `/analytics/*` não retornem dados atuais; **não foi testado** e vem de conhecimento externo ao código.
- 🔶 O `ServidorSciIntegracao` sugere o sistema `SCI` como consumidor de `/integracao/*`, mas o backend do SCI documentado no cofre não tem essa chamada registrada; consumidor ❓.
- ❓ Publicador da mensagem `expirePortal` e instância do RabbitMQ (se é a mesma usada pelo `PARTICIPA-DF`/`SCI`) não identificados.

## Relacionamentos
- [[01-Sistemas/MinIO-CGDF/MinIO-CGDF-Index|MinIO-CGDF]] · [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações do PARTICIPA-DF (MailService)]]

## Pendências e próximo passo
- Storage: identificar o `gerenciador`, confirmar a visibilidade do bucket e como os arquivos chegam ao MinIO (pendências 18 e 19).
- Confirmar o provedor de e-mail, a vigência dos endpoints de Analytics e os consumidores de `/integracao/*`.
