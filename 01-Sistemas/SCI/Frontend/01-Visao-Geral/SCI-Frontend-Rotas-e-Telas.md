---
type: reference
aliases:
  - "SCI Frontend — rotas e telas"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/app-routing.module.ts
  - src/app/pages/pages-routing.module.ts
  - src/app/pages/jad
  - src/app/pages/pip
  - src/app/pages/administracao
  - src/app/pages/demanda
  - src/app/components/layout/sidenav
  - src/app/store/services/perfil-entrada.service.ts
---
# SCI Frontend — rotas e telas

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Mapear as rotas do Angular Router, o controle por perfil (`data.role`) e a porta de entrada de cada perfil.

## Evidências
- `app-routing.module.ts`, `pages-routing.module.ts` e os 17 arquivos `*-routing.module.ts` das áreas.
- `components/layout/sidenav/sidenav.component.ts` (visibilidade do menu) e `store/services/perfil-entrada.service.ts` (rota inicial por perfil).

## Informações confirmadas
### Raiz
| Rota | Destino |
|---|---|
| `''` | redireciona para `pages` |
| `auth/login`, `auth/acesso-negado` | `AuthModule`; sem guard |
| `validacao` | `PublicModule`; página pública de validação de assinatura |
| `pages/**` | `PagesModule`; `AuthGuard` em cada área; `**` redireciona para `''` |

### `pages/*` (guard `AuthGuard`; `data.role` = perfis aceitos)
| Rota | Perfis | Conteúdo |
|---|---|---|
| `home` | todos os 11 perfis de negócio | tela inicial com o perfil do usuário |
| `demanda` | Autoridade Correcional, Apoio Correcional | `caixa-entrada-autoridade`, `caixa-entrada-apoio`, lista, `editar/:id`, `tratar/:id`, `visualizar/:id` |
| `jad` | Autoridade, Assessor Autoridade, Analista, Gestor Admissibilidade, Apoio, Revisor Jad | `cadastro`, `caixa-entrada`, `analise` (cada filha repete o `data.role`) |
| `pip` | Autoridade, Assessor Autoridade, Gestor Pip, Apoio, Investigador Pip, Revisor Pip | `caixa-entrada`, `instaurar`, `editar`, `analisar`, `diligencia` |
| `gerenciador` | Autoridade, Gestor Admissibilidade | `buscar-processos` |
| `gestao` | Gestor Gerencial | painel Power BI incorporado |
| `administracao` | Administrador | usuários, assuntos, unidades |
| `denuncias` | **sem `data.role`** (só autenticação) | lista e `analisar/:id` |
| `encaminhados` | **sem `data.role`** (só autenticação) | lista e `visualizar/:idProcesso` |

### Subrotas relevantes
- `jad/cadastro`: `jad-list`, `jad-visualizar/:idJad`, `:idJad/listar-fatos`, `fato/novo`, `fato/:idFato/editar`, envolvidos (`listar-envolvidos`, `envolvido/novo`, `envolvido/:idEnvolvido/editar`, `condutas`), evidências (`listar-evidencias`, `evidencia/novo`, `.../editar`).
- `jad/caixa-entrada`: uma caixa por perfil (`caixa-entrada-autoridade`, `-assessor-autoridade`, `-gestor`, `-apoio`, `-analista`, `-revisor`), `analise/:idJad` (`nota-tecnica`, `visualizar-analise/:idAnalise`, `visualizar-demanda`, `criar-nota`, `alterar-concluir-nota`), `nota-tecnica/:idJad`, `registrar-numero-sei/:idJad`.
- `jad/analise/:idJad`: `jad-matriz`, `jad-registrar`, `analise-envolvido`, `fundamentacao-analise`, `visualizar-analise`, `reprovar-revisao`, `concluir-revisao-preliminar`, `concluir-revisao-analise`. Perfis: analista, autoridade, assessor, gestor e revisor Jad.
- `pip/caixa-entrada`: `-investigador`, `-revisor`, `-autoridade`, `-apoio`, `-gestor`, `-assessor-autoridade`, `redistribuir-relatoria/:idPip` (Gestor Pip e Autoridade), `analise-assessor/:idPip`.
- `pip/instaurar`: `listar-pip-unidade` (Autoridade, Apoio, Gestor Pip, Revisor Pip), `iniciar-despacho-pip/:idPip` (Apoio), `concluir-despacho-pip/:idPip` (Autoridade, Apoio), `visualizar-despacho-pip/:idPip` (Autoridade), `registrar-pip-sei/:idPip` (Apoio), `visualizar/:idPip`, `designar-investigadores-pip/:idPip` (Gestor Pip).
- `pip/editar`: `pip-list`, `assinar-relatorio-pip/:idPip`, `:idPip/listar-fatos`, `fato/novo`, `fato/:idFato/...` (envolvidos, evidências, condutas) com `AlterarPipGuard`.
- `pip/analisar/:idPip` (Investigador, Gestor Pip, Autoridade, Revisor Pip): `pip-matriz`, `pip-registrar`, `pip-analisar`, `fundamentacao-analise-pip`, `providencias-adicionais-pip`, `visualizar-analise`, `reprovar-revisao`, `concluir-revisao`.
- `pip/diligencia` (Investigador, Revisor Pip): `diligencia/:pipId/cadastrar`, `diligencia/:pipId/editar/:diligenciaId`, `listar-diligencias/:pipId`.
- `administracao`: `listar-usuarios`, `cadastrar-usuario`, `exibir-usuario/:id`, `listar-assuntos`, `criar-assunto`, `exibir-assunto/:id`, `listar-unidades`, `editar-unidade/:id`.

### Entrada por perfil (`PerfilEntradaService.obterRotaInicial`)
Investigador, Revisor e Gestor Pip → caixa de entrada PIP correspondente; Autoridade → `demanda/caixa-entrada-autoridade`; Assessor, Analista, Gestor e Revisor Jad → caixa de entrada JAD correspondente; Apoio → `demanda/caixa-entrada-apoio`; demais → `jad/cadastro/jad-list`. O menu lateral decide por perfil quais grupos aparecem (denúncias, demandas, admissibilidade, PIP, buscar processos, encaminhados, gestão, administração).

## Inferências e limitações
- 🔶 O login navega para `/home`, rota que não existe na raiz; o curinga `**` redireciona para `''` e daí para `pages/home` (funciona por redirecionamentos em cadeia).
- 🔶 A rota `administracao` repete `exibir-assunto/:id` duas vezes (duplicidade inofensiva, a primeira vence).
- ❓ Rotas `pip/caixa-entrada/*` por perfil aparecem sem `data.role` próprio, exceto `redistribuir-relatoria`; a proteção é a do pai `pip/caixa-entrada`.
- A visibilidade de botões dentro das telas (por status e perfil) não foi percorrida tela a tela.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Perfis-e-Ambientes|Perfis e ambientes]] · [[01-Sistemas/SCI/Frontend/08-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Segurança e sessão]] · módulos em [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
