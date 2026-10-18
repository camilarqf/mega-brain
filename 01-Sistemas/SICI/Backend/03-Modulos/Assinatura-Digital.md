---
type: module
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - modulo
  - assinatura
  - pdf
  - qrcode
  - hmac
sources:
  - api/assinatura/AssinaturaController.java
  - application/service/assinatura/AssinaturaServiceImpl.java
  - application/service/assinatura/AssinaturaDocumentoServiceImpl.java
  - application/service/assinatura/NumeracaoServiceImpl.java
  - application/usecase/assinatura/AssinarDocumento.java
  - application/usecase/assinatura/AssinarOrdemServico.java
  - application/usecase/assinatura/AssinarOrdemServicoGenerica.java
  - application/utils/VerifyCode.java
  - application/utils/HashUtils.java
  - application/utils/ImagemUtils.java
  - application/utils/QRCodeGenerator.java
  - application/service/comum/AssinaturaProperties.java
  - infrastructure/external/config/VerifyCodeProperties.java
  - domain/model/Assinatura.java
  - domain/model/Documento.java
  - domain/model/DocumentoAssinado.java
  - infrastructure/persistence/adapter/NumeracaoRepositoryAdapter.java
  - src/main/resources/templates/*.html
---

# Assinatura eletrônica de OS

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Fluxo: [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]], [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]], [[01-Sistemas/SICI/Backend/07-Integracoes/Integracoes-Externas|Integracoes-Externas]], [[01-Sistemas/SICI/Backend/02-Dominio/Banco-e-Migrations|Banco-e-Migrations]]

> ✅ É uma **assinatura eletrônica simples** controlada pela aplicação: o login do usuário autenticado é comparado com o SUBCI titular ou o substituto vigente. Não há certificado digital, ICP-Brasil nem assinatura criptográfica do PDF.

## Endpoints — `/assinaturas` ✅
Fonte: `api/assinatura/AssinaturaController.java`. Nenhum endpoint tem `@PreAuthorize`; a autorização para assinar é feita dentro do use case.

| Método | Rota | Função |
|---|---|---|
| POST | `/assinar-os/{idOrdemServico}` | assina OS de ação de controle (body opcional `AssinarDocumentoRequest`) |
| POST | `/assinar-os-generica/{idOrdemServicoGenerica}` | assina OS genérica |
| GET | `/{idDocumentoAssinado}/download` | baixa PDF assinado + headers `X-Document-Hash-SHA256`, `X-Document-Verify-Code`, `X-Document-Signed-At`, `ETag` |
| GET | `/{idDocumentoAssinado}/download-generica` | idem, filtrando tipo de documento = OS genérica |
| GET | `/validacao?codigo=` | valida pelo código verificador; retorna `valido`, `mensagem`, `responsavel`, `assinadoEm` |

## Quem pode assinar ✅
`AssinarOrdemServico.resolverAssinanteAutorizado` (igual na genérica):
1. Busca o **SUBCI titular ativo** (`subciRepositoryPort.buscarTitularAtivo`); se não houver, `IllegalStateException`.
2. Se o login autenticado (`Authentication.getName()`, que é o `preferred_username` do JWT) for igual ao `login` do titular, ignorando maiúsculas e espaços, assina como titular.
3. Senão, se houver **substituto vigente na data de hoje** (`subciSubstitutoRepositoryPort.buscarVigente`) com o mesmo login, assina como substituto (`assinaturaSubstituto = true`, aparece no PDF).
4. Senão, `AccessDeniedException`.

O perfil gravado na assinatura é **o primeiro perfil** da lista do auditor (`AssinaturaDocumentoServiceImpl.obterPerfilAssinatura` → `getPerfis().get(0)`), não necessariamente o perfil SUBCI.

## Artefatos gerados na assinatura ✅
| Artefato | Como é gerado | Onde fica |
|---|---|---|
| **Número oficial** | `String.format("%06d/%d - %s/CGDF", seq, ano, siglaUAI)`; `seq = max(numSequencial do ano) + 1`; `ano = LocalDate.now()`; UAI = **UAI do assinante** | `TB_NUMERACAO_ORDEM_SERVICO_ASSINADA` |
| **Código verificador** | OS: `HMAC-SHA256(secret, idOS)`; OS genérica: `HMAC-SHA256(secret, "OSG:" + id)`; hex maiúsculo truncado em 32 caracteres (128 bits) — `VerifyCode.forOS` / `forDocumento` | `TB_DOCUMENTO.TX_HASH_VERIFICADOR` |
| **QR Code** | ZXing, PNG em Base64, tamanho `assinatura.qr-size` (180 px), conteúdo `assinatura.url.validacao + "?c=" + código` | embutido no PDF |
| **PDF** | template Thymeleaf → HTML → serviço externo de PDF (`PdfService`) | `TB_DOCUMENTO.TX_CONTEUDO` (`@Lob`) |
| **Hash do conteúdo** | SHA-256 dos bytes do PDF (`Documento`, `HashUtils.sha256`) | `TB_DOCUMENTO.TX_HASH` |
| **Assinatura** | `Assinatura.criar` com auditor, perfil e data; hash = SHA-256 de `idAuditor|idPerfil|data` | `TB_DOCUMENTO_ASSINADO` → `TB_ASSINATURA` |

Segredo do HMAC: propriedade `integra.verify.secret`, injetada por `VerifyCodeProperties` (`@PostConstruct` → `VerifyCode.setSecret`, campo **estático**).

## Templates de PDF ✅
`src/main/resources/templates/` — 8 arquivos (um por modelo + `erroOrdemServico.html`). Variáveis principais: `numeroFormatado`, `numeroFormatadoOriginal` (número da abertura), `acaoControle`, `ordemServico`, `fases`, `auditores`, `coordenador`, `subciNome`, `matricula`, `assinaturaSubstituto`, `mostrarAssinatura`, `codigoVerificador`, `urlValidacao`, `qrBase64`, `logoBase64`, `signIconBase64`, `dados` (prorrogação/substituição/cancelamento). Imagens em `static/imagens`.
- ✅ Todos usam `th:text` (com escape) e nenhum usa `th:utext`. Isso reduz o risco de injeção de HTML vinda de campos livres.
- ✅ O mesmo template serve para a **minuta** (`mostrarAssinatura = false`, via `GET /os-acao-controle/gerar-pdf`) e para a versão assinada.

## Validação ✅
`AssinaturaServiceImpl.validarPorCodigo`:
1. Busca o documento por `TX_HASH_VERIFICADOR = codigo`; se não achar, `IllegalArgumentException`.
2. Pega a última assinatura do documento.
3. `valido = documento.hashVerificador.equalsIgnoreCase(codigo)`.

⚠️ O passo 3 é **tautológico**: o documento foi encontrado justamente por esse código, então `valido` é sempre `true` quando há resposta. A validação **não**:
- recalcula o SHA-256 do PDF (`Documento.hashConfere()` existe, mas não é chamado);
- verifica `Assinatura.validarHash()`;
- recalcula o HMAC;
- informa se a OS foi **cancelada** depois de assinada.

🔶 O comentário em `AssinaturaProperties` indica que a URL de validação aponta para uma página do frontend. O endpoint de backend `/assinaturas/validacao` **exige autenticação** (não está no `permitAll`). Se o QR Code é lido por terceiros, a validação pública não funciona só com este backend. Ver [[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendencias]].

## Pontos de atenção
| # | Achado | Evidência | Status |
|---|---|---|---|
| 1 | Sequencial **por ano global**, não por UAI; `max+1` sem lock nem unique → **números duplicados possíveis** em assinaturas concorrentes | `NumeracaoRepositoryAdapter.buscarMaiorSequencialPorUaiEAno` ignora `idUai`; V44 sem unique | ✅ / 🔶 (concorrência) |
| 2 | A sigla do número vem da **UAI do assinante (SUBCI)**, não da UAI da ação de controle | `AssinarOrdemServico`: `unidade = assinante.getUnidadeAuditoriaInterna()` | ✅ (intenção a confirmar) |
| 3 | Status ENVIADA só é verificado **no fim**, em `osDomain.alterarStatusOs(ASSINADA)`, depois de gerar o PDF no serviço externo e gravar documento, assinatura e numeração (o rollback desfaz). Custo e chamada externa desnecessários. | ordem das instruções em `AssinarOrdemServico.executar` (`@Transactional(rollbackFor = Exception.class)`) | ✅ |
| 4 | Validação sempre `valido = true`; integridade do PDF não é verificada | `AssinaturaServiceImpl.validarPorCodigo` | ✅ |
| 5 | Código verificador **determinístico** (depende só do id): previsível para quem conhece o segredo; um vazamento do segredo compromete todos os códigos. O segredo de local é um valor público (SHA-256 de string vazia). | `VerifyCode` | ✅ |
| 6 | Download sem restrição de perfil e por id sequencial: qualquer usuário autenticado baixa qualquer PDF assinado | `AssinaturaController.download*` | ✅ |
| 7 | Hash da `Assinatura` sem segredo nem conteúdo, reproduzível | `Assinatura.calcularHashAssinatura` | ✅ |
| 8 | Perfil gravado = primeiro perfil do auditor | `obterPerfilAssinatura` | ✅ |
| 9 | `NumeracaoServiceImpl.gerarPosAssinatura` (usa a UAI do **coordenador** e trata `DataIntegrityViolationException`) **não é chamado** em lugar nenhum: código morto e regra divergente | grep sem chamadores | ✅ |
| 10 | Montagem do PDF **duplicada**: `AssinarOrdemServico.gerarPdfDaOS` e `OrdemServicoController.gerarRelatorioPdf` repetem a seleção de template e variáveis | ambos os arquivos | ✅ |
| 11 | Minuta de DESIGNACAO/EXCLUSAO/SUBSTITUICAO/CANCELAMENTO lê o número da abertura; sem abertura assinada → provável `NullPointerException` | `gerarRelatorioPdf` → `dados.getOsOriginal().getNumeroOrdemServicoResponse().getNumeroFormatado()` | 🔶 |
| 12 | `VerifyCode` guarda o segredo em campo estático mutável; se o bean não inicializar, `SECRET` é `null` → NPE na assinatura | `VerifyCode`, `VerifyCodeProperties` | ✅ |
