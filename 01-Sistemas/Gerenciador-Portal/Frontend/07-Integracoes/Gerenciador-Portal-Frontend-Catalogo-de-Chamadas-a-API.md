---
type: api
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - frontend
  - api
  - chamadas
sources:
  - src/app/components/login/loginAPI.js
  - src/app/components/arquivos/arquivoApi.js
  - src/app/components/arquivos/arquivoCtrl.js
  - src/app/components/imagem-portal/imagemApi.js
  - src/app/components/imagem-portal/imagemCtrl.js
  - src/app/components/carga-portal/cargaApi.js
  - src/app/components/palavras-chave/palavraApi.js
  - src/app/components/paginas-lai/orgaoApi.js
  - src/app/components/textos-portal/textos-portalApi.js
  - src/app/components/exclusoes-medida-protetiva/exclusoesMedidaProtetivaApi.js
---
# Catálogo de chamadas à API — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Listar as chamadas HTTP que o frontend faz ao backend, por serviço, e compará-las com o [[01-Sistemas/Gerenciador-Portal/Backend/06-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|catálogo do backend]]. Todos os caminhos são relativos a `api.url`; todas as chamadas levam `x-client-id` ([[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Integracao-API-Backend|Integração]]).

## Evidências
Os `*Api.js` (uma camada por tela) e, para os uploads, os `*Ctrl.js`.

## Informações confirmadas
Legenda: `?x` = query; `{x}` = variável de caminho; `body` = JSON; `file` = multipart.

### `loginAPI` (login)
| Verbo | Caminho | Entrada |
|---|---|---|
| POST | `/login` | body `{login, senha}` |

### `arquivoAPI` e upload ([[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Arquivos|Arquivos]])
| Verbo | Caminho | Entrada |
|---|---|---|
| POST (upload) | `/arquivo/salvar-arquivo/{login}/{categoria}/{ano}` | `file` (um pedido por arquivo; `categoria` e `ano` podem ir como `null` na URL) |
| POST | `/arquivo/salvar-informacoes-arquivo` | body `Arquivo`; `?usuarioLogado`, `?idReferenciaEscolhida`, `?prefixoCategoria`, `?nomeOriginal` |
| POST | `/arquivo/ativar-arquivo`, `/desativar-arquivo`, `/excluir-arquivo` | `?id`, `?usuarioLogado` |
| POST | `/arquivo/exclusao-multipla` | `?idArquivos`, `?usuarioLogado` |
| POST | `/arquivo/filtrar-arquivos` | body `Arquivo` (filtros `nome`, `descricao`, `codigoCategoria`, `ano`, `dataReferencia`) |
| GET | `/arquivo/listar-arquivos`, `/listar-completos`, `/listar-incompletos`, `/listar-ano`, `/listar-periodo` | — |
| GET | `/arquivo/listar-referencia` | `?idReferencia` |
| GET | `/arquivo/quantidade-arquivos-completos`, `/quantidade-arquivos-incompletos` | — |
| GET | `/arquivo/recuperar-arquivo`, `/recuperar-arquivo-incompleto` | `?id` |
| GET | `/categoria/listar-categorias` | — |

### `imagemAPI` e upload ([[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Imagens|Imagens]])
| Verbo | Caminho | Entrada |
|---|---|---|
| POST (upload) | `/imagem/salvar/{login}/{categoria}` (1 imagem), `/imagem/salvar-sem-ordenar/{login}/{categoria}` (várias) | `file` |
| POST (upload) | `/imagem/salvar-imagem-background/{login}/{idImagem}` | `file` |
| POST | `/imagem/ativar-imagem`, `/desativar-imagem` | `?id`, `?usuarioLogado` |
| PUT | `/imagem/salvar-imagem` | body `Imagem`; `?usuarioLogado` |
| PUT | `/imagem/ordenar-prioridades-imagens/{categoria}` | — |
| PUT | `/imagem/mover-prioridade-acima`, `/mover-prioridade-abaixo` | body `Imagem`; `?usuarioLogado` |
| DELETE | `/imagem/excluir-imagem`, `/excluir-background` | `?id`/`?idBackground`+`?idImagem`, `?usuarioLogado` |
| GET | `/imagem/listar-imagens-slideshow`, `/listar-imagens-setores`, `/listar-funcoes-paineis` | — |
| GET | `/imagem/recuperar-imagem` | `?id` |
| GET | `/imagem/recuperar-imagem-background-por-painel-id/{id}` | — (existe no serviço; **sem uso** nos controllers lidos) |

### `cargaAPI` ([[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Cargas|Cargas]])
`GET /carga/listar-cargas` (`?dataCarga`, `?statusCarga`, `?esquemaCarga`, `?tabelaCarga`), `/carga/listar-status`, `/carga/listar-esquema`, `/carga/listar-quantidade-status`.

### `palavraAPI` ([[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Palavras-Chave|Palavras-chave]])
`POST /palavra/salvar`, `POST /palavra/editar`, `POST /palavra/excluir` (body da palavra) e `GET /palavra/listar`.

### `orgaoAPI` ([[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Orgaos-LAI|Órgãos LAI]])
`POST /orgao`, `GET /orgao`, `PUT /orgao` (body `OrgaoLAI`), `DELETE /orgao?id`.

### `textosPortalAPI` (tela fora do menu; ver [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Textos-do-Portal|Textos do portal]])
`GET /textos-consultas` (`?idCategoria`, `?idSubCategoria`), `PUT /textos-consultas` (body), `GET /textos-consultas/categorias`, `GET /textos-consultas/sub-categorias` (`?idCategoria`).

### `exclusoesAPI` ([[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Medida-Protetiva|Medida protetiva]])
O sufixo `{consulta}` é um de `/remuneracao`, `/por-orgao`, `/despesas`, `/cadastro-expulsoes`, `/conselheiros`, `/conselhos`.
| Verbo | Caminho | Entrada |
|---|---|---|
| GET | `/servidores-medida-protetiva{consulta}` | — |
| GET | `/servidores{consulta}` | `?nomeServidor` (a consulta "conselhos" pesquisa em `/servidores/conselheiros`) |
| POST | `/servidores-medida-protetiva{consulta}` | body `{identificador, nome}`; `?usuarioAutenticado` |
| DELETE | `/servidores-medida-protetiva/{id}` | `?usuarioAutenticado` |
| GET | `/servidores-medida-protetiva/expirar-cache` | sem tratamento de resultado |

## Falhas e dependências
- ✅ **Comparação com o backend**: todos os caminhos e verbos acima existem no catálogo do backend, com os mesmos nomes de parâmetros (`usuarioLogado`/`usuarioAutenticado`).
- ✅ Endpoints do backend **sem chamada** no frontend lido: `GET /servidores-medida-protetiva/listar`, `GET /servidores-medida-protetiva?identificador`, `/healthcheck`, `/prometheus`. (`/servidores-medida-protetiva{consulta}` por GET é usado.)
- ✅ Defeito latente: `CargaController.retornarListaDeCargas` chama `cargaAPI.retornarListaDeCargas`, que **não existe** no serviço; a função não é chamada hoje (a tela usa `recuperarCarga`).
- ✅ O login e o nome do usuário vão na **URL** nos uploads (`/arquivo/salvar-arquivo/{login}/…`), o que os deixa em logs de acesso.

## Inferências e limitações
- ❓ Formato real das respostas (`UsuarioDTO` etc.) não foi verificado em execução; o frontend usa `obj.data == "OK"` como sucesso em várias operações.
- ❓ Não foram lidos os HTML para achar chamadas disparadas por diretivas.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Integracao-API-Backend|Integração com o Backend]] · [[01-Sistemas/Gerenciador-Portal/Backend/06-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Endpoints do Backend]]

## Pendências e próximo passo
- Confirmar se as chamadas sem uso (`recuperar-imagem-background-por-painel-id`, `retornarListaDeCargas`) são código morto.
