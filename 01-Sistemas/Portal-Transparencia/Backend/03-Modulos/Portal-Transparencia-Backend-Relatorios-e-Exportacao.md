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
  - relatorios
  - pdf
  - csv
sources:
  - src/main/java/br/gov/df/transparencia/util/ReportUtil.java
  - src/main/java/br/gov/df/transparencia/util/RelatorioController.java
  - src/main/java/br/gov/df/transparencia/modelo/Relatorio.java
  - src/main/java/br/gov/df/transparencia/relatorio/CabecalhoRodapePageEvent.java
  - src/main/java/br/gov/df/transparencia/api/servidor/RemuneracaoRelatorioController.java
  - src/main/resources/relatorios
---
# Relatórios e exportação (PDF e CSV)

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]]

## Objetivo
Descrever como os controllers `*RelatorioController` geram arquivos para download.

## Evidências
Leitura de `ReportUtil`, `util/RelatorioController`, `modelo/Relatorio`, `relatorio/CabecalhoRodapePageEvent`, de `RemuneracaoRelatorioController` e da listagem de `resources/relatorios`.

## Informações confirmadas
- ✅ Há **20 controllers de relatório** (19 com nome `*RelatorioController` mais `orcamento/RelatorioController`, que é um controller de orçamento com rota `/relatorio`), distribuídos por área, quase todos em rota `<área>/relatorio(s)`.
- ✅ O bean de filtro herda `modelo/Relatorio` com dois campos: `tipo` (`pdf` ou `csv`) e `colunas` (string **JSON** com as colunas, `nome` e `visible`, opcionalmente `date`, `currency`, `type`) enviados pelo cliente.
- ✅ `RelatorioController.responseWrapper` responde com `Content-Type: application/octet-stream` e `Content-Disposition: attachment; filename=relatorio.<tipo>` e escreve o corpo em fluxo (`StreamingResponseBody`).
- ✅ **CSV**: `;` como separador, cabeçalho com o título e os nomes das colunas visíveis, BOM UTF-8; valores entre aspas com `;` trocado por `,`, quebras de linha removidas e aspas duplicadas; datas `dd/MM/yyyy`; moeda formatada como `#,##0.00`. A versão por `EntityConsumer` escreve linha a linha (sem carregar tudo em memória).
- ✅ **PDF**: template Velocity (`resources/relatorios/*.vm`) renderizado para HTML e convertido por iText (`XMLWorkerHelper`) em A4 **paisagem**; autor "Portal da Transparência"; rodapé com a URL pública do portal e o número da página (`CabecalhoRodapePageEvent`). Template padrão `templateListaDefault.vm`; específicos: despesa por ação/credor/órgão e detalhamento, convênio (entidades beneficiadas), remuneração (4), servidor por órgão, empresa punida e beneficiários de programas sociais.
- ✅ O PDF é gerado **no próprio backend** (iText); não usa serviço externo de HTML→PDF.

## Inferências e limitações
- 🔶 O PDF é montado em memória (`ByteArrayOutputStream`) antes da conversão; relatórios muito grandes podem consumir bastante memória (não medido). O método `printMem()` (diagnóstico com `System.out`) existe em `ReportUtil`.
- 🔶 `relatorioRemuneracao` é `synchronized`, serializando exportações desse endpoint.
- 🔶 Os campos de texto vão entre aspas, mas valores que comecem com `=`, `+`, `-` ou `@` não são neutralizados (risco de "injeção de fórmula" ao abrir o CSV em planilha); não verificado se os dados de origem permitem.
- ❓ O conteúdo de cada template e as colunas padrão por área não foram detalhados.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] (os relatórios passam pelos mesmos serviços mascarados)

## Pendências e próximo passo
- Mapear colunas e templates por área nos módulos funcionais.
