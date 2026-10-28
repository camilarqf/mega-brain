---
type: module
aliases:
  - "SUBCI e substitutos"
  - "SUBCI-e-Substitutos"
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
sources:
  - api/subci/SubciController.java
  - application/usecase/subci/CriarSubci.java
  - application/service/subci/SubciSubstitutoServiceImpl.java
  - application/usecase/ordemServico/ObterSubciVigenteParaDocumento.java
  - application/usecase/assinatura/AssinarOrdemServico.java
  - db/migrations/V11, V17, V18, V19
---

# SUBCI e substitutos

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Assinatura-Digital|Assinatura-Digital]], [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Auditores-Coordenadores-Perfis|Auditores-Coordenadores-Perfis]], [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

> O **SUBCI titular** (ou seu **substituto vigente**) é a única pessoa que pode **assinar** OS. O vínculo é feito pela tabela `TB_SUBCI` (auditor + `STATUS_TITULAR`), **independentemente** do perfil/role SUBCI do auditor.

## Endpoints — `/subci` ✅
| Método | Rota | Roles | Função |
|---|---|---|---|
| POST | `/cadastrar` | ⚠️ **nenhuma** | `CriarSubci.salvar` |
| GET | `/listar` | SUBCI | `ListarSubci` |
| GET | `/pesquisar` | — | `PesquisarSubci` |
| POST | `/{idSubci}/substitutos` | ⚠️ **nenhuma** | `SubciSubstitutoServiceImpl.criarPeriodo` |
| GET | `/{idSubci}/substitutos` | — | `SubciSubstitutoServiceImpl.historico` |

## Regras ✅
### Titular — `CriarSubci.salvar` (`@Transactional`)
- O auditor precisa existir.
- Se `statusTitular = true`: rejeita se o auditor já é o titular; **desativa o titular atual** (`desativarTitularAtual`) e grava o novo como titular.
- Banco: índice único filtrado `UX_SUBCI_UNICO_TITULAR_ATIVO` garante **no máximo um titular** (V17).

### Substituto — `SubciSubstitutoServiceImpl.criarPeriodo` (`@Transactional`)
- SUBCI e auditor substituto precisam existir; o substituto ≠ titular.
- `dataFim ≥ dataInicio` (também `CK_SUBCI_SUBSTITUTO_DATAS`, V18).
- Sem sobreposição de períodos para o mesmo SUBCI (`existePeriodoSobreposto`).
- Os períodos são imutáveis (`SubciSubstituto` só tem `criar`/`reconstituir`): não há edição nem exclusão por API.

### Uso na assinatura e nos PDFs
- `AssinarOrdemServico.resolverAssinanteAutorizado`: titular ativo → substituto vigente **na data de hoje** → senão `AccessDeniedException`. Ver [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Assinatura-Digital|Assinatura-Digital]].
- `ObterSubciVigenteParaDocumento.executar(data)`: nome, matrícula e flag "substituto" para as **minutas** de PDF.

## ⚠️ Risco de escalada de privilégio ✅
Como `POST /subci/cadastrar` e `POST /subci/{id}/substitutos` **não têm `@PreAuthorize`**, qualquer usuário autenticado (qualquer auditor ativo com login no Keycloak) pode:
1. cadastrar a **si mesmo** como SUBCI titular (`statusTitular = true`), destituindo o titular atual; **ou**
2. cadastrar a si mesmo como **substituto vigente** do titular;

e, em seguida, **assinar OS oficiais**, já que a assinatura confere só a tabela `TB_SUBCI`/`TB_SUBCI_SUBSTITUTO`, não a role.

Evidência: `SubciController` (anotações), `CriarSubci.salvar`, `SubciSubstitutoServiceImpl.criarPeriodo`, `AssinarOrdemServico.resolverAssinanteAutorizado`. Não há trilha de auditoria de quem cadastrou o titular ou o substituto.
Prioridade alta em [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]. Confirmar se algum controle externo (gateway, frontend) bloqueia — ver [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]].
