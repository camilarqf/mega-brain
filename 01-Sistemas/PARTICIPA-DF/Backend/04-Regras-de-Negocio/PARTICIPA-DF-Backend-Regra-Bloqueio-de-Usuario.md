---
type: business-rule
aliases:
  - "Bloqueio de usuário"
  - "Bloqueio-de-Usuario"
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
sources:
  - src/OuvDF.Shared/Domain/Entities/Usuario.cs
  - src/OuvDF.Shared/Domain/Entities/BloqueioUsuario.cs
  - src/OuvDF.Shared/Domain/Commands/BloquearUsuario/BloquearUsuarioHandler.cs
  - src/OuvDF.Shared/Domain/Commands/DesbloquearUsuario/DesbloquearUsuarioHandler.cs
  - src/OuvDF.Shared/Domain/Commands/AutenticarUsuario/AutenticarUsuarioHandler.cs
  - src/OuvDF.Shared/Domain/Enums/MotivacaoBloqueioUsuarioEnum.cs
  - src/OuvDF.Shared/Domain/Enums/TipoBloqueioUsuarioEnum.cs
  - src/OuvDF.Shared/Infra/Queries/ConsultarBloqueioUsuario/ConsultarBloqueioUsuarioHandler.cs
  - src/OuvDF.Shared/Infra/Queries/ConsultarUsuarioEstaBloqueado/ConsultarUsuarioEstaBloqueadoHandler.cs
  - src/OuvDF.Shared/Jobs/BloquearUsuariosFalecidosJob.cs
  - src/OuvDF.Api/Controllers/Shared/UsuarioController.cs
---

# Bloqueio de usuário

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]]

## Objetivo
Registrar, em forma de condição → efeito, as regras verificáveis de bloqueio e desbloqueio de usuários.

## Evidências
Código em `sources`, commit `4901ad5`. Só entram aqui regras que aparecem no código.

## Informações confirmadas

### Motivos e tipos
- ✅ Motivos (`MotivacaoBloqueioUsuarioEnum`): 1 CPF dados inconsistentes, 2 CPF inexistente, 3 falecimento, 4 CNPJ inexistente, 5 CNPJ dados inconsistentes, 6 CNPJ baixado.
- ✅ Tipos (`TipoBloqueioUsuarioEnum`): `Parcial` e `Total`. O handler de bloqueio manual sempre usa `Total`.

### Regras
| # | Condição | Efeito | Evidência |
|---|---|---|---|
| R1 | Quem bloqueia é o mesmo usuário (`Id == operador.Id`) | recusa: "Usuário não pode se auto bloquear" | `Usuario.Bloquear` |
| R2 | O usuário já está bloqueado (`ConsultarUsuarioEstaBloqueado`) | recusa: "Usuário está bloqueado" | `BloquearUsuarioHandler` |
| R3 | O operador não tem a funcionalidade `Bloquear_Desbloquear_Usuario` (36) | recusa: "Operador não possui permissão de bloqueio de usuários" | `BloquearUsuarioHandler` |
| R4 | Usuário ou operador inexistente | recusa com mensagem própria | `BloquearUsuarioHandler` |
| R5 | Bloqueio aceito | cria `BloqueioUsuario` (usuário, operador, motivo, data atual) e registra log *Warning* | `Usuario.Bloquear`, `BloqueioUsuario` |
| R6 | Desbloqueio pelo mesmo usuário | recusa: "Usuário não pode se auto desbloquear" | `Usuario.Desbloquear` |
| R7 | 🔶 Intenção: bloqueio por **falecimento** não pode ser desbloqueado ("Não é possível desbloquear usuário falecido") | **não aplicada no código lido**: ver "Inferências" | `BloqueioUsuario.DesbloquearUsuario` |
| R8 | Login de usuário com qualquer bloqueio | recusa com "Usuário bloqueado" e o id do motivo | `AutenticarUsuarioHandler` |
| R9 | Pessoa com CPF em `UsuarioFalecido` e sem nenhum bloqueio | bloqueio automático por `FALECIMENTO` (até 100 por execução), usando o operador do sistema | `BloquearUsuariosFalecidosJob` |

### Consultas auxiliares
- ✅ `Usuario.IsFalecido()`, `IsCPFInconsistente()`, `IsCPFInexistente()` verificam motivos nos bloqueios.
- ✅ `Usuario.IsBloqueado()` considera apenas `CPF_DADOS_INCONSISTENTES`, `FALECIMENTO` e `CPF_INEXISTENTE` (os motivos de CNPJ **não** entram).
- ✅ Endpoints: `POST /usuario/bloquear`, `POST /usuario/desbloquear` (papel `OperadorSO`, `LogAudit`) e `GET /usuario/motivacao-bloqueio-usuario`; `POST /pessoa-fisica/desbloquear-dados-inconsistentes` e `POST /pessoa-juridica/desbloquear-dados-inconsistentes` (anônimos).

## Inferências e limitações
- 🔶 `BloquearUsuarioHandler` captura qualquer exceção e apenas a registra em log: o chamador (inclusive o job) não recebe falha. Se o operador de sistema não tiver a funcionalidade 36 (R3), o job registra a notificação e segue sem bloqueio.
- ✅ `Usuario.Desbloquear` limpa `Bloqueios` inteiro (`Bloqueios.Clear()`); `DesbloquearUsuarioHandler` usa outro caminho: `BloqueioUsuario.DesbloquearUsuario`, que preenche `UsuarioDesbloqueio` e `DataDesbloqueio`. Os dois coexistem.
- 🔶 Em `BloqueioUsuario.DesbloquearUsuario` a condição é `IsTrue(Motivacao == FALECIMENTO, …)`, que geraria a mensagem de "falecido" justamente quando o motivo **não** é falecimento (lógica invertida em relação à mensagem). Além disso o contrato (`DefaultContratValidation`) não é adicionado às notificações do bloqueio, e o handler não consulta `IsValid` dele: portanto a regra R7 **não tem efeito comprovado**. Não testado.
- ✅ (lote 3) `ConsultarBloqueioUsuario` e `ConsultarUsuarioEstaBloqueado` só consideram bloqueios com `DataDesbloqueio == null`; portanto desbloquear pelo `BloqueioUsuario` (que preenche a data) libera o login e o novo bloqueio, e a linha antiga fica como histórico.
- 🔶 Divergência: `Usuario.IsBloqueado()`, `IsFalecido()` e similares olham todos os `Bloqueios`, inclusive os já desbloqueados. Quem usa essas propriedades pode tratar como bloqueado um usuário já liberado.
- 🔶 `Usuario.Desbloquear` (`Bloqueios.Clear()` com `AllDeleteOrphan`) apagaria as linhas, ao contrário do caminho do handler; não se sabe se é usado.
- ❓ Regras de desbloqueio automático por dados inconsistentes (`DesbloquearUsuarioDadosInconsistentes`) e integração com PeoplesCheck (lote 7).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Ler `DesbloquearUsuarioDadosInconsistentes` e as extensões de consulta (`Motivacao(...)`), e confirmar a inversão em `BloqueioUsuario.DesbloquearUsuario`.
- Fontes acrescentadas no lote 3: ver [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Banco-e-Mapeamentos|Banco-e-Mapeamentos]].
