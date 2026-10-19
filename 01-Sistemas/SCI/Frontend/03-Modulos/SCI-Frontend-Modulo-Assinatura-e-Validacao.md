---
type: module
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - frontend
  - modulo
  - assinatura
  - validacao
sources:
  - src/app/public
  - src/app/store/services/public.service.ts
  - src/app/store/effects/assinatura.effect.ts
  - src/app/components/layout/assinar-nota-tecnica
  - src/app/pages/pip/pip-instauracao/despacho
  - src/app/pages/pip/pip-editar/assinar-relatorio-pip
---
# SCI Frontend — módulo Assinatura e validação

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Documentar a assinatura de documentos (nota técnica, minuta do despacho do PIP, relatório do PIP) e a validação pública de assinatura.

## Evidências
- `public/valida-assinatura`, `public.service.ts`, `assinatura.effect.ts`, `components/layout/assinar-nota-tecnica`, modais de assinatura do PIP, `jad.service.ts` e `pip.service.ts`.

## Informações confirmadas
- ✅ **Validação pública** (`/validacao`, sem login): o usuário informa o código de controle; o cliente envia `POST documento/validar` com `{ HashVerificador }` e exibe a lista devolvida (data da assinatura e nome do usuário). Sucesso e erro aparecem como avisos.
- ✅ **Assinaturas** nos fluxos: nota técnica da admissibilidade (`POST processo-admissibilidade/assinar-nota-tecnica` e `invalidar-nota-tecnica`), minuta do despacho do PIP (`POST pip/assinar-minuta`) e relatório do PIP (`POST pip/assinar-relatorio`). Os documentos PDF são baixados como blob (`GET processo-admissibilidade/nota-tecnica/{id}`, `GET pip/relatorio/{id}`) e exibidos com `ng2-pdf-viewer`.
- ✅ O modal de assinatura da nota técnica carrega os cargos do usuário (`GET cargo/por-usuario`) e envia o cargo escolhido em `assinarNotaTecnica`; o conteúdo dos modais de assinatura do PIP não foi lido.

## Inferências e limitações
- 🔶 `POST documento/validar` exige autenticação no backend ([[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]), mas a página `/validacao` é pública. Sem cookie, o `AuthInterceptor` não envia token e uma resposta 401 leva o `ErrorInterceptor` a redirecionar ao login; o comportamento não foi executado. Mesma pendência do backend (item 10).
- ❓ Como o QR Code do documento chega à página `/validacao` (parâmetro e URL) não foi verificado.
- Componentes de assinatura lidos por amostragem; ver Pendências.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Documentos-e-Assinaturas|Documentos e assinaturas (backend)]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-JAD-Admissibilidade|JAD]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-PIP|PIP]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
