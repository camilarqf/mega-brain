---
type: index
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - moc
  - frontend-sic
---

# PARTICIPA-DF — Frontend SIC (índice)

Sistema: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|PARTICIPA-DF]] · [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Outros front-ends: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Cidadão]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Ouvidoria]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ SPA **AngularJS 1.5** (módulo `Ouv-DF`, título "SIC-DF", subtítulo "Serviço de Informação ao Cidadão") com build Gulp 3, usada pelos **operadores das unidades do SIC (Lei de Acesso à Informação)**: caixa de entrada de pedidos, detalhamento e tratamento (respostas, recursos de 1ª/2ª/3ª instância, decisões, omissão de resposta, SEI, reencaminhamento, prorrogação de prazo), registro de pedido em nome do cidadão, cadastro de conta do solicitante por operador, super-busca e área gerencial (operadores, perfis, unidades e feriados). Consome o `participa-df-backend`.

🔶 **Origem e nome.** O código é um *fork* do front de Ouvidoria: módulo `Ouv-DF`, `package.json` com nome `OuvCidadania.Ui`, mesma estrutura de pastas e mesmo mecanismo de login assistido. `Frontend-SIC` é rótulo desta análise (não nome oficial). 🔶 Seria o `SistemaSicDF` para onde o [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Frontend Cidadão]] redireciona; a correspondência não está confirmada (ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]]).

## Notas (links)
**Visão geral**
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Stack-e-Dependencias|Stack-e-Dependencias]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Arquitetura|Arquitetura]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Perfis-e-Ambientes|Perfis-e-Ambientes]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Rotas-e-Telas|Rotas-e-Telas]]

**Segurança e fluxos**
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao|Fluxo-Autenticacao]]

**Fluxos**
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Caixa-de-Entrada-e-Detalhamento|Fluxo-Caixa-de-Entrada-e-Detalhamento]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Prorrogacao-e-Reencaminhamento|Fluxo-Prorrogacao-e-Reencaminhamento]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Registro-por-Operador|Fluxo-Registro-por-Operador]]

**Módulos**
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Gerencial|Modulo-Gerencial]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Conta-por-Operador|Modulo-Conta-por-Operador]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Super-Busca|Modulo-Super-Busca]]

**API e integrações**
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Integracoes-Externas|Integracoes-Externas]]

**Qualidade**
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Testes-e-Cobertura|Testes-e-Cobertura]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]]

**Controle**
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Registro-de-Analise|Registro-de-Analise]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendencias]]

## Evidências
Repositório `participa-df-sic-frontend`, branch `master`, commit `5518a81` (2026-10-14; 225 commits desde 2021-09-19). Endereço do remoto omitido.

## Inferências e limitações
- Cobertura `parcial`; ver o registro de análise.
- A validade das notas depende do commit analisado; para atualizar, usar `atualizar-documentacao`.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Registro-de-Analise|Registro-de-Analise]] (próximo passo exato).
