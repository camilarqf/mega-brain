---
type: api
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - frontend
  - api
  - chamadas
sources:
  - src/app/store/services
  - src/environments
---
# SCI Frontend — chamadas de API

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] · Contrato exposto: [[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints do backend]]

## Objetivo
Listar todas as chamadas HTTP feitas pelo `sci-frontend` ao `sci-backend` e confrontá-las com as rotas do backend.

## Evidências
- Extração textual de `this.http.<verbo>(...)` em `src/app/store/services/*.service.ts` (25 arquivos, 20 com chamadas; 142 combinações serviço + verbo + caminho extraídas, 144 com as manuais). Base: `environment.apiUrl`. Mais 2 chamadas com a URL montada em variável foram somadas à mão: `GET arquivo/download/{nomeArquivo}` (`arquivo.service.ts`) e `GET pip/minuta/{id}` (`pip.service.ts`), ambas ✅. Nenhuma chamada HTTP fora desses serviços foi encontrada pelo padrão `this.http`.
- Confronto com os atributos `[Route]` e `[Http*]` de `sci-backend/src/SCI.Api/Controllers` no commit `8e3c8648386d0ee6767df7819faea9cdd44bef9c` (mesmo commit do cofre; checkout local sem alterações em arquivos rastreados). Comparação por **verbo + caminho**; payloads e DTOs **não** foram comparados.
- Legenda: ✅ rota existe no backend; ❓ rota **não encontrada** no backend. `{x}` = parâmetro de caminho.

## Informações confirmadas
| Serviço (`store/services`) | Chamadas |
|---|---|
| `analise` | ✅ `GET analise-admissibilidade`<br>✅ `PUT analise-admissibilidade`<br>✅ `PUT analise-admissibilidade/atualizar-nota-admissibilidade`<br>✅ `POST analise-admissibilidade/concluir`<br>✅ `PUT analise-admissibilidade/concluir-nota-admissibilidade`<br>✅ `POST analise-admissibilidade/criar-nota-admissibilidade`<br>✅ `GET analise-admissibilidade/{x}`<br>✅ `POST revisao-admissibilidade/atualizar-revisao`<br>✅ `POST revisao-admissibilidade/concluir-revisao-admissibilidade`<br>✅ `POST revisao-admissibilidade/reprovar-revisao` |
| `arquivo` | ✅ `GET arquivo/get-por-demanda`<br>✅ `GET arquivo/download/{x}` (URL em variável) |
| `assunto` | ✅ `GET assunto`<br>✅ `POST assunto`<br>✅ `GET assunto/categorias`<br>✅ `GET assunto/visao-administrador`<br>✅ `DELETE assunto/{x}`<br>✅ `GET assunto/{x}`<br>✅ `PUT assunto/{x}`<br>✅ `PATCH assunto/{x}/ativar` |
| `conduta` | ✅ `GET conduta` |
| `demanda` | ✅ `POST demanda`<br>✅ `PUT demanda`<br>✅ `GET demanda/get-all`<br>✅ `GET demanda/por-admissibilidade`<br>✅ `POST demanda/tratar`<br>✅ `GET demanda/{x}`<br>✅ `POST demanda/{x}/adicionar-anexo`<br>✅ `DELETE demanda/{x}/remover-anexo/{x}` |
| `denuncia` | ✅ `POST denuncia/aceitar`<br>✅ `GET denuncia/get-all`<br>✅ `POST denuncia/recusar`<br>❓ `GET denuncia/{x}`<br>❓ `GET denuncia/{x}/download` |
| `diligencia` | ✅ `POST diligencia`<br>✅ `PUT diligencia`<br>✅ `GET diligencia/por-pip`<br>✅ `GET diligencia/{x}`<br>✅ `POST diligencia/{x}/desvincular-matriz`<br>✅ `POST diligencia/{x}/vincular-matriz`<br>✅ `GET tipo-diligencia` |
| `encaminhamento` | ✅ `POST encaminhamento`<br>✅ `POST encaminhamento/aceitar`<br>✅ `POST encaminhamento/devolver`<br>✅ `GET encaminhamento/devolvidos`<br>✅ `GET encaminhamento/enviados-pela-unidade`<br>✅ `POST encaminhamento/enviar`<br>✅ `GET encaminhamento/por-processo-admissibilidade`<br>✅ `GET encaminhamento/recebidos`<br>✅ `POST encaminhamento/rejeitar-devolucao`<br>✅ `POST encaminhamento/reprovar` |
| `jad` | ✅ `GET cargo/por-usuario`<br>✅ `PUT processo-admissibilidade`<br>✅ `POST processo-admissibilidade/assinar-nota-tecnica`<br>✅ `PUT processo-admissibilidade/atualizar-dados-sei`<br>✅ `POST processo-admissibilidade/concluir`<br>✅ `POST processo-admissibilidade/concluir-cadastro-jad`<br>✅ `POST processo-admissibilidade/distribuir-para-analista`<br>❓ `POST processo-admissibilidade/encaminhar`<br>✅ `POST processo-admissibilidade/invalidar-nota-tecnica`<br>✅ `GET processo-admissibilidade/nota-tecnica/{x}`<br>✅ `GET processo-admissibilidade/nota/{x}`<br>✅ `GET processo-admissibilidade/por-relator`<br>✅ `POST processo-admissibilidade/reabrir-jad`<br>✅ `POST processo-admissibilidade/redistribuir-jad`<br>✅ `GET processo-admissibilidade/unidade`<br>✅ `GET processo-admissibilidade/visao-analista`<br>✅ `GET processo-admissibilidade/visao-apoio`<br>✅ `GET processo-admissibilidade/visao-assessor-autoridade`<br>✅ `GET processo-admissibilidade/visao-autoridade`<br>✅ `GET processo-admissibilidade/visao-gestor`<br>✅ `GET processo-admissibilidade/visao-revisor`<br>✅ `GET processo-admissibilidade/{x}` |
| `origem-denuncia` | ✅ `GET origem-denuncia` |
| `pessoa-juridica` | ❓ `GET pessoa-juridica/pesquisar` |
| `pessoa` | ✅ `GET pessoa/pesquisar`<br>✅ `GET servidor/pesquisar` |
| `pip` | ✅ `GET analise-admissibilidade/por-pip`<br>✅ `PUT analise-pip`<br>✅ `PUT analise-pip/atualizar-nota`<br>✅ `POST analise-pip/concluir`<br>✅ `POST analise-pip/concluir-nota`<br>✅ `POST analise-pip/criar-nota`<br>✅ `GET analise-pip/nota/{x}`<br>✅ `GET analise-pip/{x}`<br>✅ `POST pip/assinar-minuta`<br>✅ `POST pip/assinar-relatorio`<br>✅ `PUT pip/atualizar-cadastro`<br>✅ `POST pip/atualizar-dados-sei`<br>✅ `PUT pip/atualizar-minuta`<br>✅ `POST pip/concluir`<br>✅ `POST pip/concluir-ato-instauracao`<br>✅ `POST pip/concluir-cadastro`<br>✅ `POST pip/designar-relatoria`<br>✅ `POST pip/finalizar`<br>✅ `GET pip/por-relator`<br>✅ `POST pip/reabrir-pip`<br>❓ `GET pip/recuperar-admissibilidade/{x}`<br>✅ `POST pip/redistribuir`<br>✅ `GET pip/relatorio/{x}`<br>✅ `GET pip/unidade`<br>✅ `GET pip/visao-apoio`<br>✅ `GET pip/visao-assessor-autoridade`<br>✅ `GET pip/visao-autoridade`<br>✅ `GET pip/visao-gestor`<br>✅ `GET pip/visao-relator`<br>✅ `GET pip/visao-revisor`<br>✅ `GET pip/{x}`<br>❓ `POST revisao-pip/admitir-revisao-preliminar`<br>✅ `POST revisao-pip/atualizar-revisao`<br>✅ `POST revisao-pip/concluir`<br>✅ `POST revisao-pip/reprovar`<br>✅ `GET pip/minuta/{x}` (URL em variável) |
| `processos-pessoa` | ❓ `GET pessoa/processos` |
| `public` | ✅ `POST documento/validar` |
| `recomendacao` | ✅ `GET recomendacao` |
| `situacao-funcional` | ✅ `GET situacao-funcional` |
| `tipificacao` | ✅ `GET tipificacao-admissibilidade` |
| `tipo-documento` | ✅ `GET tipo-documento-demanda` |
| `unidade` | ✅ `GET tipo-processo`<br>✅ `GET tipo-revisao`<br>✅ `GET tipo-vinculo`<br>✅ `GET unidade`<br>✅ `POST unidade/configuracao`<br>✅ `PUT unidade/configuracao`<br>✅ `POST unidade/configuracao/desabilitar`<br>✅ `PUT unidade/configuracao/revisoes`<br>✅ `GET unidade/configuracao/{x}`<br>❓ `GET unidade/has-assessor-autoridade`<br>✅ `GET unidade/has-gestor`<br>✅ `GET unidade/por-tipo/{x}`<br>✅ `DELETE unidade/{x}` |
| `usuario` | ✅ `GET perfil`<br>✅ `DELETE permissao/usuario/{x}/permissao/{x}`<br>✅ `POST security/auth`<br>✅ `GET servidor/pesquisar`<br>✅ `GET usuario`<br>✅ `POST usuario`<br>✅ `POST usuario/alternar-permissao`<br>✅ `GET usuario/analistas-para-distribuicao`<br>✅ `GET usuario/permissoes`<br>✅ `GET usuario/relatores-pip`<br>✅ `GET usuario/visao-administrador`<br>✅ `GET usuario/{x}` |

### Resultado do confronto
- ✅ 136 de 144 combinações existem no backend.
- ❓ 8 chamadas sem rota no backend analisado:
  1. `GET denuncia/{id}` — **usada** pela tela de análise de denúncia (`analisar-denuncia`).
  2. `GET denuncia/{identificadorExterno}/download` — **usada** para baixar e visualizar anexos da denúncia (o backend tem `GET arquivo/download/{nomeArquivo}`, outro contrato).
  3. `GET pessoa/processos` — **usada** pelo gerenciador de processos.
  4. `GET pessoa-juridica/pesquisar` — serviço `pessoa-juridica` (busca de pessoa jurídica) .
  5. `GET unidade/has-assessor-autoridade` — método `getHasAssessorAutoridade`.
  6. `POST processo-admissibilidade/encaminhar` — método `encaminharProcessoAdmissibilidade`; o fluxo de nota técnica usa `POST encaminhamento`.
  7. `GET pip/recuperar-admissibilidade/{id}` — método `recuperarAdmissibilidade`.
  8. `POST revisao-pip/admitir-revisao-preliminar` — método `admitirRevisaoPreliminar`.
- 🔶 As hipóteses para os itens 1 a 8 são: backend em outra branch ou com mudanças ainda não integradas (o último commit do frontend é de 2026-10-08 e o do backend, de 2026-10-18), endpoints removidos, ou serviço órfão. Os itens 1 a 3 são usados em telas e falhariam com o backend analisado. Não confirmado em execução.
- Rotas do backend **não** chamadas pelo frontend: `GET pip/por-processo-admissibilidade/{id}`, `GET processo-admissibilidade/por-demanda/{id}`, `GET security/is-auth`, `GET status/demanda`, `GET status/processo-admissibilidade`, `GET status/pip` (o cliente guarda os status em enums locais) e `POST support/generate-database`.

### Convenções do cliente
- ✅ Respostas de listas aceitam as formas `[]` ou `{ data: [] }` (`map` defensivo em vários serviços).
- ✅ Paginação: `PagedResponse` (`data`, `total`, `pageNumber`, `pageSize`, `totalPages`); parâmetros montados por `core/factory/build-filtro-*`.
- ✅ Downloads de PDF e anexos com `responseType: 'blob'`.
- ✅ URLs concatenadas com `${this.baseUrl}rota`, sem barra inicial: depende de `apiUrl` terminar com `/` (valor não registrado).

## Inferências e limitações
- Chamadas montadas fora do padrão `this.http.<verbo>(` (por exemplo, por métodos auxiliares) podem não ter sido capturadas; a única exceção tratada foi a exclusão de permissão (`montarUrlExcluirPermissaoUsuario`).
- Não se verificou a política de autorização de cada rota contra o perfil do chamador (ver [[01-Sistemas/SCI/Frontend/05-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Segurança e sessão]]).

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/04-API-e-Integracoes/SCI-Frontend-Integracoes|Integrações do Frontend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
