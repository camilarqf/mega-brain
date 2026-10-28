---
type: integration
aliases:
  - "SCI Frontend — integrações"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
consumer: SCI
sources:
  - src/environments
  - src/app/store/services
  - src/app/auth/login/login.component.html
  - src/app/pages/gestao/painel-gestao
---
# SCI Frontend — integrações

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar com quem o `sci-frontend` se comunica: o `sci-backend` e dois destinos externos ao SCI.

## Evidências
- `environments/*.ts` (chaves `apiUrl` e `participaUrl`), serviços de `store/services`, `auth/login/login.component.html`, `pages/gestao/painel-gestao`.
- Endereços, hosts e identificadores de painel omitidos.

## Informações confirmadas
| Consumidor | Provedor | Tecnologia / contrato | Direção | Confirmação |
|---|---|---|---|---|
| `SCI` (`sci-frontend`) | `SCI` (`sci-backend`) | HTTP JSON (REST) e blobs (PDF e anexos); cabeçalho `Authorization: Bearer`; base `apiUrl`; 144 combinações verbo + caminho | saída | ✅ cliente no código; 136 de 144 rotas existem no backend analisado, 8 não (ver [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]]) |
| `SCI` (`sci-frontend`) | `PARTICIPA-DF` | hiperlinks abertos pelo navegador sob `participaUrl`: `pages/conta/recuperar-senha` ("Esqueci minha senha") e `pages/conta/direcionar-usuario` ("Novo cadastro") | saída (navegação do usuário) | ✅ links no código; 🔶 que `participaUrl` aponta para o frontend do `PARTICIPA-DF` (a chave se chama "participa"; valor não registrado) |
| `SCI` (`sci-frontend`) | `Power-BI` (serviço externo) | `iframe` com URL fixa de relatório publicado, na tela do Gestor Gerencial | saída (navegador → serviço) | ✅ no código; ❓ dono e se o link é público |

### Detalhes da integração com o backend
- ✅ Tudo passa por `HttpClient` com os interceptors de autenticação, carregamento e erro ([[01-Sistemas/SCI/Frontend/08-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Segurança e sessão]]).
- ✅ Falha de conexão (status 0) mostra "Erro de conexão com o servidor"; erros ≥ 400 aparecem no formato `{status, requestId, title, detail, instance}`, compatível com um contrato de erro padronizado do backend (formato não comparado).
- ✅ O frontend não consome diretamente RabbitMQ, BCadastro nem o serviço HTML→PDF; esses são do backend ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas do backend]]).

## Inferências e limitações
- 🔶 `Power-BI` não está no catálogo de serviços externos; será cadastrado como serviço externo `Power-BI` por esta análise (dono não identificado).
- ❓ Cabeçalhos de CORS, política de CSP e `X-Frame` do iframe não são verificáveis pelo código.
- O frontend não chama o `PARTICIPA-DF` por API; o relacionamento é só de navegação.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Autenticacao|Integração SCI → PARTICIPA-DF (backend)]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Administracao-e-Gestao|Administração e gestão]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
