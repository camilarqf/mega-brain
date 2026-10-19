---
type: module
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - modulo
  - documentos
  - assinatura
sources:
  - src/SCI.Domain/Organizacional/Entities/DocumentoAssinado.cs
  - src/SCI.Domain/Organizacional/Entities/Assinatura.cs
  - src/SCI.GED
  - src/SCI.Templates
  - src/SCI.HtmlToPdf.Client
  - src/SCI.Application/UseCases/AssinarMinuta
  - src/SCI.Application/UseCases/AssinarNotaTecnica
  - src/SCI.Api/Controllers/DocumentoController.cs
  - src/SCI.Api/Controllers/ArquivoController.cs
  - src/SCI.Infrastructure.Services/Storage
---
# SCI Backend — módulo Documentos e assinaturas (GED)

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar a geração, assinatura, invalidação, validação e armazenamento de documentos: nota técnica, minuta e relatório do PIP.

## Evidências
- `SCI.GED/UseCases/{GerarNotaTecnica,GerarMinutaPip,GerarRelatorioPip}`, `QrCodeHelper`, `SCI.Templates/Views/{NotaTecnica,Minuta,RelatorioPip}.cshtml`, `DocumentoAssinado`, `AssinarMinutaHandler`, `FileSystemStorageService`.

## Informações confirmadas
- ✅ **Tipos**: `NotaTecnica` (admissibilidade), `Minuta` e `Relatorio_Pip` (PIP).
- ✅ **Geração**: handlers do GED consultam o conteúdo (nota técnica, minuta, relatório) via `IQueryBus`, renderizam um template Razor (`HtmlTemplateEngine`) e convertem o HTML em PDF pelo `IHtmlToPdfApiClient` ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-HtmlToPdf|integração]]). O documento inclui o `HashVerificador` e um QR Code (PNG em base64, `QRCoder`) cujo destino vem de `GEDSettings.UrlValidacao`.
- ✅ **`DocumentoAssinado`**: `Processo`, `TipoDocumento`, conteúdo (`ConteudoDocumentoAssinado`), `HashVerificador`, `Assinaturas` (usuário, cargo, perfil, data) e `DocumentoInvalidado`. `AssinarMinutaHandler` verifica o conteúdo contra o hash (`VerificarConteudo`) antes de assinar.
- ✅ **Assinatura em cadeia**: por perfil, na ordem das revisões ativas — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Admissibilidade]] e [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]].
- ✅ **Invalidação**: `Invalidar(usuario, justificativa, id)` registra `DocumentoInvalido`; a minuta pode ser substituída (`SubstituirMinuta`) e a nota técnica invalidada (`POST /processo-admissibilidade/invalidar-nota-tecnica`).
- ✅ **Validação**: `POST /documento/validar` (autenticado) envia `ValidarDocumentoQueryRequest` ao `IQueryBus`; o conteúdo do request não foi lido.
- ✅ **Arquivos**: anexos de demanda, diligência, evidência e encaminhamento gravados por `IStorageService` (`FileSystemStorageService`: grava e lê em um diretório configurado); `GET /arquivo/download/{nomeArquivo}`.
- ✅ Documentos e estados são persistidos em `TB_DOCUMENTO_ASSINADO`, `TB_CONTEUDO_DOCUMENTO_ASSINADO`, `TB_ASSINATURA`, `TB_DOCUMENTO_INVALIDO`.

## Inferências e limitações
- 🔶 Como `POST /documento/validar` exige autenticação, uma validação pública por QR Code (sem login) não seria atendida por este endpoint; o destino de `UrlValidacao` não foi identificado.
- 🔶 O algoritmo do hash não foi lido.
- ⚠️ ✅ `ArquivoController.Download` concatena `nomeArquivo` ao diretório de armazenamento (`Path.Combine`) e o `DownloadRequestValidator` só exige valor não vazio (o helper `IsValidGuid` existe e não é usado). Impacto não testado — ver [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/SCI/Backend/06-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança]] · [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|Ciclo do PIP]]

## Pendências e próximo passo
- Ler `DownloadRequest` e o algoritmo do hash.
