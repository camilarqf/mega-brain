---
type: integration
aliases:
  - "Integração IBS → SIP (SQL Server)"
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
consumer: IBS
provider: SIP-SQLServer
tags:
  - autenticacao
sources:
  - pom.xml
  - src/main/resources/application.properties
  - src/main/resources/application-prod.properties
  - src/main/java/br/gov/df/cg/ibs/infra/identidadeinstitucional/IdentidadeInstitucionalRepository.java
  - src/main/java/br/gov/df/cg/ibs/infra/fonteautenticacao/repositories/FonteAutenticacaoRepositoryImpl.java
---
# Integração IBS → SIP (SQL Server)

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `IBS` (`identity-broker-service`) | `SIP-SQLServer` | JDBC (`mssql-jdbc`, Hikari) | leitura de `tb_sigla_orgao_usuario`, `vw_listar_unidade`, `vw_autenticacao_sip` | saída |

## Evidências
- Repositórios JDBC, `application*.properties`, `deployment.params.yml` (secret da URL por ambiente); `/healthcheck` inclui `db` no grupo de readiness.

## Informações confirmadas
- ✅ Banco consultado a cada login (vínculo e unidades) e na carga/recarga do cache de fontes (a cada 30 min por instância).
- ✅ Se o banco estiver indisponível, `POST /auth` falha antes do bind LDAP (exceção de acesso a dados sem handler → 500) e a readiness vira 503.
- ✅ A URL vem de `SPRING_DATASOURCE_URL` (secret por ambiente); credenciais não aparecem nos `.properties` versionados.
- Esquema e uso por consulta: [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Banco-SIP|Banco SIP]].

## Inferências e limitações
- ❓ Dono do SIP, versão do SQL Server e política de acesso (usuário somente leitura) não identificados no repositório.
- ❓ Se dev, hom e prod usam bases ou servidores distintos não é verificável pelo repositório (só há variável por ambiente).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo]] · [[01-Sistemas/IBS/Backend/01-Visao-Geral/IBS-Backend-Perfis-e-Ambientes|Perfis e ambientes]]

## Pendências e próximo passo
- Identificar o dono do SIP e o usuário de banco usado em cada ambiente.
