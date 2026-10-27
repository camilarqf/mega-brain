---
type: analysis-log
system: PARTICIPA-DF
repository: participa-df-frontend
status: pendente
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - frontend-cidadao
  - pendencias
  - duvidas
---

# Pendências — Frontend Cidadão

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Registro-de-Analise|Registro-de-Analise]]

## Perguntas de negócio
- [ ] Qual é o nome oficial deste front-end entre os 3 do Participa? (`Frontend-Cidadao` é rótulo provisório.)
- [ ] Quais são os repositórios dos outros dois front-ends (Ouvidoria e SIC) e quem consome o `sessionId` de `security/notify`?
- [ ] Os canais que usam `registro-manifestacao-integrada/:tipoEntrada/:classificacao/:assunto` (quem gera esses links)?
- [ ] O pedido (SIC) deve continuar exigindo conta, diferente da manifestação (que aceita anonimato)?

## Perguntas técnicas
- [ ] Quem é o dono do `Servico-Localizacao-CGDF` e ele é o mesmo que o backend usa como `Servico-Geocodificacao`? O serviço precisa do `Bearer` do Participa?
- [ ] Qual ambiente (sandbox, staging, prod) corresponde a cada perfil de build (`homolog`, `production`)? Quem executa o build e o deploy (o `web.config` indica IIS)?
- [ ] `security/notify` e o login assistido: o `sessionId = MD5(token)` é exigência do backend/dos outros front-ends?
- [ ] O token é cancelado no servidor no logout? (O frontend não chama `CancelarToken`.) Há tempo de expiração e tratamento de `401`?
- [ ] O que o backend faz com `notificarExistencia: true` em `pessoa-fisica/existe` e `pessoa-juridica/existe`?
- [ ] O que significam `ExceptionDetails.Id` 1 e 5 no login (bloqueio PF/PJ)? Conferir em [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Bloqueio-de-Usuario|Bloqueio-de-Usuario]].
- [ ] O `AuthGuard` deve realmente redirecionar duas vezes quando há pendência de LGPD/senha?
- [ ] O limite de anexos (4 MB total/arquivo) é regra de negócio ou técnica? O backend impõe o mesmo?
- [ ] Um registro de pedido com vários órgãos gera um pedido por órgão (`Lote`)?
- [ ] O componente `Example` (rota `example`) deve estar em produção?

## Cobertura a completar
- [ ] Lote 6: relato/complementares/local do fato, `layout/`, modelos.
- [ ] Lote 7: confrontar verbo/payload das chamadas com os controllers do backend.
- [ ] Executar `ng test --watch=false --code-coverage` e `ng build` para medir testes e build (requer aprovação).

## Resolvido
- [x] Repositório do frontend identificado e associado ao PARTICIPA-DF (2026-10-18, confirmado pela responsável).
