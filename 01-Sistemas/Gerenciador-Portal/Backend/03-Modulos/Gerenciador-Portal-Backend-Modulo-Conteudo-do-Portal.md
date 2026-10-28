---
type: module
aliases:
  - "Módulo Conteúdo do Portal (palavras-chave, textos e órgãos da LAI)"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - busca
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api/PalavraController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/api/TextoConsultaController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/api/OrgaoLAIController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/PalavraService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/TextoConsultaService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/OrgaoLAIService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/dao/TextosConsultasDAO.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/PalavraChave.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/TextoConsultaPortal.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/OrgaoLAI.java
---
# Módulo Conteúdo do Portal (palavras-chave, textos e órgãos da LAI)

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Editar três conteúdos de apoio do Portal: palavras-chave da busca, textos explicativos das consultas e a lista de órgãos da Lei de Acesso à Informação (LAI).

## Evidências
Controllers `/palavra`, `/textos-consultas`, `/orgao`; serviços e repositórios correspondentes; entidades `PalavraChave` (Mongo), `TextoConsultaPortal` e `OrgaoLAI` (SQL Server).

## Informações confirmadas
**Palavras-chave** (`/palavra`)
- ✅ Armazenadas no MongoDB, coleção `indices`, documento `PalavraChave` com `descritivo` (a palavra), `urlConsulta`, `descricao`, `prioridade=1` e `dataset="CUSTOM-PALAVRA-CHAVE"` fixos. `listar` filtra pelo dataset e ordena por palavra decrescente.
- ✅ `editar` e `excluir` retornam `200`/`400` (`HttpStatus`); a edição recria o documento com o mesmo `_id`.

**Textos das consultas** (`/textos-consultas`)
- ✅ Categorias vêm de `Portal.TB_CATEGORIA`; subcategorias e texto de `Portal.TB_SUBCATEGORIA` (`FK_CATEGORIA`, `TX_EXPLICATIVO`).
- ✅ O texto é guardado com um **marcador de link** `##<rótulo>(<url>)` e convertido: `getTexto()` devolve a forma "codificada" e `getTextoSemParsearParaCodedHyperLink()` a forma HTML `<a href='…' target='_blank'>…</a>`. É o que `TextosTests` verifica.
- ✅ `PUT /textos-consultas` salva o texto da subcategoria (`save` direto).

**Órgãos da LAI** (`/orgao`)
- ✅ CRUD de `Portal.Orgaos_LAI` (nome, sigla, URL de destino, tipo `TipoOrgao`). `salvar` devolve `201`; erros viram `400`.

## Falhas e dependências
- ✅ Nenhuma das operações grava log de auditoria (diferente de arquivos, imagens e medida protetiva).
- ✅ `TextosConsultasDAO` concatena o inteiro `idCategoria` no SQL (sem texto livre).
- ✅ `PalavraService.editar` faz `findOne` e ignora o resultado; `excluir` busca antes de apagar e responde `400` para qualquer exceção, inclusive não encontrado.
- ✅ A conversão do texto usa `indexOf`/`substring` sem validar o formato; um marcador `##` sem `(`…`)` pode lançar exceção ao salvar ou ler.

## Inferências e limitações
- 🔶 A coleção `indices` do Mongo é lida pelo serviço de busca do Portal (`apisuperbusca`, citado no [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|frontend do Portal]]); o campo `dataset` e a coleção sugerem um índice compartilhado, não confirmado.
- ❓ Quem consome a lista de órgãos da LAI e os textos no Portal.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MongoDB|Integração com o MongoDB]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SQL-Server|SQL Server]] · [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Modelo-de-Dominio|Modelo de domínio]]

## Pendências e próximo passo
- Confirmar com o time o consumo da coleção `indices` e dos textos.
