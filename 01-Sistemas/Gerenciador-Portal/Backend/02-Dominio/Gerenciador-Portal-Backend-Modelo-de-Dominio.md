---
type: domain
aliases:
  - "Modelo de domínio"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/model
  - src/main/java/br/gov/df/cgdf/gerenciador/dto
  - src/main/java/br/gov/df/cgdf/gerenciador/enums
---
# Modelo de domínio

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Descrever as entidades, documentos, DTOs e enums do backend e como se relacionam.

## Evidências
Pacotes `model`, `dto` e `enums` no commit `14b185f`. Detalhes de tabelas em [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Banco-e-Persistencia|Banco e persistência]].

## Informações confirmadas
**Entidades JPA (SQL Server)**
| Entidade | Papel (✅) | Campos principais |
|---|---|---|
| `Arquivo` | relatório publicado | `id`, `nome` (original), `url` (chave do objeto), `ano`, `periodo`, `codigoCategoria`, `descricao`, `dataReferencia` (texto), `fonte`, `assunto`, `dataCarga`, `ativo` (0/1), `nomePadrao`, `tipoRelatorio`, `completo`; campos `@Transient`: `categoria`, `tipoReferencia`, `anoReferencia`, `referencia`, `descricaoReferencia`, `descricaoCategoria` |
| `Categoria` | categoria de relatório | `codigo`, `descricao`, `prefixo` |
| `TipoReferencia`, `AnoReferencia`, `Referencia` | tipos e valores de período (dia, mês, bimestre… ano, período) e anos | mapeadas em `Portal.TD_REFERENCIA_TEMPO` e `Portal.TD_TEMPO` |
| `Imagem` | imagem do slideshow ou painel de setor | `id`, `descricao`, `url`, `codigoCategoria` (55/56), `prioridade`, `ativo`, `completo`, `codFuncao`, `imagemBackgroundPainel` (1:1) |
| `ImagemBackgroundPainel` | fundo de um painel | `id`, `descricao`, `url` |
| `ServidorMedidaProtetiva` | pessoa oculta em uma consulta | `id`, `nome`, `identificador`, `consulta`, `coluna` |
| `TextoConsultaPortal` | texto explicativo de uma subcategoria | `id`, `idCategoria`, `texto` (com marcador de link) |
| `OrgaoLAI` | órgão da LAI | `id`, `nome`, `sigla`, `urlDestino`, `tipo` (`TipoOrgao`: `DIRETA`, `REGIONAL`, `INDIRETA`) |
| `Log` | auditoria | `id`, `tipoAlteracao`, `usuarioLogado`, `data`, `objeto` (JSON) |

**Documento Mongo**: `PalavraChave` (coleção `indices`): `_id` (`ObjectId`), `palavraChave` (campo `descritivo`), `urlConsulta`, `descricao`, `prioridade`, `dataset`, `exercicio`.

**Não persistidos**: `Carga` (POJO de leitura), `DepositoArquivo`, `MultiDepositoArquivo`, `NomesConcatenados` (enum que monta o nome padrão do arquivo por tipo de período), `INomenclaturaArquivo`.

**DTOs**: `UsuarioFormDTO` (login/senha), `UsuarioDTO` (dados do JWT: nome, login, matrícula, órgão, `servidorSUTCS`, `unidades`), `UnidadeDTO`, `ServidorDTO`, `MedidaProtetivaDTO`, `ServidorMedidaProtetivaDTO`/`InputDTO`, `FuncaoPainelDTO`, `PalavraChaveDTO`, `CategoriaTextoPortalDTO`, `SubCategoriaTextoPortalDTO`.

**Enums**: `ConsultasMedidaProtetivaEnum` (`REMUNERACAO`, `SERVIDORES_POR_ORGAO`, `DESPESA`, `CADASTRO_EXPULSOES`, `CONSELHEIROS`, `CONSELHOS`), `ColunasMedidaProtetivaEnum` (`NOME`, `CPF`, `CD_CREDOR`, `MATRICULA`). Constantes de auditoria em `ConstantesRepository`: `INATIVAR`, `ATIVAR`, `EXCLUIR`, `SALVAR_ARQUIVO`, `SALVAR_INFORMACOES_ARQUIVO`, `SALVAR_SERVIDOR_MEDIDA_PROTETIVA`, `EXCLUIR_SERVIDOR_MEDIDA_PROTETIVA`.

**Estados**
- ✅ Arquivo: **incompleto** (`completo=false`, `ativo=0`) → **completo e ativo** (`salvar-informacoes-arquivo`) → ativo/inativo → excluído.
- ✅ Imagem: prioridade 0 = não ordenada/incompleta; prioridade ≥ 1 = ordenada e completa.

## Falhas e dependências
- ✅ `Arquivo.ativo` é `Integer` (marcado com `TODO: Trocar de Integer para Boolean`); `Imagem.ativo` é `Boolean`: representações diferentes para o mesmo conceito.
- ✅ `Arquivo`, `Imagem` e `Log` serializam entidades com Gson no campo `objeto`.
- ✅ `AnoReferencia` e `Referencia` mapeiam a mesma tabela `Portal.TD_TEMPO`.

## Inferências e limitações
- 🔶 `nomePadrao` define o nome público do arquivo no Portal; o uso final não está neste repositório.
- ❓ Significado de `tipoRelatorio`, `fonte` e `assunto` (este último guarda a URL do painel nos arquivos criados a partir de imagem de setor, segundo um construtor de `Arquivo`).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Arquivos]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Imagens-do-Portal|Imagens]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Medida protetiva]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Conteúdo]]

## Pendências e próximo passo
- Confirmar o uso de `tipoRelatorio` e `fonte` com o time.
