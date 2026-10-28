---
type: system
aliases:
  - "PeoplesCheck — contexto do sistema"
system: PeoplesCheck
status: confirmado
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
sources:
  - pom.xml
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/PeopleController.java
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/ChallengeController.java
  - .jenkins-pipelines/deployment.params.yml
---
# PeoplesCheck — contexto do sistema

Voltar: [[01-Sistemas/PeoplesCheck/PeoplesCheck-Index|Índice do sistema]]

## Objetivo
Validar a identidade de uma pessoa a partir do CPF (ou CNPJ) sem expor os dados cadastrais antes da prova: o serviço confere o documento, gera um **desafio** (três perguntas com respostas mascaradas) e só devolve os dados principais da pessoa quando as respostas conferem.

## Evidências
- `pom.xml`: `<description>API de validação CPF/CNPJ</description>`, artefato `peoplescheckapi`.
- `.jenkins-pipelines/deployment.params.yml`: nome da aplicação `Peoples Check API`.
- Controllers `PeopleController`, `ChallengeController` e `JobsController`; textos das perguntas em `application.properties` (`pf.challenge.question.*`).

## Informações confirmadas
- ✅ Dois grupos de casos de uso: (1) consultar um CPF/CNPJ e abrir um desafio; (2) responder o desafio e receber os dados principais. Ver [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação de pessoa]] e [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]].
- ✅ Consulta cadastral em CouchDB (réplicas de CPF e CNPJ) e estado dos desafios em MongoDB. Ver [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco e persistência]].
- ✅ Consumidor conhecido: backend do `PARTICIPA-DF` (ver [[Mapa-de-Integracoes|Mapa de integrações]]).
- ✅ Dono: CGDF (informado pelo usuário em 2026-10-19). SLA e URLs por ambiente não identificados.

## Inferências e limitações
- 🔶 Origem e atualização das réplicas CouchDB (`chcpf_replica`, `chcnpj_replica`) não constam no repositório.
- ❓ Finalidade institucional detalhada (cadastro de cidadão, vínculo CPF–CNPJ) vem do consumidor, não deste código.

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/PeoplesCheck/Servico/99-Controle/PeoplesCheck-Servico-Pendencias|Pendências]].
