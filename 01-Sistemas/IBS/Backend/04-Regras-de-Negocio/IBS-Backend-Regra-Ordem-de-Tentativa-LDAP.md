---
type: business-rule
aliases:
  - "IBS Backend — regra: ordem de tentativa, fallback e fonte recente"
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - src/main/java/br/gov/df/cg/ibs/application/autenticacao/services/AutenticacaoService.java
  - src/main/java/br/gov/df/cg/ibs/infra/ldap/LdapBindService.java
  - src/test/java/br/gov/df/cg/ibs/application/autenticacao/AutenticarUsuarioHandlerTest.java
---
# IBS Backend — regra: ordem de tentativa, fallback e fonte recente

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar como o IBS ordena e repete os binds LDAP e quando decide que a credencial é inválida.

## Evidências
- `AutenticacaoService.ordenarFontes`, `ordenarTentativas`, `autenticar`, `registrarFonteAutenticadaComSucesso`; `LdapBindService.autenticarNoServidor`; testes `intercalaServidoresEntreFontesAntesDeRepetirMesmaFonte`, `fonteBemSucedidaEhTentadaPrimeiroNasProximasAutenticacoesDoUsuario`, `credencialInvalidaSomenteEhRetornadaDepoisDeTentarTodasAsFontes`, `todasAsFontesComFalhaTecnicaGeramExcecao`.

## Informações confirmadas
- ✅ **Ordem das fontes:** a fonte "recente" do par (órgão, login em minúsculas) vem primeiro; as demais, pelo menor id de servidor.
- ✅ **Ordem das tentativas:** dentro de cada fonte, os servidores são ordenados por id e deduplicados por `endereço:porta`. A lista final é ordenada por **índice do servidor** e depois por índice da fonte; ou seja, tenta-se o 1º servidor de todas as fontes, depois o 2º de todas, e assim por diante (intercalação).
- ✅ **Fonte recente:** após um bind com sucesso, a chave da fonte (órgão, sigla, sufixo, contexto, atributo) é guardada com validade `ibs.autenticacao.fonte-recente-ttl-ms` (padrão 30 dias), em memória local da instância. A entrada expirada é removida ao ser lida.
- ✅ **Resultado de cada bind:** `Sucesso`; `CredencialInvalida` (qualquer `AuthenticationException` do JNDI, com o código `data xxx` do AD extraído quando presente); `FalhaTecnica` (`TIMEOUT`, `CONN_REFUSED`, `UNAVAILABLE`).
- ✅ **Decisão final:** o loop **não para** em credencial inválida; segue para os demais servidores/fontes. Só após esgotar: credencial inválida (401) se houve alguma; senão `SERVICO_INDISPONIVEL` (503) se houve falha técnica; senão `FONTE_NAO_ENCONTRADA`.
- ✅ Cada tentativa usa uma cópia da senha (`senhaUsuario.copia()`), zerada ao fim do bind.
- ✅ Montagem do bind: `UPN` com sufixo → `login + sufixo`; `DISPLAY_NAME` sem sufixo → `login`; qualquer outra combinação → falha técnica `UNAVAILABLE` (log "Fonte sem regra de bind LDAP").
- ✅ O timeout efetivo (conexão e leitura) é `ibs.ldap.timeout-ms` (3000 ms); o `timeoutMs` de `ServidorAutenticacao` (vindo de `catalogo.timeout-padrao-ms`, 5000) não é usado no bind.

## Inferências e limitações
- 🔶 Uma senha errada gera um bind por servidor distinto das fontes do órgão, o que pode contar várias falhas em AD diferentes (risco de bloqueio de conta). O `README.md` diz "Não realizar tentativa cega em todos os ADs"; o código limita-se às fontes do órgão informado, mas não interrompe na primeira rejeição. Decisão de negócio não identificada.
- A sobrecarga `LdapBindService.autenticar(fonte, ...)` (que percorre os servidores da fonte e para na primeira credencial inválida) não é usada no fluxo de produção.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo de autenticação]] · [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-AD-LDAP|AD/LDAP]] · [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Fontes-de-Autenticacao|Fontes de autenticação]]

## Pendências e próximo passo
- Confirmar com o negócio se a continuação após credencial inválida é intencional.
