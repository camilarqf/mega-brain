---
type: module
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
  - modulo
  - prestacao-de-contas
sources:
  - src/main/java/br/gov/df/transparencia/api/prestandoContas
  - src/main/java/br/gov/df/transparencia/servico/prestandoContas
  - src/main/java/br/gov/df/transparencia/modelo/prestandoContas
  - src/main/java/br/gov/df/transparencia/modelo/EmpresaPunida.java
  - src/main/resources/sql/prestando-contas
---
# Módulo Prestação de Contas

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seção Prestação de contas)

## Objetivo
Documentar a segunda maior área do portal: transparência ativa sobre programas sociais, conselhos, empresas punidas e do programa de integridade, processos disciplinares e investigativos, Prospera DF, gastos com publicidade e outros relatórios.

## Evidências
Leitura da lista de métodos dos 17 serviços, dos 16 controllers (107 rotas) e análise de tabelas dos 102 arquivos SQL; leitura de trechos de `PrestandoContasService` só por nomes de método. Corpos e `.vm` não lidos.

## Informações confirmadas
| Tema | Controller (rotas) | Serviço | Dados principais |
|---|---|---|---|
| Visões gerais, conselhos e órgãos deliberativos, shows e eventos, gastos com publicidade, programas sociais, cartão material escolar, outros relatórios | `PrestandoContasController` (`/prestando-contas`, 39), `PrestandoContasRelatorioController` (7) | `PrestandoContasService`, `PrestandoContasRelatorioService` | `Prestando_Contas.Orgao_Deliberativo`, `Despesa.Show_Evento`, `Beneficiario.BENEFICIARIO_PROGRAMA_SOCIAL`, `Programa_Social`, `Material_Escolar` |
| Auxílio emergencial, artístico-cultural, mobilidade cidadã, prato cheio | `BeneficiariosAuxilioEmergencialController` (10), `...RelatorioController` (4) | `BeneficiariosAuxilioEmergencialService` | `Beneficiario.RENDA_EMERGENCIAL`, `ARTISTICO_CULTURAL`, `MOBILIDADE_CIDADA`, `PRATO_CHEIO` |
| Bolsa alimentação | `BeneficiariosBolsaAlimentacaoController` (5), `...Relatorio` (1) | `BeneficiariosBolsaAlimentacaoService` | `bolsaAlimentacao.TF_BOLSA_ALIMENTACAO`, `TD_ESCOLA`, `TD_TIPO_REGIME`, `TD_RESPONSAVEL` |
| Conselheiros | `ConselheiroController` (1) | `ConselheiroService` | entidade JPA `Conselheiro` |
| Empresas do programa de integridade | `EmpresaProgramaIntegridadeController` (7), `...Relatorio` (1) | `EmpresaProgramaIntegridadeService` | `Integridade.EMPRESA` |
| Empresas punidas | `EmpresaPunidaController` (`/empresa-punida`, 7) | `EmpresaPunidaService`, `EmpresaPunidaRelatorioService` | `Empresa_Punida.Principal` |
| PAD (processos administrativos disciplinares) | `PADController` (6), `PADRelatorioController` (1) | `PADService` | `Sucor.PAD_Principal`, `PAD_Detalhamento_acao`, `PAD_Detalhamento_fase` |
| PIP (processos de investigação preliminar) | `PIPController` (6), `PIPRelatorioController` (1) | `PIPService` | `Sucor.PIP_PRINCIPAL`, `PIP_DETALHAMENTO_ACAO` |
| Prospera DF | `ProsperaDFController` (11), `...Relatorio` (1) | `ProsperaDFService` | `Prestando_Contas.Prospera_DF` |

- ✅ Modelo (15 em `modelo/prestandoContas` + `EmpresaPunida`): `BeneficiarioAuxilioEmergencial`, `BeneficiarioArtisticoCultural`, `BeneficiarioMobilidadeCidada`, `BeneficiarioCartaoMaterialEscolar`, `BeneficiarioProgramaSocial`, `BeneficiariosBolsaAlimentacao`, `Conselheiro`, `EmpresaProgramaIntegridade`, `OrgaoDeliberativo`, `ProcessoAdministrativoDisciplinar`, `ProcessoInvestigacaoPreliminar`, `ProsperaDF`, `ShowsEventos`, `SucorAcao`, `SucorFase`.
- ✅ Dois POST: `POST /prestando-contas/categorias` e `/data-referencias` (listas de apoio).
- ✅ **Mascaramento**: `ConselheiroService.pesquisarConselheiros` (`CONSELHEIROS`, campo `NOME`) e `PrestandoContasService` (um método, `CONSELHOS`, `NOME`). Beneficiários de programas sociais, PAD/PIP e empresas **não** passam pelo filtro.
- ✅ Documentos publicados (legislação, gastos com publicidade, relatórios gerenciais, "outros relatórios", organizações sociais de saúde) vêm do catálogo `Servidor.Relatorio` por categoria (12 referências em SQL da área; ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Documentos publicados]]); `Portal.TD_TEMPO` para datas.
- ✅ O enum `ServidorRelatorio.CategoriaRelatorioEnum` tem categorias `BENEFICIARIOS_*` (ids 15, 38, 64, 66, 67, 68) que identificam documentos de legislação de programas no catálogo `Servidor.Relatorio`.

## Inferências e limitações
- 🔶 "Sucor" (schema de PAD/PIP) provavelmente é a unidade responsável pela correição; sigla não explicada no código. O "PIP" aqui (investigação preliminar) corresponde ao tema do sistema `SCI`, mas **não há evidência** de integração entre eles.
- ✅ Beneficiários: 6 listas usam `dbo.FN_MASCARA_NR_CPF` no SQL; a lista de programas sociais devolve NIS e CPF **sem máscara** e só exclui registros anonimizados (`CD_ANONIMIZADO <> 1`); empresas punidas e Prospera DF devolvem CPF/CNPJ sem máscara. Ver [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]].
- ❓ Fórmulas, critérios de elegibilidade e regras de cada programa não estão no código lido.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]] (CPF, NIS e documento por programa)
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Pendências e próximo passo
- Campos pessoais já levantados; documentar regras de elegibilidade e valores de cada programa com o time de negócio.
