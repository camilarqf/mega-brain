---
type: analysis-log
system: SICI
repository: sici-backend
status: pendente
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
created: 2026-10-16
updated: 2026-10-18
tags:
  - sici
  - pendencias
  - duvidas
---

# Pendências e pontos a confirmar

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/99-Controle/Registro-de-Analise|Registro-de-Analise]], [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Debitos-Tecnicos]]

## Perguntas de negócio (confirmar com o time)
- [ ] Expansão oficial das siglas **SICI**, **OSI**, **POAC**, **SUBCI**, **RP / RPM / RM** — ver [[01-Sistemas/SICI/Backend/01-Visao-Geral/Glossario|Glossario]].
- [ ] A validação de documento por QR Code (`GET /assinaturas/validacao`) deveria ser **pública**? Hoje exige autenticação (não está no `permitAll` de `SecurityConfig`). Existe outro sistema que faz a validação pública?
- [ ] Na Ação de Auditoria, a mensagem de erro cita "Riscos", mas o código aceita **Governança** (`AcaoControle.validarNaturezaAcaoControle`). Qual é a regra correta?
- [x] Regra de geração do código da Ação de Controle → resolvido no lote 5: o "contador" é `MAX(codigo)` do ano (`countByAnoCadastro`), e o código tem formato `SSSSAAAA`. Ver [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]].

## Perguntas técnicas
- [ ] Qual profile Spring é ativado de fato no container? O Dockerfile usa `-P SPRING_PROFILES_ACTIVE` literal — ver [[01-Sistemas/SICI/Backend/01-Visao-Geral/Stack-e-Dependencias|Stack-e-Dependencias]].
- [ ] Como as migrations são aplicadas em hom/prod, com Flyway desabilitado nesses profiles?
- [ ] O Testcontainers PostgreSQL é usado em algum teste? O banco real é SQL Server.
- [ ] `spring-boot-starter-cache` / `-aop` são usados? (nenhum `@Cacheable`/`@EnableCaching`/aspecto encontrado)
- [ ] Qual é o serviço externo de geração de PDF e qual o contrato dele? (`PdfService`)
- [ ] Qual é o frontend consumidor desta API?

## Perguntas surgidas no lote 2
- [ ] **Numeração oficial**: o sequencial deveria ser por UAI e ano (como diz o nome do método e como era a unique da V20) ou só por ano (como funciona hoje)? Já houve números duplicados em produção? — ver [[01-Sistemas/SICI/Backend/02-Dominio/Banco-e-Migrations|Banco-e-Migrations]].
- [ ] A V44 (`DROP TABLE` da numeração) foi aplicada em produção com dados? Como a numeração anterior foi preservada?
- [ ] Linhas antigas de `TB_ORDEM_SERVICO` receberam `ID_STATUS = 1` (= ENVIADA pelo ordinal) na V16? — ver [[01-Sistemas/SICI/Backend/02-Dominio/Enums-e-Estados|Enums-e-Estados]].
- [ ] Há relatórios ou consultas externas lendo `ID_STATUS`, `ID_TIPO_ACAO` etc. diretamente no banco? Esses valores são ordinais (0-based), não os ids do enum.

## Perguntas surgidas no lote 3
- [ ] Outras OS (designação, exclusão, substituição, cancelamento) **devem** exigir ABERTURA assinada? A regra existe em `OrdemServico.validarCriacaoComBaseNasOrdens`, mas nunca é chamada.
- [ ] Algum perfil deveria poder levar uma OS a ASSINADA por `PUT /alterarStatusOs` sem assinar? O frontend envia esse status em algum caso?
- [ ] Trocar o tipo/modelo de uma OS na atualização é um comportamento desejado?
- [ ] As fases das OS canceladas estão sendo apagadas ao assinar o cancelamento? — ver [[01-Sistemas/SICI/Backend/03-Modulos/Prorrogacao-e-Cancelamento|Prorrogacao-e-Cancelamento]].
- [ ] Endpoints de prorrogação, fases, justificativa de cancelamento e PDF devem ter restrição de perfil?
- [ ] A ação de controle deveria mudar de situação ao ser cancelada?

## Perguntas surgidas no lote 4
- [ ] A sigla do número oficial deve ser a da **UAI do assinante (SUBCI)** ou a da **UAI da ação de controle**?
- [ ] Onde roda a validação pública do QR Code (página do frontend)? Ela consegue chamar `/assinaturas/validacao` sem login?
- [ ] A validação deveria checar a integridade do PDF (SHA-256) e avisar se a OS foi cancelada depois de assinada?
- [ ] O download de PDFs assinados deve ser restrito por perfil ou por participação na ação?
- [ ] O perfil gravado na assinatura deveria ser sempre SUBCI, e não o primeiro perfil do auditor?
- [ ] Qual é o serviço externo de PDF (tecnologia, responsável, timeouts esperados)?

## Perguntas surgidas no lote 5
- [ ] **Urgente**: algum controle fora do backend (gateway, frontend) impede um auditor comum de chamar `POST /subci/cadastrar` ou `POST /subci/{id}/substitutos` e se tornar assinante? — ver [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]].
- [ ] A ação de controle pode ser alterada depois da OS de abertura assinada?
- [ ] OS genérica assinada pode ser excluída? Hoje pode — ver [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]].
- [ ] As situações `EM_PLANEJAMENTO` a `FINALIZADO_*` são alteradas por quem e quando?
- [ ] Cadastro de POAC deve ter restrição de perfil e validação de datas e ano?
- [ ] Como os auditores são cadastrados e inativados (`TB_AUDITOR`)? Não há API.

## Perguntas surgidas no lote 6
- [ ] Swagger, `/prometheus` e `/healthcheck` com detalhes devem ficar públicos em produção?
- [ ] A dependência do health no Keycloak é intencional? (risco de reinício em cascata)
- [ ] O `security.super-users` ainda é usado? O super-usuário não acessa nenhum endpoint com role.
- [ ] Há plano de migrar o login de ROPC para Authorization Code + PKCE no frontend?
- [ ] A suíte de testes roda em algum pipeline? Hoje o build da imagem pula os testes.

## Próximos passos sugeridos (fora do escopo desta análise)
- [ ] Analisar o repositório `sici-frontend` (ainda não analisado; HEAD local `7f497cc` em 2026-10-18) e só então consolidar a visão de negócio em [[01-Sistemas/SICI/Contexto-do-Sistema|Contexto-do-Sistema]].
- [ ] Decidir se a base pode ser sincronizada com o remoto do cofre (ver `BRAIN-RULES.md`: classificar o conteúdo e confirmar se o remoto é autorizado).
- [ ] Validar os itens 🔶 com testes ou consultas em homologação (duplicidade de numeração, fases apagadas no cancelamento, `ID_STATUS` legado).
- [ ] Revisar com o time os débitos 🔴 de [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Debitos-Tecnicos]].

## A investigar (histórico dos lotes)
- [x] Lote 2: entidades JPA × tabelas, relacionamentos e evolução do schema.
- [x] Lote 3: `fasesReconectadas` descartado em `OrdemServico.cancelar` → provável perda de fases (ver acima). `OrdemServico.id()` só é chamado em teste (`FaseOrdemServicoMapperTest`, linha 67), que recebe `null` sem perceber.
- [x] Lote 6: `java.lang.module.ResolutionException` não tem handler e não há handler genérico → 500 (`/error` padrão).
- [x] Lote 4: a ausência de lock no cálculo `max + 1` **não** é compensada no código (sem lock, sem unique, isolamento padrão e uma chamada HTTP no meio). O risco de duplicidade continua; confirmar nos dados.
- [x] Lote 4: algoritmo de `VerifyCode.forOS` / `forDocumento`, o que é coberto pelo hash SHA-256 e como funciona a validação → [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]].
- [x] Lote 5: `AcaoControle.alterarSituacaoAC` é chamado só na assinatura da ABERTURA (→ `OSI_EMITIDA`); na prática só altera `situacao`.
- [x] Lote 6: matriz completa de endpoints × roles → [[01-Sistemas/SICI/Backend/05-API/Catalogo-de-Endpoints|Catalogo-de-Endpoints]], [[01-Sistemas/SICI/Backend/06-Seguranca/Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]].
