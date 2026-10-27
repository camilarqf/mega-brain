---
type: module
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
tags:
  - portal-transparencia
  - frontend
  - modulo
  - navegacao
  - acessibilidade
sources:
  - src/app/index.route.js
  - src/app/components/pagina-inicial
  - src/app/components/acessibilidade
  - src/app/components/acesso-informacao
  - src/app/components/legislacao
  - src/app/components/quadros-tematicos
  - src/app/components/breadcrumb
  - src/app/components/compartilhado
---

# Frontend — páginas institucionais, navegação e recursos comuns

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Reunir telas que não pertencem a uma área de dados: página inicial, temas, textos institucionais, acesso à informação, legislação, acessibilidade e os componentes de navegação.

## Evidências
Commit `dca3e933`. `index.route.js`; `components/{pagina-inicial,acessibilidade,acesso-informacao,legislacao,quadros-tematicos,breadcrumb,url-arquivos}`; `components/compartilhado/**`; `template/**`.

## Informações confirmadas
| Caminho | Controller / template | Observação |
|---|---|---|
| `/` | `HomeController` (`template/home.html`) | Página inicial; o repositório tem `pt-video-carousel` e `SlideshowService` (`/v2/imagens/imagens-slideshow`) e a pesquisa de satisfação (uso na tela não conferido) |
| `/old` | `DashboardController` | Painel antigo com vários `resolve` (receitas × despesas, servidores, pesquisa); 🔶 provavelmente legado |
| `/temas` | `QuadrosTematicosController` | Quadros temáticos (`/v2/paineis-despesa*`), usa `apiGerenciador` e `caminhoImagens` |
| `/acesso-informacao`, `/informacao` | `AcessoInformacaoController` / template | Órgãos LAI (`/v2/orgaos-lai`) |
| `/legislacao/:nome` | template (10 HTMLs) | Textos de legislação por nome |
| `/sobre`, `/faq`, `/linksuteis` | templates sem controller | Textos institucionais |
| `/glossario`, `/downloads` | `GlossarioController`, `DownloadsController` | Glossário e downloads (a API `/arquivos?codCategoria=` existe em `ArquivosService`; ligação com `DownloadsController` não conferida) |
| `/url-arquivo` | `ArquivoUrlController` | Redireciona para o arquivo mais recente de uma categoria (9 consultas fixas) |
| `/busca` | `SuperBuscaController` | Ver [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Super-Busca|Super Busca]] |

- ✅ **Acessibilidade**: módulo `portal.acessibilidade` e diretivas `highContrast` e `fontResize` (com specs); troca de tema persistida em `localStorage`.
- ✅ **Navegação**: `topbar`, `rodape`, *breadcrumb* (`angular-crumble` + `Breadcrumb` service, rotas `noLink`), `menu-*`, `searchbar`, `scrolltop-button`, `share` (compartilhamento social).
- ✅ **Fale conosco** (`fale-conosco.controller.js`) envia `POST /contato/registro`; ver divergência em [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API]]. **Pesquisa de satisfação** envia `POST /v2/pesquisa-satisfacao/`.
- ✅ **Aviso de versão mobile**: `MainController` abre o modal `#modalMobile` quando `screen.width < 1023` e não há `redirect`/`modal` em `sessionStorage`; redirecionamento automático ao app está comentado.
- ✅ Testes: 9 specs (módulos `acessibilidade`, `breadcrumb` e `pagina-inicial`; serviço do *breadcrumb*; módulo, serviço e diretiva do carrossel de vídeo; diretivas de contraste e de fonte).

## Inferências e limitações
- 🔶 Textos institucionais (`sobre`, `faq`, `legislacao`) são conteúdo estático em HTML; sua vigência não é verificável pelo código.
- ❓ Rodapé/topbar contêm links externos que não foram enumerados (edição recente: commit `c4e6d508`, revertido).
- Cobertura parcial: diretivas visuais e SCSS lidos por amostragem.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Arquitetura-AngularJS|Arquitetura]] · [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|Integrações externas]] · Backend: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados|Apoio e atualização de dados]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
