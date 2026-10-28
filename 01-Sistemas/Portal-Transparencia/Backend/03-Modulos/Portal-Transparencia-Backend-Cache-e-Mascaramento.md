---
type: module
aliases:
  - "Cache e mascaramento de dados protegidos"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
tags:
  - dados-pessoais
sources:
  - src/main/java/br/gov/df/transparencia/aop/MascaramentoAspect.java
  - src/main/java/br/gov/df/transparencia/annotations/Mascaravel.java
  - src/main/java/br/gov/df/transparencia/annotations/Mascarado.java
  - src/main/java/br/gov/df/transparencia/servico/mascaramento/MascaramentoService.java
  - src/main/java/br/gov/df/transparencia/servico/mascaramento/MascaramentoAMQService.java
  - src/main/java/br/gov/df/transparencia/modelo/mascaramento
  - src/main/java/br/gov/df/transparencia/cache/CacheConfig.java
  - src/main/java/br/gov/df/transparencia/servico/comum/CacheControlService.java
  - src/main/java/br/gov/df/transparencia/api/comum/CacheControlController.java
  - src/main/resources/sql/mascaramento
---
# Cache e mascaramento de dados protegidos

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Fluxo: [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Invalidacao-de-Cache-de-Mascarados]]

## Objetivo
Documentar como o backend **oculta registros de pessoas com medida protetiva** nas consultas e como os caches em memória são mantidos e invalidados.

## Evidências
Leitura de `MascaramentoAspect`, `MascaramentoService`, `MascaramentoAMQService`, `ServidorPorOrgaoLotacaoHandler`, enums `ConsultaMascarada` e `CampoMascarado`, `CacheConfig`, `CacheControlService/Controller`, `sql/mascaramento/*` e do levantamento de `@Mascaravel`/`@Cacheable`.

## Informações confirmadas
### Mascaramento
- ✅ Fonte dos valores a proteger: `[Servidor].[TB_MEDIDA_PROTETIVA]` (colunas `TX_CONSULTA`, `TX_COLUNA`, `TX_IDENTIFICADOR`), lida por `MascaramentoService.consultarDadosMascarados()` e agrupada por `consulta + campo` → conjunto de valores (em maiúsculas, sem espaços nas pontas).
- ✅ Marcação: métodos de **serviço** anotados `@Mascaravel(consulta = ConsultaMascarada.X)` (pointcut: `within(...servico..*)` e `@annotation(Mascaravel)`) e campos do modelo anotados `@Mascarado(campo = CampoMascarado.Y)`.
- ✅ `ConsultaMascarada` (10): `DESPESA` (campos `CREDOR`, `CD_CREDOR`), `REMUNERACAO` (`NOME`, `MATRICULA`, `CPF`), `SERVIDORES_POR_ORGAO` (`NOME`, `MATRICULA`, `LOTACAO`, `CPF`), `CADASTRO_EXPULSOES` (`NOME`, `MATRICULA`), `CONTRATOS` (`NOME`), `CONVENIOS_RECEITA` e `CONVENIOS_DESPESA` (`GESTOR`), `ENTIDADES_BENEFICIADAS` (`DIRIGENTE`), `CONSELHOS` e `CONSELHEIROS` (`NOME`).
- ✅ **Efeito atual (regra)**: depois de executar o método, o `@Around` do `MascaramentoAspect` **remove da resposta** os registros em que algum campo `@Mascarado` tenha valor presente no conjunto da respectiva consulta+campo.
  - `List`: devolve só os aceitos.
  - `Page`: devolve a página sem os rejeitados; se a página for a última e curta, **subtrai** os rejeitados do total de elementos e, em `CustomPage`, subtrai dos campos `BigDecimal` do totalizador; se o total chegar a 0, o totalizador vira `{"_": ""}`.
  - `EntityConsumer` (exportação em fluxo): embrulha o consumidor para pular os rejeitados.
  - Objeto único: devolve `null` se for mascarável.
- ✅ Existe um segundo comportamento (substituir o valor por `*` do mesmo comprimento, `mascararObjeto`/`mascararValor`), mas o `@AfterReturning` que o aplicava está **comentado**; hoje o aspecto só filtra. O `ServidorPorOrgaoLotacaoHandler` (consulta `SERVIDORES_POR_ORGAO`, campo `LOTACAO`) decide mascaramento da lotação com base em `MATRICULA` ou `NOME` mascaráveis, mas só influencia `hasAnyValorMascaravel` via `isMascaravel`.
- ✅ Pontos de uso: 30 métodos `@Mascaravel` em `ConvenioService` (3), `DespesaService` (12), `DiariasPassagensService` (1), `EmendasParlamentaresService` (3), `LicitacoesContratosService` (1), `ConselheiroService` (1), `PrestandoContasService` (1), `ExpulsaoService` (1), `RemuneracaoRelatorioService` (1), `RemuneracaoService` (4) e `ServidorService` (2).

### Cache
- ✅ `@EnableCaching` com `GuavaCacheManager` (cache **local, em memória, por instância**):
| Cache | Gerenciador | Política | Uso |
|---|---|---|---|
| `cacheMascarados` | `cacheManagerMascarados` | expira 3 min após escrita | `MascaramentoService.consultarDadosMascarados()` |
| `cacheRemuneracao` | `cacheManagerRemuneracao` | máx. 100 entradas, 1 dia | `JdbcUtil.executarComTotalizadorRemuneracao` (pesquisa de remuneração; a chave inclui a data da última carga, ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Servidores-e-Remuneracao|Servidores e Remuneração]]) |
| `cacheDespesaFiltros` | `cacheManagerDespesaFiltros` | máx. 200 entradas, 1 dia | 3 métodos de filtros em `DespesaService`, chave `método:exercicio` |
- ✅ Invalidação manual por HTTP, sem autenticação: `GET /cache-expire/valores-mascarados` (limpa `cacheMascarados` **e** `cacheRemuneracao`), `GET /cache-expire/remuneracao` e `GET /cache-expire/despesa-filtros`; resposta `CacheExpireInfo` (data e lista de caches).
- ✅ Invalidação por evento RabbitMQ: ver [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Fluxo]].

## Inferências e limitações
- 🔶 Por ser cache por instância, em ambiente com várias réplicas cada uma mantém seu cache; a mensagem fanout alcança todas, mas o `GET /cache-expire` atinge uma só.
- 🔶 Como o `@Around` age só em métodos de **serviço** chamados pelo proxy, chamadas internas na mesma classe não seriam interceptadas (comportamento padrão do AOP do Spring; não verificado caso a caso).
- 🔶 "Medida protetiva" é o nome da tabela e da exchange (`medida-protetiva-topic`); o motivo legal/negócio do ocultamento é interpretação dos nomes, sem documento de requisito.
- ❓ Quem cadastra os valores em `TB_MEDIDA_PROTETIVA` e quem publica a mensagem de expiração (outro sistema) não são identificáveis neste repositório.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]]

## Pendências e próximo passo
- Confirmar com o time quem alimenta `TB_MEDIDA_PROTETIVA` e publica `expirePortal`; confirmar se o filtro (remover linhas) é o comportamento desejado e não o de substituir por `*`.
