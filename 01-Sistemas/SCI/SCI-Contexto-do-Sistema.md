---
type: system
aliases:
  - "SCI — contexto do sistema"
system: SCI
repository: sci-backend
status: pendente
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
---
# SCI — contexto do sistema

Voltar: [[01-Sistemas/SCI/SCI-Index|SCI]]

> ⚠️ **Visão a partir do backend apenas.** A visão de negócio compartilhada continua `pendente` até a análise do frontend. Expansão da sigla SCI não consta no código.

## Objetivo
Resumir, com base no código do backend, o que o SCI faz.

## Evidências
- Repositório `sci-backend`, commit `8e3c8648`. Detalhes e símbolos em cada nota linkada.

## Informações confirmadas
- **Domínio**: área correcional (perfis "Autoridade Correcional" e "Apoio Correcional"; 🔶 deduzido dos nomes dos perfis) com fluxo de **denúncia → demanda → processo de admissibilidade → processo investigativo preliminar (PIP)** — [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo denúncia até admissibilidade]], [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|Ciclo do PIP]].
- **Denúncias** chegam do `PARTICIPA-DF` por mensageria; a autoridade correcional aceita ou recusa e o resultado volta por mensageria — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denúncia e Demanda]].
- **Análise de admissibilidade**: envolvidos, fatos, evidências, tipificações e recomendações; gera **nota técnica** assinada em cadeia por perfis — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Processo de Admissibilidade]].
- **Encaminhamento** do processo a outras unidades — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Encaminhamento|Encaminhamento]].
- **PIP**: designação de relatoria, minuta (ato de instauração), diligências, análise, revisões e relatório assinado — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]].
- **Atores e perfis**: 11 perfis estáticos — [[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização]].
- **Termos**: [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Glossario|Glossário]].

## Inferências e limitações
- 🔶 Telas, jornadas e regras só do frontend: não identificadas.
- 🔶 O SEI é referenciado por número de processo digitado; não há cliente de integração com o SEI.
- Riscos conhecidos: [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/SCI/SCI-Repositorios|Repositórios]] · [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Pendências e próximo passo
- Analisar o frontend quando identificado (ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]]).
