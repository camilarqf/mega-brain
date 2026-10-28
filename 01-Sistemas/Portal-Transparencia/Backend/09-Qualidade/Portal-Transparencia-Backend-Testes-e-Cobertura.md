---
type: quality
aliases:
  - "Testes e cobertura"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
sources:
  - src/test/java
  - src/main/resources/application-test.properties
  - Dockerfile
  - pom.xml
---
# Testes e cobertura

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

## Objetivo
Descrever os testes existentes, o que cobrem e o que exigem para rodar.

## Evidências
Listagem de `src/test/java` (somente arquivos versionados), contagem de `@Test` por classe e leitura por amostragem de `ClienteIdFilterTest`, `ServidorControllerTeste`, `ConvenioControllerTeste`, `VelocityQueryTest`, `JdbcUtilTest`, `ReportUtilTest` e `NotaEmpenhoTeste`. Testes **não** foram executados.

## Informações confirmadas
- ✅ 14 classes de teste versionadas com **139 métodos `@Test`** (mais a classe auxiliar `PageableImpl`). Há também testes não versionados em `src/test/.../servico/pesquisa/` (fora do escopo por decisão do usuário).
- ✅ JUnit 4 com Spring Boot Test (`SpringJUnit4ClassRunner`, `@SpringApplicationConfiguration`, `@WebAppConfiguration`, `MockMvc`); `pom.xml` usa `spring-boot-starter-test`.
- ✅ Distribuição:
| Grupo | Classes | `@Test` | Dependência |
|---|---|---|---|
| Controllers (MockMvc, contexto completo, `@ActiveProfiles("test")`) | `ConvenioControllerTeste` (12), `LicitacoesContratosControllerTeste` (14), `EmpresaPunidaControllerTeste` (7), `PrestandoContasControllerTeste` (8), `RemuneracaoControllerTeste` (12), `ServidorControllerTeste` (18) | 71 | **banco SQL Server real** (perfil `test` com URL JDBC) |
| Modelo | `DespesaConsultaDinamicaTeste` (29), `NotaEmpenhoTeste` (22) | 51 | nenhuma (mapeamento de colunas por reflexão) |
| Filtros | `ClienteIdFilterTest` (5: sem cabeçalho → 400; com cabeçalho; `/healthcheck`, `/prometheus` e preflight dispensados), `CorsFilterTest` (1) | 6 | nenhuma |
| Util/serviço | `JdbcUtilTest` (2), `ReportUtilTest` (3), `VelocityQueryTest` (3), `EmpresaPunidaRelatorioServiceTeste` (3) | 11 | nenhuma ou mínima |
- ✅ O build da imagem **pula** os testes (`-Dmaven.test.skip=true` no `Dockerfile`); não há evidência de pipeline de testes neste repositório.
- ✅ Não há `@Ignore` nos testes versionados.

## Inferências e limitações
- 🔶 Os testes de controller verificam principalmente status e `jsonPath` contra dados reais; ficam frágeis (dependem do conteúdo do banco) e **não rodam sem acesso** ao SQL Server do perfil `test`.
- 🔶 Cobertura estimada baixa e concentrada: **nenhum teste** para `MascaramentoAspect`/`MascaramentoService`, `SendMailService`, `PortalAnalytics*`, `CacheControl*`, `MascaramentoAMQService` nem para o módulo de storage (`StorageController`, `StorageService`, `StorageUrlService`, novos) nem para a maior parte dos 71 controllers (6 controllers de 71 têm teste). Sem medição (JaCoCo não configurado).
- ❓ Resultado atual da suíte (verde/vermelho) não verificado.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] · [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Pendências e próximo passo
- Priorizar testes unitários do mascaramento (regra sensível) e da construção de consultas Velocity; executar a suíte em ambiente com banco de teste.
