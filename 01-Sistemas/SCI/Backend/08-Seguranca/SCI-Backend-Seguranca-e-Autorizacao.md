---
type: security
aliases:
  - "SCI Backend — segurança e autorização"
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
updated: 2026-10-23
tags:
  - autenticacao
sources:
  - src/SCI.Api/Program.cs
  - src/SCI.Api/Identity
  - src/SCI.Api/Controllers/SecurityController.cs
  - src/SCI.Application/UseCases/AutenticarUsuario/AutenticarUsuarioHandler.cs
  - src/SCI.Infrastructure.Services/Auth
  - src/SCI.Api/Extensions/CorsPolicyExtensions.cs
  - src/SCI.Api/Controllers/DenunciaController.cs
---
# SCI Backend — segurança e autorização

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Registrar autenticação, perfis, políticas e controles de segurança. Sem segredos nem valores sensíveis.

## Evidências
- `Program.cs` (JWT Bearer), `Identity/AuthorizationPolicies/*.cs`, `AutenticarUsuarioHandler`, `TokenService`, `ClaimsServices`, `CurrentUserIdentity`.

## Informações confirmadas
### Autenticação
- ✅ JWT Bearer próprio (HMAC-SHA256, chave simétrica de `JwtSettings`); valida emissor, audiência, validade e assinatura. Emissão por `TokenService.CreateToken`; validade = `ExpirationDays` dias.
- ✅ Claims do token: id do usuário, id da unidade, id do perfil, nome e `ClaimTypes.Role` = nome do `PerfilEnum` da **permissão atual**.
- ✅ A senha **não** fica no SCI: `AutenticarUsuarioHandler` valida CPF + senha no `PARTICIPA-DF` ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Autenticacao|integração]]). Antes, exige que o usuário exista (por CPF) e tenha `PermissaoAtual`.
- ✅ Fluxo completo: [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Autenticacao|Fluxo de autenticação]].
- ✅ `CurrentUserIdentity` relê o usuário no banco a cada chamada (`GetOrThrowAsync`) e usa o perfil/unidade da permissão atual; o CPF é mascarado ao compor o `UserIdentity`.

### Autorização
- ✅ Política nova `enc.ConsultarEncaminhamentoRecebidoPorProcesso` (10 perfis). `GET /denuncia/{id}` e `GET /denuncia/{denunciaId}/download` exigem só autenticação.
- ✅ Todos os controllers usam `[Authorize]`, exceto `SecurityController` e `SupportController` (`[AllowAnonymous]`) e `RevisaoAdmissibilidadeController`/`RevisaoPipController`/`PerfilController`, que não têm `[Authorize]` na classe mas protegem cada rota com política.
- ✅ Políticas por papel (`RequireRole(nameof(PerfilEnum.X))`) em 11 classes de `AuthorizationPolicies`. Resumo:
  - **Administrador**: quase todas as políticas de gestão, e as exclusivas de unidade, usuário, perfil, permissão, assunto e suporte.
  - **AutoridadeCorrecional**: tratar demanda, distribuir/redistribuir, invalidar nota técnica, concluir ato de instauração do PIP, aceitar/devolver encaminhamento.
  - **AnalistaAdmissibilidade**: cadastro, análise, conclusão e encaminhamento do processo de admissibilidade.
  - **GestorAdmissibilidade**, **RevisorJad**: revisões e assinatura da nota técnica; **GestorPip**, **RevisorPip**, **InvestigadorPip**: o mesmo para o PIP.
  - **ApoioCorrecional**: aceitar/recusar denúncia (desde `29989114`; antes AutoridadeCorrecional), criar/atualizar demanda, atualizar minuta e SEI, enviar encaminhamento, finalizar PIP.
  - **AssessorAutoridade**: criar/atualizar/concluir notas de admissibilidade e do PIP.
- ✅ Perfis: [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|11 valores de `PerfilEnum`]]. O usuário pode ter várias `Permissoes` (perfil + unidade) e alterna a atual por `POST /usuario/alternar-permissao` (regra: a permissão escolhida deve pertencer ao usuário).
- ✅ A assinatura de documentos valida o perfil no domínio: `NotaTecnicaAptaParaAssinatura` e `OrquestrarAssinatura` ("Usuário não é o próximo revisor a assinar"); `RelatorioAptoParaAssinatura`.
- ✅ Trilha de auditoria: cada evento de domínio guarda CPF mascarado, unidade, perfil, IP (`X-Forwarded-For` quando presente) e user-agent em `TB_EVENTO`.

### Outros controles
- ✅ CORS padrão: qualquer origem, método e cabeçalho.
- ✅ Download de arquivo validado por `DownloadRequest` (FluentValidation); armazenamento em diretório configurado (`StorageServiceSettings.Path`).
- ✅ `SecurityId`: cifra AES-GCM de identificadores (chave de 256 bits em `DataSecuritySettings`); ver limitação abaixo.
- ✅ Segredos/credenciais vêm de seções de configuração; `.docker/inject-docker-secrets-entrypoint.sh` sugere injeção de segredos no contêiner (conteúdo não lido).

## Inferências e limitações
- ⚠️ Riscos de segurança (fatos e recomendações separados) estão em [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]]: bypass de senha por CPF, endpoint anônimo de recriação do banco, rota de exclusão de unidade sem política, segredos em `appsettings` versionados.
- 🔶 `SecurityId` não é usado em requests/responses da API (apenas registrado).
- Valores reais de chave JWT, tempo de expiração e CPFs de bypass **não são reproduzidos aqui**.
- A POC de SSO (não commitada) está fora do escopo.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/06-API/SCI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Identidade-e-Permissoes|Identidade e permissões]]

## Pendências e próximo passo
- Confirmar o prazo de validade do token por ambiente e a política de rotação da chave (sem registrar valores).
