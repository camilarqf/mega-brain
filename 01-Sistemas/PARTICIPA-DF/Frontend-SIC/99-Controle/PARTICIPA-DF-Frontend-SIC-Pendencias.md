---
type: analysis-log
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: pendente
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - pendencias
  - duvidas
---

# Pendências — Frontend SIC

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Registro-de-Analise|Registro-de-Analise]]

## Perguntas de negócio
- [ ] Qual é o nome oficial deste front-end? É o `SistemaSicDF` apontado por `configuration/front-end-urls`? (`Frontend-SIC` é rótulo provisório.)

## Perguntas técnicas
- [ ] Qual versão de Node é a oficial? (`Dockerfile` usa 10.17.0; não há `.tool-versions` nem README.)
- [ ] Onde estão `Web.config`, `Web.Producao.config` e `auth.html` exigidos pelo `gulpfile.js`? A hospedagem em IIS ainda existe, ou foi substituída pelo `nginx`?
- [ ] A variável `ENVIRONMENT` dos `*.env.yml` é usada pelo pipeline? O pipeline passa `--build-arg profile`?
- [ ] Qual a finalidade das regras para `/participa-df-sic-test/` em `nginx.conf`?
- [ ] A rota `/bloquear-usuario` (sem controller nem template) e `visualizar-conta` (sem rota) ainda são necessárias?
- [ ] **Segurança (🔴)**: a `application-key` do interceptor é segredo ou só identificador da aplicação? Se segredo, rotacionar e rever o histórico do Git.
- [ ] Qual o tempo de expiração do token? O backend o invalida no logout?
- [ ] Quem emite o `sessionId` de `/#/auth/{sessionId}` e qual é o repositório do front-end de login?
- [ ] Os códigos de ação (`PRG_PDD`, `RPT_PDD`, `RRE_PDD`, `RPT_RPI`, `RPT_RSI`, `RPP_RTI`, `RPP_NOR`, `RGS_SEI`, `DCS_RTI`, `DCS_NOR`, `RPD_PDD`, `MPR_PDD`, `NXR_RQN`, `RMV_RQV`) têm o significado inferido dos rótulos?
- [ ] Qual a regra de sigilo na resposta (`comboGrauSigilo.splice(2)` e `GrauSigilo.Id == 2`)?
- [ ] Os endpoints `notificacao/omissao-resposta-cgdf/registrar-resposta` e `.../registrar-decisao` devem ter autorização explícita no backend (constam como "sem atributo")?
- [ ] O limite de anexos de 25 MB (front e `nginx`) é o desejado, considerando o acréscimo do base64 e os 40 MB do backend?
- [ ] Os motivos de bloqueio `Id` 1 (PF) e 5 (PJ) e a regra de 2 tentativas / 24 h são os do backend?
- [ ] Quantos dias a prorrogação concede no SIC? (o front só envia a justificativa.)
- [ ] Há etapas de teste ou lint no pipeline externo?
- [ ] Corrigir os defeitos D1 a D4 e tratar S1 de [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]].

## Cobertura a completar
- [ ] Lote 6: ler os templates de detalhamento, registro, conta e gerencial e as diretivas `app/shared/*`.
- [ ] Lote 7: confrontar payloads e códigos de ação com os controllers do backend.
- [ ] Executar `npm install` + `gulp prod` em Node 10 para validar a saída do build (requer aprovação).
- [ ] Confirmar o nome oficial do front-end e a correspondência com `SistemaSicDF`.

## Resolvido
- [x] Repositório identificado e associado ao PARTICIPA-DF (2026-10-18, plano aprovado pela responsável). Resolve a pendência "front-end SIC não identificado" de [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências do Frontend Ouvidoria]] quanto ao repositório (a correspondência com `SistemaSicDF` segue 🔶).
