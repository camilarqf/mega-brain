---
type: analysis-log
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: pendente
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - frontend-ouvidoria
  - pendencias
  - duvidas
---

# Pendências — Frontend Ouvidoria

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Registro-de-Analise|Registro-de-Analise]]

## Perguntas de negócio
- [ ] Qual é o nome oficial deste front-end? É o `SistemaOuvDF` apontado por `configuration/front-end-urls`? (`Frontend-Ouvidoria` é rótulo provisório.)
- [ ] Qual é o repositório do terceiro front-end (SIC, `SistemaSicDF`)?

## Perguntas técnicas
- [ ] Qual versão de Node/AngularJS é a oficial? (`.tool-versions` = Node 6.17.1; `Dockerfile` e README = Node 10.)
- [ ] Onde estão `Web.config`, `Web.Producao.config` e `auth.html` exigidos pelo Gulp? A hospedagem é IIS?
- [ ] O ambiente `Treinamento` (`Properties/PublishProfiles`) ainda existe?
- [ ] Quais rotas estão em uso: `/painel-avaliacao`, `/exportar-pdf/:id`, `/listaDeNotificacao`, `/criarFormulario`, `/bloquear-usuario` têm templates, controllers ou serviços ausentes? Há outro código (ou branch) que os define?
- [ ] `app/api.config.js` e `app/views-dist.js` (gerados) devem estar versionados?
- [ ] **Segurança (🔴)**: o login/senha fixos de `app/login/login-ctrl.js` e a `application-key` do interceptor são reais/ativos? Trocar a senha e rever o histórico do Git.
- [ ] A `application-key` é segredo ou apenas identificador da aplicação?
- [ ] O token é cancelado no servidor no logout? Qual o tempo de expiração? O frontend não trata expiração.
- [ ] Quem emite o `sessionId` de `/#/auth/{sessionId}` e qual é o repositório desse front-end?
- [ ] Os códigos de ação (`MPR_MNF`, `RPT_DFN`, `RPT_PRL`, `RPT_CMP`, `RGT_PRV`, `TRM_MNF`, `TRM_SEC`, `PRG_PRZ`, `NVL_MNF`, `RCL_INT`, `RCL_PAR`, `RCL_SEC`, `CMP_MNF`) têm esse significado no backend?
- [ ] Os limites de texto (providência 1000; respostas 8000; relato 13000; motivações 2240/2400) são os mesmos do backend? O limite de anexos (40 MB no backend) é validado em `arquivo/validar`?
- [ ] O que significam as motivações de bloqueio `Id` 1 (PF) e 5 (PJ) e o prazo de 24 h após 2 tentativas?
- [ ] O padrão de 20 dias em `prorrogacao.QtdDias` é regra de negócio?
- [ ] O `Bloquear` dos atributos de formulário (Data, Hora, TextoSimples) bloqueia o quê?
- [ ] Quem é o dono de `Servico-Localizacao-CGDF` e `Servico-WMS-Ortofoto-DF`? O primeiro é o mesmo do Frontend Cidadão?
- [ ] A notificação de prazo (`grid-prazo`, `form-prazo`) e os relatórios `rel_*` ainda são necessários? Hoje não há rota.
- [ ] Os 7 caminhos sem correspondência no backend (`operador`, `notificacao`, `notificacoes`, `acao-para-remover-notificacao`, `unidade/subordinadas`, `unidade/tipo-unidade`, `manifestacao/securityId`) foram removidos?

## Cobertura a completar
- [ ] Lote 6: ler templates de conta/registro, `app/shared/*` e as diretivas de formulário.
- [ ] Lote 7: confrontar payloads e códigos de ação com os controllers do backend.
- [ ] Executar build (`npm ci` + `gulp homolog` em Node 10) para validar a estrutura de saída (requer aprovação).
- [ ] Identificar o repositório do front-end SIC e do que emite o `sessionId`.

## Resolvido
- [x] Repositório identificado e associado ao PARTICIPA-DF (2026-10-18, plano aprovado pela responsável).
