---
type: domain
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - dominio
  - claims
sources:
  - src/main/java/br/gov/df/cg/ibs/domain/claims/ClaimsUsuario.java
  - src/main/java/br/gov/df/cg/ibs/api/auth/AutenticarUsuarioResponse.java
  - src/main/java/br/gov/df/cg/ibs/application/claims/services/ClaimsService.java
  - src/main/java/br/gov/df/cg/ibs/infra/identidadeinstitucional/IdentidadeInstitucionalService.java
---
# IBS Backend — modelo de claims

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Mostrar de onde vem cada claim devolvida por `POST /auth`.

## Evidências
- `ClaimsUsuario`, `AutenticarUsuarioResponse.Claims`, `ClaimsService.montar`, `IdentidadeInstitucionalService.buscarIdentidade`; `MontarClaimsHandlerTest`, `IdentidadeInstitucionalServiceTest`.

## Informações confirmadas
| Claim (resposta) | Origem |
|---|---|
| `login` | login enviado (sem sufixo); em `ClaimsUsuario` também preenche `sub` e `preferredUsername` (esses dois não vão na resposta) |
| `idUsuario`, `matricula`, `nomePessoa`, `nomeSocial` | primeira linha de `tb_sigla_orgao_usuario` (`id_usuario`, `nr_matricula`, `nm_usuario`, `nm_social`) |
| `idOrgao` | `id_orgao` do vínculo |
| `siglaOrgao` | trecho antes de `/` da sigla da primeira unidade válida |
| `nomeOrgao` | `ds_unidade` da sigla raiz em `vw_listar_unidade` (sem filtro de ativo) |
| `unidades[]` | vínculos distintos com sigla; descrição de `vw_listar_unidade` (apenas ativas e não globais) |
| `correlationKey` | header ou UUID gerado |

- ✅ A resposta é `{ autenticado: true, correlationKey, claims }`; `sub` e `preferredUsername` existem só no modelo interno.
- ✅ O Keycloak consome `login`, `idOrgao`, `siglaOrgao`, `nomeOrgao`, `nomePessoa`, `nomeSocial`, `matricula`, `unidades` e `idUsuario` ([[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo de claims do Keycloak]]).
- ✅ O AD não fornece claims; é usado apenas para validar a credencial.

## Inferências e limitações
- 🔶 `nomeSocial` e `descricaoUnidade` podem ser `null` (campos vazios ou "NULL" viram `null`).
- 🔶 O row do repositório chama de `nomeOrgao` o valor de `ds_usuario`, mas o serviço o ignora e usa a descrição da unidade raiz.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/05-API/IBS-Backend-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Banco-SIP|Banco SIP]] · [[01-Sistemas/IBS/Backend/03-Regras-de-Negocio/IBS-Backend-Regra-Vinculo-Ativo-e-Matricula|Vínculo e matrícula]]

## Pendências e próximo passo
- Nenhuma específica.
