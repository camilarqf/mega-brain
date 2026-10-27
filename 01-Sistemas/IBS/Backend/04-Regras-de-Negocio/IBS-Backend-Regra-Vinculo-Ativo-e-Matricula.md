---
type: business-rule
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - regra
  - vinculo
  - matricula
sources:
  - src/main/java/br/gov/df/cg/ibs/infra/identidadeinstitucional/IdentidadeInstitucionalService.java
  - src/main/java/br/gov/df/cg/ibs/infra/identidadeinstitucional/IdentidadeInstitucionalRepository.java
  - src/main/java/br/gov/df/cg/ibs/application/claims/services/ClaimsService.java
  - src/main/java/br/gov/df/cg/ibs/application/autenticacao/services/AutenticacaoService.java
---
# IBS Backend — regra: vínculo ativo com o órgão e matrícula

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar as condições de negócio que impedem a emissão de claims, independentemente da senha.

## Evidências
- `IdentidadeInstitucionalRepository.SELECT_VINCULOS_ATIVOS`; `IdentidadeInstitucionalService.buscarIdentidade`; `AutenticacaoService.buscarIdentidadeDoOrgao`; `ClaimsService.montar`; commit `d100394` ("informa ausência de vínculo ativo com o órgão"); testes `usuarioSemVinculoNoOrgaoNaoTentaAutenticacaoLdap`, `sucessoNoFallbackComUsuarioSemMatriculaBloqueiaClaims`.

## Informações confirmadas
- ✅ **Vínculo ativo:** o login precisa ter ao menos um registro em `tb_sigla_orgao_usuario` com `nm_sigla_usuario = login`, `id_orgao = idOrgao` e `is_ativo = 1`. Sem registro → `USUARIO_SEM_VINCULO_NO_ORGAO`, HTTP 401, mensagem "Usuário não possui vínculo ativo com o órgão informado.", **sem tentar LDAP**.
- ✅ **Matrícula:** depois do bind com sucesso, matrícula nula ou em branco (após `TextoInstitucional`, que também trata o texto "NULL" como vazio) → `USUARIO_SEM_MATRICULA`, HTTP 409, "Usuário sem matrícula cadastrada. Contate o administrador." O erro é registrado em log com `correlationKey` e `idOrgao`.
- ✅ **Dados da identidade:** são lidos da primeira linha de vínculo (ordenada por `nm_sigla_orgao`); as unidades vêm de todas as linhas, sem repetição e ignorando as de sigla nula.

## Inferências e limitações
- 🔶 `ClaimsService` lança `IdentidadeInstitucionalIndisponivelException` se o status for `INATIVO`, mas a consulta já filtra `is_ativo = 1`, então o ramo parece inalcançável no fluxo atual; essa exceção não tem handler (resultaria em 500).
- ✅ Consequência de segurança: a ordem (vínculo antes da senha) permite distinguir "login sem vínculo no órgão" de "senha inválida" sem informar senha correta (ver [[01-Sistemas/IBS/Backend/08-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Segurança]]).

## Relacionamentos
- [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo de autenticação]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Claims|Modelo de claims]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Banco-SIP|Banco SIP]]

## Pendências e próximo passo
- Nenhuma específica.
