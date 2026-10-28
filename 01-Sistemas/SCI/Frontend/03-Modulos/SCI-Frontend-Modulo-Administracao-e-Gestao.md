---
type: module
aliases:
  - "SCI Frontend — módulo Administração e Gestão"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/pages/administracao
  - src/app/pages/gestao
  - src/app/store/services/usuario.service.ts
  - src/app/store/services/assunto.service.ts
  - src/app/store/services/unidade.service.ts
---
# SCI Frontend — módulo Administração e Gestão

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Documentar as áreas do Administrador (usuários, assuntos, unidades) e do Gestor Gerencial (painel).

## Evidências
- `pages/administracao` (`usuarios`, `assuntos`, `unidades`, `header-admin`), `pages/gestao/painel-gestao`, serviços de usuário, assunto e unidade.

## Informações confirmadas
### Administração (`/pages/administracao`, perfil `Administrador`)
- ✅ **Usuários:** lista por visão do administrador (`GET usuario/visao-administrador`, com filtros), detalhe (`GET usuario/{id}`), cadastro e exclusão de permissão (`DELETE permissao/usuario/{usuarioId}/permissao/{permissaoId}`). No cadastro, o administrador procura um servidor (`GET servidor/pesquisar`), informa e-mail (obrigatório e válido), marca os perfis disponíveis (`GET perfil`) e salva (`POST usuario`).
- ✅ **Assuntos:** lista paginada, criar, editar (`PUT assunto/{id}`), excluir (`DELETE assunto/{id}`), ativar (`PATCH assunto/{id}/ativar`) e categorias (`GET assunto/categorias`).
- ✅ **Unidades:** lista, edição da configuração da unidade (`GET/POST/PUT unidade/configuracao`), das revisões (`PUT unidade/configuracao/revisoes`) e desabilitar (`POST unidade/configuracao/desabilitar`); catálogos `tipo-processo`, `tipo-revisao`, `tipo-vinculo`. Existe também `DELETE unidade/{id}` no serviço.

### Gestão (`/pages/gestao`, perfil `Gestor Gerencial`)
- ✅ Uma página com um `iframe` apontando para um painel de BI de terceiros (Power BI), com URL fixa no código-fonte (endereço omitido aqui).

## Inferências e limitações
- 🔶 `cadastrar-usuario` volta para `/pages/administracao/caixa-entrada-administrador`, rota que não existe no roteador (cai no curinga).
- ❓ Quem é o dono do painel Power BI e se o link é público (publicação na web) não é verificável pelo código.
- Formulários e filtros de usuário/assunto/unidade lidos por amostragem.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Identidade-e-Permissoes|Identidade e permissões (backend)]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Unidade-e-Configuracao|Unidade e configuração (backend)]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Cadastros-de-Apoio|Cadastros de apoio (backend)]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
