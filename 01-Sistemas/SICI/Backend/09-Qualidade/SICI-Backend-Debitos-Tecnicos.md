---
type: technical-debt
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - qualidade
  - debitos-tecnicos
  - riscos
---

# Débitos técnicos e riscos (consolidado)

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]], [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]]

> Consolidação dos achados dos lotes 1–6. Cada item aponta a nota com as evidências (arquivo, classe, método).
> **Severidade**: 🔴 crítica (risco à integridade de atos oficiais ou segurança) · 🟠 alta · 🟡 média · 🟢 baixa.
> **Status**: ✅ confirmado no código · 🔶 inferência que precisa de confirmação (teste/dados).

## 🔴 Críticos
| ID | Débito | Impacto | Onde | Status |
|---|---|---|---|---|
| D01 | Endpoints de SUBCI/substituto sem `@PreAuthorize` → qualquer auditor vira assinante | assinatura de OS oficiais por pessoa não autorizada | [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]] | ✅ |
| D02 | Segredos (senha do banco, segredo do HMAC, super-usuários) versionados em `application-*.properties` | vazamento de credenciais; quem tem acesso ao repositório consegue forjar códigos verificadores | [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]], [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] | ✅ |
| D03 | Numeração oficial `max+1` por ano, sem lock nem unique (removida na V44), com chamada HTTP no meio | **números oficiais duplicados** | [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Banco-e-Migrations|Banco-e-Migrations]] | ✅ código / 🔶 ocorrência |
| D04 | Status ASSINADA atingível sem assinatura (`PUT /alterarStatusOs`) | OS "assinada" sem documento nem número; libera prorrogação; não efetiva equipe | [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] | ✅ |

## 🟠 Altos
| ID | Débito | Onde | Status |
|---|---|---|---|
| D05 | Regra "abertura assinada antes das demais OS" implementada e nunca chamada (`validarCriacaoComBaseNasOrdens`) | [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] | ✅ |
| D06 | Validação do código verificador sempre `true`; sem integridade do PDF nem aviso de cancelamento | [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]] | ✅ |
| D07 | 46 endpoints sem role, incluindo escrita/exclusão (OS genérica inteira, prorrogações, fases, POAC) | [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] | ✅ |
| D08 | Exclusão de OS genérica assinada permitida | [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]] | ✅ |
| D09 | Provável perda das fases das OS canceladas (`cancelar` sem fases + `orphanRemoval`) | [[01-Sistemas/SICI/Backend/03-Modulos/Prorrogacao-e-Cancelamento|Prorrogacao-e-Cancelamento]] | 🔶 |
| D10 | Enums persistidos por **ordinal**; `DEFAULT 1` da V16 = ENVIADA | [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Enums-e-Estados|Enums-e-Estados]] | ✅ / 🔶 dados |
| D11 | Atualização de OS permite trocar o modelo e não revalida as regras de criação; não bloqueia OS CANCELADA | [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] | ✅ |
| D12 | Ação de controle editável depois da abertura assinada; validação de objetivos PPA só na criação | [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]] | ✅ |
| D13 | Testes quebrados (11 de 62) e build da imagem com `-Dmaven.test.skip=true` | [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] | ✅ |

## 🟡 Médios
| ID | Débito | Onde | Status |
|---|---|---|---|
| D14 | IDOR em downloads de PDF assinados e consultas por id | [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] | ✅ |
| D15 | Login ROPC (`grant_type=password`) e CORS `*` | [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]] | ✅ |
| D16 | Healthcheck público com detalhes; Prometheus e Swagger públicos; health depende do Keycloak (risco de reinício em cascata) | [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] | ✅ / 🔶 |
| D17 | Sem handler genérico de exceções: `ResolutionException`, `IllegalStateException` etc. → 500; NPE → 400 | [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] | ✅ |
| D18 | JSON para o serviço de PDF montado à mão (escape incompleto); sem timeout explícito nem retry | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integracoes-Externas]] | ✅ |
| D19 | PDF gerado antes de validar o status na assinatura | [[01-Sistemas/SICI/Backend/05-Fluxos/Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]] | ✅ |
| D20 | Sigla do número oficial = UAI do assinante (intenção a confirmar) | [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]] | ✅ / ❓ regra |
| D21 | `SUPER_USUARIO` sem efeito nos endpoints com role (bypass inconsistente) | [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]] | ✅ |
| D22 | Profile Maven literal no Dockerfile (`-P SPRING_PROFILES_ACTIVE`) | [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] | 🔶 |
| D23 | Migrations destrutivas (V44 `DROP TABLE`) e Flyway desligado em hom/prod | [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Banco-e-Migrations|Banco-e-Migrations]] | ✅ |
| D24 | Testcontainers em PostgreSQL com banco real SQL Server | [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] | ✅ |
| D25 | Sem trilha de auditoria de alterações | [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] | ✅ |

## 🟢 Baixos / manutenibilidade
| ID | Débito | Onde |
|---|---|---|
| D26 | Desvios hexagonais: domínio importa `application` e `infrastructure` (`Auditor` → entidade JPA); use cases usam repositórios JPA; portas `in` recebem DTOs | [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Arquitetura-Hexagonal|Arquitetura-Hexagonal]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] |
| D27 | Lógica de PDF duplicada (controller × `AssinarOrdemServico`) e no controller | [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]] |
| D28 | Código morto: `NumeracaoServiceImpl.gerarPosAssinatura`, `OrdemServico.id()`, `buscarPorOrdemServico` da numeração (sempre vazio), `if` vazios em `AlterarStatus*`, `dataFinalAtual` sem uso, classes vazias (`ExternalClass`, `AdviceClass`, `ErrorClass`) | várias notas |
| D29 | `POST /salvar-os` recebe lista e usa só o primeiro item | [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] |
| D30 | Ids mágicos (`999` = "A DEFINIR"; tipos 1/4/5 em `if`s) | [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]] |
| D31 | Testes `== null` sobre adapters que lançam exceção (`AcaoControleRepositoryAdapter.buscarPorId`) | [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]] |
| D32 | Exceções inadequadas (`java.lang.module.ResolutionException`, `RuntimeException` genérica) | [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] |
| D33 | Dependências: `hibernate-core` fixado em 6.2.3 sob Boot 3.3; dialeto `SQLServer2012Dialect` obsoleto; `cache`/`aop` possivelmente não usados; `allow-bean-definition-overriding=true` | [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] |
| D34 | API sem padrão REST (verbos no caminho, camelCase misturado); README é o template padrão do GitLab | [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] |
| D35 | `spring.thymeleaf.cache=false` e log `DEBUG` como padrão base | [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] |

## Sugestão de ordem de ataque (🔶 recomendação, não decisão)
1. **D01, D04, D07**: travar autorização (`@PreAuthorize` nos endpoints de SUBCI, OS genérica e escrita; proibir ASSINADA fora do fluxo de assinatura).
2. **D02**: rotacionar segredos e mover para variáveis de ambiente ou cofre de segredos; limpar o histórico com o time de infraestrutura.
3. **D03**: unique `(ANO, NUM_SEQUENCIAL)` (e UAI, se a regra for por UAI) + sequence ou lock pessimista; levantar duplicidades existentes.
4. **D05, D06, D08, D11**: aplicar as regras de domínio já escritas e completar a validação.
5. **D13**: consertar os testes e passar a rodá-los no pipeline.
