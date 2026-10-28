---
type: integration
aliases:
  - "Chamadas de API — SICI Frontend"
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-28
sources:
  - src/core/services/**/*.ts
  - src/app/components/layout/assinatura-autenticacao/assinatura-autenticacao.component.ts
---

# Chamadas de API — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Contrato exposto: [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints do Backend]] · Relacionado: [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Integracoes|Integracoes]]

## Objetivo
Listar as chamadas HTTP que o frontend faz ao `sici-backend` (consumidor → provedor), com a comparação ao catálogo do backend.

## Evidências
Busca por `http.get|post|put|delete` e `urlApi` em `src/core/services` e no componente de assinatura. Base: `environment.urlApi` (`/api` nos ambientes empacotados; o nginx repassa `/api/` ao backend). **Não** houve execução nem comparação de *payloads* campo a campo com os DTOs do backend.

## Informações confirmadas ✅ (por grupo)
Total: **52 caminhos/verbos** distintos nos serviços. Coluna "Catálogo": ✔ existe no catálogo do backend com o mesmo verbo; ✖ não consta.

| Grupo | Verbo e caminho | Quem usa | Catálogo |
|---|---|---|---|
| Autenticação | `POST /auth/login` · `GET /auth/account` · `GET /me` | `AuthService`; popup (`login`) | ✔ |
| Ação de controle | `GET /acao-controle/listar` · `GET /acao-controle/pesquisar?id=` · `POST /acao-controle/cadastrar` · `PUT /acao-controle/atualizar/{id}` · `DELETE /acao-controle/inativar?id=` · `GET /acao-controle/validar/{id}` | efeitos NgRx / `AcaoControleService` | ✔ |
| POAC | `GET /poac/pesquisar-ano?anoPoac=` | `PoacService` | ✔ |
| Cadastros auxiliares | `GET /unidade-auditoria/listar` · `GET /area-executora/listar/{id}` · `GET /programa-governo/listar` · `GET /objetivo-ppa/listar/{codigo}` · `GET /unidade-auditada/listar` | serviços de `acao-controle-services` | ✔ |
| OS (por ação) | `POST /os-acao-controle/salvar-os/{acao}` · `PUT .../atualizar/{id}` · `DELETE .../excluir/{id}` · `GET .../listar-os/{acao}` · `GET .../listar?page&size` · `GET .../pesquisar?id=` · `GET .../gerar-pdf?id=` · `PUT .../alterarStatusOs/{id}` · `POST .../{base}/prorrogacoes` · `PUT .../{id}/prorrogacoes` · `POST .../cancelar-os/{acao}` · `PUT .../cancelamento/{os}/{canc}` | `OrdemServicoService` | ✔ |
| OS (por ação) | `GET /ordem-servico/por-acao/{acao}` | `buscarPorAcaoControle` | ✖ |
| Fases | `GET /fase/listar` · `GET /fase/descricao-fase` | `FaseService`, `OrdemServicoService` | ✔ |
| Fases | `GET /fase/descricao-fase/listar` | `FaseService`, `OrdemServicoService` | ✖ |
| Equipe | `GET /auditor/listar` · `GET /auditor/listar-por-acao/{acao}` · `GET /auditor/listar-nao-relacionados-por-acao/{acao}` · `GET /coordenador/listar-por-coordenador/{acao}` · `GET /coordenador/listar-nao-relacionados/{acao}` | `OrdemServicoService`, `AuditorPerfilService` | ✔ |
| OS genérica | `GET /ordem-servico-generica/listar?page&size&search` · `POST .../salvar-os` · `PUT .../atualizar/{id}` · `PUT .../alterarStatusOs/{id}` · `GET .../gerar-pdf?id=` · `GET .../pesquisar` | `OrdemServicoGenericaService` | ✔ |
| Assinatura | `POST /assinaturas/assinar-os/{id}` · `POST /assinaturas/assinar-os-generica/{id}` · `GET /assinaturas/validacao?codigo=` | popup, `OrdemServicoService`, efeito de validação | ✔ |
| SUBCI | `POST /subci/cadastrar` · `GET /subci/listar` · `POST /subci/{id}/substitutos` · `GET /subci/{id}/substitutos` | `GestaoSubciService` | ✔ |
| Perfis | `GET /perfis` · `GET /auditores/com-perfil` · `PUT /auditores/{id}/vincular-perfis` | `AuditorPerfilService` | ✔ |

Cabeçalhos: `Authorization: Bearer` anexado pelo interceptor (exceto `/auth/login` e a chamada de assinatura, que monta o próprio cabeçalho). Os erros HTTP não são padronizados na tela: cada efeito exibe um toast; a mensagem do backend é lida em alguns (`message`/`detail`).

### Endpoints do catálogo do backend sem uso no frontend (busca textual)
`GET /poac/listar`, `GET /poac/pesquisar`, `POST /poac/cadastrar`, `GET /acao-controle/pesquisar-poac/{idPoac}`, `POST /os-acao-controle/{id}/fases`, `GET /os-acao-controle/validar-data-prorrogacao`, `GET /assinaturas/{id}/download` e `.../download-generica`, `DELETE /ordem-servico-generica/excluir/{id}`, `GET /subci/pesquisar`, `GET /coordenador/listar`.

## Inferências e limitações
- 🔶 Duas chamadas estão com a URL montada **sem barra** (`${urlApi}os-acao-controle/pesquisar`); ver [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]].
- 🔶 `GET /os-acao-controle/pesquisar` e `GET /os-acao-controle/listar` são restritos por perfil no backend (SUBCI/DIRETOR e SUBCI); as telas que os usam estão liberadas a mais perfis.
- 🔶 Serviços sem uso: `UserInfoService` (`GET /api/me`) e `DescricaoFaseService` (`/fase/descricao-fase` relativo, sem `urlApi`) não têm referência em outros arquivos.
- 🔶 O PDF da OS genérica assinada é pedido com `gerar-pdf?id=<idDocumentoAssinado>` (a lista usa esse id no caminho); o endpoint é o mesmo usado para a OS não assinada, e o backend também expõe `GET /assinaturas/{id}/download-generica` (não usado). Confirmar qual id `gerar-pdf` espera.
- Os verbos nos caminhos (`/cadastrar`, `/listar`, `/salvar-os`) seguem o backend (RPC sobre HTTP).
- Cobertura `parcial`: DTOs de requisição/resposta (`src/core/models`) não foram comparados com os do backend.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Integracoes|Integracoes]] · [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
