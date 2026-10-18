---
type: index
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - participa-df
  - moc
  - frontend-cidadao
---

# PARTICIPA-DF — Frontend Cidadão (índice)

Sistema: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|PARTICIPA-DF]] · [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ SPA Angular 13 (`participa-df-frontend`, pacote `eou-df`) que apresenta a home "Participa DF" e permite ao cidadão: criar e manter conta (PF/PJ), fazer login, registrar **manifestações de ouvidoria** e **pedidos de acesso à informação (SIC)**, e acompanhá-los (complementar, avaliar, recorrer, responder pesquisas) na caixa de entrada. Consome o backend `participa-df-backend`.

🔶 **Nome do componente.** O Participa tem 3 front-ends (informação do time); este repositório é o voltado ao cidadão (registro, caixa de entrada e conta). `Frontend-Cidadao` é um rótulo desta análise, **não** um nome oficial: confirmar e, se houver outro, renomear com `git mv` e atualizar os links (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]). Os outros dois são, 🔶, os front-ends de Ouvidoria (`SistemaOuvDF`) e SIC (`SistemaSicDF`) a que a SPA redireciona; **não analisados**.

## Notas (links)
**Visão geral**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Stack-e-Dependencias|Stack-e-Dependencias]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Arquitetura|Arquitetura]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Perfis-e-Ambientes|Perfis-e-Ambientes]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Rotas-e-Telas|Rotas-e-Telas]]

**Fluxos**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/02-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Autenticacao|Fluxo-Autenticacao]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/02-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Cadastro-de-Conta|Fluxo-Cadastro-de-Conta]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/02-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Registro-de-Manifestacao|Fluxo-Registro-de-Manifestacao]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/02-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Registro-de-Pedido|Fluxo-Registro-de-Pedido]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/02-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Caixa-de-Entrada|Fluxo-Caixa-de-Entrada]]

**API e integrações**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas-de-API]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas|Integracoes-Externas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

**Segurança e qualidade**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/04-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Testes-e-Cobertura|Testes-e-Cobertura]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Debitos-Tecnicos]]

**Controle**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Registro-de-Analise|Registro-de-Analise]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendencias]]

## Evidências
Repositório `participa-df-frontend`, branch `master`, commit `d250804` (2026-07-03). Endereço do remoto omitido.

## Inferências e limitações
- Cobertura `parcial`: componentes de `layout/`, telas de relato/complementares/local do fato, páginas estáticas e modelos foram lidos só por chamadas ou nome.
- A validade das notas depende do commit analisado; para atualizar, usar `atualizar-documentacao`.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Registro-de-Analise|Registro-de-Analise]] (próximo passo exato).
