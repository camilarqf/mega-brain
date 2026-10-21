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
  - receita
sources:
  - src/main/java/br/gov/df/transparencia/api/receita
  - src/main/java/br/gov/df/transparencia/servico/receita
  - src/main/java/br/gov/df/transparencia/modelo/receita
  - src/main/java/br/gov/df/transparencia/repositorio/receita
  - src/main/resources/sql/receita
---
# Módulo Receita

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seção Receita)

## Objetivo
Documentar a consulta da arrecadação do GDF: receita por órgão, consulta dinâmica, multas de trânsito, transferências da União e gráficos.

## Evidências
Leitura da lista de métodos de `ReceitaService` (392 linhas), `ReceitaUniaoService`, `ReceitaRelatorioService`, `RelatorioService` (receita), dos controllers e da análise de tabelas dos 39 arquivos de `resources/sql/receita`. Corpo dos métodos e dos `.vm` não lidos.

## Informações confirmadas
| Controller | Rotas | Serviço |
|---|---|---|
| `ReceitaController` (`/receita`) | 26 | `ReceitaService` |
| `ReceitaUniaoController` (`/receita-uniao`) | 9 | `ReceitaUniaoService` |
| `ReceitaRelatorioController` (`/receita/relatorio`) | 5 | `ReceitaRelatorioService` |

- ✅ **Tabelas**: quase tudo em `Receita.Principal` (44 referências nos SQL) e `Receita.MULTA_TRANSITO` (2). Entidade JPA `ReceitaPrincipal` (`Receita.Principal`) com repositório Spring Data e `ReceitaSpecs` (consulta por *Specification*).
- ✅ Consultas: consulta dinâmica, por órgão e detalhamento por órgão, multas de trânsito (lista e total), por fonte de recurso e **receita da União** (auxílio), com filtros de unidade gestora, fonte, subfonte, rubrica, alínea, subalínea, gestão, categoria e origem.
- ✅ Gráficos/indicadores: evolução da receita por exercício, impostos por exercício, receita corrente, por categoria, evolução de impostos, percentuais de impostos e de taxas e `recuperarReceitaImposto`; `listReceitasAnuais` (usado pelo gráfico receita × despesa).
- ✅ Relatórios PDF/CSV: multas de trânsito, por órgão, consulta dinâmica, por fonte de recurso e transferência da União (`ReceitaRelatorioService`).
- ✅ `servico/receita/RelatorioService.ultimoAnoDisponivel(categoria)` está no pacote de receita, mas é usado pelo `RelatorioController` de orçamento (`/relatorio/loa|ldo|relatorios-gerenciais/ultimo-ano`); ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Orçamento e documentos publicados]].
- ✅ Datas de atualização específicas (painel de receitas, multas de trânsito, receitas por órgão, consulta dinâmica e receitas da União) vêm de `DataAtualizacaoController` ([[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados|Apoio]]).
- ✅ Nenhum método de receita usa `@Mascaravel`: **receita não passa pelo filtro de medida protetiva**.

## Inferências e limitações
- 🔶 Os "percentuais de impostos/taxas" são calculados pelo serviço ou pelo SQL; não foi lido onde nem a fórmula.
- ❓ Regras de classificação (rubrica, alínea, subalínea, origem) são as da contabilidade pública, mas o código só as trata como filtros; nada foi validado contra norma.
- ❓ Conteúdo dos 39 `.vm` não lido.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]]

## Pendências e próximo passo
- Ler `listReceita*.vm` e os cálculos de percentual para documentar regras.
