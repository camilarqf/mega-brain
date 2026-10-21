---
type: analysis-log
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
commit_data: 2026-09-24
branch: master
tags:
  - portal-transparencia
  - controle
  - cobertura
---

# Registro de análise

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|Pendencias]]

## Base analisada
- Repositório: `portal-transparencia-backend` (pasta local `PT2016_BackEnd`; GitLab interno, endereço omitido). Branch `master`, commit `9434e58f` (2026-09-24).
- Atualização de 2026-10-21: `HEAD` `e98fcc38` (master). O `analyzed_commit` das notas avançou só nas **11 verificadas** no lote 9 (Stack, Perfis, Integrações, Catálogo de endpoints, Segurança, Débitos, Testes, Backend-Index, Registro, Pendências e Index do sistema); as notas de módulo, domínio, fluxos, Revisão de injeção de SQL e Dados pessoais continuam em `9434e58f` porque o diff não toca seus `sources` (arquivo `portal2016.log.2` removido, sem efeito funcional).
- Working tree: com arquivos não versionados (`RELATORIO_*_LEGADO.md` ×4, `logback-spring.xml`, `src/test/.../servico/pesquisa/`). **Excluídos por decisão do usuário (2026-10-19)**; não foram lidos.
- Método: leitura estática; catálogo de endpoints gerado por script a partir das anotações. Testes não executados; aplicação não iniciada.
- ID do sistema escolhido pelo usuário: `Portal-Transparencia` (hífen no lugar do espaço, conforme a seção 3 do `BRAIN-RULES.md`).

## Regras de proteção aplicadas
- Valores de `application*.properties`, `persistence.xml`, `GoogleAnalyticsConstantes.java`, chaves do filtro comentado e `newrelic.yml` **não registrados** (só nomes de chaves e existência do problema).
- Endereços de infraestrutura, usuários e senhas não reproduzidos.

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Cadastro `Portal-Transparencia`, índices, repositório, stack, perfis, controle | ✅ concluído | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Index\|Index]], [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Repositorios\|Repositorios]], [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index\|Backend-Index]], [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Stack-e-Dependencias\|Stack]], [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes\|Perfis-e-Ambientes]], Registro, Pendências |
| 1 | Arquitetura, segurança e débitos | ✅ concluído | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas\|Arquitetura-em-Camadas]], [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao\|Seguranca-e-Autorizacao]], [[01-Sistemas/Portal-Transparencia/Backend/08-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos\|Debitos-Tecnicos]] |
| 2 | API | ✅ concluído (parâmetros e respostas não detalhados) | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints\|Catalogo-de-Endpoints]] |
| 3 | Persistência e domínio | ✅ concluído (parcial: campos e SQL por área não detalhados) | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio\|Modelo-de-Dominio]], [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations\|Banco-e-Migrations]] |
| 4 | Cache, mascaramento, relatórios e fluxo | ✅ concluído | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento\|Cache-e-Mascaramento]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao\|Relatorios-e-Exportacao]], [[01-Sistemas/Portal-Transparencia/Backend/04-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados\|Fluxo-Invalidacao]] |
| 5 | Integrações | ✅ concluído | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas\|Integracoes-Externas]]; `Mapa-de-Integracoes` e `Catalogo-de-Sistemas` atualizados |
| 6 | Qualidade | ✅ concluído | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/08-Qualidade/Portal-Transparencia-Backend-Testes-e-Cobertura\|Testes-e-Cobertura]] |
| 7 | Módulos por área funcional | ✅ concluído (parcial: `.vm` e corpos de serviço lidos só por amostragem) | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa\|Despesa]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Receita\|Receita]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Servidores-e-Remuneracao\|Servidores-e-Remuneracao]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Licitacoes-e-Contratos\|Licitacoes-e-Contratos]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Convenios\|Convenios]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Patrimonio\|Patrimonio]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Prestacao-de-Contas\|Prestacao-de-Contas]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados\|Orcamento-e-Documentos-Publicados]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados\|Apoio-e-Atualizacao-de-Dados]] |
| 8 | Leitura dirigida: (1) injeção de SQL em todos os `.vm` e rotas POST; (2) cálculos dos `.vm` principais de despesa; (3) campos pessoais expostos | ✅ concluído (parcial: 126 referências SQL não resolvidas e 142 `.vm` de despesa não lidos; sem teste dinâmico) | 2026-10-19 | [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL\|Revisão de injeção de SQL]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Despesa-Consultas-e-Calculos\|Despesa: consultas e cálculos]], [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos\|Dados pessoais expostos]] |
| 9 | Atualização `9434e58f` → `e98fcc38` (13 commits da `feat/servico-minio`): `StorageController`, `StorageService`, `StorageUrlService`, `pom.xml` e `application-hom/prod.properties` | ✅ concluído (leitura estática; consumidor do storage só por informação do usuário) | 2026-10-21 | [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas\|Integracoes-Externas]], [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints\|Catalogo-de-Endpoints]], [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes\|Perfis-e-Ambientes]], Stack, [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao\|Seguranca-e-Autorizacao]], [[01-Sistemas/Portal-Transparencia/Backend/08-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos\|Debitos-Tecnicos]], Testes, Backend-Index |

## O que não foi coberto
- Corpo dos 547 templates `.vm` e de grande parte dos 65 serviços: as notas de módulo trazem estrutura, tabelas, rotas e as regras lidas; cálculos, filtros fixos e campos expostos por modelo ficaram para leitura dirigida.
- Parâmetros, corpos e respostas por endpoint; rotas do Spring Data REST.
- Teste dinâmico da injeção de SQL e de `/download/arquivos/{nome}`; 126 referências SQL sem origem resolvida; `.vm` de despesa fora dos 7 principais.
- Execução da suíte de testes; `settings.xml`, `newrelic.yml` e `logback` (não lidos por conterem ou poderem conter segredos / ser não versionado).

## Resultado final (lotes 0 a 9)
- **30 notas** do Portal-Transparencia (2 na raiz do sistema e 28 no backend) mais atualização de `Catalogo-de-Sistemas` e `Mapa-de-Integracoes`.

## Próximo passo exato
- (1) **Correção** (fora desta Skill, pelo time): corrigir as 5 rotas POST e planejar a migração dos `.vm` para parâmetros vinculados; (2) **validação dinâmica** em ambiente de teste, com autorização, da injeção de SQL e do conteúdo de `[NR-CPF]`/`cpf_formatado`/`NR_CPF`; (3) revisar à mão as 126 referências SQL não resolvidas; (4) ler o diff da `feature/novoFiltroLicitacao` e os `.vm` de diárias e passagens, emendas, QDD e execução OCA; (5) confirmar semântica de `NR_NE_ORIGINAL`, evento `400091` e restos a pagar; (6) **storage**: identificar o `gerenciador`, confirmar a visibilidade do bucket e os perfis `dev`/`test` (pendências 18 a 20) e, se o time quiser, ler o repositório do gerenciador para tornar o consumidor ✅.
- Em paralelo, tratar as perguntas de [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|Pendências]].
- Se o código mudar: `git diff e98fcc38c21e0f2063bf0c2c9377d4b492ee5062..HEAD --stat` e usar a skill `atualizar-documentacao`.
