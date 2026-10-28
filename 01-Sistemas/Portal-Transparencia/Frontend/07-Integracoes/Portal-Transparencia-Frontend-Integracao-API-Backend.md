---
type: integration
aliases:
  - "Integração Frontend → API do Backend"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
consumer: Portal-Transparencia
provider: Portal-Transparencia
sources:
  - src/app/token-interceptor.js
  - src/app/index.module.js
  - src/app/components/compartilhado/services/relatorio.service.js
  - src/app/components/compartilhado/directives/tabela-consulta.directive.js
  - src/app/components/compartilhado/services/paginacao.service.js
---

# Integração Frontend → API do Backend

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Portal-Transparencia` (`portal-transparencia-frontend`) | `Portal-Transparencia` (`portal-transparencia-backend`) | HTTP/JSON (REST), `GET` em quase todas as chamadas | URL-base `api.url` + caminho; cabeçalho `x-client-id`; sem autenticação de usuário | saída (navegador → API) |

## Evidências
Commit `dca3e933`. `src/app/token-interceptor.js` (cabeçalho), `index.module.js` (registro do interceptador e limpeza dos cabeçalhos padrão), `RelatorioService` (exportação), `tabela-consulta.directive.js` (`$resource`), `paginacao.service.js` (`$http.get(api.url + data.url)`), serviços `*.service.js` por área. Caminhos: [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]].

## Informações confirmadas
- ✅ **Endereço**: constante `api.url`, definida por perfil (ver [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis]]). Todos os serviços de área montam `api.url + '/<caminho>'`.
- ✅ **Identificação do cliente**: o `tokenInterceptor` gera um UUID por carga da página (`crypto.randomUUID` ou fallback com `Math.random`) e o envia no cabeçalho `x-client-id` quando o URL começa com `api.url`. O cabeçalho **não** é enviado a `apisuperbusca` nem a outros hosts. O Backend exige esse cabeçalho (ver [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Segurança do Backend]]).
- ✅ **Sem credenciais**: nenhum token/`Authorization` é enviado; `$httpProvider.defaults.headers.*` são zerados.
- ✅ **Verbos**: 350 chamadas `GET` e 9 `POST` extraídas por script dos serviços (359 no total; não inclui as chamadas por `tabela-consulta` e `RelatorioService`, abaixo).
- ✅ **Exportações**: `RelatorioService.exportar(url, obj)` faz `GET api.url + url` com `responseType: arraybuffer` e `params: obj`; se `obj.tipo == 'pdf'` abre o PDF em nova janela (`Blob` + `window.open`), senão salva `relatorio.csv` (`FileSaver`). Há 61 chamadas em controllers, em rotas `/…/relatorio/…` ou `/v2/*/relatorios`.
- ✅ **Tabelas paginadas**: a diretiva `tabela-consulta` recebe `url` por atributo HTML e usa `$resource(api.url + url)` (ou o URL absoluto se começar com `http://`).
- ✅ **Datas de atualização**: `DataAtualizacaoService` consulta `GET /dataAtualizacao/<chave>`; muitas rotas carregam essa data no `resolve`.
- ✅ **Dois estilos de API**: caminhos históricos (`/despesa/*`, `/receita/*`, `/servidor/*` …) e a família `/v2/*` (32 chamadas: licitações, itens licitados, bens imóveis/móveis, pesquisa de satisfação, painéis de despesa, dashboard de execução, imagens do *slideshow*, órgãos LAI).

## Falhas e dependências
- ✅ Erros de rede/HTTP são tratados caso a caso; `RelatorioService` só faz `console.log` do erro (sem aviso ao usuário).
- ✅ Contrato quebrado ou ausente: comparação por texto dos caminhos com os mapeamentos do Backend (commit `e98fcc38`) não encontrou rota correspondente para estes caminhos usados no frontend: `/despesa/porAcao/empenhado/{codigo}`, `/receita/multas/total`, `/servidor/listarDataReferenciaPorOutrosOrcamento`, `/prestando-contas/detalhamento-conselheiro`, `/licitacoes-contratos/anos`, `/licitacoes-contratos/licitacao/orgao`, `/licitacoes-contratos/licitacao/situacao` e `/licitacoes-contratos/grafico/{especie,objeto,situacao,orgaos-contratos}`. O uso efetivo em telas ativas não foi verificado em todos os casos.
- ✅ Formulário "Fale conosco": `POST /contato/registro` (form-urlencoded, campos concatenados com `;`); o controller correspondente do Backend (`FormularioContatoController`) está comentado, conforme [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|Pendências do Backend]] (#11). 🔶 O envio provavelmente falha com 404.
- ✅ A dependência é de disponibilidade da API; não há *retry*, *timeout* explícito nem *fallback*.

## Inferências e limitações
- 🔶 Consumo de arquivos/imagens **não** passa por esta API: o frontend compõe URLs diretas com `caminhoImagens/Arquivos/DadosAbertos` (ver [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|Integrações externas]]); os endpoints `/storage/health` e `/storage/url` do Backend não são chamados pelo frontend.
- Parâmetros, respostas e DTOs não foram comparados campo a campo; a comparação de caminhos é textual (não considera verbo nem parâmetros).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catálogo de endpoints do Backend]]
- [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Arquitetura-AngularJS|Arquitetura]]

## Pendências e próximo passo
- Confirmar com o time as rotas sem correspondência e o formulário de contato (ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]]).
