---
type: analysis-log
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
commit_data: 2026-10-08
branch: master
tags:
  - sci
  - frontend
  - registro
---
# SCI Frontend — registro de análise

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] · [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]]

## Objetivo
Controlar lotes, cobertura e o próximo passo da análise do `sci-frontend`.

## Evidências
- `git rev-parse HEAD` = `5e20fda1ec781719cb277c36d160db2efd5a6c1b`, branch `master`, último commit em 2026-10-08.
- Árvore de trabalho: `src/environments/environment.dev.ts` modificado e `docs/` não rastreado. **Fora do escopo** por decisão do usuário (o documento em `docs/` não foi incluído).
- Autorização do usuário em 2026-10-19: o `sci-frontend` pertence ao sistema `SCI`; executar os lotes 0 a 4.

## Informações confirmadas
### Lotes
| Lote | Escopo | Estado |
|---|---|---|
| 0 | stack, arquitetura, perfis e ambientes | concluído |
| 1 | rotas e telas, segurança e sessão, fluxo de autenticação | concluído |
| 2 | módulos: denúncia/demanda, JAD, PIP, encaminhamento/gerenciador, administração/gestão, assinatura/validação | concluído (por rotas, serviços, enums e amostragem de componentes) |
| 3 | chamadas de API e integrações; confronto com o `sci-backend` | concluído |
| 4 | fluxos (denúncia → admissibilidade, ciclo do PIP), testes, débitos | concluído |

### Cobertura por área
| Área | Lido integralmente | Lido parcialmente | Não lido |
|---|---|---|---|
| `package.json`, `angular.json`, `Dockerfile` | ✅ (configs) | Jenkinsfiles (cabeçalho) | |
| `app-routing`, `pages-routing` e 17 roteadores | ✅ | | |
| `core/guard`, `core/interceptors`, `meta.reducer` | ✅ | | |
| `store/services` (25) | URLs de todos | corpo dos métodos | |
| `store/actions`, `effects`, `reducers`, `selectors` | | `usuario`, `assinatura` | demais |
| `core/enums` | ✅ (status, perfis, tipos) | | |
| `pages/denuncias`, `pages/gerenciador`, `pages/gestao`, `pages/encaminhados` | `analisar-denuncia` (lógica), gerenciador, gestão | `encaminhados` | templates |
| `pages/jad`, `pages/pip` | rotas e serviços | `caixa-entrada-gestor`, listas | maior parte dos componentes e templates |
| `pages/administracao` | rotas | `cadastrar-usuario` | demais |
| `components/layout/sidenav`, `tratar-demanda` | lógica | | demais componentes |
| `*.html`, `*.scss` | | `login`, `sidenav` | restante |
| `core/models`, `core/view-models` | | | DTOs (sem comparação campo a campo) |
| Execução (`ng build`, `ng test`, app) | | | não executado |

### Confronto com o backend
- Script de extração local (não versionado) comparou verbo + caminho das chamadas do cliente com os atributos `[Route]` e `[Http*]` dos controllers do `sci-backend` no commit `8e3c8648`: 136 de 144 combinações coincidem; 8 sem rota (ver [[01-Sistemas/SCI/Frontend/04-API-e-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]]).

### Alterações de estrutura no cofre (2026-10-19)
- Criada a pasta `01-Sistemas/SCI/Frontend/` com 21 notas.
- Atualizados: `Catalogo-de-Sistemas`, `Mapa-de-Integracoes`, `SCI-Index`, `SCI-Repositorios` e a pergunta 1 de [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências do backend]]. Serviço externo `Power-BI` cadastrado.

## Inferências e limitações
- Análise estática: nenhuma regra foi observada em execução.
- Conflitos relatados, não resolvidos: Apoio × Autoridade em aceitar/recusar denúncia; endpoints do cliente ausentes no backend; página pública de validação × endpoint autenticado.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro do backend]]

## Pendências e próximo passo
1. Responder as perguntas de [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]] (principalmente 1 a 3).
2. Lote 5 (opcional): ler os componentes de análise e revisão do JAD e do PIP, as caixas de entrada restantes, `core/models` (DTOs) e comparar com os `Requests/Responses` do backend; ler `Jenkinsfile.*` por completo.
3. Após novos commits: `git diff 5e20fda1ec781719cb277c36d160db2efd5a6c1b..HEAD --stat` e reabrir as notas cujos `sources` mudaram (`atualizar-documentacao`).
4. Sincronização do cofre só com `sincronizar-brain` e autorização da categoria de conteúdo (b).
