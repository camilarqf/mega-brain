---
type: analysis-log
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
created: 2026-10-18
updated: 2026-10-27
commit_data: 2026-07-03
branch: master
tags:
  - participa-df
  - frontend-cidadao
  - controle
  - cobertura
---

# Registro de análise — Frontend Cidadão

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]

## Base analisada
- Repositório: `participa-df-frontend` (endereço omitido); branch `master`; commit `d250804` (2026-07-03); working tree limpa.
- Método: leitura estática. Testes não executados, aplicação não iniciada, build não executado.

## Regras de proteção aplicadas
- Não foram reproduzidos endereços de ambiente, o identificador do Google Analytics, tokens nem dados pessoais; só nomes de chaves.
- O código não foi alterado.

## Decisões de classificação
- O repositório foi associado ao `PARTICIPA-DF` por: caminho do remoto (`.../participa-df/participa-df-frontend`), `applicationName: 'Participa-DF'`, e correspondência dos 66 endpoints consumidos com o catálogo do backend, **confirmado pela responsável** em 2026-10-18.
- Componente nomeado `Frontend-Cidadao` (rótulo provisório; o sistema tem 3 front-ends, informado pela responsável). Pasta e prefixo `PARTICIPA-DF-Frontend-Cidadao-` nos arquivos.

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Cadastro, retomada e esqueleto | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Index]], este registro, [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendencias]]; atualizados Repositórios, Index do sistema, Catálogo e Pendências do Backend |
| 1 | Fundamentos | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Stack-e-Dependencias|Stack]], [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Arquitetura|Arquitetura]] (parcial), [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Perfis-e-Ambientes|Perfis-e-Ambientes]], [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-Modulos/PARTICIPA-DF-Frontend-Cidadao-Rotas-e-Telas|Rotas-e-Telas]] |
| 2 | Segurança e sessão | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/08-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]] (parcial), [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Autenticacao|Fluxo-Autenticacao]] (parcial) |
| 3 | Fluxos de negócio | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Registro-de-Manifestacao|Registro-de-Manifestacao]], [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Registro-de-Pedido|Registro-de-Pedido]], [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Caixa-de-Entrada|Caixa-de-Entrada]], [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Cadastro-de-Conta|Cadastro-de-Conta]] (todas parciais) |
| 4 | API consumida e integrações | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas-de-API]] (parcial), [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas|Integracoes-Externas]] (parcial); atualizados Mapa e Catálogo (IDs `Servico-Localizacao-CGDF`, `Google-Analytics`, `Perto-Digital`) |
| 5 | Qualidade | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/09-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/09-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Debitos-Tecnicos]] (parcial) |

## O que não foi coberto
- Componentes de `layout/` (exceto upload e mapa), formulários de relato, atributos complementares e local do fato, telas `mensagem-*`, `direcionar-usuario`, páginas estáticas (conteúdo), modelos em `core/models/` e validadores/serviços de formatação de documentos.
- Comparação de verbo/payload de cada chamada com os controllers do backend.
- Execução de `ng test`, `ng build` e da aplicação.
- Os outros dois front-ends do Participa.

## Próximo passo exato
1. Confirmar o nome do componente (`Frontend-Cidadao`) e responder as [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]].
2. Rodar `git diff d250804..HEAD --stat` no repositório e, se houver mudanças, invocar `atualizar-documentacao`.
3. Para aprofundar: lote 6 — telas de relato/complementares/local do fato e `layout/`; lote 7 — comparação com os controllers do backend.
4. Documentar os front-ends de Ouvidoria (OuvDF) e SIC quando os repositórios forem informados; depois consolidar a visão integrada de telas em [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Contexto-do-Sistema|Contexto do sistema]].
5. Sugerir `sincronizar-brain` (nenhum `git add`/commit/push foi executado).

## Histórico de estrutura
- 2026-10-27: pastas reorganizadas conforme a seção 1 do `BRAIN-RULES.md` (numeração fixa; melhorias do cofre, lote 3).
