---
type: module
aliases:
  - Acao-de-Controle
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - modulo
  - acao-de-controle
sources:
  - api/acaoControle/AcaoControleController.java
  - application/service/AcaoControle/AcaoControleServiceImpl.java
  - application/usecase/acaoControle/*
  - domain/model/AcaoControle.java
  - infrastructure/persistence/repository/AcaoControleRepository.java
  - infrastructure/persistence/adapter/AcaoControleRepositoryAdapter.java
---

# Ação de Controle

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-POAC|POAC]], [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Cadastros-Auxiliares|Cadastros-Auxiliares]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Enums-e-Estados|Enums-e-Estados]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

> Unidade de planejamento do controle interno: um trabalho de auditoria, consultoria ou inspeção de um ano, ligado a um POAC, a uma UAI e área executora, às unidades auditadas e ao programa/objetivos do PPA. Todas as [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Ordem-de-Servico|OS]] nascem a partir dela.

## Endpoints — `/acao-controle` ✅
| Método | Rota | Roles | Delegação |
|---|---|---|---|
| POST | `/cadastrar` | SUBCI, COORDENADOR, DIRETOR | `CriarAcaoControle.salvar` |
| GET | `/listar` | — (autenticado) | só ações com `STATUS = 1` (`AcaoControleRepository`, SQL nativo) |
| GET | `/pesquisar?id=` | — | `PesquisarAcaoControle` |
| GET | `/pesquisar-poac/{idPoac}` | — | ações do POAC (**sem** filtro de status) |
| PUT | `/atualizar/{id}` | SUBCI, COORDENADOR, DIRETOR | `AtualizarAcaoControle.atualizar` |
| DELETE | `/inativar?id=` | SUBCI, COORDENADOR | `AcaoControleServiceImpl.inativaAcaoControle` → `InativarAcaoControle` |
| GET | `/validar/{id}` | — | `AcaoControleServiceImpl.validarAcaoControle` |

## Regras ✅
### Criação — `CriarAcaoControle.salvar`
- **Acumula erros** e lança `MultiplasValidacoesException` com a lista: UAI, área executora, programa de governo, objetivos PPA e unidades auditadas inexistentes.
- Objetivos PPA: não aceita ids duplicados e exige que **todos pertençam ao programa de governo** informado.
- Tipo × natureza validado no construtor do domínio (`AcaoControle` → `validarNaturezaAcaoControle`) — ver [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Enums-e-Estados|Enums-e-Estados]].
- **Código da ação**: formato `SSSSAAAA` (sequencial com 4 dígitos + ano com 4 dígitos).
  - `AcaoControleRepository.countByAnoCadastro(ano)` → apesar do nome, retorna `MAX(codigo)` onde `codigo % 10000 = ano`;
  - `AcaoControle.gerarCodigo`: `seq = max / 10000 + 1`; `codigo = parseInt("%04d%04d")`.
  - Ex.: o terceiro código de 2026 vira `00032026`, gravado como inteiro `32026`.
  - O ano usado é o **ano de programação** do request, não o ano corrente.
  - `CD_ACAO_CONTROLE` é `UNIQUE` (V1): em criação concorrente o segundo insert falha (erro de integridade, não número duplicado).
- `idPoac` **não é validado** (não verifica se o POAC existe).

### Atualização — `AtualizarAcaoControle.atualizar`
- Mesmas buscas com acúmulo de erros, **porém sem** checar duplicidade de objetivos PPA nem se eles pertencem ao programa (regra assimétrica em relação à criação).
- Revalida tipo × natureza (`AcaoControle.atualizar`).
- ⚠️ Não verifica se a ação já tem OS assinadas: tipo, natureza, unidades e UAI podem mudar depois da OS de abertura assinada.

### Inativação
- `AcaoControleServiceImpl.inativaAcaoControle`: **bloqueia se existir qualquer OS** vinculada (`IllegalArgumentException`).
- Inativação lógica (`status = false`). `InativarAcaoControle` lança `RuntimeException` genérica se não achar a ação.

### Validação "a definir"
`GET /validar/{id}` → `RegraNegocioException` se a ação tem **programa de governo com id 999** ou **unidade auditada com id 999** (placeholders "A DEFINIR" carregados por seeder).
- ✅ Só é chamado pelo endpoint, e **nenhuma regra de OS** o usa. 🔶 O frontend provavelmente chama antes de criar a OS de abertura.
- ⚠️ Ids mágicos `999` fixos no código (`AcaoControleRepository`).

### Situação
Só muda automaticamente na assinatura da ABERTURA → `OSI_EMITIDA` ([[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Ordem-de-Servico|Ordem-de-Servico]]). As demais situações (`EM_PLANEJAMENTO`… `FINALIZADO_*`) não têm fluxo no backend analisado. 🔶 Podem ser enviadas no request de atualização ou ainda não ter sido implementadas.

## Observações
- ✅ `AcaoControleRepositoryAdapter.buscarPorId` lança `ResourceNotFoundException`, mas vários chamadores testam `== null`: esses testes nunca são verdadeiros.
- ✅ A join column de unidades auditadas chama-se `ID_ACAO_CONTROLE_UNIDADE_AUDITADA`, mas guarda o id da **ação**, e a de naturezas `ID_ACAO_CONTROLE_NATUREZA`. Os nomes confundem.
- ✅ A entidade usa `@Enumerated(ORDINAL)` para tipo, naturezas, situação e classificação — ver [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Enums-e-Estados|Enums-e-Estados]].
