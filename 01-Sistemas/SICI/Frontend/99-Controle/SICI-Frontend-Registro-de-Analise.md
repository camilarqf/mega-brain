---
type: analysis-log
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
created: 2026-10-18
updated: 2026-10-18
commit_data: 2026-09-29
branch: master
tags:
  - sici
  - frontend
  - controle
  - cobertura
---

# Registro de análise — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]]

## Base analisada
- Repositório: `sici-frontend` (endereço omitido); branch `master`; commit `418642f` (2026-09-29); working tree com apenas arquivos não rastreados (`.agents/`, um log `hs_err_pid*.log`), sem alteração em arquivos versionados.
- Método: leitura estática. Depois dos lotes, `ng build` (produção) e `ng test` foram executados em 2026-10-18 (resultados em [[01-Sistemas/SICI/Frontend/06-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]]); a aplicação **não** foi executada. Nenhum arquivo do repositório foi alterado (saídas temporárias removidas).
- O `HEAD` registrado antes em [[01-Sistemas/SICI/SICI-Repositorios|Repositórios]] (`7f497cc`) era só uma leitura de hash, sem análise; foi substituído por este commit.

## Regras de proteção aplicadas
- Não foram reproduzidos endereços de ambiente, IPs de servidores de deploy, nomes de credenciais do Jenkins, valores de variáveis de ambiente nem tokens; só nomes de chaves e de arquivos.
- O código não foi alterado.

## Decisões de classificação
- O repositório foi associado ao sistema `SICI` pelo catálogo (`Catalogo-de-Sistemas`) e confirmado no código: as chamadas HTTP do frontend casam com os controllers do backend já documentado (`/os-acao-controle`, `/assinaturas`, `/subci`, `/auth/login`, `/me`), e a rota `/validacao` é o destino provável do QR Code (ver [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]]).
- Componente nomeado `Frontend` (pasta `Frontend/`, prefixo `SICI-Frontend-`), igual ao componente `Backend`.
- Nomes de módulos e fluxos que existem no backend (`Acao-de-Controle`, `Ordem-de-Servico`, `OS-Generica`, `Fluxo-Assinatura-OS`, `Fluxo-Ciclo-de-Vida-OS`) levam o prefixo `SICI-Frontend-` para manter nomes de arquivo únicos (`BRAIN-RULES.md`, seção 3).
- Não foi criada nota de estado NgRx à parte (lote 6 opcional): o estado global está em [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]].

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Cadastro, retomada e esqueleto | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Index]], este registro, [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendencias]]; atualizados Repositórios, Index do sistema e Catálogo |
| 1 | Fundamentos | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Stack-e-Dependencias|Stack]], [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]] (parcial), [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Perfis-e-Ambientes|Perfis-e-Ambientes]] (parcial), [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]] |
| 2 | Segurança e sessão | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Frontend/05-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]] (parcial), [[01-Sistemas/SICI/Frontend/02-Fluxos/SICI-Frontend-Fluxo-Autenticacao|Fluxo-Autenticacao]] |
| 3 | Módulos e fluxos | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Acao-de-Controle|Acao-de-Controle]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-OS-Generica|OS-Generica]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Gestao-SUBCI-e-Perfis|Gestao-SUBCI-e-Perfis]] (todas parciais), [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]], [[01-Sistemas/SICI/Frontend/02-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]], [[01-Sistemas/SICI/Frontend/02-Fluxos/SICI-Frontend-Fluxo-Ciclo-de-Vida-OS|Fluxo-Ciclo-de-Vida-OS]] (parcial) |
| 4 | API consumida e integrações | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Frontend/04-API-e-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]] (parcial), [[01-Sistemas/SICI/Frontend/04-API-e-Integracoes/SICI-Frontend-Integracoes|Integracoes]] (parcial); atualizados Mapa de integrações (linha frontend → backend e hipótese do QR Code). Catálogo: sem ID novo |
| 5 | Qualidade | ✅ concluído | 2026-10-18 | [[01-Sistemas/SICI/Frontend/06-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/SICI/Frontend/06-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]] (parcial) |

## O que não foi coberto
- Templates HTML e SCSS (lidos só por trechos pontuais); `ordem-servico-cadastrar` (1607 linhas) e `-atualizar` (790) por trechos; `acao-controle-visualizar`/`atualizar`; `ckeditor`; modais de layout; reducers/seletores/efeitos além de OS, validação e autenticação.
- Comparação de verbo/payload/DTO de cada chamada com os controllers e DTOs do backend.
- Execução da aplicação e `npm audit`; valores de variáveis de ambiente, endereços e credenciais (não lidos de propósito).
- Notas de regra de negócio (`business-rule`): o frontend não contém regras verificáveis além de validações de formulário; as regras ficam no backend.
- Contexto integrado do sistema: [[01-Sistemas/SICI/SICI-Contexto-do-Sistema|Contexto do sistema]] **não** foi alterado.

## Próximo passo exato
1. Responder as [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]] (nome "Integra", validação pública do QR Code, perfil id 1, endpoints fora do catálogo).
2. Rodar `git diff 418642f..HEAD --stat` no `sici-frontend`; se houver mudanças, invocar `atualizar-documentacao`.
3. Reproduzir D1/D2 no navegador (a aplicação não foi executada) e decidir sobre o `KeycloakService` e os specs quebrados.
4. Para aprofundar: lote 6 — `ordem-servico-cadastrar`/`atualizar` (regras de formulário por modelo de OS), reducers/seletores e comparação de DTOs com o backend.
5. Consolidar a visão integrada (tela → API → regra) em [[01-Sistemas/SICI/SICI-Contexto-do-Sistema|Contexto do sistema]] quando houver aprovação.
6. Sugerir `sincronizar-brain` (nenhum `git add`/commit/push foi executado).
