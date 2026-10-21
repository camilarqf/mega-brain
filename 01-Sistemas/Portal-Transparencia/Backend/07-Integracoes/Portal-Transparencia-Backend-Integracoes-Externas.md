---
type: integration
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
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
---
# Integrações externas do backend

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Índice geral: [[Mapa-de-Integracoes|Mapa de integrações]]

> Endereços, chaves, contas e senhas **não** são registrados; só nomes de configuração.

## Objetivo
Registrar as comunicações do `portal-transparencia-backend` com outros sistemas e serviços (nota canônica; consumidor = `Portal-Transparencia`).

## Evidências
Leitura de `SendMailService`/`SendMailController`/`externalServices`, `PortalAnalyticsController`/`PortalAnalyticsService`/`GoogleAnalyticsConstantes`, `MascaramentoAMQService`, `IntegracaoSistemasController`, dos `application-*.properties` e do `pom.xml`.

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Portal-Transparencia` | `MailService` (🔶) | HTTP POST JSON (OkHttp) | `EmailRequest` (`from`, `to[]`, `subject`, `content`) | saída |
| `Portal-Transparencia` | `Google-Analytics-API` | HTTPS, Google Analytics Core Reporting API v3, conta de serviço (`.p12`) | métricas `ga:*` dos últimos 7 dias | saída |
| `Portal-Transparencia` | `RabbitMQ` | AMQP; exchange fanout `medida-protetiva-topic` | JSON com `expirePortal` | entrada (consumo) |
| consumidores não identificados | `Portal-Transparencia` | HTTP GET JSON, `/integracao/*` | 8 rotas | entrada (o backend é provedor) |

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
- ✅ O backend consome mensagens de uma fila anônima ligada à exchange fanout `medida-protetiva-topic`; ver [[01-Sistemas/Portal-Transparencia/Backend/04-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Fluxo]]. Chaves: `spring.rabbitmq.host/port/username/password/virtual-host` (virtual hosts `development`, `homolog`, `prod`).

### 4. API para outros sistemas (backend como provedor)
- ✅ `/integracao/*` (8 rotas GET): `funcao-servidor`, `verificar-sutcs`, `consultar-servidor`, `nome-servidor`, `consultar-servidor-ativo`, `pesquisar-servidor` (por CPF, matrícula, órgão ou nome), `nota-empenho/{gestão}/{unidade}/{número}` e `listar-nl-ob/{ug}/{gestão}/{empenho}`. Sem autenticação além do cabeçalho `x-client-id`.
- ✅ Os modelos `ServidorSciIntegracao`, `NotaEmpenhoIntegracao` e `OrdemBancariaIntegracao` e o método `recuperarServidorAtivoSci` indicam o uso por sistemas externos.

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
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações do PARTICIPA-DF (MailService)]]

## Pendências e próximo passo
- Confirmar o provedor de e-mail, a vigência dos endpoints de Analytics e os consumidores de `/integracao/*`.
