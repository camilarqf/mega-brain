---
type: flow
aliases:
  - "Fluxo — assinatura de OS (frontend)"
system: SICI
repository: sici-frontend
status: confirmado
coverage: completa
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
sources:
  - src/app/components/layout/assinatura-autenticacao/assinatura-autenticacao.component.ts
  - src/core/services/assinatura.service.ts
  - src/core/services/ordem-servico-generica-service/assinatura-generica.service.ts
  - src/core/services/assinatura-popup-context.service.ts
  - src/app/pages/ordem-servico/ordens-servico-listagem/ordens-servico-listagem.component.ts
  - src/app/pages/ordem-servico/visualizar-pdf/visualizar-pdf.component.ts
  - src/app/pages/ordem-servico/visualizar-pdf-generica/visualizar-pdf-generica.component.ts
---

# Fluxo — assinatura de OS (frontend)

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Backend: [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS (Backend)]] · Relacionado: [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]], [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Ciclo-de-Vida-OS|Ciclo-de-Vida-OS]]

## Objetivo
Descrever o que o cliente faz para assinar uma OS (comum ou genérica), do botão ao resultado.

## Evidências
Arquivos em `sources`; contrato do backend em [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Assinatura-Digital|Assinatura-Digital]].

## Informações confirmadas ✅
```mermaid
sequenceDiagram
    participant T as Tela (lista geral ou PDF)
    participant P as Popup /assinatura/autenticacao
    participant B as sici-backend
    T->>T: grava contexto no localStorage (ctx = UUID)
    T->>P: window.open (500x650) com ?ctx=UUID
    P->>P: lê contexto; preenche usuário da sessão
    P->>B: POST /auth/login (sem interceptors) usuário e senha digitados
    B-->>P: access_token
    P->>P: confere preferred_username do token com o usuário logado
    P->>B: POST /assinaturas/assinar-os/{id} {status: ASSINADA} (Bearer do novo token)
    Note over P,B: genérica: POST /assinaturas/assinar-os-generica/{id} com o corpo da OS
    B-->>P: 2xx ou erro
    P->>T: postMessage assinatura-toast (mesma origem) e grava assinatura_toast
    P->>P: remove contexto e fecha a janela
    T->>T: sucesso: recarrega listas / volta à lista geral
```
1. **Origem do botão**: lista geral (`confirmarAssinatura`/`confirmarAssinaturaGenerica`) ou visualizador de PDF quando `status === ENVIADA` e `origem === LISTA_GERAL`.
2. **Reautenticação**: o usuário digita usuário e senha de novo; o token novo vale só para a assinatura (a chamada ignora os interceptors, então o token da sessão não é usado).
3. **Conferência no cliente**: se há conta na sessão, o `preferred_username` do token novo (decodificado sem verificar assinatura) deve ser igual; senão, mensagem "As credenciais nao pertencem ao usuario logado na sessao atual." Se não há conta guardada, a conferência é dispensada (retorna verdadeiro).
4. **Assinatura**: `POST` ao backend com `Bearer` do token novo. Quem pode assinar (SUBCI titular ou substituto vigente) é decidido pelo **backend**; o frontend não verifica perfil para exibir o botão no popup, apenas no menu/rota da lista geral (`LISTAR_OS`).
5. **Resultado**: erro de autenticação ("Usuario ou senha invalidos." para 400/401) ou de assinatura (mensagem do backend `message`/`detail`) aparece no popup; o toast final vai à origem por `postMessage` (origem validada na recepção) e pelo `localStorage`.
6. **Origem após sucesso**: o visualizador de PDF navega para `ordens-servicos-lista`; a lista geral recarrega OS e genéricas.

## Inferências e limitações
- 🔶 A senha é enviada ao backend duas vezes por sessão (login e assinatura) e nunca guardada pelo frontend; a segurança do canal (HTTPS) depende do ambiente e não foi verificada.
- 🔶 A checagem de que o token é do mesmo usuário é só do cliente; o backend valida o assinante pelo token que recebe, não pelo que a sessão tinha.
- 🔶 Se o popup é fechado antes de terminar, a chave `assinatura_popup_ctx_<uuid>` permanece no `localStorage`; para a genérica contém o corpo da OS.
- 🔶 `postMessage` do popup para `window.opener` depende de a janela de origem continuar aberta.
- Não executado.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]] · [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-OS-Generica|OS-Generica]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
