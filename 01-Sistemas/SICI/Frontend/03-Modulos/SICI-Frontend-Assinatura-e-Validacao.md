---
type: module
system: SICI
repository: sici-frontend
status: confirmado
coverage: completa
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - modulo
  - assinatura
  - validacao
  - qr-code
sources:
  - src/app/components/layout/assinatura-autenticacao/assinatura-autenticacao.component.ts
  - src/app/pages/ordem-servico/validar-assinatura-os/validar-assinatura-os.component.ts
  - src/core/services/assinatura.service.ts
  - src/core/services/assinatura-popup-context.service.ts
  - src/core/services/ordem-servico-generica-service/assinatura-generica.service.ts
  - src/core/services/pdf-hash.service.ts
  - src/core/store/effects/ordem-servico-effects/validar-ordem.effect.ts
  - src/core/models/ordem-servico/assinatura.models.ts
  - src/app/app-routing.module.ts
---

# Módulo — Assinatura e validação (frontend)

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Backend: [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital (Backend)]] · Fluxo: [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]] · Relacionado: [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Objetivo
Dois blocos: o **popup de reautenticação e assinatura** e a **página de validação** de assinatura por código verificador.

## Evidências
Arquivos em `sources`; contrato do backend em [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]].

## Informações confirmadas ✅
### Popup de assinatura (`/assinatura/autenticacao?ctx=<uuid>`)
- Aberto por `window.open` (500×650) a partir de `AssinaturaService.iniciarAssinatura` (OS comum) ou `AssinaturaGenericaService.iniciarAssinatura` (genérica); a URL usa `document.baseURI`, respeitando o *base href*.
- O contexto (`tipo` `PADRAO`/`GENERICA`, `ordemId` e, na genérica, o corpo da OS) é gravado no `localStorage` em `assinatura_popup_ctx_<uuid>` (UUID de `crypto.randomUUID`) e apagado ao terminar.
- Sem `ctx` ou com contexto ausente/expirado, o popup mostra mensagem e não prossegue.
- Detalhes da sequência (reautenticação, comparação de usuário, chamadas) em [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]].

### Página de validação (`/validacao` e `pages/home/ordem-servico/validar-assinatura|validar-os`)
- Componente *standalone* `ValidarAssinaturaOsComponent`. Lê o código de `?codigo=` ou do `history.state`, converte para maiúsculas e valida pelo botão.
- A validação é feita por NgRx: ação `validarAssinatura` → `GET /assinaturas/validacao?codigo=` → `AssinaturaEffects` mostra toast de sucesso (`valido = true`) ou aviso ("Código informado não corresponde a uma assinatura válida"); erro de rede/HTTP vira o resultado "Código inválido ou assinatura não encontrada."
- Resposta modelada: `valido`, `mensagem`, `responsavel?`, `assinadoEm?`.
- Quando navegada a partir de uma OS, tenta carregar a OS (`listarOrdemServicoById`) para contexto.
- **Código verificador**: `PdfHashService` extrai do **texto do PDF** o padrão `Informe o código verificador: <32 hex>` (ou qualquer sequência de 32 hex) e o guarda em cache por id da OS. O botão "Validar assinatura" do visualizador de PDF abre `${origem}/validacao?codigo=<código>` em nova aba; "ir para validação" navega internamente.

## Inferências e limitações
- 🔶 **Rota pública que chama endpoint autenticado.** A rota `validacao` está fora do `AuthGuard`, mas `GET /assinaturas/validacao` **exige token** no backend. Sem sessão, a chamada recebe `401` e o `AuthErrorInterceptor` redireciona para `/login`. Portanto o link do QR Code só valida para quem já está logado (ou após login, sem retorno à URL de origem). Ver S5 e a pendência de validação pública no [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|backend]].
- 🔶 **Este frontend é o destino provável do QR Code** (`assinatura.url.validacao` do backend, parâmetro `?c=<código>`), mas a página lê `?codigo=`, não `?c=`: se o QR Code envia `c`, o código **não** será preenchido automaticamente. O valor real da propriedade não foi lido (configuração omitida). Fecha parcialmente a hipótese do [[Mapa-de-Integracoes|Mapa de integrações]]; confirmar.
- 🔶 `PdfHashService.validarAssinatura` usa `window.location.origin + '/validacao'` e **ignora o *base href***; em ambientes com prefixo (`/integra/`, `/integra-dev/`) a aba aberta não resolveria para a aplicação. Não executado.
- 🔶 Como o backend sempre responde "válido" (S5), a tela não distingue documento adulterado.
- O código extraído do PDF depende do texto do PDF gerado pelo `Servico-HtmlToPdf`; mudança no rótulo quebra a extração.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]] · [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-OS-Generica|OS-Generica]] · [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Integracoes|Integracoes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
