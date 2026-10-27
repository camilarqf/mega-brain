---
type: security
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
  - seguranca
  - sql-injection
  - revisao
sources:
  - src/main/resources/sql
  - src/main/java/br/gov/df/transparencia/util/JdbcUtil.java
  - src/main/java/br/gov/df/transparencia/util/ArraysUtil.java
  - src/main/java/br/gov/df/transparencia/servico
  - src/main/java/br/gov/df/transparencia/api/despesa/DespesaController.java
  - src/main/java/br/gov/df/transparencia/api/orcamento/OrcamentoController.java
  - src/main/java/br/gov/df/transparencia/api/patrimonio/PatrimonioController.java
---
# Revisão de injeção de SQL (análise estática)

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

> Nenhuma exploração foi tentada e nenhum payload é registrado. A nota mostra **onde há risco** e **o que já protege**, para orientar a correção.

## Objetivo
Confirmar, por leitura estática de todos os templates SQL, se os parâmetros vindos da requisição chegam ao SQL sem proteção, e classificar o risco por área e por rota.

## Evidências
- Script de análise estática (não versionado) sobre `src/main/resources/sql` (547 arquivos, `.vm` e `.sql`) cruzado com os `map.put("chave", expressão)` dos serviços. Para cada referência `$variável` dentro do SQL, foi resolvido o tipo do valor de origem (campo de modelo ou variável do serviço) e classificado como seguro (numérico, data, booleano), texto bruto, lista de texto, sanitizado, interno ou não resolvido.
- Leitura direta de `JdbcUtil.orderBy`, `ArraysUtil`, `RemuneracaoService.escaparAspasSimples`, dos helpers `tratarStringRecebida`/`removerCaracteresEspeciais` e das 9 rotas POST.
- Busca por configuração de escape no Velocity: **não existe** (nenhum `event handler` em `resources` nem classe de configuração do `VelocityEngine`).

## Informações confirmadas
### Mecanismo
- ✅ `JdbcUtil` renderiza o template com `VelocityEngineUtils.mergeTemplateIntoString` e executa o texto resultante em `JdbcTemplate` **sem parâmetros vinculados**. Valores entram no SQL por substituição de texto (`'$nome'`, `like '%$nome%'`, `in ( $lista )`, `= $numero`).
- ✅ Os parâmetros chegam por *binding* do Spring MVC em beans de modelo (query string de `GET`) ou, em poucos casos, por `@RequestBody String`. Campos `String` e `List<String>` aceitam qualquer texto; campos `Integer`/`Long`/`Date` falham no *binding* com texto inválido (400) e são seguros neste aspecto.

### Números (commit `9434e58f`)
| Item | Quantidade |
|---|---|
| Arquivos de consulta com alguma referência `$variável` | 221 de 547 (os demais não interpolam ou usam parâmetros nomeados `:x` da classe gerada `Sql`) |
| Referências `$variável` no SQL | 1.422 |
| 🔴 Texto/lista de texto **bruto** da requisição no SQL | **860 referências em 103 arquivos** (212 nomes de variável distintos) |
| ↳ dentro de aspas (`'...$x...'`) | 608 |
| ↳ lista de texto montada por `ArraysUtil.asString` (cada item entre aspas, sem escape) em `IN (...)` | 186 |
| ↳ texto sem aspas (valor "numérico" que o campo Java declara como `String`) | 66 |
| 🟢 Origem numérica, de data ou booleana | 360 |
| ⚪ Variável interna (consulta já renderizada para contagem/totais) | 74 |
| 🟡 Origem não resolvida pela análise (a revisar à mão) | 126 |
| 🟢 Sanitizada (escape de aspas) | 1 (`RemuneracaoService`, filtro `nomeServidor`) |

### Distribuição por área (referências de risco / arquivos)
| Área | Risco | Arquivos |
|---|---|---|
| `despesa` | 544 | 27 |
| `prestando-contas` | 99 | 23 |
| `convenio` | 63 | 5 |
| `receita` | 38 | 6 |
| `servidor` | 36 | 10 |
| `licitacoes-contratos` | 20 | 4 |
| `remuneracao` | 18 | 7 |
| `patrimonio` | 17 | 9 |
| `orcamento` | 15 | 8 |
| `expulsao` | 6 | 1 |
| `comum` | 4 | 3 |

Variáveis mais frequentes: `nomeCategoriaEconomica`, `nome`, `nomeProgramaTrabalho`, `nomeCredor`, `nomeSubtitulo`, `codigoCredor`, `listaCodigoUnidadeGestora`, `numeroProcesso`, `nomeFonteRecurso`, `listaFonteRecurso`. Templates com mais referências de risco: `despesa/pesquisaAgrupada/listDespesaOrdemBancariaPorNotaEmpenho.vm` (62), `despesa/diariasPassagens/listDespesaOrdemBancariaPorNotaEmpenhoDiariasPassagens.vm` (48), `convenio/listDetalhamentoValorPagoEntidadeBeneficiada.vm` (44), `despesa/listDespesaConsultaDinamica.vm` e suas versões `_Count` e `_Total` (44 cada).

### O que protege hoje (e o que não protege)
- ✅ **Ordenação** (`sort=`): `JdbcUtil.orderBy` só aceita nomes de campos declarados na classe (`getDeclaredField`) e usa o nome da coluna anotada; é lista branca. Defeito: se **todas** as propriedades forem inválidas, o resultado é `order by ` vazio e o SQL falha (500).
- ✅ **`GROUP BY` da consulta dinâmica de despesa**: montado em Java a partir de nomes fixos conforme as colunas "visíveis"; o JSON `colunas` da requisição só liga e desliga blocos (`.visible`), não entra no SQL. Seguro quanto a injeção; `isVisible` lança `NullPointerException` se o campo `visible` faltar.
- ✅ **Consultas `.sql` com `:parametro`** executadas pela classe gerada `Sql` usam parâmetros vinculados (seguras). Atenção: alguns `.sql` também usam `$variável` (por exemplo `despesa/paineis-despesa/sqlTotalLiquidado.sql`) e entram na estatística acima.
- ❌ `tratarStringRecebida` só converte vazio em `null` (não escapa nada); `tratarStringMascaradaRecebida` só rejeita texto feito de `*`.
- ❌ `removerCaracteresEspeciais` remove apenas `.`, `-` e `/` (formatação de CPF/CNPJ); não remove aspas.
- ❌ `ArraysUtil.asString`/`asStringNotEmpty` colocam aspas simples em cada item sem escapar aspas internas.
- ❌ Decodificar Base64 (campos `cm`, `codigoCredorCodificado`) não valida o conteúdo decodificado.
- ❌ Não há filtro global, WAF no código, nem escape de referência no Velocity.

### Rotas POST (9) — classificação
| Rota | Entrada | Destino | Risco |
|---|---|---|---|
| `POST /orcamento/data-referencias` | corpo bruto (`String`) | `rel.CD_CATEGORIA in ( $codigos )` | 🔴 confirmado no código |
| `POST /prestando-contas/data-referencias` | corpo bruto | delega ao serviço de orçamento (mesmo template) | 🔴 confirmado |
| `POST /patrimonio/bens-moveis/unidades-gestoras` | corpo bruto | `AA_EXERCICIO in ( $anos )` | 🔴 confirmado |
| `POST /patrimonio/bens-moveis/gestoes` | corpo bruto | `CO_UG in ( $codigosUnidadeGestora )` | 🔴 confirmado |
| `POST /despesa/ordens-cancelamento` | parâmetro `numeroOrdemBancaria` (`String`) | `NR_OB='$NR_OB'` | 🔴 confirmado (os outros dois parâmetros são `int`) |
| `POST /despesa/diarias-passagens/subitemPorElemento` | corpo bruto | o template **não usa** a variável | 🟢 sem risco (parâmetro ignorado) |
| `POST /orcamento/categorias` e `POST /prestando-contas/categorias` | corpo (`String`) | `switch` com tipos fixos que gera ids a partir de um enum | 🟢 sem injeção; corpo vazio causa `NullPointerException` (500) |
| `POST /v2/pesquisa-satisfacao` | JSON | gravação por JPA (parametrizada) | 🟢 |

### Exemplos de padrão (sem valores)
- Consulta dinâmica de despesa: `credor.NM_CREDOR LIKE '%$nomeCredor%'`, `ne.CD_CREDOR = '$codigoCredor'`, `ug.NM_UG = '$nomeUnidadeGestora'`, `ne.CD_UG IN ($listaCodigoUnidadeGestora)`, `AND SUM(ne.VL_PAGO) = '$valorObFinal'` (cláusula `HAVING`).
- Beneficiários: `lower(NR_NIS) LIKE lower('%$nrNis%')`, `AND NR_CPF = '$cpf'`.
- Integração: `WHERE [NR-CPF] = '$cpfServidor'`, `WHERE NOME like '$nomeServidor%'`, `[CD-MATRICULA] like '%$matriculaServidor%'`.

## Inferências e limitações
- 🔶 **Alcance real depende de verificação dinâmica**: a análise é estática e heurística (tipos resolvidos pelo nome de variável declarado no serviço). Podem existir falsos positivos (por exemplo, um campo `String` que nunca recebe texto arbitrário por algum motivo que não vi) e falsos negativos (126 referências sem origem resolvida; origens montadas em métodos auxiliares).
- 🔶 O **impacto** vai além de leitura indevida: dependendo do usuário de banco da aplicação (privilégios não conhecidos ❓) e do driver (consultas em lote com `;` costumam ser aceitas no SQL Server), poderia haver escrita ou outras ações. Ligado também às credenciais versionadas ([[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]).
- 🔶 `Date` e números são seguros quanto a injeção, mas um valor inválido produz erro 400/500, não SQL malicioso.
- ❓ Se existe WAF ou gateway que filtre aspas e palavras-chave na frente da aplicação (pergunta aberta nas Pendências).

## Recomendações (não são fatos do código)
1. **Imediato**: confirmar o privilégio do usuário de banco da aplicação (somente leitura nos schemas consultados) e revisar se há WAF/rate limit na frente; corrigir primeiro as 5 rotas POST, que são triviais de acionar.
2. **Correção estrutural**: migrar os `.vm` para parâmetros vinculados (`:nome` com `NamedParameterJdbcTemplate`; listas com `IN (:lista)`), mantendo o Velocity só para blocos condicionais (`#if`) e nomes de coluna fixos. Começar pelas 27 consultas de `despesa`, que concentram 63% das referências de risco.
3. **Paliativo**: ativar escape de referência SQL no Velocity (o Velocity 1.x traz um *event handler* para isso; verificar compatibilidade com a versão do Spring Boot 1.3) e validar tipo/formato dos códigos (numéricos e listas) antes de montar a consulta. O escape de aspas não protege valores sem aspas; por isso validar números é obrigatório.
4. **Testes**: criar testes automatizados com entradas hostis (em banco de teste descartável) que garantam que cada filtro continua sendo tratado como dado; incluir uma regra de revisão que proíba `$variável` fora de `#if`/nomes fixos.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Despesa-Consultas-e-Calculos|Despesa: consultas e cálculos]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]] · [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]]

## Pendências e próximo passo
- Revisar à mão as 126 referências não resolvidas; validar em ambiente de teste (com autorização) que as 5 rotas POST e os filtros de texto mais usados realmente aceitam entrada hostil; acompanhar a correção.
