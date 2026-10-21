---
type: analysis-log
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: pendente
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
tags:
  - portal-transparencia
  - pendencias
---

# Pendências

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Registro-de-Analise|Registro de análise]]

## Perguntas ao time
| # | Pergunta | Origem |
|---|---|---|
| 1 | Qual é o repositório do frontend (e de outros componentes, como o ETL das tabelas de carga) do Portal da Transparência? | Lote 0 |
| 2 | A ausência de autenticação é intencional (portal público)? Há API gateway, WAF ou rate limit na frente que proteja `/cache-expire/*`, `/integracao/*`, `/send-email` e `/download`? | Lote 1 |
| 3 | As credenciais versionadas (`persistence.xml`, constantes do Google Analytics, RabbitMQ dos `application-*.properties`) e o `.p12` já foram rotacionados/retirados? Usuário e senha do banco chegam ao container por qual secret? | Lote 1 |
| 4 | Quem aplica os changelogs Liquibase (`changelog-master.xml`) e qual processo carrega os schemas `Carga`, `Despesa`, `Servidor` etc.? | Lote 3 |
| 5 | Quem alimenta `[Servidor].[TB_MEDIDA_PROTETIVA]` e publica `expirePortal` na exchange `medida-protetiva-topic`? Filtrar (remover) as linhas é o comportamento desejado? | Lote 4 |
| 6 | O provedor de `email.service.url` é o mesmo `MailService` do PARTICIPA-DF? | Lote 5 |
| 7 | Os endpoints `/analytics/*` (Core Reporting API v3, Universal Analytics) ainda funcionam? | Lote 5 |
| 8 | Quem consome `/integracao/*` (o `ServidorSciIntegracao` sugere o SCI)? | Lote 5 |
| 9 | O agente New Relic é ativado em algum ambiente (a imagem não usa `-javaagent`)? | Lote 5 |
| 10 | Os 5 mapeamentos `@RequestMapping` sem verbo devem aceitar só `GET`? Para que serve `src/main/resources/data-h2.sql`/`schema-h2.sql`? | Lote 2 e 3 |
| 11 | `FormularioContatoController` (`POST /contato/registro`) está comentado; o formulário de contato foi desativado de propósito? E o controller antigo de pesquisa e a `EnqueteService` (esqueleto)? | Lote 7 |
| 12 | Os ids duplicados das categorias de `Servidor.Relatorio` (ex.: 19, 20, 8) são intencionais? Quem carrega esse catálogo? | Lote 7 |
| 13 | Significado de OCA, QDD, Sisgepat, SUTCS e Sucor para o glossário do sistema. | Lote 7 |
| 14 | `[NR-CPF]` de `Servidor.Principal` guarda o CPF completo? `cpf_formatado` (remuneração) e `NR_CPF` (programas sociais) estão mascarados/truncados? O que `FN_MASCARA_NR_CPF` faz com CNPJ? | Lote 8 |
| 15 | `/integracao/*` precisa devolver CPF e dados de servidores sem autenticação? Quem usa? | Lote 8 |
| 16 | Qual o privilégio do usuário de banco da aplicação (somente leitura?) e há WAF na frente, para dimensionar o impacto da injeção de SQL? | Lote 8 |
| 17 | Qual a semântica de `NR_NE_ORIGINAL = ''`, do evento contábil `400091` e das colunas de restos a pagar (processados × não processados)? | Lote 8 |
| 18 | Qual é o sistema `gerenciador` que consome `/storage/health` e `/storage/url` (informado pelo usuário em 2026-10-21, sem evidência no código)? Qual o ID e o repositório dele? | Atualização `e98fcc38` |
| 19 | O bucket do MinIO é de leitura pública? É intencional `/storage/url` devolver o host interno em `prod`? Quem grava os arquivos no bucket? | Atualização `e98fcc38` |
| 20 | Os perfis `dev` e `test` recebem `storage.url` e `storage.bucket` por variável de ambiente? Sem elas o contexto pode falhar ao subir. A dependência `io.minio` e `storage.endpoint` serão usadas ou removidas? | Atualização `e98fcc38` |

## Lacunas de cobertura (a documentar)
- Leitura dirigida dos `.vm` e dos corpos de serviço de cada módulo (cálculos, filtros fixos e campos expostos); módulos documentados no Lote 7 em nível de estrutura e regras lidas.
- Teste dinâmico (em ambiente de teste e com autorização) da injeção de SQL e de `/download/arquivos/{nome}`; revisão manual de 126 referências SQL não resolvidas; `.vm` de despesa fora dos 7 principais (diárias e passagens, emendas, QDD, OCA).
- Contexto de negócio do sistema (objetivo oficial, atores, exigências legais): requer fonte além do código.

## Próximo passo
- Leitura dirigida na ordem descrita em [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Registro-de-Analise|Registro de análise]].
