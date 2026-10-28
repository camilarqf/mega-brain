---
type: module
aliases:
  - "SCI Backend — módulo Identidade e permissões"
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
sources:
  - src/SCI.Domain/Identidade
  - src/SCI.Application/UseCases/CriarUsuario
  - src/SCI.Application/UseCases/Identidade/AlternarPermissao
  - src/SCI.Application/UseCases/ExcluirPermissao
  - src/SCI.Api/Controllers/UsuarioController.cs
  - src/SCI.Api/Controllers/PermissaoController.cs
---
# SCI Backend — módulo Identidade e permissões

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar usuários, perfis, permissões (perfil + unidade) e a troca da permissão atual.

## Evidências
- `Usuario.{Criar, AddPermissao, AdicionarPermissoes, AlternarPermissao}`, `CriarUsuarioHandler`, `AlternarPermissaoHandler`, `UsuarioPodeAlternarPermissao`.

## Informações confirmadas
- ✅ `Usuario`: CPF, nome, e-mail, matrícula e coleção de `Permissao` (perfil + unidade + flag `Atual`). A primeira permissão criada é a atual.
- ✅ **Criar usuário** (`POST /usuario`, Administrador): se o CPF já existe, adiciona as permissões que faltam (na mesma unidade apenas as inexistentes); se não, cria o usuário com todas e dispara `UsuarioCriado`.
- ✅ **Alternar permissão** (`POST /usuario/alternar-permissao`, qualquer autenticado): o usuário vem do token (`ICurrentUserIdentity`), não do corpo. Regra: a permissão escolhida deve pertencer ao usuário ("A permissão selecionada não é permitida para este usuário."); devolve **novo token** com o perfil e a unidade escolhidos.
- ✅ **Excluir permissão** (`DELETE /permissao/usuario/{usuarioId}/permissao/{permissaoId}`, Administrador); `PermissaoExcluida`, `PermissaoAlternada` são eventos.
- ✅ Consultas: `GET /usuario/relatores-pip`, `/analistas-para-distribuicao`, `/permissoes`, `/{id}` e `/visao-administrador` (Administrador), `GET /perfil` (Administrador).
- ✅ O login depende de o usuário existir por CPF e possuir permissão atual — [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Autenticacao|Fluxo de autenticação]].

## Inferências e limitações
- ❓ Não há tela/endpoint de autocadastro: usuários são criados por Administrador ou por seed (`05-Insert-TB_USUARIO.sql`, não lido).
- A tabela `TB_USUARIO_IDENTIDADE` e o código de SSO são da POC e ficam fora do escopo.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização]] · [[01-Sistemas/SCI/Backend/06-API/SCI-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Confirmar o processo de provisionamento de usuários em produção.
