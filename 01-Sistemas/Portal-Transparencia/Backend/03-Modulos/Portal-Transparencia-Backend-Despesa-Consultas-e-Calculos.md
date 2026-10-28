---
type: module
aliases:
  - "Despesa: consultas SQL e cálculos"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
sources:
  - src/main/resources/sql/despesa/listDespesaConsultaDinamica.vm
  - src/main/resources/sql/despesa/listDespesaConsultaDinamica_Total.vm
  - src/main/resources/sql/despesa/pesquisaAgrupada/listDespesaNotaEmpenho.vm
  - src/main/resources/sql/despesa/pesquisaAgrupada/listDespesaPorCredor.vm
  - src/main/resources/sql/despesa/pesquisaAgrupada/listObPorCredor.vm
  - src/main/resources/sql/despesa/pesquisaAgrupada/listDespesaOrdemBancariaPorNotaEmpenho.vm
  - src/main/resources/sql/despesa/listDespesaDetalhamento.vm
  - src/main/resources/sql/despesa/restosAPagar/listRestosAPagar.vm
  - src/main/java/br/gov/df/transparencia/servico/despesa/DespesaService.java
---
# Despesa: consultas SQL e cálculos

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Módulo: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]]

## Objetivo
Documentar o que os templates SQL mais importantes de despesa calculam: colunas de valor, filtros fixos, joins e regras por tipo de consulta. Complementa o módulo Despesa, que traz só a estrutura.

## Evidências
Leitura dos templates listados em `sources` com um extrator que separa o SQL **fixo** (fora de `#if`/`#foreach`) dos blocos **condicionais**; leitura do trecho do `DespesaService` que monta `groupBy`. Foram lidos 7 dos 149 arquivos de `resources/sql/despesa` (os de maior uso); os demais seguem o mesmo padrão e não foram revisados.

## Informações confirmadas
### Consulta dinâmica (`listDespesaConsultaDinamica.vm`, com `_Count` e `_Total`)
- ✅ Base: `Despesa.TF_NOTA_EMPENHO ne` (empenho), com `INNER JOIN` só das dimensões necessárias às colunas ou filtros escolhidos (UG, gestão, credor, esfera, tipo de licitação, programa de trabalho, função, subfunção, programa, projeto/ação, subtítulo, grupo, modalidade de aplicação, elemento, fonte de recurso, notas de lançamento e ordens bancárias).
- ✅ **Filtro fixo**: `ne.NR_NE_ORIGINAL = ''` (só empenhos originais, sem os de reforço/anulação vinculados a outro empenho).
- ✅ **Colunas de valor** (somas): `valorNeFinal = SUM(VL_EMPENHADO)`, `valorNlBruto = SUM(VL_LIQUIDADO)`, `valorObFinal = SUM(VL_PAGO)` (sempre incluída), e, se a coluna estiver visível, `valorPagoExercicio = SUM(VL_PAGO_EXERCICIO)`, `valorPagoRPNP = SUM(VL_PAGO_RPNP)`, `valorPagoRPP = SUM(VL_PAGO_RPP)` e `valorPagoRET = SUM(VL_PAGO_RET)`. A sigla RPP/RPNP indica restos a pagar processados e não processados (🔶 pelo nome).
- ✅ **Colunas dinâmicas**: o cliente envia `colunas` (JSON com `visible` por coluna); o SQL inclui só os campos visíveis e o `GROUP BY` é montado em Java com nomes fixos na mesma ordem (`criarGroupByConsultaDinamica`). O total (`_Total`) soma o resultado agrupado (`SELECT SUM(...) FROM (...) tmp`).
- ✅ **Flags com elemento de despesa fixo**: `ressarcimento` → `CD_ELEMENTO_DESPESA = 96`; `consultaExerciciosAnteriores` → `= 92`; `consultaObrasInstalacoes` → `= 51`.
- ✅ **Covid**: `consultaCovid` → `CD_TIPO_LICITACAO IN ('19','22')` **ou** `CD_FONTE_RECURSO` em uma lista fixa de cerca de 30 códigos de fonte (códigos escritos no template).
- ✅ **Período**: com `dataInicio` e `dataFim`, filtra `ne.DT_LANCAMENTO BETWEEN <início> AND <fim>` e agrupa também por `ne.NR_ANO_NE`; sem datas, filtra por `ne.NR_ANO_NE = <ano>`.
- ✅ **Filtros** de texto: `LIKE '%…%'` para nome do credor, esfera, programa de trabalho, projeto, subtítulo, fonte de recurso e processo (o processo é comparado sem `-`, `/` e `.`); igualdade para código do credor, número da NE, NL e OB; listas `IN (...)` para UG, gestão, esfera, tipo/modalidade de licitação, função, subfunção, programa, categoria, grupo, modalidade de aplicação, elemento e fonte.
- ✅ **Filtro de valor**: valores finais viram `HAVING SUM(...) = '<valor>'` (igualdade exata).
- ✅ Ordenação padrão: `colunaPadrao` e `NR_ANO_NE DESC`.

### Pesquisa agrupada de empenhos (`pesquisaAgrupada/listDespesaNotaEmpenho.vm`)
- ✅ Retorna uma linha por **empenho** (`ne.NR_NE_ORIGINAL = ''` também aqui) com data de lançamento e emissão, UG, gestão, credor (código, **código mascarado** por `dbo.FN_MASCARA_NR_CPF` e nome), valor empenhado (`VL_EMPENHADO`), esfera, processo, modalidade de licitação, programa de trabalho, função, subfunção, programa, ação, subtítulo, categoria econômica (`3` = Despesas Correntes, `4` = Despesas de Capital), grupo, modalidade de aplicação, elemento, fonte, modalidade de empenho e unidade orçamentária.
- ✅ Mesmos flags de elemento (96/92/51); sem datas, filtra pelo ano do empenho.

### Despesa por credor (`listDespesaPorCredor.vm`) e ordens bancárias por credor (`listObPorCredor.vm`)
- ✅ Por credor: soma `VL_NE_FINAL`, `VL_NL_BRUTO` e `VL_OB_FINAL`, **somente do evento contábil `400091`** (`ne.CD_EVENTO = 400091`), agrupado por código e nome do credor, ordenado pelo nome.
- ✅ OB por credor: soma por ano/credor/UG/gestão/UG liquidante os valores `VL_EVENTO`, `VL_CANCELADO` e `VL_FINAL` das ordens bancárias vinculadas a empenhos (`TF_ORDEM_BANCARIA` × `TF_ORDEM_BANCARIA_X_NOTA_EMPENHO`), com nomes das UGs e gestões (pagadora e liquidante).

### Ordem bancária por empenho (`listDespesaOrdemBancariaPorNotaEmpenho.vm`)
- ✅ Parte de `TF_ORDEM_BANCARIA` ligada a `TF_PAGAMENTO_EMPENHO` (documento tipo `OB`) e ao empenho, e a **ordens canceladas** (`TF_OB_CANCELADA`) somadas por empenho.
- ✅ Parâmetro `tipoValorPago` escolhe o valor: `pago-final` (`VL_PAGO` + `VL_LANCAMENTO` das canceladas), `pago-exercicio`, `pago-rpp`, `pago-rpnp`, `pago-ret` (cada um somando o `VL_PAGO_*` correspondente com o das canceladas; em uma segunda variante do mesmo template, só o pago).
- ✅ Mostra domicílio bancário de origem (banco-agência-conta), fatura, nota de lançamento de referência, prioridade e hora da transação. 🔶 Banco, agência e conta de origem são da administração (não de pessoa física), mas o dado de pagamento fica público.

### Detalhamento da despesa (`listDespesaDetalhamento.vm`)
- ✅ Origem `Despesa.QDD_UG_GESTAO`, somando por UG: `vr_lei`, `VR_ALTERACAO`, `VR_MOVIMENTACAO`, `VR_BLOQUEADO`, `VR_DEPESA_AUTORIZADA`, `VR_EMPENHADO` e `VR_LIQUIDADO`; filtros por ano, UGs e gestões; ordenado pelo nome da UG. (QDD é lido aqui como quadro de detalhamento de despesa; 🔶 pela convenção dos nomes.)

### Restos a pagar (`restosAPagar/listRestosAPagar.vm`)
- ✅ Origem `Despesa.TF_CONSOLIDADO_RESTOS_PAGAR` ligada ao empenho; tipo `1` = PROCESSADO e `2` = NÃO PROCESSADO; valores `valorInscrito` (`VL_RP_NPROCESS_INSCRITO`), `valorCancelado` (`VL_RP_PROCESS_CANCELADOS`), `valorPago` (`VL_RP_PROCESS_PAGOS`) e `valorAPagar` (`VL_RP_PROCESS_APAGAR`), com credor, UG, gestão e classificação orçamentária.
- 🔶 Os nomes das colunas misturam "NPROCESS" e "PROCESS" nos quatro valores; não se sabe se há uma única fonte de valores para ambos os tipos ou se o `CASE` seleciona por tipo; precisa de leitura do restante do template e da base.

## Inferências e limitações
- 🔶 O filtro `NR_NE_ORIGINAL = ''` significa "empenho que não é cópia/reforço de outro"; a semântica exata (reforço, anulação, complemento) não está no código.
- 🔶 O evento `400091` é fixo; deve ser o evento contábil de empenho, mas não há comentário no código.
- 🔶 Os códigos dos elementos 96, 92 e 51 correspondem a "ressarcimento", "despesas de exercícios anteriores" e "obras e instalações" pelo nome do flag; a tabela de elementos da contabilidade não foi consultada.
- 🔶 A lista de fontes Covid está **fixa no template**; novas fontes exigem alterar o arquivo.
- ❓ Os demais 142 arquivos de `despesa` (diárias e passagens, emendas, QDD, execução OCA, painéis, gráficos) não foram revisados em nível de cálculo.
- ⚠️ Esses mesmos templates contêm os pontos de injeção de SQL descritos em [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]].

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]]

## Pendências e próximo passo
- Ler os `.vm` de diárias e passagens, emendas, QDD por UG/gestão e execução OCA; confirmar a semântica de `NR_NE_ORIGINAL`, evento `400091` e restos a pagar com o time de negócio.
