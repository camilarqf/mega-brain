---
type: module
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
tags:
  - portal-transparencia
  - backend
  - modulo
  - servidores
  - remuneracao
sources:
  - src/main/java/br/gov/df/transparencia/api/servidor
  - src/main/java/br/gov/df/transparencia/servico/servidor
  - src/main/java/br/gov/df/transparencia/modelo/Servidor.java
  - src/main/java/br/gov/df/transparencia/modelo/Remuneracao.java
  - src/main/java/br/gov/df/transparencia/modelo/servidor
  - src/main/java/br/gov/df/transparencia/modelo/expulsao
  - src/main/java/br/gov/df/transparencia/repositorio/expulsao
  - src/main/java/br/gov/df/transparencia/util/JdbcUtil.java
  - src/main/resources/sql/servidor
  - src/main/resources/sql/remuneracao
  - src/main/resources/sql/expulsao
---
# Módulo Servidores e Remuneração

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seção Servidor e remuneração)

## Objetivo
Documentar as consultas de servidores (cadastro por órgão, cargos, quadros, perfil), a remuneração (consulta, extrato anual e rubricas), expulsões e militares cedidos, além da API de integração por CPF.

## Evidências
Leitura de `RemuneracaoService` (linhas 30 a 212), `JdbcUtil.executarComTotalizadorRemuneracao`, `selectDataUltimaAtualizacaoCarga.sql`, lista de métodos de todos os serviços do pacote e análise de tabelas de 72 arquivos SQL (`servidor` 52, `remuneracao` 16, `expulsao` 4). Corpo de `ServidorService` e dos `.vm` não lido.

## Informações confirmadas
| Controller | Rotas | Serviço |
|---|---|---|
| `ServidorController` (`/servidor`) | 32 | `ServidorService` |
| `ServidorGraficoController` (`/servidor/grafico`) | 12 | `ServidorGraficoService` (regime, situação, ativo, aposentado, pensão, outros, status, carreira, sexo, escolaridade × sexo, idade) |
| `ServidorRelatorioController` | 1 | `ServidorRelatorioService` (servidores por órgão) |
| `RemuneracaoController` (`/remuneracao`) | 13 | `RemuneracaoService` |
| `RemuneracaoRelatorioController` | 4 | `RemuneracaoRelatorioService` (detalhamento, lista, extrato anual, rubrica) |
| `ExpulsaoController` / `ExpulsaoRelatorioController` | 5 / 1 | `ExpulsaoService` / `ExpulsaoRelatorioService` |
| `MilitaresCedidosController` / `...RelatorioController` | 4 / 1 | `MilitaresCedidosService` / `MilitaresCedidosRelatorioService` |
| `IntegracaoSistemasController` (`/integracao`, parte servidor) | 6 de 8 | `ServidorService` |

### Dados
- ✅ Tabelas: `Servidor.Principal` (32 referências), `Remuneracao.Principal` (16), `Remuneracao.Principal_Detalhamento`, `Remuneracao.Orgao/Cargo/Funcao/Situacao_Funcional`, `Servidor.Relatorio` e `Servidor.CategoriaRelatorio` (catálogo de documentos; ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Orçamento e documentos]]), `Servidor.Relatorio_Cargo_Funcao`, `Servidor.Relatorio_Cargo_Efetivo`, `Expulsao.Principal/Orgao/Punicao` e, para militares cedidos, `militaresCedidos.TF_REMUNERACAO`, `TD_ORGAO`, `TD_MILITAR`, `TD_QUADRO`, `TD_POSTO_GRADUACAO`.
- ✅ Modelo: `Servidor`, `ServidorRelatorio`, `Remuneracao`, `Rubrica`, `CargoEfetivo`, `CargoFuncao`, `Expulsao` (entidade JPA `Expulsao.Principal`, com repositório e `ExpulsaoSpecs`), `MilitaresCedidos`; enums `StatusServidorEnum`, `SituacaoFuncionalServidorEnum`, `SituacaoFuncionalDescServidorEnum`.

### Regras verificadas no código
- ✅ **Ano padrão**: na pesquisa de remuneração, sem `anoExercicio` o filtro usa o **ano corrente** (`LocalDate.now().getYear()`), mesmo que ainda não haja carga do ano.
- ✅ **Filtros** de remuneração: ano, mês, nome (com aspas simples duplicadas), órgãos por **nome** (convertidos em códigos por `selecionarIdsOrgaos`), cargos, funções e situações funcionais (listas viram texto separado por vírgula) e **CPF** (recebido no parâmetro `cm` em Base64 e decodificado).
- ✅ **Cache por versão de carga**: a pesquisa usa `JdbcUtil.executarComTotalizadorRemuneracao`, `@Cacheable` no cache `cacheRemuneracao` (1 dia, 100 entradas). Os parâmetros incluem `cacheVersion` = data da última carga (`Carga.Controle`, schema `remuneracao`, últimos `con_status` em `atualizado`, `realizado`, `sem alter.` ou `sucesso`); como a chave padrão contém o mapa de parâmetros, uma nova carga muda a chave e invalida na prática o cache. Se a data não puder ser lida, o campo é omitido (aviso em log).
- ✅ **Mascaramento** (`REMUNERACAO`: nome, matrícula, CPF): `pesquisar`, `pesquisarConsumer`, `listarExtratoAnual`, `listarRubricaPorServidor` e `RemuneracaoRelatorioService.consultarRecumeracaoPorId`; `SERVIDORES_POR_ORGAO` em `ServidorService` (2); `CADASTRO_EXPULSOES` em `ExpulsaoService`. Ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]].
- ✅ **API de integração** (por CPF, matrícula, órgão ou nome): `verificarFuncaoServidor`, `verificarSutcs`, `listaServidoresRetornados`, `recuperarNomeServidor`, `recuperarServidorAtivoSci`, `pesquisarServidorPorNome` → `/integracao/*` ([[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]]).
- ✅ Dados de apoio: quadros de servidores, tabelas de remuneração, cargos comissionados e efetivos, carreiras, símbolos, arquivos e PDF de pendências (`getPendenciasPdfUrl` via `Sql.selectUrlPendencias`).

## Inferências e limitações
- ✅ O CPF entra como filtro em Base64 (codificação, **não** proteção). A resposta traz nome, matrícula, cargo, órgão e o detalhamento completo da remuneração, e `cpfServidor` (🔶 provavelmente mascarado); o CPF cru (`cpfComparacao`) não é serializado. Ver [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]].
- 🔶 `relatorioRemuneracao` é `synchronized` (uma exportação por vez).
- ❓ "SUTCS" (`verificar-sutcs`) e "pendências" não têm explicação no código.
- ❓ Cálculos e filtros fixos nos `.vm` (por exemplo, o que é "ativo", "aposentado", "pensão") não foram lidos.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]] (campos pessoais por rota)
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados|Apoio-e-Atualizacao-de-Dados]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]] · [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Campos pessoais por rota já levantados em [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]; falta ler `ServidorService` e os cálculos dos `.vm` de `servidor/` e `remuneracao/`.
