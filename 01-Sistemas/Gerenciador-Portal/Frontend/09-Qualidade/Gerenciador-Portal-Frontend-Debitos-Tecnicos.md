---
type: technical-debt
aliases:
  - "Débitos técnicos — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/app/components
  - src/app/config.js
  - bower.json
  - Dockerfile
  - .bowerrc
---
# Débitos técnicos — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Listar débitos, riscos e melhorias, **separados dos fatos** das demais notas. Cada item aponta a evidência.

## Evidências
Leitura dos controllers, serviços de API, `bower.json`, `Dockerfile` e `config.js`.

## Informações confirmadas
### Fatos (evidência no código)
| # | Fato | Evidência |
|---|---|---|
| 1 | Sem guarda de rota, sem token e sem tratamento de `401` | [[01-Sistemas/Gerenciador-Portal/Frontend/08-Seguranca/Gerenciador-Portal-Frontend-Seguranca-e-Sessao|Segurança e sessão]] |
| 2 | `CargaController.retornarListaDeCargas` chama método inexistente | `cargaCtrl.js:20-25`, `cargaApi.js` |
| 3 | `apiPortal` e `apiSuperbusca` injetadas e sem uso; perfil `teste` não as define | `exclusoesMedidaProtetivaApi.js:1`, `config.json` |
| 4 | `src/app/config.js` gerado, mas versionado e desatualizado | `config.js` × `config.json` |
| 5 | Mistura de jQuery com AngularJS nos controllers (modais, backdrop) | `arquivoCtrl.js`, `cargaCtrl.js` |
| 6 | `console.log` de depuração e dados no console | `arquivoCtrl.js` (`filtroInicial`), `palavraCtrl.js` |
| 7 | Controllers extensos (`arquivoCtrl` 504 e `imagemCtrl` 406 linhas) com duplicação dos avisos `toaster.pop` e do tratamento do `"OK"` | idem |
| 8 | Valores fixos de negócio no código (categorias 43–47, 50–59, 55 e 56; posições de tipos de referência; ordem dos cartões de carga) | `arquivoCtrl.js`, `imagemCtrl.js`, `cargaCtrl.js` |
| 9 | Falhas de API sem aviso ao usuário em várias telas (palavras, órgãos, arquivos, cargas) | `.then` sem erro |
| 10 | `bower update` no `Dockerfile` e dependências Git sem versão fixa; `strict-ssl: false` | `Dockerfile`, `bower.json`, `.bowerrc` |
| 11 | Stack fora de suporte: AngularJS 1.6, Node 6, Gulp 3, PhantomJS | [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Stack-e-Dependencias|Stack]] |
| 12 | Nenhum teste automatizado | [[01-Sistemas/Gerenciador-Portal/Frontend/09-Qualidade/Gerenciador-Portal-Frontend-Testes-e-Cobertura|Testes]] |
| 13 | `Dockerfile` não define como servir `dist/` | `Dockerfile` |
| 14 | `LoginController.main` e `recuperarImagemBackgroundPorPainelId` sem uso; item "Textos Portal" comentado no menu | `loginCtrl.js`, `imagemApi.js`, `navbar.html` |
| 15 | Upload leva `null` na URL se não houver categoria/ano filtrados; e envia login no caminho | `arquivoCtrl.js:62-64` |
| 16 | `bloquearBotaoPesquisar` referencia campos inexistentes | `exclusoesMedidaProtetivaCtrl.js:193-195` |

## Inferências e limitações
### Recomendações (não são fatos)
- 🔶 Prioridade alta: autenticação com token validado no servidor e guarda de rota (itens 1, 15).
- 🔶 Remover código morto e `console.log` (2, 3, 6, 14, 16); tirar `config.js` do Git (4).
- 🔶 Fixar versões e travar o build (10); definir servidor web e pipeline no repositório (13).
- 🔶 Extrair constantes de negócio e uma função única de aviso (7, 8); tratar erros de API (9).
- 🔶 Migração do AngularJS (11) é decisão de roadmap, não corrigível pontualmente.
- ❓ Esforço e prioridade reais dependem do time.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos do Backend]] · [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Arquitetura-AngularJS|Arquitetura]]

## Pendências e próximo passo
- Validar a lista com o time.
