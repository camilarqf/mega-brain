---
type: module
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - modulo
  - fontes
  - cache
sources:
  - src/main/java/br/gov/df/cg/ibs/application/fonteautenticacao
  - src/main/java/br/gov/df/cg/ibs/application/roteamento
  - src/main/java/br/gov/df/cg/ibs/domain/fonteautenticacao
  - src/main/java/br/gov/df/cg/ibs/infra/fonteautenticacao
---
# IBS Backend — fontes de autenticação (roteamento e cache)

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Descrever como o IBS conhece os ADs de cada órgão: carga da view, agrupamento, cache e resolução por órgão.

## Evidências
- `FonteAutenticacaoRepositoryImpl`, `FonteAutenticacaoMapper`, `FonteAutenticacaoCacheService`, `ResolverFontesAutenticacaoService`; testes `FonteAutenticacaoCacheServiceTest` (16), `FonteAutenticacaoRepositoryImplTest` (6), `FonteAutenticacaoMapperTest`, `ResolverFontesPorOrgaoHandlerTest` (10).

## Informações confirmadas
- ✅ **Origem:** view `dbo.vw_autenticacao_sip` (colunas `id_orgao`, `descricao`, `sigla`, `id_servidor_autenticacao`, `nome`, `endereco`, `porta`, `sufixo`, `contexto_pesquisa`, `atributo_filtro_pesquisa`, `versao`). Uma linha por servidor.
- ✅ **Agrupamento (mapper):** linhas com o mesmo (órgão, sufixo normalizado, contexto, atributo) formam uma `FonteAutenticacao` com vários `ServidorAutenticacao`. O sufixo é normalizado (minúsculas, prefixo `@`); `atributo_filtro_pesquisa` aceita `userprincipalname` → `UPN` e `displayname` → `DISPLAY_NAME`; outro valor lança `FonteAutenticacaoException`. O contexto precisa conter `DC=`.
- ✅ **Cache em memória por instância:** dois índices (por sufixo e por órgão). Carga no `ApplicationReadyEvent` (se `carregar-ao-iniciar=true`, padrão do projeto), recarga agendada a cada 30 min (`fixedDelay`, com atraso inicial igual) e carga preguiçosa se ainda não carregado. `recarregar()` é `synchronized`; se a consulta falhar, o cache anterior é mantido porque os índices só são trocados depois da leitura.
- ✅ **Resolução:** `resolverPorOrgao(login, idOrgao)` valida o login, devolve as fontes do órgão ordenadas pelo menor id de servidor e lança `FonteAutenticacaoNaoEncontradaException` se não houver. O login não é usado para escolher a fonte (não há roteamento por sufixo do login).
- ✅ Log de carga: registros lidos, fontes agrupadas, sufixos indexados e registros sem sufixo.

## Inferências e limitações
- 🔶 Os índices e consultas por sufixo (`buscarPorSufixo`, `ObterFontesPorSufixoHandler`) existem, mas nenhum controller os usa; `ResolverFontesPorOrgaoHandler` (que expõe endereços e portas dos servidores) também não tem rota — apenas testes o exercitam.
- 🔶 Não há endpoint para forçar a recarga; mudança na view só aparece após o próximo ciclo (até 30 min) ou reinício.
- Com 2 réplicas em produção, cada uma mantém seu próprio cache.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Banco-SIP|Banco SIP]] · [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Ordem-de-Tentativa-LDAP|Ordem de tentativa]]

## Pendências e próximo passo
- Nenhuma específica.
