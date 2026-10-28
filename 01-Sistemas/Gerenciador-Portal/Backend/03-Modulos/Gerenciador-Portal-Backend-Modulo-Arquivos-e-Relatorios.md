---
type: module
aliases:
  - "Módulo Arquivos e Relatórios"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - armazenamento-objetos
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api/ArquivoController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/api/CategoriaController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/ArquivoService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/CommonService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/StorageService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/CategoriaService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/dao/ArquivoDAO.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/Arquivo.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/NomesConcatenados.java
---
# Módulo Arquivos e Relatórios

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Cadastrar, descrever, ativar e excluir os arquivos (relatórios) publicados no Portal da Transparência, organizados por categoria, ano e período de referência.

## Evidências
`ArquivoController`, `ArquivoService`, `CommonService`, `StorageService`, `ArquivoDAO`, `ArquivosRepository`, `Arquivo`, `NomesConcatenados`, `CategoriaService`.

## Informações confirmadas
**Ciclo de vida** (fluxo em [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Cadastro-de-Arquivo|Fluxo de cadastro de arquivo]]):
1. ✅ **Upload** (`POST /arquivo/salvar-arquivo/...`): se o arquivo não é vazio, gera nome `<uuid><extensão>`, envia ao bucket `portal-arquivos` do MinIO e grava um `Arquivo` **incompleto** (`completo=false`, `ativo=0`, `dataCarga=hoje`) na tabela `Servidor.Relatorio`. Os valores textuais `"null"`/`"undefined"` de categoria e ano são tratados como ausentes.
2. ✅ **Completar** (`salvar-informacoes-arquivo`): calcula o **nome padrão** `[<prefixo>_]A<ano><código de período><data>-<nome original>` conforme o tipo de referência escolhido (`idReferenciaEscolhida` 1 a 8: dia `D`, mês `M`, bimestre `B`, trimestre `T`, quadrimestre `Q`, semestre `S`, ano `A`, período) e marca o arquivo como completo e ativo (`atualizarArquivo`). Se o prefixo da categoria é `N/A`, usa só `A<ano>`.
3. ✅ **Ativar/desativar**: `IN_ATIVO` 1/0. Para as **categorias de arquivo único** (50, 51, 52, 53, 54, 56, 57, 58, 59), ativar ou completar um arquivo **desativa os demais da mesma categoria** (`disableOldPendencias`).
4. ✅ **Excluir** (`excluir-arquivo`, `exclusao-multipla`): ver "Falhas".
5. ✅ **Consultas**: listar completos/incompletos/todos, contar, filtrar (nome, descrição, ano, categoria, data de referência), anos e tipos/períodos de referência (`Portal.TD_TEMPO`, `TD_REFERENCIA_TEMPO`); a categoria vem de `Servidor.Categoria_Relatorio` (entidade `Categoria`: código, descrição, prefixo).
6. ✅ **Auditoria**: cada operação grava `SALVAR_ARQUIVO`, `SALVAR_INFORMACOES_ARQUIVO`, `ATIVAR`, `INATIVAR` ou `EXCLUIR` em `arquivo.LOG_ARQUIVOS` com o `usuarioLogado` informado pelo cliente.

## Falhas e dependências
- ✅ **A exclusão não remove o objeto do MinIO.** `CommonService.deletarArquivo` apaga o arquivo no **diretório local** `default.diretorio` (`java.io.File.delete`) e remove a linha do banco; o upload vai para o MinIO. Em produção o objeto permanece no bucket.
- ✅ A linha é removida **antes** do resultado do `File.delete`; como o arquivo local normalmente não existe, `File.delete` devolve `false` e `excluirArquivo` responde `400`, apesar de o registro já ter sido apagado. `excluirMultiplosArquivos` ignora o retorno de cada exclusão e responde `200`.
- ✅ O objeto é enviado ao MinIO **antes** do `INSERT`; se o banco falhar, o objeto fica órfão. Não há transação distribuída.
- ✅ `recuperarArquivo` assume que a categoria existe (`queryForObject`); categoria ausente gera `500`/`404` pelo handler.
- ✅ Filtros do `ArquivoDAO` e `CategoriaService.buscarCategoria` montam SQL por concatenação (nome, descrição, data de referência são texto livre); ver [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos]].
- ✅ Tamanho máximo de upload de 900MB (`spring.http.multipart.*`).

## Inferências e limitações
- 🔶 As consultas `CategoriaService` leem `Servidor.CategoriaRelatorio` (nome sem sublinhado, filtro `IN_ATIVO`), enquanto a entidade mapeia `Servidor.Categoria_Relatorio`; podem ser objetos diferentes (view) — ❓ não verificado no banco.
- 🔶 As categorias 55 (slideshow) e 56 (setores) são usadas pelo módulo de [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Imagens-do-Portal|imagens]]; o significado das demais categorias de arquivo único (50 a 59) não consta no código.
- ❓ Como o Portal-Transparencia lê esses arquivos (URL do objeto no bucket) não é visível aqui.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MinIO-S3|Integração com MinIO/S3]] · [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/Gerenciador-Portal/Backend/06-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Confirmar se o objeto deve ser removido do bucket na exclusão e o significado das categorias de arquivo único.
