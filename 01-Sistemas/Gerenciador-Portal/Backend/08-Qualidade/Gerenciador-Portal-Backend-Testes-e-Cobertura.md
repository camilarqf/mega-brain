---
type: quality
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - backend
  - testes
  - qualidade
sources:
  - src/test/java/br/gov/df/cgdf/gerenciador/GerenciadorPortalApplicationTests.java
  - src/test/java/br/gov/df/cgdf/gerenciador/TextosTests.java
  - .docker/Dockerfile
---
# Testes e cobertura

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Registrar os testes existentes e o que não é coberto. Nada foi **executado** nesta análise (leitura estática).

## Evidências
Árvore `src/test` no commit `14b185f` e o estado da árvore de trabalho.

## Informações confirmadas
**Versionados (no commit)**
| Classe | Testes | O que valida |
|---|---|---|
| `GerenciadorPortalApplicationTests` | `contextLoads` | sobe o contexto Spring completo (`@SpringBootTest`) |
| `TextosTests` | `shouldSetTextFieldWithHtmlTag`, `shouldGetTextFieldWithCodedHyperLink` | conversão do marcador `##Rótulo(url)` ↔ HTML em `TextoConsultaPortal` (✅ regra do módulo de [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|conteúdo]]) |

- ✅ Os testes de contexto exigem os mesmos recursos da aplicação (SQL Server, MongoDB, credenciais do S3 ou variáveis `STORAGE_*`, propriedades de SSO), e `spring.profiles.active=@activatedProperties@` depende do perfil Maven; em ambiente sem esses recursos o contexto não sobe (🔶 não executado).
- ✅ O build da imagem **ignora** testes (`-Dmaven.test.skip=true`).

**Fora do escopo (não versionados no momento da análise)**: `src/test/.../comum/HealthcheckTest` e `src/test/.../config/ClientIdFilterTest` (decisão do usuário em 2026-10-27). Só se registra que existem e que `ClientIdFilterTest` espera que o filtro libere a requisição de erro cujo atributo `javax.servlet.error.request_uri` termina em `/healthcheck`; o `ClientIdFilter` do commit analisado verifica apenas `getRequestURI()`, então 🔶 esse teste **não passaria** contra o código versionado (trabalho em andamento; não executado).

## Falhas e dependências
- ✅ **Sem testes** para: controllers, serviços (arquivos, imagens, medida protetiva, cargas), autenticação/autorização, DAOs, `S3Config`/`StorageService`, `ResourceExceptionHandler`.
- ✅ Nenhuma ferramenta de cobertura (JaCoCo etc.) configurada no `pom.xml`.
- 🔶 Cobertura efetiva muito baixa (3 testes versionados sobre 100 arquivos de código).

## Inferências e limitações
- ❓ Existência de testes manuais/E2E no cliente web.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/08-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Sugestão (fora do escopo): testes de regra para `ArquivoService` (arquivo único), `AutorizacaoService` e `ClientIdFilter`.
