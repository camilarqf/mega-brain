---
type: module
aliases:
  - Reclassificacao-e-Invalidacao
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - backend
  - ouvidoria
  - reclassificacao
  - invalidacao
sources:
  - src/OuvDF.Api/Controllers/ServicoOuvidoria/ReclassificacaoController.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/ReclassificarManifestacao
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/RegistrarReclassificacaoSeccional
  - src/OuvDF.ServicoOuvidoria/Domain/Commands/InvalidarManifestacao
  - src/OuvDF.ServicoOuvidoria/Domain/Entities/Manifestacao.cs
---

# Reclassificação e invalidação

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestacao]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Fluxo-Tramitacao-e-Resposta]]

## Objetivo
Documentar a mudança de classificação/assunto de uma manifestação (integral, parcial e seccional) e a invalidação.

## Evidências
Workflow `ReclassificarManifestacaoWorkflow` (passos `ValidarPermissao`, `RecuperarDadosReclassificacaoParcial`, `CriarReclassificacao`, `CriarTramite` lidos), `RegistrarReclassificacaoSeccionalHandler`, `InvalidarManifestacaoHandler`; commit `4901ad5`. Passos `Validar`, `RecuperarDadosBd`, `RecuperarDadosReclassificacaoIntegral`, `AdicionarAtributosComplementares`, `PersistirDadosBd`, `NotificarManifestante` só pelo nome.

## Informações confirmadas

### Reclassificação (`POST …/reclassificacao/registrar-reclassificacao`, papel `OperadorSO`)
Passos: Validar → RecuperarDadosBd → **ValidarPermissao** → RecuperarDadosReclassificacaoParcial → RecuperarDadosReclassificacaoIntegral → **CriarReclassificacao** → AdicionarAtributosComplementares → **CriarTramite** → PersistirDadosBd → NotificarManifestante.
1. ✅ Precisa de `RCL_INT` (reclassificação integral, funcionalidade `ReclassificarManifestacao`) **ou** `RCL_PAR` (parcial, funcionalidade `ReclassificarAssunto`); sem nenhuma, erro "Reclassificação não disponível para esta manifestação".
2. ✅ **Parcial** (sem permissão integral): mantém a classificação atual; muda só o assunto; a unidade destino é a de tramitação inicial da classificação ou, se nula, a do assunto.
3. ✅ **Integral**: dados vêm da classificação/assunto informados (passo lido só pelo nome).
4. ✅ Exige mudança: se classificação e assunto são os mesmos, "Para reclassificar a manifestação é necessário alteração do assunto e/ou classificação".
5. ✅ Cria `Reclassificacao` com o resultado serializado da manifestação original (classificação, assunto, atributos complementares) e a motivação; `AddReclassificacao` troca classificação e assunto da manifestação.
6. ✅ Se a unidade destino é diferente da atual, cria um `Tramite` com ação `Responder`, remove o operador corrente e desmarca "visualizada"; se for a mesma, não tramita.
7. ✅ O protocolo recebe novo prefixo conforme a classificação (`AlterarPrefixoDoProtocolo`).

### Reclassificação seccional (`…/registrar-reclassificacao-seccional`)
1. ✅ Exige `RCL_SEC` (funcionalidade `ReclassificacaoSeccional`).
2. ✅ Se o novo assunto tem formulário ativo e não vieram atributos complementares, erro "O assunto selecionado requer o preenchimento dos atributos complementares".
3. ✅ Define se há trâmite e o destino por `DefinirTramitePorReclassificacao`, cria a `Reclassificacao` e, quando o assunto muda, remove os atributos complementares antigos e grava os novos.

### Invalidação (`POST …/manifestacao/invalidar`, papel `OperadorSO`)
1. ✅ Exige a funcionalidade `InvalidarManifestacao`.
2. ✅ Cria `Invalidacao` (motivação, operador, manifestação) e leva a situação para `Invalida` (`AtualizarSituacao`, sem validar a origem).
3. ✅ A ação `NVL_MNF` (consulta de permissão) exige operador corrente, na unidade, não inválida e não bloqueada.

## Inferências e limitações
- 🔴 Em `RegistrarReclassificacaoSeccionalHandler` a variável `assuntoEhDiferenteDoOriginal` é calculada com **igualdade** (`command.Assunto.Id == manifestacao.Assunto.Id`). Com isso, o teste de formulário e a remoção dos atributos antigos acontecem quando o assunto **não** muda, e **não** acontecem quando muda: lógica provavelmente invertida (a confirmar com o time/testes).
- 🔶 `ValidarPermissao` (reclassificação integral/parcial) envia as consultas de permissão ao mediador **sem `await`** e lê `Response` na sequência; só funciona se o handler for síncrono.
- 🔶 `InvalidarManifestacaoHandler` exige só a funcionalidade e **não** consulta `NVL_MNF`: um operador com `InvalidarManifestacao` poderia invalidar manifestação de outra unidade ou já inválida (a consulta de ações esconde o botão, mas o comando não repete a regra).
- 🔶 Nenhum e-mail ao manifestante em `InvalidarManifestacao`; em `ReclassificarManifestacao` há o passo `NotificarManifestante` (conteúdo ❓).
- ❓ Regras de `DefinirTramitePorReclassificacao` e do passo integral.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Confirmar com o time a regra da reclassificação seccional (comparação invertida).
- Ler os passos pendentes da reclassificação.
