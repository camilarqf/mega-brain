---
type: reference
aliases:
  - "Rotas e telas — SICI Frontend"
system: SICI
repository: sici-frontend
status: confirmado
coverage: completa
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
sources:
  - src/app/app-routing.module.ts
  - src/app/pages/pages-routing.module.ts
  - src/app/pages/acao-controle/acao-controle-routing.module.ts
  - src/app/pages/ordem-servico/ordem-servico-routing.module.ts
  - src/app/pages/gestao-subci/gestao-subci-routing.module.ts
  - src/app/auth/auth-routing.module.ts
  - src/core/services/auth/authorization.config.ts
  - src/app/components/layout/sidenav/sidenav.component.ts
---

# Rotas e telas — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]], [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Objetivo
Mapear as rotas do roteador Angular, a proteção de cada uma e as telas correspondentes.

## Evidências
Arquivos de roteamento em `sources`. "Permissão" é a chave de `PermissionProfiles`; perfis por permissão em [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]].

## Informações confirmadas ✅
### Rotas da raiz (`AppRoutingModule`)
| Caminho | Destino | Proteção |
|---|---|---|
| `` | redireciona para `pages/home` | — |
| `login` | `LoginComponent` (módulo lazy `AuthModule`) | pública |
| `validacao` | `ValidarAssinaturaOsComponent` | **sem guard** (ver [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]]) |
| `assinatura/autenticacao` | `AssinaturaAutenticacaoComponent` (popup de assinatura) | sem guard |
| `template-editor` | `TemplateEditorComponent` | sem guard |
| `acesso-negado` | `AcessoNegadoComponent` (lazy, *standalone*) | pública |
| `pages` | `PagesModule` (lazy) | `AuthGuard` em `canActivate` e `canActivateChild` |
| `**` | redireciona para `acesso-negado` | — |
| `acao-controle/**`, `ordem-servico/**`, `gestao-subci/**` | redirecionamentos de URLs antigas para `pages/home/...` | — |

### Rotas autenticadas (sob `pages/home`)
| Caminho (após `pages/home`) | Tela | Guard de perfil | Permissão |
|---|---|---|---|
| `` | lista de ações de controle | não | — |
| `cadastrar-acao-controle` | cadastro de ação | **não** (`data.permissions` sem `canActivate`) | `CRIAR_ACAO` (só declarada) |
| `visualizar/:id` | detalhe da ação | `GuardPerfil` | `CONSULTAR_ACAO` |
| `atualizar/:id` | edição da ação | `GuardPerfil` | `EDITAR_ACAO` |
| `ordem-servico/listar/:acaoControleId` | OS da ação | `GuardPerfil` | `CONSULTAR_OS_POR_AC` |
| `ordem-servico/cadastrar-ordem-servico/:acaoControleId` | cadastro/edição/prorrogação de OS (modo por *query param*) | `GuardPerfil` | `EMITIR_OS` |
| `ordem-servico/atualizar-ordem-servico/:acaoControleId/:id` | edição de OS | `GuardPerfil` | `EDITAR_OS` |
| `ordem-servico/ordens-servicos-lista` | lista geral de OS | `GuardPerfil` | `LISTAR_OS` |
| `ordem-servico/visualizar-pdf/:id` | PDF da OS | `GuardPerfil` | `CONSULTAR_OS_POR_AC` |
| `ordem-servico/visualizar-pdf-generica/:id` | PDF da OS genérica | `GuardPerfil` | `CONSULTAR_OS_POR_AC` |
| `ordem-servico/ordem-generica-lista` | lista de OS genéricas | `GuardPerfil` | `CONSULTAR_OS_POR_AC` |
| `ordem-servico/ordem-generica-cadastrar` | cadastro de OS genérica | `GuardPerfil` | `EDITAR_OS` |
| `ordem-servico/validar-assinatura` e `.../validar-os` | validação de assinatura (mesmo componente de `validacao`) | não | — |
| `gestao-subci` | cadastro de titular/substituto SUBCI | `GuardPerfil` (módulo inteiro) | `EDITAR_PERFIL` |
| `gestao-subci/auditor-perfil` | vínculo auditor ↔ perfis | `GuardPerfil` | `EDITAR_PERFIL` |

O módulo `gestao-subci` ainda tem `GuardPerfil` na rota-pai (`pages-routing`), com a mesma permissão.

### Menu lateral (`SidenavComponent`) ✅
Grupos: **Ações de Controle**, **Gestão Ordens de Serviço** (visível se `LISTAR_OS` ou `CONSULTAR_OS_POR_AC`), **Administração** (visível se `EDITAR_PERFIL`) e **Logout**. A exibição usa `PermissaoService.possuiPermissao`, só no cliente.

## Inferências e limitações
- 🔶 `template-editor` não é usada pelo menu lido; o componente só tem navegação de volta. A finalidade não foi identificada.
- 🔶 `GuardPerfil` só atua quando a rota declara `permissions`/`perfis` **e** o guard está em `canActivate`: a rota de cadastro de ação declara a permissão sem o guard. Registrado em [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]].
- Conteúdo de `*.html` não foi lido em detalhe.

## Relacionamentos
- Módulos: [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Acao-de-Controle|Acao-de-Controle]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-OS-Generica|OS-Generica]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Gestao-SUBCI-e-Perfis|Gestao-SUBCI-e-Perfis]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
