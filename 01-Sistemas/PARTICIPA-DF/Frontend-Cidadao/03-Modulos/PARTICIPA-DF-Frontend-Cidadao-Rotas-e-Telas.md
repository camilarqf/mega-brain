---
type: index
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: completa
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - participa-df
  - frontend-cidadao
  - rotas
  - telas
sources:
  - src/app/app-routing.module.ts
  - src/app/pages/pages-routing.module.ts
  - src/app/pages/conta/conta-routing.module.ts
  - src/app/pages/registro-manifestacao/registro-manifestacao-routing.module.ts
  - src/app/pages/registro-manifestacao-integrada/registro-manifestacao-integrada-routing.module.ts
  - src/app/pages/registro-pedido/registro-pedido-routing.module.ts
  - src/app/pages/caixa-entrada/caixa-entrada-routing.module.ts
  - src/app/pages/validacao/validacao-routing.module.ts
---

# Frontend Cidadão — rotas e telas

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]]

## Objetivo
Mapa das rotas da SPA e dos fluxos a que pertencem (navegação, sem análise própria).

## Evidências
Arquivos `*-routing.module.ts` em `sources`, commit `d250804`.

## Informações confirmadas
Prefixo: as rotas de `pages` respondem em `/` e em `/pages`. `static` é separado.

| Área | Rotas (relativas) | Guard | Fluxo |
|---|---|---|---|
| Home | `` (`Home`), `example` (componente de exemplo/teste) | — | — |
| Login | `auth`, `logout` | — | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Autenticacao\|Autenticação]] |
| Validação pós-login | `validacao/gerenciar-validacao` (LGPD e troca de senha pendentes) | — | idem |
| Conta | `conta/inicio`, `conta/alterar-senha`, `conta/historico-cpf-vinculado` | `AuthGuard` | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Cadastro-de-Conta\|Cadastro de conta]] |
| Conta (aberta) | `conta/direcionar-usuario`, `validar-cpf`, `validar-cnpj`, `desafio-pessoa-fisica`, `criar-conta-pessoa-fisica`, `criar-conta-pessoa-juridica`, `atualizar-dados` e `atualizar-dados/:id`, `recuperar-senha`, `redefinir-senha`, `mensagem-conta`, `mensagem-redefinir-senha` | — | idem |
| Registro de manifestação | `registro-manifestacao` e `registro-manifestacao/:id`: `relato`, `assunto`, `form-complementar`, `local-fato`, `resumo`, `identificacao`, `anexos`, `finalizar` | — (identificação exige login no passo) | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Registro-de-Manifestacao\|Registro de manifestação]] |
| Registro integrado | `registro-manifestacao-integrada/:tipoEntrada/:classificacao/:assunto`: `relato`, `resumo`, `identificacao`, `anexos`, `finalizar` (resolver `ManifestacaoResolver`) | — | idem |
| Registro de pedido (SIC) | `registro-pedido`: `verifica-autenticidade`, `registrar/descricao-registro`, `registrar/resumo-registro`, `registrar/pedido-finalizado` | `AuthGuard` nas três telas de `registrar` | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Registro-de-Pedido\|Registro de pedido]] |
| Caixa de entrada | `caixa-entrada`: `minhas-manifestacoes`, `manifestacao/:id`, `pesquisa-manifestacao/:id`, `meus-pedidos`, `pedido/:id`, `pesquisa-pedido/:id` | `AuthGuard` no módulo | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Caixa-de-Entrada\|Caixa de entrada]] |
| Páginas estáticas | `static/...`: FAQ (Participa DF, Ouvidoria, LAI), "o que é" (Participa DF, Ouvidoria, Acesso à Informação), termos de uso, orientação de manifestação, informativo de solicitação de zeladoria | — | — |

- ✅ `AuthGuard`: chama `security/is-auth`; se autenticado e sem pendência (LGPD/troca de senha), libera; senão redireciona para `pages/auth` com `returnUrl`.
- ✅ Na home, o cartão do e-SIC leva a `/pages/registro-pedido` e o da Ouvidoria chama `novaManifestacao()` (limpa o rascunho e abre `pages/registro-manifestacao`). A home exibe um aviso a empresas sobre vincular um CPF válido ao CNPJ (`pages/_home/home.component.html`).

## Inferências e limitações
- 🔶 A rota `registro-manifestacao-integrada` recebe `tipoEntrada`, `classificacao` e `assunto` no caminho; parece ser a entrada para canais que já definem esses dados (ex.: link direto). O emissor desses links não está neste repositório.
- 🔶 `conta/atualizar-dados` (sem `:id`) não tem `AuthGuard`; a proteção real depende do backend.
- Rotas das páginas estáticas foram lidas só no nível de módulo.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Arquitetura|Arquitetura]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas-de-API]]

## Pendências e próximo passo
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]].
