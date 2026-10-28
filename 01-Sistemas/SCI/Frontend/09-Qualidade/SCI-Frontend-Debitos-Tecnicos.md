---
type: technical-debt
aliases:
  - "SCI Frontend — débitos técnicos e riscos"
system: SCI
component: Frontend
repository: sci-frontend
status: inferido
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/store/services
  - src/app/core/guard
  - src/app/pages
  - Dockerfile
---
# SCI Frontend — débitos técnicos e riscos

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Listar riscos e melhorias observados, **separados dos fatos** (🔶 = recomendação ou hipótese; os fatos estão nas notas de origem).

## Evidências
- Leitura estática do `sci-frontend` no commit `5e20fda`. Nada foi executado.

## Informações confirmadas (fatos que sustentam os itens)
| # | Fato | Origem |
|---|---|---|
| 1 | 8 chamadas do cliente não têm rota no backend analisado, 3 delas usadas em telas (`denuncia/{id}`, `denuncia/{id}/download`, `pessoa/processos`) | [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]] |
| 2 | Rotas `denuncias` e `encaminhados` não têm `data.role`; só aceite e recusa têm checagem de perfil no componente | [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Rotas-e-Telas|Rotas e telas]] |
| 3 | Aceitar e recusar denúncia: cliente restringe a `Apoio Correcional`; catálogo do backend indica política da autoridade | [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Denuncia-e-Demanda|Denúncia e demanda]] |
| 4 | Token em cookie legível por JavaScript, sem `Secure`/`SameSite` no `set`; sem renovação | [[01-Sistemas/SCI/Frontend/08-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Segurança e sessão]] |
| 5 | URL de painel Power BI fixa no código-fonte | [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Integracoes|Integrações]] |
| 6 | Nenhum teste automatizado | [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Testes-e-Cobertura|Testes]] |
| 7 | `cadastrar-usuario` volta para uma rota inexistente; login navega para `/home` (depende do curinga); rota `exibir-assunto/:id` duplicada | [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Administracao-e-Gestao|Administração]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Rotas-e-Telas|Rotas]] |
| 8 | Lista do investigador filtra por siglas `AAS` e `AG` que não existem em `StatusPipEnum`; status duplicados como literais em vários componentes | [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-PIP|PIP]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-JAD-Admissibilidade|JAD]] |
| 9 | `Dockerfile` usa `npm install --force`; `package.json` contém `"sci-novo": "file:"` e `mute-stream`/`wrap-ansi` como dependências de aplicação | [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Stack-e-Dependencias|Stack]] |
| 10 | 5 chamadas `console.error`/`console.log` em componentes; `bypassSecurityTrustResourceUrl` em 2 pontos; `AuthInterceptor` anexa o token a toda requisição | código |

## Inferências e limitações (riscos e recomendações)
1. 🔶 **Contrato cliente–servidor desalinhado** (item 1): confirmar a versão do backend implantada; tela de denúncia e gerenciador falhariam com o backend analisado.
2. 🔶 **Autorização só no cliente** (itens 2 e 3): conferir se o backend barra os perfis; resolver o conflito Apoio × Autoridade em aceitar/recusar.
3. 🔶 **Sessão** (item 4): avaliar cookie `Secure`/`SameSite`, expiração e armazenamento menos exposto a XSS; limitar o `AuthInterceptor` à `apiUrl`.
4. 🔶 **Painel Power BI** (item 5): mover a URL para `environment` e confirmar se o relatório é de acesso público.
5. 🔶 **Testes** (item 6): cobrir `AuthGuard`, `AuthInterceptor`, `ErrorInterceptor` e as regras de status ↔ ação.
6. 🔶 **Limpeza** (itens 7 a 10): corrigir rotas, centralizar siglas de status, revisar dependências e remover logs.
- Impacto real de cada risco depende de execução e de configuração de implantação, não verificadas.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos do backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
