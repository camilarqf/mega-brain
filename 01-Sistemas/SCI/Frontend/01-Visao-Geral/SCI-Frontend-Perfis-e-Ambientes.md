---
type: reference
aliases:
  - "SCI Frontend — perfis e ambientes"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/core/enums/user-roles.enum.ts
  - src/app/core/enums/Perfil.enum.ts
  - src/app/pages/pages-routing.module.ts
  - src/environments
  - angular.json
---
# SCI Frontend — perfis e ambientes

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Listar os perfis conhecidos pelo cliente e a configuração por ambiente (sem valores).

## Evidências
- `core/enums/user-roles.enum.ts`, `core/enums/Perfil.enum.ts`, `pages/pages-routing.module.ts` e demais roteadores, `environments/*.ts`, `angular.json`.

## Informações confirmadas
### Perfis (`UserRoles`, texto comparado ao campo `perfil` do usuário autenticado)
| Valor | Áreas liberadas nas rotas de `/pages` |
|---|---|
| `Administrador` | `home`, `administracao` |
| `Autoridade Correcional` | `home`, `demanda`, `jad`, `pip`, `gerenciador`; menu também mostra `denuncias` e `encaminhados` |
| `Assessor Autoridade` | `home`, `jad`, `pip` (caixa de entrada) |
| `Analista de Admissibilidade` | `home`, `jad` |
| `Gestor Admissibilidade` | `home`, `jad`, `gerenciador` |
| `Revisor Jad` | `home`, `jad` |
| `Apoio Correcional` | `home`, `demanda`, `jad`, `pip`; menu mostra `denuncias` (e só ele aceita ou recusa); a tela inicial exibe "Apoio a Autoridade" |
| `Gestor Pip` | `home`, `pip` |
| `Investigador Pip` | `home`, `pip` |
| `Revisor Pip` | `home`, `pip` |
| `Gestor Gerencial` | `home`, `gestao` |
| `FEATURE_DISABLED` (`bloqueado`) | valor reservado; nenhuma rota o lista |

As rotas `denuncias` e `encaminhados` têm só `AuthGuard`, sem `data.role` (acesso por URL a qualquer usuário autenticado). Detalhe em [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Rotas-e-Telas|Rotas e telas]]. `PerfilEnum` (numérico, 1 a 5) existe em `Perfil.enum.ts`; uso não procurado.

### Ambientes
- ✅ `environment.ts` reexporta `environment.dev`; os arquivos `dev`, `hom` e `prod` definem as chaves `production`, `apiUrl` e `participaUrl` (valores omitidos).
- ✅ `apiUrl` é a base de todas as chamadas ao `sci-backend`; `participaUrl` só é usada nos links da tela de login (ver [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Integracoes|Integrações]]).
- ✅ `environment.dev.ts` estava modificado na árvore de trabalho; fora do escopo e não registrado.
- ✅ Perfis de build `development`, `homolog` e `production` ([[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Stack-e-Dependencias|Stack]]).

## Inferências e limitações
- 🔶 Os nomes de perfil precisam coincidir letra a letra com o texto devolvido pelo backend; a comparação com [[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização do backend]] não foi feita.
- A tabela vem das rotas e do menu; o que cada tela permite por perfil só foi lido onde indicado nos módulos.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/08-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Segurança e sessão]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
