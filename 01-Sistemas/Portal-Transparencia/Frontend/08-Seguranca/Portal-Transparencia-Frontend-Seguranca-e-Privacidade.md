---
type: security
aliases:
  - "Frontend — segurança e privacidade"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
tags:
  - dados-pessoais
sources:
  - src/app/token-interceptor.js
  - src/app/index.module.js
  - src/app/index.config.js
  - src/app/config.js
  - src/app/components/super-busca/super-busca.service.js
  - src/app/components/compartilhado/directives/internal-header.directive.js
  - src/app/components/compartilhado/directives/cabecalho-pagina.directive.js
  - src/app/components/compartilhado/directives/despesas-ras/mapa-ras.js
  - src/app/components/compartilhado/controllers/main.controller.js
  - .bowerrc
  - src/index.html
---

# Frontend — segurança e privacidade

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

> Nenhum valor sensível é reproduzido aqui; só a existência e o local.

## Objetivo
Registrar controles e riscos de segurança do frontend, separados de recomendações.

## Evidências
Commit `dca3e933`; arquivos em `sources`. Leitura estática; nenhum teste dinâmico.

## Informações confirmadas
**Controles existentes**
- ✅ Portal **público e sem autenticação de usuário**: não há login, perfis nem token de sessão; o único elemento enviado à API é o `x-client-id` (UUID aleatório por carga da página), que **não é um controle de segurança** (qualquer cliente pode enviar um valor).
- ✅ `ngSanitize` carregado; interpolações Angular escapam HTML por padrão.
- ✅ Estado local só de interface: tema (`localStorage`), enquete/*todo* (`localStorage`), aviso mobile (`sessionStorage`); sem dados pessoais.

**Pontos de atenção (fatos)**
- ✅ **Endereços de infraestrutura versionados**: `src/app/config.js` está no Git e contém endereços absolutos (incluindo IPs de rede interna) dos perfis gerados; foi editado nos commits `cc44e3f1` e `21068a92`. Não há segredo/credencial identificada nele; os valores não são reproduzidos aqui.
- ✅ **CPF/CNPJ no caminho da URL**: a super busca envia os dígitos (`/indice-cpf/{pagina}/{cpf}`) ao serviço `apisuperbusca`; ficam em *logs* de acesso e histórico de proxies. Ver [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Super-Busca|Super Busca]].
- ✅ **Formulário "Fale conosco"** envia nome, e-mail, assunto e mensagem (concatenados com `;`) por `POST` a `/contato/registro`; no Backend o controller correspondente está comentado.
- ✅ **HTML confiável explícito**: `$sce.trustAsHtml` em `internal-header.directive.js` (título/descrição da página) e `cabecalho-pagina.directive.js` (`textoAdicional`); `ng-bind-html` em listas de seleção; `innerHTML` em `area-chart.directive.js`, `print-area.directive.js` e `mapa-ras.js` (este usa campos do GeoJSON local `delimitacao_ras.json`). A origem dos textos passados às diretivas de cabeçalho não foi rastreada em todas as telas.
- ✅ **Depuração ligada**: `$logProvider.debugEnabled(true)` e 14 `console.log` fora de testes (`RelatorioService` registra o erro no console).
- ✅ **Cadeia de build**: `.bowerrc` com `strict-ssl: false` (TLS sem verificação ao baixar dependências); imagem `node:6.11.3`; dependências bower via URLs `github.com`.
- ✅ **Terceiros**: `gtag.js` (Google) e *scripts*/fontes por CDN no `index.html` sem *Subresource Integrity* aparente.
- ✅ Arquivos de falha de JVM (`hs_err_pid*.log`) existem na raiz do diretório local, mas **não são versionados** (`*.log` no `.gitignore`).

## Inferências e limitações
- 🔶 **Dados pessoais**: as telas de remuneração por servidor e de beneficiários/conselheiros exibem dados de pessoas físicas vindos da API; o mascaramento é responsabilidade do Backend ([[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]). O frontend não aplica proteção adicional.
- 🔶 Sem política de segurança de conteúdo (CSP) identificada em `index.html`/`nginx.conf` (cabeçalhos de resposta do proxy não estão no repositório).
- 🔶 Versões antigas de AngularJS (1.4) e bibliotecas têm vulnerabilidades públicas conhecidas; não foi feita varredura de dependências.
- Recomendações ficam em [[01-Sistemas/Portal-Transparencia/Frontend/09-Qualidade/Portal-Transparencia-Frontend-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Segurança do Backend]] · [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API]] · [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]] (#5, #8).
