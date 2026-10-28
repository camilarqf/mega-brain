---
type: api
aliases:
  - "Frontend Ouvidoria — chamadas de API ao backend"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
sources:
  - app/api.service.js
  - app/token-auth-interceptor.js
  - app/manifestacao
  - app/gerencial
  - app/conta
  - app/dashboard
  - app/nav/nav-ctrl.js
  - app/auth/auth-ctrl.js
  - app/upload/upload-directive.js
  - app/open-street-map
---

# Frontend Ouvidoria — chamadas de API ao backend

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Integrações: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas|Integracoes-Externas]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]

## Objetivo
Listar os caminhos e verbos que o frontend de Ouvidoria chama no `participa-df-backend` (consumidor → provedor). Esta nota é o inventário do **cliente**; o contrato é do backend.

## Evidências
Busca por `Api.GET/POST/GETe/POSTe` em `app/` (exceto `views-dist.js`, gerado) e leitura das diretivas `upload` e `mapOpenStreet`, commit `9d8ecdb`. Todas as chamadas passam por `Api` (`app/api.service.js`), prefixadas por `configService.urlApi`; o frontend usa **apenas `GET` e `POST`**. Cobertura `parcial`: payloads foram lidos só nas telas principais; a correspondência de caminho e verbo com o catálogo de endpoints do backend (notas `Backend/05-API`, commit `4901ad5`) foi feita por script, **sem** comparar payloads.

## Informações confirmadas

### Segurança e sessão
| Verbo | Caminho | Uso |
|---|---|---|
| GET | `security/token-retrieve/{sessionId}` | obtém o token no login assistido |
| GET | `security/is-auth` | valida sessão (sem spinner) |
| GET | `configuration/front-end-urls` | URLs `Login` e `Principal` (redirecionamentos de 401/403 e logout) |
| GET | `security/check`, `security/check-cpf-vinculado-pj`, `security/count-try` | desafio de dados cadastrais e contagem de tentativas |
| POST | `security/challenge` | resposta do desafio |
| POST | `security/auth` | apenas em `loginCtrl` (sem rota) |
| GET | `v2/usuario/false/true` | dados do usuário logado |

### Operador, unidade e perfil (menu e gerencial)
| Verbo | Caminho | Uso |
|---|---|---|
| GET | `operador-so/consultar-permissoes`, `operador-so/unidades`, `operador-so/consultar-por-unidade`, `operador-so/existe` | permissões do menu, unidades do operador, usuários da unidade, existência por CPF |
| POST | `operador-so/alterar-unidade`, `operador-so`, `operador-so/id`, `operador-so/listar` | troca de unidade e CRUD de operadores |
| GET/POST | `perfil-so/ativos`, `perfil-so/funcionalidade`; `perfil-so`, `perfil-so/id`, `perfil-so/listar` | perfis |
| GET/POST | `unidade/subordinadasSO` (8 telas), `unidade/subordinadas`, `unidade/tipo-unidade`, `unidade/so/tipo-unidade`; `unidade/so`, `unidade/so/id`, `unidade/so/listar` | unidades |
| GET/POST | `notificacao`, `notificacao/por-unidade`, `notificacoes`, `acao-para-remover-notificacao` | notificação de prazo (telas sem rota) |
| GET/POST | `usuario/motivacao-bloqueio-usuario`; `usuario/id`, `usuario/bloquear`, `usuario/desbloquear` | bloqueio de usuário e consulta de cadastro |
| GET/POST | `operador`, `manifestacao/securityId` | controllers legados |

### Conta (pessoa física e jurídica)
`POST pessoa-fisica/existe`, `pessoa-fisica/por-operador`, `pessoa-fisica/atualizar/por-operador`, `pessoa-fisica/desbloquear-dados-inconsistentes`; `POST pessoa-juridica/existe`, `pessoa-juridica/por-operador`, `pessoa-juridica/atualizar/por-operador`, `pessoa-juridica/atualizar-responsavel`, `pessoa-juridica/historico-responsavel-por-operador`, `pessoa-juridica/desbloquear-dados-inconsistentes`; `GET pessoa-juridica/tipo-entidade`, `GET necessidade-especial`.

### Manifestação (`servico-ouvidoria/…`)
| Área | Caminhos |
|---|---|
| Consulta | `POST manifestacao/na-unidade`, `manifestacao/registrada-na-unidade`, `manifestacao/unidade/detalhe`, `manifestacao/acoes`, `manifestacao/resumo`, `manifestacao/consultar-por-termo`, `manifestacao/permite-detalhar`, `manifestacao/historico-visualizacao` |
| Registro | `POST manifestacao/por-operador`, `ia/assunto`, `formulario/por-assunto`; `GET tipo-entrada/com-agrupamento`, `assunto/por-palavra-chave/{texto}`, `assunto/por-unidade`, `regiao-administrativa` |
| Tratamento | `POST resposta/preliminar`, `resposta/definitiva`, `resposta/complementar`, `providencia`, `complementacao/solicitar`, `manifestacao/invalidar`, `manifestacao/remover-atribuicao-operador` |
| Trâmite | `POST tramite`, `tramite/acoes-por-manifestacao`, `tramite/unidades`, `tramite/seccional`, `tramite/seccional/unidades`; `GET tramite/acoes` |
| Reclassificação | `POST reclassificacao/unidades`, `reclassificacao/registrar-reclassificacao`, `reclassificacao/registrar-reclassificacao-seccional`, `classificacao/listar-para-reclassificacao-seccional`; `GET classificacao`, `classificacao/listar-para-registro-interno/{identificada}` |
| Prorrogação | `POST prorrogacao-prazo/solicitar`, `listar`, `deferir`, `indeferir`; `GET prorrogacao-prazo/situacoes` |
| Anexos | `POST arquivo/validar`, `arquivo/enviar`, `arquivo/download`, `arquivo/excluir-por-operador` |
| Impressão | `POST manifestacao/exportar-pdf-operador`, `exportar-pdf-operador-dados-usuario` (PDF em base64) |
| Cadastros | `POST assunto`, `assunto/id`, `assunto/listar`, `formulario`, `formulario/id`, `formulario/listar`; `GET assunto/com-formulario`, `assunto/sem-formulario`, `formulario/formato`, `colecoes/situacao`, `colecoes/tema` |

### Dashboards
`POST dashboard/produtividade-operador-so`, `dashboard/produtividade-unidade`.

### Chamadas fora do backend
`POSTe` ao serviço de localização (`/lat-long`, `/endereco`, `/ra`) — ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas|Integracoes-Externas]].

### Correspondência com o backend (texto, sem executar)
- ✅ Dos 107 caminhos distintos chamados, **99 têm caminho e verbo iguais** a um endpoint listado no catálogo do backend (127 combinações caminho+verbo conferidas), 7 não têm correspondência e 1 é parcial (abaixo).
- ✅ `GET v2/usuario/false/true`: o backend lista `GET v2/usuario` (entrada `bool`); 🔶 os dois booleanos seguem como segmentos de rota, não confirmados.
- ⚠️ **Sem correspondência** no catálogo (7 caminhos, todos de controllers legados e sem rota na SPA): `operador`, `notificacao`, `notificacoes`, `acao-para-remover-notificacao`, `unidade/subordinadas`, `unidade/tipo-unidade`, `manifestacao/securityId`. Se essas telas voltarem a ser usadas, falharão (404).
- ✅ Os caminhos de `arquivo/download` e `arquivo/enviar` existem; o backend marca `enviar` com limite de 40 MB, enquanto o frontend não impõe limite próprio (validação por `arquivo/validar`).

### Convenções observadas
- ✅ Cabeçalhos: `Content-Type: application/json`; o interceptor acrescenta `application-key`, `Authorization: Bearer` e `X-Requested-With`.
- ✅ Listas paginadas: corpo `{…filtro, PageNumber, FiltroAplicado}`; resposta é o objeto de paginação (`Pager.Rows`, `CurrentPage`).
- ✅ Erros 400 do backend trazem `Notifications[]` (`Message`) ou `error`; 500 traz `Message` usada como código de rastreamento.
- ✅ Nomes de propriedades em PascalCase (`Descricao`, `PageNumber`) misturados a camelCase em alguns corpos (`cpfCnpj`, `manifestacao`, `challenge`).
- ⚠️ Chamadas `GET` de segurança levam CPF/CNPJ na query string (`security/count-try?data=`, `security/check?data=`, `security/check-cpf-vinculado-pj?cpf=&cnpj=`), logo em logs de acesso.

## Inferências e limitações
- 🔶 Os 7 caminhos sem correspondência pertencem a controllers não alcançáveis por rota; podem ter sido removidos do backend.
- ❓ Payloads, nomes de propriedades e códigos de retorno não foram comparados. Pendência registrada em [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas de API do Frontend Cidadão]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Confrontar payloads e códigos de retorno com os controllers do backend (lote futuro).
