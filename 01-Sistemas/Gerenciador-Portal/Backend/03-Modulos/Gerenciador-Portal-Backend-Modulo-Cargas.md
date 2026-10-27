---
type: module
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - backend
  - modulo
  - cargas
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api/CargaController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/CargaService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/Carga.java
---
# Módulo Cargas

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Permitir que o operador acompanhe o controle de cargas de dados do Portal (somente leitura).

## Evidências
`CargaController` (`/carga`), `CargaService` (consultas `JdbcTemplate` em `Carga.Controle`), `Carga` (POJO).

## Informações confirmadas
- ✅ `GET /carga/listar-cargas`: lê `Carga.Controle` (colunas `CON_ESQUEMA`, `CON_INICIOCARGA`, `CON_FIMCARGA`, `CON_STATUS`, `CON_TABELA`) com filtros opcionais por data de início (`dd/MM/yyyy`, via `CONVERT(VARCHAR, ..., 103)`), status, esquema e tabela, ordenado por início decrescente. Datas saem como `dd/MM/yyyy HH:mm`; campos nulos viram o texto "Campo não preenchido".
- ✅ `listar-status` e `listar-esquema`: valores distintos de `CON_STATUS` e `CON_ESQUEMA`.
- ✅ `listar-quantidade-status`: lista fixa de 4 inteiros na ordem `ATUALIZADO`, `ERRO`, `SEM ALTER.`, `REALIZADO` (contagens em `Carga.Controle`).
- ✅ O módulo **não grava nem dispara cargas**; só consulta.

## Falhas e dependências
- ✅ Os quatro filtros opcionais são concatenados diretamente ao SQL entre aspas: **injeção de SQL** possível em `listar-cargas` (análise estática; exploração não testada). Ver [[01-Sistemas/Gerenciador-Portal/Backend/08-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos]].
- ✅ A resposta de `listar-quantidade-status` depende da **posição** na lista; status novos não são contados.
- ✅ Depende do esquema `Carga` do banco `DB_PRT_TRANSPARENCIA`, o mesmo citado nas pendências do Portal ([[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|pendência 4]]).

## Inferências e limitações
- 🔶 O significado dos status (`SEM ALTER.`, `REALIZADO`) e quem alimenta `Carga.Controle` (ETL) não constam neste repositório.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SQL-Server|Integração com o SQL Server]] · [[01-Sistemas/Gerenciador-Portal/Backend/05-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Identificar o processo que escreve em `Carga.Controle`.
