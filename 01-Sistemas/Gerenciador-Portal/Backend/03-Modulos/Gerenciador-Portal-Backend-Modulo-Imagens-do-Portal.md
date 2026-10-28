---
type: module
aliases:
  - "Módulo Imagens do Portal"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api/ImagemController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/ImagemService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/dao/ImagemDAO.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/Imagem.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/ImagemBackgroundPainel.java
  - src/main/java/br/gov/df/cgdf/gerenciador/repository/ImagensRepository.java
---
# Módulo Imagens do Portal

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Gerenciar as imagens exibidas no Portal: **slideshow** (categoria 55) e **painéis de setores** (categoria 56), com prioridade de exibição, função de despesa associada e imagem de fundo.

## Evidências
`ImagemController`, `ImagemService` (constantes `COD_SLIDESHOW=55`, `COD_SETORES=56`, prefixos `slide_`, `painel_`, `background_`), `ImagemDAO`, `Imagem` (`Portal.Imagem_Pagina_Portal`), `ImagemBackgroundPainel` (`Portal.Imagem_Background_Painel`).

## Informações confirmadas
- ✅ **Upload** (`salvar/{usuario}/{categoria}`): grava no bucket `portal-imagens` com chave `<prefixo><uuid><extensão>`, calcula a próxima prioridade (`MAX(prioridade)+1` na categoria) e cria a `Imagem`: em **slideshow** nasce completa; em **setores** nasce incompleta. Imagens de categoria diferente de 55/56 resultam em `Imagem` nula (ver "Falhas").
- ✅ **Prioridade**: `mover-prioridade-acima/abaixo` troca a prioridade com a vizinha (±1) e salva as duas; `ordenar-prioridades-imagens` atribui prioridades sequenciais às imagens com prioridade 0 (ordem alfabética da descrição); `salvarImagem` com prioridade 0 força `ativo=false`/`completo=false`, senão `completo=true`. Ao excluir, as imagens seguintes sobem uma posição.
- ✅ **Ativar/desativar/excluir** e **editar** (`PUT salvar-imagem`) gravam log em `arquivo.LOG_ARQUIVOS`.
- ✅ **Função do painel**: `listar-funcoes-paineis` lê `Despesa.TD_FUNCAO` (código e nome) para vincular um painel a uma função orçamentária (`CD_FUNCAO`).
- ✅ **Imagem de fundo do painel**: `salvar-imagem-background` envia ao MinIO, cria `ImagemBackgroundPainel` e associa ao painel (`CD_IMAGEM_BACKGROUND`); `excluir-background` desassocia e apaga o registro.
- ✅ Listagens `listar-imagens-slideshow` e `listar-imagens-setores` ordenadas por prioridade.

## Falhas e dependências
- ✅ `salvar-sem-ordenar` **ainda grava no disco local** (`default.imagem.diretorio`) e não no MinIO (usa `FileCopyUtils`), enquanto `salvar` e o fundo gravam no MinIO: dois caminhos de armazenamento no mesmo módulo.
- ✅ `excluirImagem` usa `CommonService.deletarArquivo` (sistema de arquivos local): o objeto no MinIO não é removido (mesma falha do módulo de [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|arquivos]]). Se o arquivo local não existir, o método devolve `400` mesmo após apagar o registro, e a reordenação não ocorre.
- ✅ `excluir-background` apaga só o registro; o objeto no bucket permanece.
- ✅ `mover-prioridade-*` usa `Optional.get()`: se não houver vizinha (primeira/última), lança `NoSuchElementException` (sem handler dedicado).
- ✅ Categoria diferente de 55/56 faz `imagem` ficar nula e `saveAndFlush(null)` falhar, depois do upload ao MinIO (objeto órfão).
- ✅ `ImagemDAO` monta SQL por concatenação de inteiros (`Integer`): sem risco de injeção por texto, mas sem parâmetros vinculados.

## Inferências e limitações
- 🔶 O módulo alimenta o slideshow da página inicial e os painéis de setores do Portal-Transparencia (nomes `Portal.*`, `apiGerenciador` citado no frontend do Portal); a associação visual não foi verificada no frontend.
- ❓ Se a leitura pelo Portal usa o bucket `portal-imagens` ou ainda o diretório compartilhado.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MinIO-S3|Integração com MinIO/S3]] · [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|Integrações do Frontend do Portal]]

## Pendências e próximo passo
- Confirmar se `salvar-sem-ordenar` ainda é usado pelo cliente e o fluxo de leitura das imagens no Portal.
