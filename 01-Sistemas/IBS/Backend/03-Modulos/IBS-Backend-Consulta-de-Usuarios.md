---
type: module
aliases:
  - "IBS Backend — consulta de usuários"
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
sources:
  - src/main/java/br/gov/df/cg/ibs/api/usuarios
  - src/main/java/br/gov/df/cg/ibs/application/usuario
  - src/main/java/br/gov/df/cg/ibs/infra/usuario
  - src/main/java/br/gov/df/cg/ibs/infra/identidadeinstitucional/UnidadeInstitucionalRepository.java
---
# IBS Backend — consulta de usuários

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Documentar a busca e a consulta de usuários do SIP expostas em `/usuarios/*`.

## Evidências
- `UsuarioController`, `BuscarUsuariosQuery/Handler`, `ObterUsuarioQuery/Handler`, `UsuarioRepository`, `UnidadeInstitucionalRepository`; testes `UsuarioRepositoryTest` (9), `BuscarUsuariosQueryTest`, `ObterUsuarioHandlerTest`, `UsuarioControllerTest` (ver Testes).

## Informações confirmadas
- ✅ **Busca** (`GET /usuarios/buscar`): só usuários com `is_ativo = 1`. Filtros combinados com AND: `nome` (cada termo separado por espaço vira `LIKE %termo%` em `nm_usuario`), `login` (`LIKE %x%` em `nm_sigla_usuario`), `matricula` (igualdade após remover `-`, `.` e espaços) e `orgao` (`LIKE` na descrição ou na sigla do órgão, derivadas de `vw_autenticacao_sip`). Ordenação por nome, órgão, login e matrícula; paginação `OFFSET/FETCH`; `size` ≤ 100.
- ✅ **Granularidade:** a consulta junta `tb_sigla_orgao_usuario` com `vw_listar_unidade`, então um usuário com várias lotações aparece em várias linhas, e `totalElements` conta linhas, não pessoas.
- ✅ **Detalhe** (`GET /usuarios/{idUsuario}`): lê todas as linhas do `id_usuario`; os dados pessoais vêm da primeira; as unidades são as siglas não vazias, sem repetição, com descrição buscada em `vw_listar_unidade` (primeiro só unidades ativas e não globais, depois sem esse filtro). Sem linhas → 404.
- ✅ Só leitura; transações `readOnly`.

## Inferências e limitações
- 🔶 Para cada unidade do detalhe há uma ou duas consultas extras de descrição (padrão N+1).
- ❓ Quem consome esses endpoints não foi identificado no código.
- Cobertura parcial: SQL lido, testes só inventariados.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/06-API/IBS-Backend-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Banco-SIP|Banco SIP]] · [[01-Sistemas/IBS/Backend/08-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Segurança]]

## Pendências e próximo passo
- Identificar os consumidores de `/usuarios/*`.
