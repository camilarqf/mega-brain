---
type: domain
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
tags:
  - portal-transparencia
  - backend
  - dominio
  - modelo
sources:
  - src/main/java/br/gov/df/transparencia/modelo
  - src/main/java/br/gov/df/transparencia/dto
  - src/main/java/br/gov/df/transparencia/enums
---
# Modelo de domínio

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]]

## Objetivo
Mapear as classes de `modelo`, `dto` e `enums` por área funcional, para localizar rapidamente onde cada conceito é representado.

## Evidências
Listagem dos pacotes `modelo` (122 arquivos), `dto` (10), `enums` (7); leitura das 6 classes `@Entity` e de `modelo/mascaramento`. Os campos de cada classe **não** foram lidos um a um.

## Informações confirmadas
- ✅ As classes de `modelo` são, em sua maioria, **beans anêmicos** que acumulam dois papéis: bean de **filtro** de entrada (parâmetros da query string) e **linha de resultado** mapeada por `BeanPropertyRowMapper` a partir das colunas do SQL (ex.: `Remuneracao`). Há poucas regras no próprio modelo (⚠️ exceção: `modelo/mascaramento`).
- ✅ Só 6 classes são entidades JPA: `PesquisaSatisfacao` (`Portal.Registro_Pesquisa`), `RegistroContato` (`Portal.Registro_Contato`), `NotaLancamentoEvento` (`Despesa.TF_NOTA_LANCAMENTO_EVENTO`), `Expulsao` (`Expulsao.Principal`), `ReceitaPrincipal` (`Receita.Principal`) e `Conselheiro` (sem `@Table` explícito).
- ✅ `modelo/configuracao`: 26 classes de apoio (`CustomPage` com totalizador, `Coluna` e `RowMapper`s de gráficos/geo).

| Área | Classes principais (pacote `modelo`) |
|---|---|
| Despesa (28) | `NotaEmpenho`, `NotaLancamento`, `NotaFiscal`, `OrdemBancaria`, `OrdemCancelamento`, `RestoAPagar`, `DiariasPassagens`, `EmendaParlamentar`, `EmendaParlamentarFederal*`, `PagamentoCredor*`, `Credor`, `ProgramaTrabalho*`, `Funcao`/`SubFuncao`/`Programa`/`Projeto`, `DespesaConsultaDinamica`, `DespesaCovidPorItem`, `TipoLicitacao` |
| Receita (5) | `Receita`, `ReceitaPrincipal`, `ReceitaConsultaDinamica`, `ReceitaFonteRecurso`, `ReceitaImposto`; na raiz `Arrecadacao` |
| Servidor e remuneração | `Servidor`, `ServidorRelatorio`, `Remuneracao`, `Rubrica`, `CargoEfetivo`, `CargoFuncao`, `servidor/MilitaresCedidos`, `expulsao/Expulsao` |
| Licitações e contratos (8) | `Licitacao`, `Contrato`, `Aditivo`, `ItemLicitado`, `Proposta`, `Vencedor`, `FornecedorPregao`, `ProcessoOrgao` |
| Convênios (3) | `Convenio`, `EntidadeBeneficiada`, `DetalhamentoEntidadeBeneficiada` |
| Patrimônio (7) | `BensImoveis`, `BensMoveis`, `BensMoveisV2`, `BensOrgaoLocalizacao`, `Edificacao`, `Obra`, `Terreno` |
| Prestação de contas (15) | beneficiários (`BeneficiarioAuxilioEmergencial`, `BeneficiariosBolsaAlimentacao`, `BeneficiarioProgramaSocial`, `BeneficiarioArtisticoCultural`, `BeneficiarioCartaoMaterialEscolar`, `BeneficiarioMobilidadeCidada`), `EmpresaProgramaIntegridade`, `ProcessoAdministrativoDisciplinar`, `ProcessoInvestigacaoPreliminar`, `ProsperaDF`, `OrgaoDeliberativo`, `Conselheiro`, `ShowsEventos`, `SucorAcao`, `SucorFase`; na raiz `EmpresaPunida` |
| Comum | `ArquivosDownloadModelo`, `ChaveOrgao`, `PesquisaSatisfacao`, `RegistroContato`, `ServidorIntegracao`, `ServidorSciIntegracao`, `OrdemBancariaIntegracao`; raiz: `CargaAtualizacao`, `QddUgGestao`, `GraficoBarra`/`GraficoDonut`, `Relatorio` |
| DTOs (10) | `OrgaoLAIDTO`, `Arquivo`, `DashboardExecucaoDespesaDTO`, `DespesaRAsDTO`, `FuncaoImagemDTO`, `FornecedorDTO`, `ItemLicitadoDetalhamentoDTO`, `PainelDespesaDTO`, `PesquisaSatisfacaoDTO`, `TextosConsultasDTO` |
| Mascaramento (6) | `ConsultaMascarada`, `CampoMascarado`, `DadoMascarado`, `MascaramentoHandler`, `ServidorPorOrgaoLotacaoHandler`, `SetOperation` (ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]]) |

### Enums (7)
`OcupacaoEnum` (Servidor, Jornalista, Estudante, Advogado, Empresário, Outros), `SatisfacaoEnum` (de Muito Satisfeito a Muito Insatisfeito; usados na pesquisa de satisfação), `StatusServidorEnum` (aposentado ou pensionista, desligado, desligado no mês), `SituacaoFuncionalServidorEnum` (aposentado, pensão), `SituacaoFuncionalDescServidorEnum` (conselheiro, servidor militar), `FaixaEtariaEnum` e `FundoEnum` (valores não lidos).

## Inferências e limitações
- 🔶 Os nomes das tabelas de carga (`carga`, `despesa`, `servidor`…) indicam que os dados são **carregados por processo externo** (ETL) e o backend só consulta; o processo de carga não faz parte do repositório.
- ❓ Campos, chaves e significado de negócio de cada classe não foram detalhados; fica para os módulos por área.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]]

## Pendências e próximo passo
- Módulos por área criados no lote 7 (ver [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]]); falta detalhar os campos de cada classe.
