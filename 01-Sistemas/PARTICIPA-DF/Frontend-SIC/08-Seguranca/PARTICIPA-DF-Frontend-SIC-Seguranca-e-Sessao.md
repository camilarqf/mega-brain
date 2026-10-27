---
type: security
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - seguranca
  - sessao
  - permissoes
sources:
  - app/token-auth-interceptor.js
  - app/token-storage-service.js
  - app/shared/storage-service.js
  - app/nav/nav-ctrl.js
  - app/auth/auth-ctrl.js
  - app/exception/app-exception-module.js
  - app/app.routes.js
  - app/upload/upload-arquivos-directive.js
  - app/registro/por-operador/pedido-por-operadorCtrl.js
  - app/caixa-entrada/detalhamento-pedido.html
  - index.html
---

# Frontend SIC — segurança e sessão

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Fluxo: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao|Fluxo-Autenticacao]]

## Objetivo
Registrar os controles de segurança do frontend (sessão, permissões, proteção de dados) e os riscos observados, **sem reproduzir segredos**.

## Evidências
Arquivos em `sources`, commit `5518a81`. Cobertura `parcial`: não foi feita busca exaustiva de XSS (`ng-bind-html`, `$sce`) nos templates.

## Informações confirmadas

### Autenticação e token
- ✅ Não há tela de login neste front-end: o login é **assistido** por outro front-end (entrada em `/#/auth/{sessionId}`). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao|Fluxo-Autenticacao]].
- ✅ O token fica em `localStorage` sob a chave `auth_token_sic` (`tokenStorage`), com *fallback* para `$cookieStore`. `logout` redireciona para `${Principal}/pages/logout` (de `configuration/front-end-urls`) e executa `localStorage.clear()`.
- ✅ `tokenAuthInterceptor` envia, para URLs que contêm `urlApi`, o cabeçalho `application-key` (valor **fixo no código**, omitido aqui), `Authorization: Bearer <token>` e `X-Requested-With: XMLHttpRequest` (os dois últimos só se há token).
- ✅ `tokenStorage.token()` decodifica o primeiro segmento do token (separado por `.`) com `atob` e `JSON`; 🔶 isso sugere um token com cabeçalho legível (JWT), mas **nenhum código chama `token()`** (busca em `app/`).
- ❓ Expiração e renovação: o front não trata; a sessão só é revalidada por `security/is-auth` ao carregar o menu e por 401/403 nas chamadas.

### Autorização
- ✅ **Não há guarda de rota** (nenhum `resolve`); o menu é filtrado por `vm.isAuth` e por `operador-sic/consultar-permissoes` (`GerenciarSistema`, `PermissoesDeGerenciamento` com `URL` e `DescricaoFuncionalidade`). A navegação direta por URL a `/operador`, `/perfil` etc. depende da resposta 401/403 do backend.
- ✅ `Permissoes.IsUnidadeAtualSuperioSic` (resposta de `consultar-permissoes`) altera o cadastro de operador: se `false`, a unidade atual passa a ser a primeira unidade adicionada.
- ✅ Ações no detalhe do pedido são controladas pelo objeto `pedido.Acoes` (`acoes-operador`), com 14 códigos (`PRG_PDD`, `RPT_PDD`, `RRE_PDD`, `RPT_RPI`, `RPT_RSI`, `RPP_RTI`, `RPP_NOR`, `RGS_SEI`, `DCS_RTI`, `DCS_NOR`, `RPD_PDD`, `MPR_PDD`, `NXR_RQN`, `RMV_RQV`); o significado de cada um é inferido do rótulo do botão. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Caixa-de-Entrada-e-Detalhamento|Fluxo da caixa de entrada]]. Quem decide é o backend; o front só esconde botões.

### Tratamento de erros
- ✅ 401/403: `tokenAuthInterceptor` busca `configuration/front-end-urls` e leva o navegador ao `Login`; `exceptionInterception` também faz `$location.path('/')`.
- ✅ 400 exibe `Notifications`/`error` do backend em `custom-exception`; 500 abre modal com `Message`.

### Proteção de dados pessoais (PII)
- ✅ As rotas de cadastro de pessoa física e jurídica incluem nome, nome da mãe, data de nascimento, CPF, razão social e CNPJ **no caminho da URL** (`/cadastrar-pessoa-fisica/:nome/:data/:mae/:cpf`), o que os grava no histórico do navegador e em registros de acesso de proxies. 🔶 Como a URL é de hash (`#/...`), o servidor web não a recebe; permanece no histórico do navegador.
- ✅ CPF/CNPJ são enviados por `GET` em query string em `security/count-try?data=`, `security/check?data=` e `security/check-cpf-vinculado-pj?cpf=&cnpj=` — expostos a logs do `nginx` e do backend.
- ✅ Verificação de identidade do cidadão por operador: o operador informa o CPF/CNPJ e o cidadão responde a um **desafio** (`security/check` → `security/challenge`); mais de 2 tentativas (`count-try > 2`) bloqueiam por 24 h (texto da tela). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Registro-por-Operador|Fluxo-Registro-por-Operador]].
- ✅ Anexos: enviados em base64 dentro do JSON; nome tratado por `TratarNomeDoArquivo` (remove acentos e caracteres não alfanuméricos); limite de **25 MB** somados verificado no cliente (`uplArquivos`); cada arquivo também passa por `acesso-informacao/arquivo/validar` antes de ser aceito (regras do servidor ❓ não conferidas).

## Inferências e limitações
- 🔴 **Risco**: a `application-key` está em texto no JavaScript entregue ao navegador (`app/token-auth-interceptor.js`). Se for segredo, está exposta; se for só identificador da aplicação, ainda assim deve estar em configuração. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]].
- 🔶 Token em `localStorage` fica acessível a qualquer script da página; combinado com bibliotecas antigas (AngularJS 1.5, jQuery 1.11, Bootstrap 3.3.6), amplia o impacto de uma falha de XSS.
- 🔶 `exceptionInterception` e `tokenAuthInterceptor` reagem ao mesmo 401/403; o efeito combinado (redirecionar a `/` e ao login) não foi testado.
- `nav-ctrl.js` escuta `acessoNegadoEvt` e chama `verificarToken()`, função **não definida**; nenhum código dispara o evento.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Integracoes-Externas|Integracoes-Externas]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Arquitetura|Arquitetura]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao do Backend]]

## Pendências e próximo passo
- Confirmar se a `application-key` é segredo; confirmar expiração do token e se o logout o invalida no servidor. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
