---
type: flow
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
  - fluxo
  - arquivos
  - minio
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api/ArquivoController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/ArquivoService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/StorageService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/CommonService.java
---
# Fluxo de cadastro de arquivo

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Mostrar o caminho de um relatório desde o upload até estar ativo (ou excluído).

## Evidências
`ArquivoController` → `ArquivoService` → `StorageService`/`ArquivosRepository`/`LogService`.

## Informações confirmadas
1. ✅ **Upload** — `POST /arquivo/salvar-arquivo/{usuario}/{categoria}/{ano}` com o arquivo: gera `<uuid><ext>`, `StorageService.upload` (`PutObject` no bucket `portal-arquivos`), grava `Arquivo` incompleto, registra o log `SALVAR_ARQUIVO`. Devolve o `Arquivo` (com `id`).
2. ✅ **Listagem de pendentes** — `GET /arquivo/listar-incompletos` e `quantidade-arquivos-incompletos` mostram o que falta completar.
3. ✅ **Completar** — `POST /arquivo/salvar-informacoes-arquivo` com descrição, período/data de referência, `idReferenciaEscolhida`, prefixo da categoria e `nomeOriginal`: monta o `nomePadrao` (`NomesConcatenados`) e chama `atualizarArquivo` (`ativo=1`, `completo=true`). Se a categoria é de arquivo único, desativa os outros da mesma categoria. Log `SALVAR_INFORMACOES_ARQUIVO`.
4. ✅ **Ativar/Desativar** — `ativar-arquivo` / `desativar-arquivo` mudam `IN_ATIVO`; logs `ATIVAR`/`INATIVAR`.
5. ✅ **Excluir** — `excluir-arquivo` / `exclusao-multipla`: apaga a linha e tenta apagar o arquivo local; log `EXCLUIR`. O objeto no MinIO não é removido.
6. ✅ Falha no upload: `StorageUploadException` é capturada em `salvar` e a resposta é `400` com a mensagem; falha de banco depois do upload deixa o objeto órfão.

## Falhas e dependências
Ver [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Módulo de arquivos]] (exclusão local × armazenamento S3, retorno `400` após a linha apagada).

## Inferências e limitações
- 🔶 O cliente chama os passos nessa ordem (upload → completar → ativar); o backend não impõe a sequência (`salvar-informacoes-arquivo` com arquivo já completo mantém o nome padrão).
- ❓ Como o Portal-Transparencia resolve a URL pública final do objeto.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MinIO-S3|Integração com MinIO/S3]]

## Pendências e próximo passo
- Confirmar o passo de leitura no Portal.
