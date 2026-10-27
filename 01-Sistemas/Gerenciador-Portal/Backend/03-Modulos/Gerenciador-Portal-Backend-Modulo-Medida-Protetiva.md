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
  - medida-protetiva
  - dados-pessoais
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api/ServidoresMedidaProtetivaController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/api/ServidoresController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/ServidorMedidaProtetivaService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/dao/ServidorMedidaProtetivaDAO.java
  - src/main/java/br/gov/df/cgdf/gerenciador/dao/ServidorDAO.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/ServidorMedidaProtetiva.java
  - src/main/java/br/gov/df/cgdf/gerenciador/enums/ConsultasMedidaProtetivaEnum.java
  - src/main/java/br/gov/df/cgdf/gerenciador/enums/ColunasMedidaProtetivaEnum.java
  - src/main/java/br/gov/df/cgdf/gerenciador/util/HttpClientImpl.java
---
# Módulo Medida Protetiva

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Manter a lista de pessoas (servidores, credores, conselheiros etc.) cujos dados devem ser **ocultados em consultas específicas** do Portal por medida protetiva, e buscar essas pessoas nas bases de origem.

## Evidências
`ServidoresMedidaProtetivaController` (`/servidores-medida-protetiva`), `ServidoresController` (`/servidores`), `ServidorMedidaProtetivaService`, `ServidorDAO`, `ServidorMedidaProtetivaDAO`, `ServidorMedidaProtetiva` (`Servidor.TB_MEDIDA_PROTETIVA`), enums de consulta e coluna.

## Informações confirmadas
- ✅ **Seis "consultas"** (`ConsultasMedidaProtetivaEnum`): `REMUNERACAO`, `SERVIDORES_POR_ORGAO`, `DESPESA`, `CADASTRO_EXPULSOES`, `CONSELHEIROS`, `CONSELHOS`. Cada uma tem `GET` (lista) e `POST` (ocultar) em `/servidores-medida-protetiva/...`.
- ✅ **Coluna identificadora** por consulta (`ColunasMedidaProtetivaEnum`): `CPF` (remuneração e servidores por órgão), `CD_CREDOR` (despesa), `MATRICULA` (cadastro de expulsões), `NOME` (conselheiros e conselhos).
- ✅ **Busca de pessoas** (`GET /servidores/{remuneracao|por-orgao|despesas|cadastro-expulsoes|conselheiros}?nomeServidor=`): `ServidorDAO` consulta `LIKE` por nome nas tabelas de origem (`Remuneracao.Principal`, `Servidor.Principal`, `Despesa.TD_CREDOR`, `Expulsao.Principal`, `Prestando_Contas.Orgao_Deliberativo`) e devolve nome, identificador e CPF/credor formatado.
- ✅ **Cadastro** (`POST`): exige `usuarioAutenticado` não vazio; rejeita duplicidade por (`identificador`, `consulta`) com `400` "Servidor já cadastrado"; salva em `Servidor.TB_MEDIDA_PROTETIVA` (nome, identificador, consulta, coluna) e grava log `SALVAR_SERVIDOR_MEDIDA_PROTETIVA`.
- ✅ **Exclusão** (`DELETE /{id}`): exige `usuarioAutenticado`, apaga o registro e grava log `EXCLUIR_SERVIDOR_MEDIDA_PROTETIVA`; resposta `204`.
- ✅ `GET /servidores-medida-protetiva?identificador=` devolve o identificador (sem pontos e traço) se existir; `GET /listar` devolve consulta/coluna/identificador de todos.
- ✅ **Expirar cache** (`GET /expirar-cache`): publica uma mensagem no RabbitMQ para que o Portal e o serviço de busca invalidem o cache; fluxo em [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Expirar-Cache-Medida-Protetiva|Fluxo]] e integração em [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-RabbitMQ-Expirar-Cache|RabbitMQ]].

## Falhas e dependências
- ✅ **Bug**: em `deletarServidorMedidaProtetiva`, quando o registro não existe, o `ResponseEntity.badRequest()` é criado mas **não retornado**; o código segue para `delete(null)` e falha (`500`).
- ✅ **Bug**: em `expirarCache`, a guarda `url == null && url.trim().isEmpty()` usa `&&`: com `url` nulo lança `NullPointerException`, e com `url` vazia segue em frente.
- ✅ `expirarCache` captura `Throwable` e responde sempre `200` (`ok` ou `failed [<mensagem>]`); a falha só aparece no corpo.
- ✅ **Injeção de SQL** possível em `ServidorDAO` (`nomeServidor` concatenado em `LIKE`) e em `verificarServidorMedidaProtetiva` (`identificador` concatenado). Ver [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos]].
- ✅ A API devolve CPF e nome de pessoas protegidas sem autenticação além do `x-client-id`; o autor é o `usuarioAutenticado` do cliente.
- ✅ O cadastro e a exclusão **não chamam** `expirarCache`: a expiração do cache é uma chamada separada (`GET /expirar-cache`).

## Inferências e limitações
- 🔶 O Portal-Transparencia filtra (remove) os registros listados nesta tabela, conforme sua própria documentação ([[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache e mascaramento do Portal]]); neste repositório só há a escrita. A pendência 5 do Portal ("quem alimenta `TB_MEDIDA_PROTETIVA`?") fica **respondida em parte**: esta API grava na tabela e publica `expirePortal`.
- ❓ Se o cliente chama `expirar-cache` automaticamente após cadastrar ou excluir.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Expirar-Cache-Medida-Protetiva|Fluxo de expirar cache]] · [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Fluxo de invalidação no Portal]] · [[01-Sistemas/Gerenciador-Portal/Backend/06-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Confirmar o comportamento do Portal diante da tabela e se o cliente dispara a expiração.
