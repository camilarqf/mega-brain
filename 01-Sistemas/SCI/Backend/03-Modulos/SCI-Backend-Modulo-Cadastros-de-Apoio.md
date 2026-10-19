---
type: module
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - modulo
  - cadastros
  - assunto
sources:
  - src/SCI.Domain/GestaoProcessual/Entities/Assunto.cs
  - src/SCI.Application/UseCases/CriarAssunto
  - src/SCI.Application/UseCases/GestaoIntegracao
  - src/SCI.Api/Controllers/AssuntoController.cs
  - src/SCI.Api/Controllers/PessoaController.cs
  - src/SCI.Api/Controllers/ServidorController.cs
  - src/SCI.Application/Builders/EnvolvidoBuilder.cs
---
# SCI Backend — módulo Cadastros de apoio

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar as tabelas de apoio consultadas pela aplicação e o cadastro administrativo de assuntos.

## Evidências
- `AssuntoController`, `Assunto.{Criar, Atualizar, Excluir, Ativar}`, controllers de listas, `EnvolvidoBuilder`.

## Informações confirmadas
- ✅ **Assunto e categoria de assunto**: CRUD administrativo (Administrador): `GET visao-administrador`, `GET {id}`, `GET categorias`, `POST`, `PUT {id}`, `DELETE {id}` (exclusão lógica por `Assunto.Excluir`), `PATCH {id}/ativar`. A listagem `GET /assunto` está liberada para os perfis operacionais. Eventos `AssuntoCriado/Atualizado/Excluido/Ativado`.
- ✅ **Listas somente de leitura** (autenticado): tipos (`tipo-processo`, `tipo-revisao`, `tipo-diligencia`, `tipo-documento-demanda`, `tipo-vinculo`), `conduta`, `recomendacao`, `tipificacao-admissibilidade`, `origem-denuncia`, `situacao-funcional`, `cargo/por-usuario`, `status/{demanda,processo-admissibilidade,pip}`.
- ✅ **Pessoas e servidores**: `GET /pessoa/pesquisar` e `GET /servidor/pesquisar`. Ao registrar envolvidos, o `EnvolvidoBuilder` usa o `IBCadastroClient` para obter pessoa física (CPF) e jurídica (CNPJ + representante legal) — [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-BCadastro|Integração BCadastro]].
- ✅ Dados de apoio são carregados por scripts de seed (`01` a `25`) via `POST /support/generate-database`.

## Inferências e limitações
- Conteúdo de listas e seeds não lido. Tabelas de status são espelho dos enums ([[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums e estados]]).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco]] · [[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Ler `EnvolvidoBuilder` por completo para documentar o preenchimento de envolvidos.
