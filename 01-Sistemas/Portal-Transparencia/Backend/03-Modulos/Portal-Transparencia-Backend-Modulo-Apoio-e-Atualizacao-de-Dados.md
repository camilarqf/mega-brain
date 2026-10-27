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
  - apoio
  - atualizacao-de-dados
sources:
  - src/main/java/br/gov/df/transparencia/api/dataAtualizacao
  - src/main/java/br/gov/df/transparencia/servico/dataAtualizacao/DataAtualizacaoService.java
  - src/main/java/br/gov/df/transparencia/api/comum
  - src/main/java/br/gov/df/transparencia/api/v2/pesquisaSatisfacao
  - src/main/java/br/gov/df/transparencia/api/v2/acessoInformacao
  - src/main/java/br/gov/df/transparencia/api/v2/imagens
  - src/main/java/br/gov/df/transparencia/servico/pesquisa/RegistroPesquisaService.java
  - src/main/java/br/gov/df/transparencia/servico/comum
  - src/main/resources/sql/data-atualizacao
  - src/main/resources/sql/comum
  - src/main/resources/sql/enquete
---
# Módulo Apoio e atualização de dados

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seções Comum, Data de atualização e API v2)

## Objetivo
Documentar as funções transversais: "data da última atualização" de cada consulta, arquivos e textos, pesquisa de satisfação, imagens, órgãos da LAI, e-mail, analytics e utilitários.

## Evidências
Leitura de `DataAtualizacaoService`/`Controller`, de `selectDataUltimaAtualizacaoCarga.sql` e de um SQL de `data-atualizacao/despesas`, de `RegistroPesquisaService` e dos controllers de pesquisa (v2), LAI, texto explicativo, `FormularioContatoController`, `ArquivoService`; lista de métodos dos serviços.

## Informações confirmadas
### Datas de atualização
- ✅ `DataAtualizacaoController` (`/dataAtualizacao`, **62 rotas GET**, cada uma devolvendo uma `Date`) e `DataAtualizacaoService` (uma busca por consulta: painéis e consultas de receita, despesa, servidores, remuneração, licitações e contratos, convênios, patrimônio, orçamento etc.). SQL em `resources/sql/data-atualizacao/<área>` (56 arquivos).
- ✅ A data vem de `Carga.Controle`: `isnull(con_fimcarga, con_iniciocarga)` do esquema da área (`despesa`, `remuneracao`, `servidor`…) cujo `con_status` esteja entre `atualizado`, `realizado`, `sem alter.` (e, na consulta de remuneração/servidores, também `sucesso`). O modelo `CargaAtualizacao` usa chaves como `REMUNERACAO_SERVIDORES` e `SERVIDORES`.
- 🔶 A consulta de despesa lida (`selectDataAtualizacaoConsultaDinamicaDespesas.sql`... e a pasta `despesas`) usa `select top 1 ...` **sem `order by`**; o SQL Server não garante qual linha volta. Só um arquivo foi lido; os demais não foram verificados.

### Arquivos, textos e imagens
- ✅ `ArquivoController` (`/arquivos`, 3): lista arquivos por categoria e devolve a **URL do último arquivo** de uma categoria (e de categoria + exercício); `GET /v2/imagens/imagens-slideshow` devolve URLs (`Portal.Imagem_Pagina_Portal`); `GET /download/arquivos/{nome}` serve arquivos do diretório `/home/PortalFiles/Arquivos/`.
- ✅ `TextosConsultasController` (`/textos-consultas`) e `TextoExplicativoController` (`/texto-explicativo/beneficiario/programa-social`, via `PrestandoContasService`) servem textos explicativos da base.
- ✅ `GET /v2/orgaos-lai`: lista de órgãos da LAI (`OrgaoLAIDTO`).

### Pesquisa de satisfação
- ✅ `POST /v2/pesquisa-satisfacao` (JSON `PesquisaSatisfacao`) grava em `Portal.Registro_Pesquisa` (JPA, via `PersistenceHelper`); falha de persistência vira `NegocioException("Campo da pesquisa não pode ser nulo!")` → `400` com `{"erros":[...]}`.
- ✅ Níveis de satisfação (`SatisfacaoEnum`): Muito Satisfeito, Satisfeito, Indiferente, Insatisfeito e Muito Insatisfeito; ocupações (`OcupacaoEnum`): Servidor, Jornalista, Estudante, Advogado, Empresário, Outros.
- ✅ **Regra**: se a satisfação é *Insatisfeito* ou *Muito Insatisfeito*, o serviço monta e envia um e-mail com o "texto de desagrado" pelo `SendMailService`, com nome do remetente fixo "Portal da Transparência" e assunto "Pesquisa de Satisfação - Detalhamento". Remetente e destinatário são os **endereços institucionais padrão** definidos como valor inicial em `SendMailRequest` (`emailCidadao` e `emailDestinatario`; endereços não reproduzidos aqui).
- 🔶 Código redundante: `setEmailCidadao(getEmailCidadao())` e `setEmailDestinatario(getEmailDestinatario())` atribuem o próprio valor (o padrão da classe); não há efeito. O resultado do envio (`ResponseEntity`) é ignorado, então falha no e-mail não afeta a resposta da pesquisa. O texto de desagrado entra no corpo sem escape de HTML.
- ✅ Resultados agregados em `GET /pesquisa/grafico/*` (4 rotas: ocupação, faixa etária, nível de satisfação, total de respostas), com SQL em `sql/enquete`.
- ✅ O controller antigo `comum/PesquisaSatisfacaoController` e o `FormularioContatoController` (`POST /contato/registro`) estão **comentados**: o formulário de contato não tem rota ativa, embora a entidade `RegistroContato` e `RegistroContatoPersistence` existam.
- ✅ `EnqueteService` é um esqueleto (retorna `null`).

### Outros utilitários
- ✅ `GET /send-email`, `/cache-expire/*`, `/analytics/*`, `/integracao/*` e `/healthcheck`: ver [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]], [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] e [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]].
- ✅ SQL de gráficos gerais em `sql/comum` (`selectGraficoDespesasXReceitas`, `selectEvolucaoGrupoDespesa`).

## Inferências e limitações
- 🔶 `GET /pesquisa/grafico` é consumido por um painel de resultados; o consumidor (frontend) não foi identificado.
- ❓ O processo que preenche `Carga.Controle` é externo ao repositório.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Orçamento e documentos]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Receita|Receita]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]]

## Pendências e próximo passo
- Verificar os demais SQL de `data-atualizacao` quanto a `top 1` sem `order by`; confirmar se o e-mail de insatisfação chega à caixa institucional esperada.
