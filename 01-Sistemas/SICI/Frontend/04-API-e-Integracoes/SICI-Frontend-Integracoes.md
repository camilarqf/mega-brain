---
type: integration
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
consumer: SICI
provider: SICI
tags:
  - sici
  - frontend
  - integracao
  - backend
  - keycloak
sources:
  - src/environments/environment.prod.ts
  - nginx.conf
  - src/core/services/interceptor/http-token.service.ts
  - src/core/services/auth/auth.service.ts
  - src/core/services/keycloak/keycloak.service.ts
  - src/app/pages/ordem-servico/validar-assinatura-os/validar-assinatura-os.component.ts
---

# Integrações — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · [[Mapa-de-Integracoes|Mapa de integrações]] · Backend: [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integrações externas do Backend]] · Relacionado: [[01-Sistemas/SICI/Frontend/04-API-e-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]]

## Objetivo
Registrar com quem o `sici-frontend` se comunica (consumidor `SICI` frontend → provedor `SICI` backend) e o que **não** foi encontrado.

## Evidências
Arquivos em `sources`; lista completa de chamadas em [[01-Sistemas/SICI/Frontend/04-API-e-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]].

## Informações confirmadas ✅
| Consumidor | Provedor | Tecnologia | Direção | Observação |
|---|---|---|---|---|
| `SICI` (`sici-frontend`) | `SICI` (`sici-backend`) | HTTP JSON (REST), `Bearer` JWT; PDF como *blob* | saída | base `urlApi` (`/api` nos ambientes empacotados); em produção o nginx repassa `/api/` ao backend por `BACKEND_TARGET`; **52** caminhos/verbos |
- **Autenticação**: o frontend envia usuário e senha ao backend (`POST /auth/login`), que faz a ponte com o `Keycloak` ([[01-Sistemas/SICI/Backend/04-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo do Backend]]). **Não há chamada direta do navegador ao Keycloak** em nenhum código ativo; `KeycloakService` (que usaria `keycloak-js`) não é referenciado e depende de `environment.keycloak`, ausente.
- **Origens aceitas pelo interceptor de token**: a do próprio frontend e a de `urlApi`. Chamadas a outras origens não recebem o `Bearer`.
- 🔶 **CORS**: nos perfis empacotados o navegador chama a mesma origem (`/api`), então o CORS aberto do backend (`allowedOrigins = *`) só tem efeito no perfil `local` (`urlApi` absoluto).

## Relações de entrada (hipóteses) 🔶
- **QR Code**: o backend grava no PDF um link para `assinatura.url.validacao`; a rota `validacao` deste frontend é o destino provável, mas o valor real da propriedade não foi lido e a página lê `?codigo=` (o backend usa `?c=`). Ver [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]]. Mantida em hipótese no [[Mapa-de-Integracoes|Mapa]].
- **Fontes (Google Fonts)** ✅: `index.html` e `styles/ckeditor.scss`/`sidenav.scss` carregam folhas de estilo de fontes de `fonts.googleapis.com` (única origem externa encontrada por busca de URLs em `src`). É dependência de CDN no navegador; não foi cadastrada como serviço no catálogo por ser apenas estilo (decisão a confirmar nas [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]]).
- **Outros serviços externos**: nenhum cliente de analytics, mapas, e-mail ou outro serviço de terceiros foi encontrado no código.

## Inferências e limitações
- 🔶 `Servico-de-PDF` e `Keycloak` são consumidos **pelo backend**; o frontend não os conhece.
- Falhas: não há *retry* nem fila; erros HTTP viram toasts. Em `401` o usuário é levado ao login.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/05-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]] · [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
