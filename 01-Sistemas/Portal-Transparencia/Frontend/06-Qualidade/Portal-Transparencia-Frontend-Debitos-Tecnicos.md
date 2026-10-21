---
type: technical-debt
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
  - debitos-tecnicos
sources:
  - package.json
  - bower.json
  - Dockerfile
  - .bowerrc
  - src/app/index.route.js
  - src/app/config.js
  - src/app/components/compartilhado/services
---

# Frontend — débitos técnicos e riscos

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Listar débitos e riscos **separados dos fatos**: a coluna "Fato" é verificável no código; "Recomendação" é sugestão.

## Evidências
Commit `dca3e933`; arquivos em `sources`. Leitura estática.

## Informações confirmadas
| # | Fato (✅) | Risco / impacto | Recomendação |
|---|---|---|---|
| 1 | AngularJS 1.4.x, Node 6.11, gulp 3, PhantomJS 2, Bower e Karma 0.13 (manifestos e `Dockerfile`) | Tecnologias sem suporte; vulnerabilidades sem correção; difícil contratar/atualizar | Plano de migração (AngularJS → Angular atual) ou, no mínimo, isolar o build em imagem fixa e varrer dependências |
| 2 | `src/app/config.js` versionado com endereços de infraestrutura; é regenerado a cada `gulp --profile` | Expõe topologia interna; ruído em *diffs*; risco de subir perfil errado | Remover do Git (gerar no build) e usar caminhos relativos via proxy |
| 3 | `.bowerrc` com `strict-ssl: false` | Instalação de dependências sem verificar TLS | Corrigir a cadeia de certificados e remover a exceção |
| 4 | Sem pipeline versionado (`Jenkinsfile.prod` removido em 2026-10-14) | Build/deploy não reproduzível a partir do repositório | Versionar o pipeline ou documentar o processo |
| 5 | `index.route.js` com 2170 linhas, 103 rotas, lógica repetida de `resolve`; `var ANO_ATUAL = 2019` sem uso | Difícil manutenção | Dividir por módulo de área |
| 6 | 22 usos de `$http(...).success/.error` (removidos no AngularJS 1.6) | Bloqueia atualização do AngularJS | Trocar por `.then` |
| 7 | Chamadas sem rota correspondente no Backend (ver [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend\|Integração com a API]]) e `POST /contato/registro` | Erros 404 em telas ou funcionalidade morta | Confirmar uso e remover/alinhar |
| 8 | Código legado: `/old`, `todo-widget`, `upload.controller.js` (`url: '#'`), rotas comentadas (`restos-a-pagar`, `execucao-emendas`, `acao`, `servidores/tabela`) com controllers ainda presentes | Peso e confusão | Remover após confirmação |
| 9 | Dois controllers de bens móveis; reuso do `OrdemBancariaController` em Convênios | Acoplamento entre módulos | Rever |
| 10 | Debug ligado (`$logProvider.debugEnabled(true)`), 14 `console.log` | Vazamento de informação no console | Desligar em produção |
| 11 | Testes: 28 specs, 1 e2e frágil (`browser.sleep`), sem cobertura em vários módulos | Regressões não detectadas | Ver [[01-Sistemas/Portal-Transparencia/Frontend/06-Qualidade/Portal-Transparencia-Frontend-Testes-e-Cobertura\|Testes e cobertura]] |
| 12 | Serviços `*.service.js` repetem o mesmo padrão manual de `$http` (359 chamadas) e `RelatorioService` ignora erro | Duplicação | Camada de cliente da API centralizada com tratamento de erro |
| 13 | CPF no caminho da URL na busca (ver [[01-Sistemas/Portal-Transparencia/Frontend/05-Seguranca/Portal-Transparencia-Frontend-Seguranca-e-Privacidade\|Segurança e privacidade]]) | Exposição em *logs* | Enviar por *query*/`POST` ou mascarar |

## Inferências e limitações
- 🔶 A relevância de cada item depende de decisões do time (ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]]).
- Cobertura parcial: não foi feita varredura automática de dependências nem análise de desempenho (tamanho do *bundle*).

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/08-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Débitos do Backend]]

## Pendências e próximo passo
- Priorizar com o time; ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Registro-de-Analise|Registro de análise]].
