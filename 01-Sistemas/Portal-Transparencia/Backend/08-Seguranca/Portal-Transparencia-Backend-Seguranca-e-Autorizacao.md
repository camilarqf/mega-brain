---
type: security
aliases:
  - "Segurança e autorização"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
sources:
  - src/main/java/br/gov/df/transparencia/filtro/ClienteIdFilter.java
  - src/main/java/br/gov/df/transparencia/filtro/CorsFilter.java
  - src/main/java/br/gov/df/transparencia/filtro/UserInterceptorFilter.java
  - src/main/java/br/gov/df/transparencia/aop/MascaramentoAspect.java
  - src/main/java/br/gov/df/transparencia/api/comum/CacheControlController.java
  - src/main/java/br/gov/df/transparencia/api/comum/SendMailController.java
  - src/main/java/br/gov/df/transparencia/api/comum/DownloadController.java
  - src/main/java/br/gov/df/transparencia/api/comum/IntegracaoSistemasController.java
  - src/main/resources/application-prod.properties
  - pom.xml
  - src/main/java/br/gov/df/transparencia/api/comum/StorageController.java
  - src/main/java/br/gov/df/transparencia/servico/comum/storage
---
# Segurança e autorização

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

> Nenhum segredo, usuário, host ou chave é reproduzido aqui; só a existência e a localização do problema.

## Objetivo
Registrar como o backend controla acesso, o que protege dados pessoais e onde estão os controles (e as lacunas).

## Evidências
Leitura de `filtro/*`, `aop/MascaramentoAspect.java`, controllers listados em `sources`, `application-prod.properties` e `pom.xml` (ausência de Spring Security).

## Informações confirmadas
- ✅ **Não há autenticação nem autorização de usuário.** Não existe `spring-boot-starter-security` no `pom.xml`, e nenhum controller verifica identidade ou perfil. É coerente com um portal de consulta pública (🔶 intenção não confirmada com o time).
- ✅ `ClienteIdFilter` (`@Order(HIGHEST_PRECEDENCE + 1)`): exige o cabeçalho `x-client-id` **não vazio** em toda requisição, exceto `OPTIONS` e URIs terminadas em `/healthcheck` ou `/prometheus`; sem ele responde `400` com `{"message":"Header x-client-id obrigatório."}`. **O valor não é validado**, então não é credencial: serve só para identificar/exigir um cabeçalho do cliente.
- ✅ `CorsFilter` (`HIGHEST_PRECEDENCE`): `Access-Control-Allow-Origin: *`; métodos `POST, GET, PUT, OPTIONS, DELETE`; cabeçalhos permitidos incluem `x-client-id`; responde preflight (`OPTIONS`) sem encadear.
- ✅ `UserInterceptorFilter` (verificação do cabeçalho `X-BROWSER-VERSION` contra duas chaves fixas) está **inteiramente comentado**, com `TODO` de migrar para Spring Security com OAuth. Não é executado; as chaves ficam no histórico do repositório (⚠️ valores não reproduzidos).
- ✅ **Proteção de dados pessoais por filtragem**: o `MascaramentoAspect` (`@Around` em métodos de serviço `@Mascaravel`) **remove** dos resultados os registros cujos campos `@Mascarado` coincidam com valores cadastrados em `[Servidor].[TB_MEDIDA_PROTETIVA]`; para resultado único, devolve `null`. Detalhes em [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]].
- ✅ Endpoints operacionais sem proteção: `GET /cache-expire/{valores-mascarados|remuneracao|despesa-filtros}` (limpa caches), `GET /prometheus` e `GET /healthcheck` (os dois últimos isentos do `x-client-id`).
- ✅ `GET /send-email` (apesar do verbo, lê `@RequestBody` `SendMailRequest`): aciona o envio de e-mail pelo serviço externo, usando `emailDestinatario` como remetente (`from`) e `emailCidadao` como destinatário; ambos têm valor padrão institucional em `SendMailRequest`, mas a requisição pode sobrescrevê-los. Há validação (`@Valid`): e-mail bem formado, nome, assunto e conteúdo obrigatórios, conteúdo de 10 a 500 caracteres. Sem autenticação. Ver [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]].
- ✅ `GET /download/arquivos/{nome_arquivo:.+}` lê `/home/PortalFiles/Arquivos/<nome>` e devolve o conteúdo; imprime o caminho em `System.out`.
- ✅ `/integracao/*` (8 rotas GET) expõe dados de servidores (CPF → função, nome, servidor ativo, busca por nome) e de notas de empenho/ordens bancárias a outros sistemas, **sem autenticação**.
- ✅ `GET /storage/health` e `GET /storage/url?arquivo=` (novos, `feat/servico-minio`): sem autenticação além do `x-client-id`. `/storage/url` devolve `{storage.url}/{bucket}/{arquivo}` sem validar o nome do arquivo e, em `prod`, revela o **host interno** do MinIO ao chamador. Não lê nem grava arquivo; o risco de travessia de diretório não se aplica a esta rota, que só concatena texto. `/storage/health` faz uma chamada HTTP de saída ao MinIO a cada requisição, sem cache nem timeout.
- ✅ Credenciais e material sensível **versionados no repositório**: `META-INF/persistence.xml` (URL, usuário e senha do banco em texto), `api/comum/GoogleAnalyticsConstantes.java` (conta de serviço, perfil e senha do certificado), `resources/PortalGDF-*.p12` (certificado da conta de serviço do Google, copiado para a imagem pelo `Dockerfile`) e as chaves do `UserInterceptorFilter` comentado. Também há credenciais do RabbitMQ nos `application-<perfil>.properties` de `dev`, `hom` e `prod`.
- ✅ Segredos de ambiente (URL do datasource e chave de API do e-mail) entram por Docker Secrets (`inject-docker-secrets-entrypoint.sh`), prática adotada recentemente (commits `chore: configura Docker Swarm Secrets`).
- ✅ `hibernate.show_sql=true` no perfil `prod`.

## Inferências e limitações
- ✅ **Injeção de SQL confirmada por análise estática** (lote 8, ver [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]]): 860 referências de texto bruto da requisição em 103 arquivos SQL, e **5 rotas POST** com fluxo direto para o SQL: `POST /orcamento/data-referencias`, `POST /prestando-contas/data-referencias`, `POST /patrimonio/bens-moveis/unidades-gestoras`, `POST /patrimonio/bens-moveis/gestoes` e `POST /despesa/ordens-cancelamento` (parâmetro `numeroOrdemBancaria`). A exploração **não foi testada**.
- ✅ **Injeção de SQL (caso geral)**: os `.vm` de `resources/sql` interpolam parâmetros direto no texto do SQL (ex.: `like lower('%$nomeServidor%')`, `nr_cpf = '$cpf'`; cerca de 500 linhas de `.vm` têm `like ... $var` ou `= '$var'`). Só se encontrou uma função de escape de aspas (`escaparAspasSimples` em `RemuneracaoService`); o `cpf` é decodificado de Base64 sem escape nesse mesmo serviço. Não foi verificado, caso a caso, se cada parâmetro é validado antes. Não se tentou explorar nada.
- 🔶 `GET /download/arquivos/{nome:.+}` concatena o nome ao diretório; se o nome puder conter `..` depois da decodificação do Spring, haveria leitura fora do diretório. Não verificado.
- 🔶 `GET /send-email` sem autenticação pode servir de relé de e-mail com remetente e destinatário controlados pelo chamador (limitado pelas validações de formato e de tamanho do conteúdo), a depender do serviço de e-mail (não analisado).
- 🔶 Credenciais do banco e do RabbitMQ em repositório sugerem necessidade de rotação; o valor atual em uso não foi verificado.
- 🔶 A decisão de expor o host interno do storage em `/storage/url` pode ser intencional (o gerenciador precisa da URL); depende de o bucket ser público e de o host ser alcançável pelo cliente (pendência 19).
- ❓ Não se sabe se há WAF, API gateway ou rate limit na frente da aplicação (poderia mitigar CORS aberto e endpoints operacionais).

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] · [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]]

## Pendências e próximo passo
- Dados pessoais: ver [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]] (inclui `/integracao/*` devolvendo CPF).
- Confirmar com o time: a ausência de autenticação é intencional? Há gateway na frente? As credenciais versionadas já foram rotacionadas?
