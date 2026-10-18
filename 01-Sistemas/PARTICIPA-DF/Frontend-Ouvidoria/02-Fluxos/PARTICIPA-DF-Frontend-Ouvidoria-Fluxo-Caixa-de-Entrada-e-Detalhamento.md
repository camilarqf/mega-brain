---
type: flow
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
tags:
  - participa-df
  - frontend-ouvidoria
  - fluxo
  - manifestacao
  - caixa-de-entrada
sources:
  - app/manifestacao/caixa-de-entrada/caixa-de-entrada-ctrl.js
  - app/manifestacao/caixa-de-entrada/caixa-de-entrada.html
  - app/manifestacao/caixa-de-entrada/detalhar-manifestacao-ctrl.js
  - app/manifestacao/caixa-de-entrada/detalhar-manifestacao.html
  - app/manifestacao/super-busca/super-busca.ctrl.js
  - app/manifestacao/impressao
---

# Frontend Ouvidoria — caixa de entrada, detalhamento e tratamento

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Rotas: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Rotas-e-Telas|Rotas-e-Telas]] · API: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/04-API-e-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]]

## Objetivo
Descrever como o operador lista, filtra, abre e trata uma manifestação do ponto de vista do frontend.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`. Cobertura `parcial`: o template de detalhe (~70 KB) foi lido nas ações e limites de campo, não integralmente. As regras de negócio por trás das ações (quem pode, quando) estão no backend e são devolvidas em `vm.acoes`.

## Informações confirmadas

### 1. Caixa de entrada (`/`, `caixaDeEntradaCtrl`)
- ✅ Duas visões: **Principal** (`servico-ouvidoria/manifestacao/na-unidade`) e **Registradas por esta unidade** (`.../registrada-na-unidade`), ambas `POST` com o filtro e `PageNumber`.
- ✅ Filtros: ano, unidade (e subordinadas), período, classificação, assunto, situação, ação do último trâmite, pesquisa de satisfação, relato, forma de entrada (macro e detalhada), identificada, resposta preliminar/complementar, possui complementação/manifestação vinculada/providência e indicadores (`EmAnalise`, `Respondida`, `ForaDoPrazo`, `Recebida`, `Resolvida`, `NaoResolvida`, `Prorrogada`, visualizada/não visualizada na unidade atual).
- ✅ Atalhos de indicador: cada `onFilter*` zera o filtro, liga o indicador e fixa `Ano` = ano corrente; `ForaDoPrazo` também liga `UnidadesSubordinadas`.
- ✅ Prazo restante: para cada linha, `prazoRestante.dias` = dias entre hoje e `Vencimento` (calculado no navegador).
- ✅ Filtro ativo é guardado em `localStorage` (`current-view`) e restaurado ao voltar à tela; `alternarUnidade` limpa o cache e recarrega.
- ✅ **Exportação**: reenvia a mesma consulta com `ExportConfig: true`; o frontend apenas informa que o arquivo CSV será enviado ao e-mail cadastrado do operador (geração no backend).
- ✅ Bloqueio por manifestação bloqueante: se a visão traz `ManifestacaoBloqueanteId`, só se abre aquela manifestação, salvo `PermiteDetalharManifestacaoBloqueada`. `Ctrl+clique` abre em nova aba.

### 2. Super busca (`/super-busca`, `superBuscaCtrl`)
✅ `POST servico-ouvidoria/manifestacao/consultar-por-termo`; ao abrir um resultado consulta `.../permite-detalhar` e só navega se permitido (a chamada é repetida para **cada linha** do resultado em `detalharManifestacao`).

### 3. Detalhe e tratamento (`/detalhar-manifestacao/:id`, `detalheManifestacaoCtrl`)
Ao abrir: `POST .../manifestacao/unidade/detalhe` e, em seguida, `POST .../manifestacao/acoes` (objeto `vm.acoes` com códigos que mostram/ocultam cada item do menu).

| Ação no menu | Código em `vm.acoes` | Chamada |
|---|---|---|
| Imprimir sem/com dados do solicitante | `MPR_MNF` (com dados exige `Identificada`) | `manifestacao/exportar-pdf-operador` e `...-dados-usuario` (PDF em base64 aberto em nova janela) |
| Solicitar informação complementar | `CMP_MNF` (e não anônimo, e sem complementação pendente) | `complementacao/solicitar` |
| Resposta definitiva / preliminar / complementar | `RPT_DFN` / `RPT_PRL` / `RPT_CMP` | `resposta/definitiva`, `/preliminar`, `/complementar` |
| Registrar providência | `RGT_PRV` | `providencia` |
| Tramitar | `TRM_MNF` | `tramite/acoes-por-manifestacao`, `tramite/unidades`, `tramite` |
| Tramitar entre seccionais | `TRM_SEC` | `tramite/seccional/unidades`, `tramite/seccional` |
| Prorrogar prazo (solicitar) | `PRG_PRZ` | `prorrogacao-prazo/solicitar` (fluxo de decisão em [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/02-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Prorrogacao-de-Prazo|Prorrogacao-de-Prazo]]) |
| Invalidar manifestação | `NVL_MNF` | `manifestacao/invalidar` |
| Reclassificar | `RCL_INT` ou `RCL_PAR` | `classificacao/listar-para-registro-interno/{Identificada}`, `reclassificacao/unidades`, `formulario/por-assunto`, `reclassificacao/registrar-reclassificacao` |
| Reclassificação seccional | `RCL_SEC` | `classificacao/listar-para-reclassificacao-seccional`, `tramite/unidades`, `registrar-reclassificacao-seccional` |

Outros comportamentos:
- ✅ Após resposta, providência, invalidação ou complemento, a tela **recarrega o detalhe**; após tramitar, reclassificar, remover atribuição e tramitar entre seccionais, volta à caixa de entrada com `toastr` de sucesso (destino devolvido pelo backend).
- ✅ Anexar arquivo: normaliza o nome (remove acentos e caracteres fora de `[0-9a-zA-Z.]`), `POST arquivo/enviar`, recarrega a página inteira.
- ✅ Manifestação vinculada: resumo por `manifestacao/resumo`; navegação por `detalhar-manifestacao/{id}`.
- ✅ Histórico de visualização: `manifestacao/historico-visualizacao`. Remover atribuição de operador: `remover-atribuicao-operador`.
- ✅ Mapa do local do fato (OpenLayers) a partir de `LocalDoFato.Latitude/Longitude` (troca vírgula por ponto).
- ✅ Limites de texto nos modais (atributo `maxlength`): resposta definitiva, preliminar e complementar 8000 caracteres; **providência 1000** (ajustado em commit recente: "aumentar limite e contador de providências para 1000 caracteres"); motivação de reclassificação 2240; motivação de prorrogação 2400; informação complementar 1000. Os limites são do frontend; ❓ se o backend impõe os mesmos.

## Inferências e limitações
- 🔶 Os códigos de ação (`MPR_MNF`, `RPT_DFN` etc.) são mnemônicos do backend; o significado acima vem do texto do menu, não de enumeração. Conferir com o backend.
- ⚠️ Inconsistências no código (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/06-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Débitos técnicos]]): `onDetailById` navega para `detalheManifestacao/<id>` (rota inexistente); o evento `atualizarCaixaDeEntrada` chama `init()` indefinido; `exportarPDF` usa `/exportarPDF/` (a rota é `/exportar-pdf/:id`).

## Relacionamentos
- Backend: [[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Tramitação e resposta]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Manifestacao|Manifestacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Reclassificacao-e-Invalidacao|Reclassificacao-e-Invalidacao]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Gerencial|Modulo-Gerencial]] (assuntos e prazos que alimentam as ações)

## Pendências e próximo passo
- Comparar os códigos de ação e os limites de texto com o backend (lote de confronto, ainda não feito). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
