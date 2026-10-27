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
  - prestando-contas
  - dados-pessoais
sources:
  - src/app/index.route.js
  - src/app/components/prestando-contas
---

# Frontend — módulo Prestando Contas

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Maior módulo do frontend (86 arquivos, 28 rotas): relatórios e dados de transparência ativa — programas sociais e beneficiários, órgãos deliberativos e conselhos, processos disciplinares, empresas punidas, entre outros.

## Evidências
Commit `dca3e933`. `index.route.js`; `components/prestando-contas/**` (30 JS, 52 HTML); `prestando-contas.service.js` (59 chamadas), `pads/pads.service.js` e `pips/pips.services.js` (6 cada).

## Informações confirmadas
**Rotas por tema (28).**
| Tema | Caminhos (`/prestando-contas/…`) | Controllers |
|---|---|---|
| Processos | `pads`, `pips` | `PADsController`, `PIPsController` |
| Contas e relatórios | `relatorio-contas`, `outros-relatorios`, `gastos-publicidade` | `RelatorioContasController`, `OutrosRelatoriosController`, `GastosPublicidadeCtrl` |
| Empresas | `empresa-punida`, `empresas-programa-integridade`, `prospera-df` | `EmpresaPunidaCtrl`, `EmpresaProgramaIntegridadeController`, `ProsperaDfController` |
| Órgãos e entidades | `conselhos`, `conselheiros`, `organizacoes-sociais-saude`, `orgaos-deliberativos/saiba-mais`, `shows-eventos` | `OrgaoDeliberativoController`, `ConselheiroController`, `OrganizacoesSociaisSaudeController`, `ShowsEventosController` |
| Beneficiários | `beneficiario/{programas-sociais, renda-emergencial, prato-cheio, cartao-material-escolar, artistico-cultural, mobilidade-cidada}`, `beneficiarios-acoes-emergenciais/saiba-mais`, `mobilidade-por-bicicleta` e páginas "saiba mais"/legislação correspondentes | `Beneficiario*Controller`, `*SaibaMaisController` |

Rotas `noLink` (apenas rótulo de navegação): `/prestando-contas`, `/prestando-contas/beneficiario`, `…/programa-social`, `…/cartao`. Há rota comentada de `beneficiarios-bolsa-alimentacao` (o controller continua no repositório).

- ✅ Serviços: `/prestando-contas/*` (várias famílias por programa), `/empresa-punida/*`, `/texto-explicativo/beneficiario/programa-social`, `/dataAtualizacao/*`, PADs e PIPs (`…/processos-administrativos-disciplinares/*`, `…/processos-investigacoes-preliminares/*`).
- ✅ Exportação: 15 controllers chamam `RelatorioService.exportar('/prestando-contas/relatorio(s)/…')`.
- ✅ Testes: 3 specs (empresa punida, órgão deliberativo, órgãos deliberativos "saiba mais").

## Inferências e limitações
- ⚠️ 🔶 As telas de beneficiários de programas sociais e de conselheiros exibem **dados de pessoas físicas** vindos do Backend (campos exatos não conferidos); a proteção (mascaramento) está no Backend: [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]. O frontend não aplica máscara própria (não verificado em todos os templates).
- ✅ Chamada sem rota no Backend: `GET /prestando-contas/detalhamento-conselheiro`.
- 🔶 Várias telas sazonais (renda emergencial, prato cheio, auxílio emergencial) parecem ligadas a programas da pandemia; vigência ❓.
- Cobertura parcial: dos 30 controllers só a estrutura e o serviço foram lidos.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Prestacao-de-Contas|Backend: Prestação de Contas]] · [[01-Sistemas/Portal-Transparencia/Frontend/08-Seguranca/Portal-Transparencia-Frontend-Seguranca-e-Privacidade|Segurança e privacidade]] · [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
