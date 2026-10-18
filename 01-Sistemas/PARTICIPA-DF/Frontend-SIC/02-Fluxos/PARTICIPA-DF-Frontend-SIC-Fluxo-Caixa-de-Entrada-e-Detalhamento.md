---
type: flow
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - fluxo
  - caixa-de-entrada
  - pedido
  - recurso
sources:
  - app/caixa-entrada/caixa-entrada-unidade-ctrl.js
  - app/caixa-entrada/caixa-entrada-unidade.html
  - app/caixa-entrada/detalhamento-pedido-ctrl.js
  - app/caixa-entrada/detalhamento-pedido.html
  - app/upload/upload-arquivos-directive.js
  - app/upload/upload-pedido-directive.js
  - app/shared/storage-service.js
---

# Frontend SIC — caixa de entrada e detalhamento do pedido

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Rotas: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Rotas-e-Telas|Rotas-e-Telas]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Endpoints-SIC|Endpoints-SIC]]

## Objetivo
Descrever a lista de pedidos da unidade do operador e o tratamento de um pedido (respostas, recursos, decisões, SEI, reencaminhamento, prorrogação).

## Evidências
Arquivos em `sources`, commit `5518a81`. `detalhamento-pedido.html` (799 linhas) lido só pelas ações e pelos blocos de anexos.

## Informações confirmadas

### Caixa de entrada (`/`, `/caixa-entrada`)
1. ✅ Ao abrir, `init()` cria a única *view* "Caixa de Entrada" (endpoint `acesso-informacao/pedido/unidade`), consulta as permissões (`operador-sic/consultar-permissoes`), carrega as opções de filtro (`acesso-informacao/pedido/unidade/itens-filtro`: assuntos e situações) e o último filtro guardado em `localStorage`.
2. ✅ **Filtros rápidos** (um por vez; trocam todo o filtro): em andamento (padrão), não visualizado, respondido, fora do prazo, em recurso, em reclamação, concluído, deferido.
3. ✅ **Filtros avançados**: período de entrada, vencimento do prazo, unidade, assuntos, situações, autor, palavra-chave, "pesquisar textos dos recursos", possui recurso de 1ª/2ª/3ª instância.
4. ✅ **Ordenação** por colunas (data de entrada, protocolo, assunto, unidade, situação, prazo); clique alterna descendente → ascendente → padrão (data de entrada, descendente). Paginação por `PageNumber`.
5. ✅ Quando há filtro aplicado, a *view* inteira é guardada em `localStorage` e restaurada na próxima visita (limpa por `removeFilters`/`removeCache` ou em erro).
6. ✅ **Exportação**: mesmo endpoint com `ExportacaoConfig` (formato único **CSV**; grupos: dados básicos, recursos de 1ª/2ª/3ª instância, histórico, anexos) e `DescricaoFiltros`; a resposta é uma mensagem de que o arquivo chegará **por e-mail** cadastrado no ParticipaDF (a geração é do backend).
7. ✅ **Sinalização de prazo** (`sinalizacaoPrazo`, sobre `PrazoVigenteTermino`): menos de 2 dias → vermelho; de 2 a 5 → laranja; `Situacao === 'Respondido 3ª Instancia'` → azul. 🔶 Dias calculados com a hora local do navegador.
8. ✅ O clique em um pedido navega para `/detalhar-pedido/:id`.

### Detalhamento (`/detalhar-pedido/:id`)
1. ✅ Carrega `acesso-informacao/pedido/detalhar-por-unidade` (`{Pedido:{Id}}`) e depois as **ações permitidas** (`acesso-informacao/pedido/acoes-operador`, sem *spinner*) em `pedido.Acoes`.
2. ✅ Botões de ação por código (rótulo do `detalhamento-pedido.html`; semântica 🔶 inferida do rótulo):

| Código | Rótulo | Chamada |
|---|---|---|
| `PRG_PDD` | Prorrogar Prazo | `pedido/prorrogar-prazo` — ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/02-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Prorrogacao-e-Reencaminhamento\|Prorrogação e reencaminhamento]] |
| `RPT_PDD` | Responder Pedido | `pedido/registrar-resposta` |
| `RRE_PDD` | Reencaminhar | `pedido/reencaminharPedido` |
| `RPT_RPI` | Responder Recurso de 1ª Instância | `recurso/primeira-instancia/registrar-resposta` |
| `RPT_RSI` | Responder Recurso de 2ª Instância | `recurso/segunda-instancia/registrar-resposta` |
| `RPP_RTI` | Resposta Preliminar do Recurso de 3ª Instância | `recurso/terceira-instancia/registrar-resposta-preliminar` |
| `RPP_NOR` | Resposta Preliminar da Notificação de Omissão de Resposta | `notificacao/omissao-resposta-cgdf/registrar-resposta` |
| `RPD_PDD` | Resposta Definitiva do Pedido | `pedido/registrar-resposta-definitiva` |
| `DCS_RTI` | Decisão do Recurso de 3ª Instância | `recurso/terceira-instancia/registrar-decisao` |
| `DCS_NOR` | Decisão da Notificação de Omissão de Resposta | `notificacao/omissao-resposta-cgdf/registrar-decisao` |
| `RGS_SEI` | Enviar para o SEI | `pedido/registrar-pedido-sei` (`{Pedido:{Id}, Especificacao}`); a resposta traz o número do processo SEI, exibido ao operador |
| `MPR_PDD` | Imprimir | `pedido/exportar-operador` → PDF em base64 aberto em nova janela |
| `NXR_RQN` | (libera envio de anexos) | `permitir-upload` das diretivas de anexo |
| `RMV_RQV` | (libera remoção de anexos) | `permite-remover` de `uplPedido` |

(prefixo comum das chamadas: `acesso-informacao/`).

3. ✅ **Resposta** (`registrarResposta`): editor com situação da resposta (`acesso-informacao/situacao/situacao-resposta`), classificação (`acesso-informacao/classificacao/por-situacao`), texto e anexos; só `RPT_PDD` consulta tipos de sigilo (`pedido/tipos-de-sigilo`); confirmação (`$ngConfirm`) → `POST` → fecha o editor e recarrega o pedido. Em 3 dos editores (preliminar de 3ª instância, definitiva e preliminar da omissão) a indicação é opcional (`isIndicacaoObrigatoria=false`).
4. ✅ **Decisão** (3ª instância e omissão de resposta): carrega `recurso/terceira-instancia/tipo-decisao`; no envio inclui a `NotificacaoCGDF` do pedido, quando existe.
5. ✅ **Histórico**: `consultarEventoPorId` chama `pedido/detalhar-evento-pedido/` e rola até a seção de detalhe do evento.
6. ✅ **Remover operador atual** (`removerOperadorAtual`): `pedido/remover-operador-atual` e volta à caixa de entrada. 🔶 Não localizei o botão que o aciona nos trechos lidos do template.
7. ✅ **Anexos**: `uplArquivos` (envio, ≤ 25 MB somados, `arquivo/validar`) e `uplPedido` (lista, download por `arquivo/download` em base64, remoção por `arquivo/excluir-por-operador`). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/04-API-e-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]].

## Inferências e limitações
- 🔶 Os códigos de ação têm o sentido do rótulo; o backend é a fonte da verdade (ver [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Endpoints-SIC|Endpoints-SIC]]).
- 🔶 `vm.tipoDeSigilo = vm.comboGrauSigilo.splice(2, ...)` remove os itens a partir do índice 2 de `comboGrauSigilo` e só se aplica ao grau de id 2 em `registrarResposta`; a regra de sigilo não ficou clara.
- 🔶 `$scope.$on('alternarUnidade')` (limpa o cache e recarrega a lista) nunca é disparado: a troca de unidade usa `$route.reload()` em `navCtrl`.
- ❓ Regras de situação, classificação e prazos são do backend; não analisadas aqui.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/02-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Prorrogacao-e-Reencaminhamento|Prorrogacao-e-Reencaminhamento]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Super-Busca|Super-Busca]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/06-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]] · Regras de prazo no backend: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Regras-de-Prazo-do-SIC|Regras-de-Prazo-do-SIC]]

## Pendências e próximo passo
- Confrontar payloads e códigos de ação com os controllers do backend (lote 7 sugerido). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
