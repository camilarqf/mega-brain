---
type: module
aliases:
  - "SCI Frontend — módulo PIP (processo investigativo preliminar)"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/pages/pip
  - src/app/store/services/pip.service.ts
  - src/app/store/services/diligencia.service.ts
  - src/app/core/guard/alterar-pip.guard.ts
  - src/app/core/enums/status-pip-enum.ts
---
# SCI Frontend — módulo PIP (processo investigativo preliminar)

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Documentar as telas do PIP: instauração, edição, análise, revisão, diligências e caixas de entrada.

## Evidências
- `pages/pip` (`pip-instauracao`, `pip-editar`, `pip-analise`, `pip-diligencia`, `caixa-entrada-pip`), `pip.service.ts` (cerca de 230 linhas) e `diligencia.service.ts`, enum `status-pip-enum.ts`, `AlterarPipGuard`.

## Informações confirmadas
### Instauração (`/pages/pip/instaurar`)
- ✅ Telas e perfis pela rota; 🔶 a ordem e a ligação de cada tela com o endpoint vêm dos nomes, sem leitura completa dos componentes: lista da unidade → **iniciar despacho** (Apoio; minuta, `PUT pip/atualizar-minuta`) → **concluir despacho** (Autoridade e Apoio; `pip/concluir-ato-instauracao`) → **visualizar e assinar despacho** (Autoridade; `pip/assinar-minuta`) → **registrar número SEI** (Apoio; `pip/atualizar-dados-sei`) → **designar investigadores** (Gestor Pip; `pip/designar-relatoria`).
- ✅ Dados vindos da admissibilidade são recuperados por `GET pip/recuperar-admissibilidade/{id}` e `GET analise-admissibilidade/por-pip`.

### Edição / cadastro (`/pages/pip/editar`)
- ✅ Lista do investigador (`pip-list`, filtra por status do próprio PIP) e cadastro de fatos, envolvidos, condutas e evidências (com `AlterarPipGuard` nas rotas de fato). Concluir cadastro: `POST pip/concluir-cadastro`; salvar: `PUT pip/atualizar-cadastro`.
- ✅ Relatório: `GET pip/relatorio/{id}?gerarAssinaturas=true` e assinatura em `assinar-relatorio-pip` (`POST pip/assinar-relatorio`, modal do investigador).

### Análise e revisão (`/pages/pip/analisar/:idPip`)
- ✅ Matriz, registro de análise por envolvido, fundamentação, **providências adicionais**, visualização, reprovação e conclusão de revisão (`PUT analise-pip`, `POST analise-pip/concluir`, `POST revisao-pip/admitir-revisao-preliminar`, `reprovar`, `concluir`, `atualizar-revisao`).
- ✅ Notas do assessor da autoridade: `analise-pip/criar-nota`, `atualizar-nota` e `concluir-nota`.

### Diligências (`/pages/pip/diligencia`)
- ✅ Cadastro, edição e lista por PIP; tipos em `GET tipo-diligencia`; vincular ou desvincular à matriz por `POST diligencia/{id}/vincular-matriz` e `.../desvincular-matriz`.

### Caixas de entrada e ações de gestão
- ✅ Visões por perfil: relator/investigador, revisor, autoridade, apoio, gestor e assessor da autoridade (`GET pip/visao-*`), todas paginadas e filtráveis (`build-filtro-pip-params.factory.ts`).
- ✅ Ações: redistribuir relatoria (`POST pip/redistribuir`; Gestor Pip e Autoridade), reabrir (`POST pip/reabrir-pip`), concluir (`POST pip/concluir`) e finalizar (`POST pip/finalizar`; o histórico Git traz o commit `7a12f0e` "permitir que apoio correcional finalize processos").

### Status no cliente (`StatusPipEnum`)
`ADI` Aguardando designação dos investigadores, `ACM` Aguardando conclusão da minuta, `ADA` Aguardando despacho da autoridade, `ARS` Aguardando registro no SEI, `EC` Em cadastro, `EA` Em análise, `ERR`/`ERG`/`ERA` Em revisão (Revisor, Gestor, Autoridade), `AAI`/`AAR`/`AAG`/`AAA` Aguardando assinatura (Investigador, Revisor, Gestor, Autoridade), `PC` Processo concluído, `AF` Aguardando finalização.

## Inferências e limitações
- ✅ Na lista do investigador (`listar-pip-investigador`), os PIPs só aparecem se o status estiver em `EC, EA, ERG, AAI, AAG, AAS, PC, ERR, AAR, ERA, AG, AAA, AF` (`AAS` e `AG` não existem em `StatusPipEnum`; origem não identificada).
- ❓ Significado de "matriz" (pendência 5 do backend) e conteúdo de "providências adicionais" não estão definidos no cliente.
- Telas de formulário e modais lidos por amostragem.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|Módulo do backend]] · [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Ciclo-do-PIP|Fluxo do ciclo do PIP]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Assinatura-e-Validacao|Assinatura e validação]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
