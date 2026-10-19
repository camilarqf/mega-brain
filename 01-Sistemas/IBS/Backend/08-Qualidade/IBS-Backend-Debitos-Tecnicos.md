---
type: technical-debt
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - debitos-tecnicos
sources:
  - src/main/java/br/gov/df/cg/ibs/application/autenticacao/services/AutenticacaoService.java
  - src/main/java/br/gov/df/cg/ibs/api/exceptions/GlobalExceptionHandler.java
  - src/main/java/br/gov/df/cg/ibs/infra/ldap/LdapBindService.java
  - src/test/java/br/gov/df/cg/ibs/api/usuarios/UsuarioControllerTest.java
---
# IBS Backend — débitos técnicos e riscos

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Separar fatos verificados de recomendações. As recomendações são sugestões, não decisões.

## Evidências
- Arquivos em `sources` e as demais notas do componente.

## Informações confirmadas (fatos)
1. **Sem controle de acesso** em nenhuma rota, inclusive `/usuarios/*` com dados pessoais ([[01-Sistemas/IBS/Backend/06-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Segurança]]).
2. **`X-IBS-Secret` enviado pelo Keycloak não é validado**; correlação divergente (`X-Correlation-ID` × `X-Correlation-Key`).
3. **Credenciais em texto claro** em `application-local.properties` (fora do Git; inclui credenciais comentadas de outros ambientes).
4. **LDAP sem TLS** (`ldap://`, bind simples).
5. **Cache de fonte recente sem limite de entradas** (`ConcurrentHashMap` em `AutenticacaoService`; remove só ao ler entrada expirada); cresce com pares órgão+login distintos durante 30 dias.
6. **Erros sem handler viram 500:** órgão sem fonte, banco indisponível, `IdentidadeInstitucionalIndisponivelException`, `MediatorException`; o Keycloak os trata como `server_error` (iguais aos 503).
7. **Vários binds por tentativa:** o loop continua após credencial inválida (risco de bloqueio de conta em mais de um AD).
8. **Testes quebrados:** 4 em `UsuarioControllerTest` (rota `/usuarios/busca` errada) e 1 de integração dependente de banco real.
9. **Código sem uso encontrado:** `Bus`, `EventHandler`, `Listener`, `domain.events.Event`, `application.exceptions.Exception`, `ObterIdentidadeInstitucionalHandler` (sem consumidor além da configuração), `ObterFontesPorSufixoHandler` e `ResolverFontesPorOrgaoHandler` (só testes), `LdapBindService.autenticar(fonte, …)` sem servidor, `LoginUsuario.mascararLogin()`.
10. **Duplicação:** dois `LoginUsuario` (`_sharedkernel` e `fonteautenticacao`); ordenação por menor id de servidor repetida em `FonteAutenticacaoCacheService`, `ResolverFontesAutenticacaoService`, `AutenticacaoService` e no mapper.
11. **Configuração duplicada de timeout:** `ServidorAutenticacao.timeoutMs` (5000, de `catalogo.timeout-padrao-ms`) é exposto mas o bind usa `ibs.ldap.timeout-ms` (3000).
12. **Sem auditoria nem métricas de negócio** (`infra/data/auditoria` e `infra/services/observabilidade` vazios); sem medição de cobertura de testes.
13. **N+1 em unidades** (`ObterUsuarioHandler`, `IdentidadeInstitucionalService`) e contagem de `totalElements` por linha, não por pessoa.
14. **README** descreve responsabilidades "futuras" (OIDC, fontes corporativas) que o código não implementa.

## Inferências e limitações (recomendações)
- 🔶 Proteger as rotas (ou garantir isolamento de rede) e validar o segredo compartilhado.
- 🔶 Rotacionar as credenciais do arquivo local e removê-las; usar variáveis de ambiente também no perfil `local`.
- 🔶 Usar `ldaps`/StartTLS; avaliar parar na primeira credencial inválida conforme a regra de negócio.
- 🔶 Limitar o cache de fonte recente (ex.: Caffeine com tamanho máximo).
- 🔶 Tratar as exceções restantes no `GlobalExceptionHandler` com status coerente (503 para indisponibilidade de banco).
- 🔶 Corrigir os testes e marcar o de integração por perfil/tag.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Pendencias|Pendências]] · [[01-Sistemas/IBS/Backend/08-Qualidade/IBS-Backend-Testes-e-Cobertura|Testes]]

## Pendências e próximo passo
- Priorizar com a equipe; nenhuma alteração de código foi feita.
