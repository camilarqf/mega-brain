---
type: quality
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - qualidade
  - testes
sources:
  - src/test/java/br/gov/df/cg/sici/**
  - target/surefire-reports/*.txt (execução local de 2026-10-09)
  - pom.xml
  - .docker/Dockerfile
---

# Testes e cobertura

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/08-Qualidade/SICI-Backend-Debitos-Tecnicos|Debitos-Tecnicos]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Stack-e-Dependencias|Stack-e-Dependencias]]

## Inventário ✅
- **31 classes** em `src/test` (incluindo `TestSiciApplication`, um runner com Testcontainers) e **64 `@Test`**.
- Estilo predominante: **unitário com Mockito** (`@ExtendWith(MockitoExtension.class)`) sobre use cases.
- Testes de contexto Spring: `SiciApplicationTests` e `FaseOrdemServicoMapperTest` (`@SpringBootTest`), `ValidacaoAssinaturaTest` (`@WebMvcTest`).
- Não há plugin de cobertura (JaCoCo) no `pom.xml`, nem testes de contrato ou de segurança da matriz de endpoints.

| Área | Classes de teste |
|---|---|
| Ação de Controle | `AcaoControleControllerTest`, `AcaoControleServiceTest`, `Criar/Atualizar/Inativar/ListarAcaoControleTest`, `AcaoControleRepositoryAdapterTest` |
| Ordem de Serviço | `CriarOrdemServicoTest`, `AtualizarOrdemServicoTest`, `AtualizarOrdemServicoUseCaseTest`, `ExcluirOrdemServicoTest`, `ListarOrdemServicoTest`, `PesquisarOrdemServicoTest`, `CriarProrrogacaoOrdemServicoTest`, `AtualizarProrrogacaoOrdemServicoTest` |
| Fases | `BuscarDescricaoFaseAcaoUseCaseTest`, `FaseOrdemServicoMapperTest`, `FaseServiceTest`, `SalvarFaseOrdemServicoUseCaseTest` |
| Assinatura | `CriarAssinaturaTest`, `ValidacaoAssinaturaTest`, `AssinarOrdemServicoGenericaTest` |
| OS Genérica | `AtualizarOrdemServicoGenericaUseCaseTest` |
| SUBCI / Auditor | `CriarSubciTest`, `ListarSubciTest`, `PesquisarSubciTest`, `AuditorServiceTest` |
| Segurança / Keycloak | `JwtAuthenticationConverterCustomTest`, `KeycloakAuthAdapterTest` |

## Última execução encontrada ✅
Relatórios Surefire em `target/surefire-reports`, datados de **2026-10-09** (execução local anterior a esta análise; 🔶 pode não corresponder exatamente ao commit `1871e32`). **Não executei** a suíte nesta análise.

| Total | Falhas | Erros | Ignorados |
|---|---|---|---|
| 62 | 4 | 7 | 0 |

29 relatórios: 8 classes com falha ou erro. `CriarAssinaturaTest` não tem relatório.

| Classe | Causa resumida |
|---|---|
| `AtualizarAcaoControleTest`, `CriarAcaoControleTest` | `MultiplasValidacoesException`: mocks não cobrem as validações novas (unidade, área, programa, objetivos) |
| `ValidacaoAssinaturaTest` | `ApplicationContext` não sobe (`@WebMvcTest` sem os beans necessários) |
| `AtualizarProrrogacaoOrdemServicoTest` | NPE: `osBaseProrrogacao` nulo (mock desatualizado) |
| `FaseOrdemServicoMapperTest` | NPE no mapper: usa `OrdemServico.id(1)`, que retorna `null` |
| `SalvarFaseOrdemServicoUseCaseTest` | NPE: dependência nova (`ordemServicoRepositoryPort`) não injetada no teste |
| `AssinarOrdemServicoGenericaTest` | `UnnecessaryStubbingException` (Mockito strict) |

🔶 As falhas parecem de **testes desatualizados** em relação ao código, não regressões funcionais. O build da imagem não detecta isso, porque o Dockerfile roda `mvn -Dmaven.test.skip=true`.

## Lacunas de cobertura (por leitura) ✅
Sem teste identificado para:
- `AssinarOrdemServico` (efeitos por modelo, numeração, assinante autorizado);
- numeração (`NumeracaoRepositoryAdapter`, concorrência);
- `CancelarOrdemServico` e o efeito de cancelamento na assinatura;
- `AlterarStatusOrdemServico` (incluindo a brecha ASSINADA);
- `SubciSubstitutoServiceImpl` e a autorização dos endpoints de SUBCI;
- matriz `@PreAuthorize` × roles (nenhum teste de segurança HTTP);
- `PdfService` (escape do JSON);
- `CriarOrdemServicoGenerica`, `ExcluirOrdemServicoGenerica`;
- migrations (Testcontainers usa **PostgreSQL**, enquanto o banco real é **SQL Server**).
