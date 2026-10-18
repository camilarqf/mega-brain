---
type: index
status: pendente
updated: 2026-10-18
tags:
  - integracoes
  - moc
---

# Mapa de integrações

Voltar: [[Catalogo-de-Sistemas|Catálogo de sistemas]] · Regras: `BRAIN-RULES.md`, seção 7.

Índice de todas as integrações entre sistemas e serviços externos. Cada linha aponta para a **nota canônica** da integração; o detalhe não é repetido aqui. IDs conforme o catálogo.

## Integrações com evidência
| Consumidor | Provedor | Tecnologia | Direção | Confirmação | Nota canônica |
|---|---|---|---|---|---|
| `SICI` (`sici-backend`) | `Servico-de-PDF` | HTTP POST JSON | saída | ✅ cliente no código; ❓ provedor não identificado | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `SICI` (`sici-backend`) | `Keycloak` | OIDC / JWKS (validação de JWT) | entrada (tokens) | ✅ | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `SICI` (`sici-backend`) | `Keycloak` | HTTP (token endpoint e userinfo) | saída | ✅ | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |

## Relações não confirmadas (hipóteses)
- 🔶 O backend do SICI grava no QR Code um link de validação (`assinatura.url.validacao`) que aponta para um frontend de validação. Não está confirmado se é o `sici-frontend`, que ainda não foi analisado.

## Como manter
- Toda integração nova ou alterada atualiza uma linha deste mapa e a nota canônica correspondente.
- Relação sem evidência entra apenas na seção de hipóteses.
