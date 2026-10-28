---
type: security
aliases:
  - "Frontend Ouvidoria — segurança e sessão"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - app/token-auth-interceptor.js
  - app/token-storage-service.js
  - app/shared/storage-service.js
  - app/nav/nav-ctrl.js
  - app/login/login-ctrl.js
  - app/exception/app-exception-module.js
  - app/app.routes.js
  - app/manifestacao/registro/por-operador/manifestacao-por-operadorCtrl.js
  - app/manifestacao/registro/por-operador/registrar-manifestacao-por-operador-ctrl.js
  - app/manifestacao/caixa-de-entrada/detalhar-manifestacao-ctrl.js
  - app/manifestacao/caixa-de-entrada/caixa-de-entrada-ctrl.js
---

# Frontend Ouvidoria — segurança e sessão

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Fluxo: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Fluxo-Autenticacao]]

## Objetivo
Registrar os controles de segurança do frontend (sessão, permissões, proteção de dados) e os riscos observados, **sem reproduzir segredos**.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`. Cobertura `parcial`: não foi feita busca exaustiva de XSS nos templates.

## Informações confirmadas

### Sessão e credenciais
| Tema | Situação |
|---|---|
| Token | ✅ `localStorage`, chave `auth_token_ouv_df`; enviado como `Bearer` só para URLs que contêm a `urlApi` |
| Armazenamento alternativo | ✅ há *fallback* para `$cookieStore` se `localStorage` não existir (código praticamente inalcançável nos navegadores atuais) |
| `application-key` | ⚠️ ✅ chave de aplicação **fixa no código** do interceptor, enviada em toda requisição à API (valor omitido). É pública para qualquer usuário do navegador. |
| Credenciais de teste | ⚠️ ✅ `app/login/login-ctrl.js` contém login e senha fixos; o controller não está roteado (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Fluxo-Autenticacao]]). Valores omitidos; devem ser tratados como comprometidos e removidos. |
| Expiração | ❓ sem tratamento de expiração/renovação além do redirecionamento em 401/403 |
| Logout | ✅ limpa `localStorage` e redireciona; ❓ cancelamento do token no servidor não é chamado |

### Autorização
- ✅ O menu usa as permissões devolvidas por `operador-so/consultar-permissoes`: `PesquisarManifestacao`, `VisualizarPaineis`, `GerenciarSistema`, `PermissoesDeGerenciamento[]`, e (nos templates) `RegistrarManifestacao`, `VisualizarManifestacao`, `GerenciarPainelAvaliacao`.
- ✅ As rotas em `app.routes.js` **não têm guarda** (`resolve`/`$routeChangeStart`): qualquer rota pode ser aberta digitando a URL; a proteção depende de o backend responder 401/403/400.
- ✅ Regra de detalhamento na caixa de entrada: se existe `ManifestacaoBloqueanteId`, só se detalha a própria manifestação bloqueante, salvo `PermiteDetalharManifestacaoBloqueada`.
- ✅ Bloqueio de edição de operador bloqueado: `gridOperadorCtrl.onDetail` exibe erro se o usuário está bloqueado.

### Proteção de dados pessoais
- ⚠️ ✅ Nas rotas de cadastro de conta, **nome, nome da mãe, data de nascimento e CPF/CNPJ vão na URL** (`/cadastrar-pessoa-fisica/...`, `/cadastrar-pessoa-juridica/...`), logo ficam em histórico do navegador e em logs de proxy.
- ✅ A senha de acesso do cidadão não é tratada aqui; a conta é criada/atualizada por operador (`.../por-operador`).
- ✅ O fluxo de desafio de dados cadastrais (`security/check`, `security/challenge`, `count-try`) limita as tentativas: mais de 2 tentativas bloqueia por 24 h (mensagem exibida; contagem no backend). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Registro-por-Operador|Fluxo-Registro-por-Operador]].
- ⚠️ `console.log` do histórico de CPF vinculado em `manifestacao-por-operadorCtrl.js` (`consultarHistoricoCpfVinculado`) escreve dados no console do navegador.
- ✅ Download de anexo pela diretiva `upload`: `POST arquivo/download` (autenticado pelo interceptor; conteúdo em base64). Há também, em `detalhar-manifestacao-ctrl.js`, a função `efetuarDownloadAnexo`, que abriria `urlApi + "Dados/<id>/<nome>"` **sem** autorização, mas referencia `configService`, não injetado nesse controller; não há chamada a ela encontrada (código morto, 🔶).

### Outros riscos de frontend
- 🔶 Autocompletes de assunto montam rótulo com `$sce.trustAsHtml('<div>' + Descricao + '</div>')`: se `Descricao` vier com HTML, é renderizado. Risco depende do conteúdo do backend. (13 ocorrências de `trustAsHtml`/`ng-bind-html` no código.)
- ✅ Dependências antigas e sem gerenciador (jQuery 1.11.1, Bootstrap 3, AngularJS 1.x), com vulnerabilidades públicas conhecidas nas faixas antigas (conhecimento externo; versões exatas não verificadas).
- ✅ O serviço de localização e a API de homologação são chamados por HTTP (sem TLS) nos perfis `local` e `homologacao`.

## Inferências e limitações
- 🔶 Se `application-key` for realmente secreta no backend, deve ser rotacionada; se é só um identificador de aplicação, o nome do cabeçalho induz a erro. Confirmar com o time.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Debitos-Tecnicos]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca do Backend]]

## Pendências e próximo passo
- Remover credenciais do código (ação do time, fora do escopo da documentação) e confirmar o papel da `application-key`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
