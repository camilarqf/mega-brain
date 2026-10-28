---
type: flow
aliases:
  - "Frontend Cidadão — fluxo da caixa de entrada"
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
sources:
  - src/app/pages/caixa-entrada/caixa-entrada-routing.module.ts
  - src/app/pages/caixa-entrada/manifestacao/consultar-manifestacoes/consultar-manifestacoes.component.ts
  - src/app/pages/caixa-entrada/manifestacao/detalhar-manifestacao/detalhar-manifestacao.component.ts
  - src/app/pages/caixa-entrada/manifestacao/responder-pesquisa-manifestacao/responder-pesquisa-manifestacao.component.ts
  - src/app/pages/caixa-entrada/pedido-informacao/consultar-pedidos/consultar-pedidos.component.ts
  - src/app/pages/caixa-entrada/pedido-informacao/detalhar-pedido/detalhar-pedido.component.ts
  - src/app/pages/caixa-entrada/pedido-informacao/responder-pesquisa-pedido/responder-pesquisa-pedido.component.ts
---

# Frontend Cidadão — fluxo da caixa de entrada

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Tramitação-e-Resposta]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Recursos-e-Instâncias]]

## Objetivo
Descrever o que o cidadão logado faz com as próprias manifestações e pedidos: consultar, complementar, avaliar, recorrer e responder pesquisas.

## Evidências
Arquivos em `sources`, commit `d250804`. Cobertura `parcial`: componentes de listagem lidos por chamadas.

## Informações confirmadas
O módulo inteiro (`caixa-entrada`) exige `AuthGuard`.

### Manifestações
| Rota | Ação | Chamada |
|---|---|---|
| `minhas-manifestacoes` | Lista com filtros | `POST servico-ouvidoria/manifestacao/manifestante/itens-filtro` |
| `manifestacao/:id` | Detalhe | `POST servico-ouvidoria/manifestacao/manifestante/detalhe` |
| (detalhe) | Responder pedido de complementação da ouvidoria | `POST servico-ouvidoria/complementacao/responder` |
| (detalhe) | Complementação pró-ativa do cidadão | `POST servico-ouvidoria/complementacao/pro-ativa` |
| (detalhe) | Avaliar a resposta | `POST servico-ouvidoria/manifestacao/avaliar` |
| (detalhe) | Baixar anexo / imprimir PDF | `POST servico-ouvidoria/arquivo/download-manifestante`, `.../manifestacao/exportar-pdf-manifestante` |
| (detalhe) | Registrar manifestação vinculada | limpa o rascunho e abre `registro-manifestacao` com `manifestacaoVinculada` (`Id` e `Protocolo`) |
| `pesquisa-manifestacao/:id` | Pesquisa de satisfação | `POST questionario`, `POST questionario/responder` |

### Pedidos
| Rota | Ação | Chamada |
|---|---|---|
| `meus-pedidos` | Lista paginada com filtros | `POST acesso-informacao/pedido/manifestante/itens-filtro`, `POST acesso-informacao/pedido/manifestante/` |
| `pedido/:id` | Detalhe | `POST acesso-informacao/pedido/detalhar-por-manifestante` |
| (detalhe) | Ações permitidas ao autor | `POST acesso-informacao/pedido/acoes-autor` |
| (detalhe) | Detalhar um evento do histórico | `POST acesso-informacao/pedido/detalhar-evento-pedido/` |
| (detalhe) | Recurso de 1ª, 2ª ou 3ª instância | `POST acesso-informacao/recurso/primeira-instancia/registrar` · `segunda-instancia` · `terceira-instancia`; justificativas em `GET acesso-informacao/recurso/justificativa` |
| (detalhe) | Baixar anexo / comprovante | `POST acesso-informacao/arquivo/download`, `.../pedido/exportar-pedido-usuario` |
| `pesquisa-pedido/:id` | Pesquisa de satisfação | `POST acesso-informacao/questionario`, `.../questionario/responder-pesquisa` |

- ✅ Os três editores de recurso são montados no frontend (título, rótulo e endpoint); todos exigem `Motivacao` e `JustificativaRecurso`; o envio inclui os `Arquivos` e recarrega a página.
- ✅ Quais ações aparecem ao autor (por exemplo, recorrer) vêm de `acoes-autor`, ou seja, a regra de elegibilidade e prazo está no backend, não no frontend.
- ✅ O limite de 2.000 caracteres vale para a resposta de complementação (`maxCaracteres` no detalhe da manifestação).

## Inferências e limitações
- 🔶 O frontend chama `window.location.reload()` após registrar o recurso e ao navegar entre manifestações vinculadas (atualização por recarga completa).
- ❓ Mapeamento exato entre `acoes-autor` e os botões/editores de recurso não foi lido.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Pedido-e-Recurso|Pedido-e-Recurso (Backend)]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-do-SIC|Regras-de-Prazo-do-SIC]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas-de-API]]

## Pendências e próximo passo
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]].
