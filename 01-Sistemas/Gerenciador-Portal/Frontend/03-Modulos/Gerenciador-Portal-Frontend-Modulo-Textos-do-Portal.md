---
type: module
aliases:
  - "Módulo Textos do Portal — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/app/components/textos-portal/textos-portalCtrl.js
  - src/app/components/textos-portal/textos-portalApi.js
  - src/app/components/navbar.html
  - src/app/index.route.js
---
# Módulo Textos do Portal — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Tela `/textos-portal` (`TextosPortalController`, `textosPortalAPI`): editar o texto explicativo de cada consulta do Portal, escolhendo categoria e subcategoria. Backend: [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Conteúdo do portal]].

## Evidências
`textos-portalCtrl.js` (55 linhas) e `textos-portalApi.js` lidos integralmente; `navbar.html` (item comentado); HTML da tela não lido.

## Informações confirmadas
- ✅ **Fora do menu**: o item "TEXTOS PORTAL" está **comentado** em `navbar.html`, mas a rota `/textos-portal` continua registrada e acessível por URL direta.
- ✅ Fluxo: carregar categorias → escolher categoria (carrega subcategorias) → escolher subcategoria (carrega o texto) → `PUT /textos-consultas` com o texto alterado; avisos de sucesso e de erro (esta tela trata a falha da gravação).
- ✅ Não envia o usuário logado.

## Falhas e dependências
- A tela editável **sem login** e sem auditoria do usuário, já que não há guarda de rota ([[01-Sistemas/Gerenciador-Portal/Frontend/08-Seguranca/Gerenciador-Portal-Frontend-Seguranca-e-Sessao|Segurança]]); no backend o `PUT` também não valida token.
- Se o texto aceita HTML, `textAngular` e `ngSanitize` estão no projeto, mas o HTML não foi lido (❓).

## Inferências e limitações
- 🔶 A funcionalidade foi desativada do menu de propósito; o motivo não aparece no código (histórico do Git não foi lido).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Backend: Conteúdo do portal]] · [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Perguntar ao time se a tela está desativada em definitivo ([[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Pendencias|controle]]).
