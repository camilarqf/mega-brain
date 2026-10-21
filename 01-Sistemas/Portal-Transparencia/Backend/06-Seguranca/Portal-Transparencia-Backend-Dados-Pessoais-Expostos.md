---
type: security
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
  - seguranca
  - dados-pessoais
  - lgpd
sources:
  - src/main/java/br/gov/df/transparencia/modelo
  - src/main/resources/sql/remuneracao
  - src/main/resources/sql/servidor
  - src/main/resources/sql/comum
  - src/main/resources/sql/prestando-contas
  - src/main/resources/sql/expulsao
  - src/main/java/br/gov/df/transparencia/api/comum/IntegracaoSistemasController.java
---
# Dados pessoais expostos pela API

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]]

> Nenhum dado real foi consultado nem é registrado. A nota descreve **quais campos pessoais** o código devolve e **quais controles** existem. Não é parecer jurídico sobre o que a lei exige publicar.

## Objetivo
Inventariar os campos pessoais (nome, CPF, NIS, matrícula, filiação, endereço, remuneração) devolvidos pelas rotas de servidores, remuneração e beneficiários, e classificar a proteção aplicada.

## Evidências
Leitura dos modelos (`Remuneracao`, `Rubrica`, `Servidor`, `Expulsao`, `MilitaresCedidos`, `Conselheiro`, `Servidor*Integracao`, beneficiários e empresas) com suas anotações (`@JsonIgnore`, `@Mascarado`), e das listas `SELECT` dos templates SQL correspondentes. Apenas o **SQL** define o que é preenchido; campos do modelo sem coluna correspondente saem `null`.

## Informações confirmadas
### Controles existentes
- ✅ **`@JsonIgnore` no CPF de comparação**: `Remuneracao.cpfComparacao` e `Servidor.cpfComparacao` (coluna do CPF cru) são selecionados no SQL mas **não** são serializados.
- ✅ **Máscara no SQL**: a função de banco `dbo.FN_MASCARA_NR_CPF` é usada em 6 listas de beneficiários (auxílio emergencial, artístico-cultural, mobilidade cidadã, prato cheio, bolsa alimentação e cartão material escolar) e na coluna `codigoCredorMascarado` da despesa. A função em si não faz parte do repositório (formato exato da máscara ❓).
- ✅ **Anonimização por flag**: `BENEFICIARIO_PROGRAMA_SOCIAL` só devolve linhas com `CD_ANONIMIZADO <> 1`.
- ✅ **Medida protetiva**: remove registros (não só mascara) de pessoas cadastradas, em 30 métodos de serviço ([[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]]).
- ✅ **Dados de menores** do cartão material escolar: o modelo tem campos de aluno (nome, NIS, data de nascimento, endereço, mãe), mas a consulta devolve apenas **responsável (nome, CPF mascarado), série, escola, exercício e valor**.

### Inventário por rota (campos pessoais devolvidos)
| Área / rota | Campos pessoais retornados (pelo SQL) | Controle | Observação |
|---|---|---|---|
| `/remuneracao` (lista) | nome, matrícula, órgão, cargo, função, situação, detalhamento completo da remuneração (básica, benefícios, funções, hora extra, imposto de renda, seguridade, líquido, bruto), `cpfServidor` (`cpf_formatado`) | mascaramento por medida protetiva; CPF cru oculto | 🔶 `cpf_formatado` parece a versão mascarada, mas isso é inferido (a coluna vem pronta da base) |
| `/remuneracao/...` extrato anual e rubricas | matrícula, nome, rubricas com valores | idem | — |
| `/servidor` (lista) | nome, matrícula, órgão, cargo, função, lotação, datas de admissão/desligamento/aposentadoria, regime, carga horária | mascaramento; CPF cru oculto | `cpf`, `mae`, `conjuge` e `sexo` existem no modelo, mas **não** são selecionados na lista |
| `/integracao/pesquisar-servidor` (por nome) | **`[NR-CPF]` como `cpf`**, nome, matrícula, órgão, status | ❌ nenhum (sem autenticação, sem `@Mascaravel`) | 🔴 devolve o campo CPF da base; a base **não** parece guardá-lo mascarado (é comparado por igualdade com CPF decodificado em outras consultas) 🔶 |
| `/integracao/consultar-servidor` (por matrícula/órgão) | nome e **CPF** de todos os servidores do último mês carregado | ❌ nenhum | idem |
| `/integracao/nome-servidor`, `/funcao-servidor`, `/verificar-sutcs`, `/consultar-servidor-ativo` | nome, CPF, função e símbolo da função por **CPF informado** | ❌ nenhum | permite confirmar a existência/função de um CPF |
| `/servidor/militares-cedidos` | nome, **matrícula**, remuneração bruta, graduação, órgãos | ❌ **sem `@Mascaravel`** | `MilitaresCedidosService` não passa pelo filtro de medida protetiva |
| `/empresa-punida` | tipo de pessoa, **CPF/CNPJ** (`numeroCpfCnpj`), nomes, sanção | ❌ sem máscara no SQL | podem ser pessoas físicas; formato do CPF cru |
| `/prestando-contas/prospera-df` | **`TX_CPF_CNPJ`** (`documento`), tomador, valores | ❌ sem máscara | idem |
| `/prestando-contas/...` programas sociais (`BENEFICIARIO_PROGRAMA_SOCIAL`) | nome, **NIS** (`NR_NIS`), **`NR_CPF`** (modelo `Integer`), programa, valor | só `CD_ANONIMIZADO <> 1`; **sem máscara no SQL**; busca por `like` no NIS | 🔶 o tipo `Integer` do CPF sugere valor truncado ou parcial na base; não confirmado |
| auxílio emergencial, artístico-cultural, prato cheio, bolsa alimentação, cartão escolar, mobilidade cidadã | nome do beneficiário/responsável, CPF **mascarado**, valores | `FN_MASCARA_NR_CPF` | mobilidade usa a mesma função para `documento` (que pode ser CNPJ; efeito ❓) |
| `/expulsao` | nome, matrícula, cargo, órgão, motivo, fundamento, processo, link do Diário Oficial | mascaramento (medida protetiva) | dado de publicação oficial |
| `/prestando-contas/conselheiros` e órgãos deliberativos | nome do conselheiro, representação, **valor de remuneração**, mandato | mascaramento (`NOME`) | — |
| Despesa (credor) | nome e código do credor; `codigoCredorMascarado` | mascaramento (credor/código); máscara no SQL para CPF | credores pessoa física incluídos |
| `/send-email` e pesquisa de satisfação | e-mail do cidadão (entrada) | validação de formato | a pesquisa grava `Portal.Registro_Pesquisa`; `RegistroContato` gravaria nome/e-mail, mas o formulário está desativado |

- ✅ Os filtros de busca por CPF recebem o valor em **Base64** (`cm`, `codigoCredorCodificado`). Isso é ofuscação do transporte, não proteção: qualquer cliente gera o Base64.
- ✅ Nenhuma rota exige autenticação (ver [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]); o controle depende só do que o SQL devolve.

## Inferências e limitações
- 🔶 Se `Servidor.Principal.[NR-CPF]` guardar o CPF completo, as rotas `/integracao/*` entregam o CPF de todos os servidores ativos a qualquer chamador que envie `x-client-id`. Isso precisa ser confirmado olhando a coluna na base (sem acesso aqui) ou perguntando ao time.
- 🔶 `FN_MASCARA_NR_CPF` pode mascarar só CPF (11 dígitos); em campos que também carregam CNPJ a máscara pode falhar ou expor o número.
- 🔶 O risco de injeção de SQL ([[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão]]) amplia o impacto: uma consulta adulterada poderia ler colunas de CPF cru que a API hoje oculta (`cpfComparacao`) e outras tabelas.
- ❓ O que a lei e as normas internas exigem publicar (por exemplo, remuneração nominal de servidores) não foi avaliado aqui; a nota só aponta onde a exposição é **maior que a máscara aparente** ou **inconsistente entre rotas**.

## Recomendações (não são fatos do código)
1. Decidir com o time se `/integracao/*` deve existir aberta; se sim, exigir credencial por consumidor e retornar apenas o mínimo (sem CPF em listagens por nome/órgão).
2. Padronizar: toda saída de CPF/NIS/documento passa por máscara no SQL ou no modelo (incluindo programas sociais, empresas punidas e Prospera DF), e todo serviço de pessoas passa pelo filtro de medida protetiva (incluindo militares cedidos).
3. Retirar os campos não usados dos modelos expostos (`cpf`, `mae`, `conjuge`, dados de aluno) para evitar vazamento futuro por mudança de SQL.
4. Registrar o formato da `FN_MASCARA_NR_CPF` e testar CPF e CNPJ.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Servidores-e-Remuneracao|Servidores e Remuneração]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Prestacao-de-Contas|Prestação de Contas]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Pendências e próximo passo
- Confirmar com o time (ou na base) o conteúdo de `[NR-CPF]`, `cpf_formatado` e `NR_CPF` de programas sociais, e se `/integracao/*` precisa mesmo devolver CPF.
