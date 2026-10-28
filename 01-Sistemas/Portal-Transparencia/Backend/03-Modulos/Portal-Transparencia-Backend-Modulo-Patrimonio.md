---
type: module
aliases:
  - "Módulo Patrimônio"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
sources:
  - src/main/java/br/gov/df/transparencia/api/patrimonio
  - src/main/java/br/gov/df/transparencia/api/v2/patrimonio
  - src/main/java/br/gov/df/transparencia/servico/patrimonio
  - src/main/java/br/gov/df/transparencia/modelo/patrimonio
  - src/main/resources/sql/patrimonio
---
# Módulo Patrimônio

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seções Patrimônio v1 e API v2)

## Objetivo
Documentar a consulta de bens móveis, bens imóveis (terrenos, edificações e obras) e demonstrativos patrimoniais.

## Evidências
Leitura da lista de métodos dos 5 serviços e dos controllers; tabelas dos 30 arquivos SQL. Corpos e `.vm` não lidos.

## Informações confirmadas
| Versão | Controller (rotas) | Serviço |
|---|---|---|
| v1 | `PatrimonioController` (`/patrimonio`, 12), `PatrimonioRelatorioController` (2) | `PatrimonioService` (demonstrativos por ano e data de referência, bens móveis, localização por órgão, unidades gestoras e gestões) e `PatrimonioRelatorioService` (bens móveis, por órgão/localização) |
| v2 imóveis | `BensImoveisController` (`/v2/bens-imoveis`, 8), `BensImoveisRelatorioController` (1) | `BensImoveisService` (listagem, detalhe, regiões administrativas, órgãos, situações, terrenos, edificações, obras), `BensImoveisRelatorioService` |
| v2 móveis | `BensMoveisController` (`/v2/patrimonio/bens-moveis`, 4) | `BensMoveisService` (listagem, tipos, órgãos, estados) |

- ✅ Tabelas: `Patrimonio.Bens_Moveis`, `TF_BENS_MOVEIS`, `BensMoveis_Sisgepat`, `TD_TIPO_BEM_MOVEL`, `TD_ORGAO`, `TD_GESTAO`, `TD_SITUACAO`, `TF_IMOVEL`, `TF_EDIFICACAO`, `TF_OBRA`, `TF_TERRENO`; os demonstrativos usam o catálogo `Servidor.Relatorio`/`CategoriaRelatorio` (🔶 categoria `PATRIMONIO`, id 27, do enum `CategoriaRelatorioEnum`; uso não confirmado; ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Documentos publicados]]); `Despesa.TD_UG` para unidade gestora.
- ✅ Modelo (7): `BensImoveis`, `BensMoveis`, `BensMoveisV2`, `BensOrgaoLocalizacao`, `Edificacao`, `Obra`, `Terreno`.
- ✅ Endpoints POST: `POST /patrimonio/bens-moveis/unidades-gestoras` e `/gestoes` (únicos POST da área; recebem uma lista de códigos como `String` crua no corpo e a interpolam em `IN ( $anos )`/`IN ( $codigosUnidadeGestora )` nos `.vm`; ver [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]).
- ✅ Nenhum método de patrimônio usa `@Mascaravel`.
- ✅ "Sisgepat" aparece no nome de tabela (`BensMoveis_Sisgepat`).

## Inferências e limitações
- 🔶 `BensMoveisV2` e a rota v2 substituem gradualmente `BensMoveis` e a v1; coexistem.
- ❓ Sigla Sisgepat e origem dos dados (carga) não explicadas no código.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Pendências e próximo passo
- Ler os `.vm` de `patrimonio/` e confirmar a relação v1 × v2.
