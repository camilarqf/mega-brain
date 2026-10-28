---
type: persistence
aliases:
  - "IBS Backend — banco SIP (persistência)"
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
sources:
  - src/main/java/br/gov/df/cg/ibs/infra/identidadeinstitucional/IdentidadeInstitucionalRepository.java
  - src/main/java/br/gov/df/cg/ibs/infra/identidadeinstitucional/UnidadeInstitucionalRepository.java
  - src/main/java/br/gov/df/cg/ibs/infra/fonteautenticacao/repositories/FonteAutenticacaoRepositoryImpl.java
  - src/main/java/br/gov/df/cg/ibs/infra/usuario/UsuarioRepository.java
  - src/main/resources/application.properties
---
# IBS Backend — banco SIP (persistência)

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar as tabelas e views do SQL Server que o IBS consulta e como.

## Evidências
- Os quatro repositórios em `sources`; testes `IdentidadeInstitucionalRepositoryTest` (6), `UnidadeInstitucionalRepositoryTest` (4), `FonteAutenticacaoRepositoryImplTest` (6), `UsuarioRepositoryTest` (9).

## Informações confirmadas
- ✅ Banco **SQL Server**, base `DB_SIP` (nome citado em SQL; a URL real vem de secret). Acesso por `JdbcTemplate`/`NamedParameterJdbcTemplate`, SQL em texto, parâmetros posicionais/nomeados. **Não há entidades JPA, migrations nem escrita**: `ddl-auto=none` e repositórios com `@Transactional(readOnly = true)`.

| Objeto | Colunas lidas | Usado por |
|---|---|---|
| `[DB_SIP].[dbo].[tb_sigla_orgao_usuario]` | `id_usuario`, `nm_sigla_orgao`, `id_orgao`, `ds_usuario`, `nm_social`, `nm_sigla_usuario`, `is_ativo`, `nm_perfil`, `nm_usuario`, `nr_matricula` | vínculo no login; busca e detalhe de usuários |
| `[DB_SIP].[dbo].[vw_listar_unidade]` | `id_unidade`, `id_orgao`, `nm_sigla_unidade`, `ds_unidade`, `is_ativo`, `is_global` | unidades e descrições |
| `dbo.vw_autenticacao_sip` | `id_orgao`, `descricao`, `sigla`, `id_servidor_autenticacao`, `nome`, `endereco`, `porta`, `sufixo`, `contexto_pesquisa`, `atributo_filtro_pesquisa`, `versao` | fontes LDAP; nome/sigla de órgão na busca de usuários |

- ✅ Junção usuário × unidade: `unidade.id_orgao = usuario.id_orgao AND unidade.nm_sigla_unidade = usuario.nm_sigla_orgao AND unidade.is_ativo = 1 AND unidade.is_global = 0` (LEFT JOIN).
- ✅ O nome e a sigla do órgão na busca vêm de `vw_autenticacao_sip` agrupada por órgão (`MAX(descricao)`, `MAX(sigla)`), ou seja, só órgãos que tenham fonte de autenticação aparecem com nome/sigla.

## Inferências e limitações
- 🔶 `vw_autenticacao_sip` é citada sem prefixo de banco, enquanto as demais usam `[DB_SIP]`; a resolução depende do banco padrão da conexão.
- ❓ DDL, índices e donos das tabelas/views não estão no repositório; o esquema é compartilhado (dono do SIP não identificado).
- 🔶 A dependência `spring-boot-starter-data-jpa` é usada apenas pelo datasource/transações (`JpaTransactionManager`, visto no erro do teste de integração).

## Relacionamentos
- [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-SIP-SQLServer|Integração IBS → SIP]] · [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Fontes-de-Autenticacao|Fontes]] · [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Consulta-de-Usuarios|Consulta de usuários]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Claims|Claims]]

## Pendências e próximo passo
- Obter DDL/documentação do SIP com o dono do banco.
