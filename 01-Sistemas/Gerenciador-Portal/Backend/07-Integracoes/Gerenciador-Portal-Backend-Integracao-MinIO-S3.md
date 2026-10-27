---
type: integration
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
consumer: Gerenciador-Portal
provider: MinIO-CGDF
tags:
  - gerenciador-portal
  - integracao
  - s3
  - minio
sources:
  - pom.xml
  - src/main/java/br/gov/df/cgdf/gerenciador/config/S3Config.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/StorageService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/comum/Healthcheck.java
  - src/main/resources/application-homolog.properties
  - src/main/resources/application-prod.properties
  - .jenkins-pipelines/deployment.params.yml
---
# Integração Gerenciador-Portal → armazenamento S3 (MinIO)

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integrações externas do Gerenciador-Portal Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Gerenciador-Portal` (`gerenciador-portal-backend`) | `MinIO-CGDF` 🔶 | AWS SDK v2 `S3Client` (2.17.290, `url-connection-client`), path-style, região `us-east-1` | `PutObject` e `HeadBucket` nos buckets `portal-arquivos` e `portal-imagens` | saída (escrita e verificação de saúde) |

## Evidências
`S3Config` (bean `S3Client`), `StorageService.upload`, `Healthcheck` (indicador `minio`), propriedades `storage.*`, secrets do pipeline.

## Informações confirmadas
- ✅ **Endpoint**: `storage.endpoint` (`http://minio-sandbox:9000` em `homolog`; `http://minio-production:9000` em `prod`; em `dev` um endereço IP fixo, omitido). Todos usam **HTTP sem TLS**.
- ✅ **Credenciais**: `storage.access-key`/`storage.secret-key` (de `${STORAGE_ACCESS_KEY}`/`${STORAGE_SECRET_KEY}`) ou, se vazias, as variáveis de ambiente homônimas; sem nenhuma, `S3Config` lança `IllegalStateException("Credenciais do MinIO não encontradas.")` e a aplicação não sobe. No pipeline os secrets são `…-minio-storage-access-key` e `…-minio-root-pwd` (a chave secreta é a **senha root** do MinIO, por nome do secret).
- ✅ **Escrita**: `StorageService.upload(bucket, arquivo, chave)` faz `PutObject` com `Content-Type` do arquivo e o fluxo de entrada; falha vira `StorageUploadException`. Usado por `ArquivoService.salvar`, `ImagemService.salvar` e `salvarImagemBackground`.
- ✅ **Chaves de objeto**: arquivos `<uuid><ext>`; imagens `slide_`/`painel_`/`background_` + `<uuid><ext>`.
- ✅ **Saúde**: `Healthcheck` faz `HeadBucket` nos dois buckets e publica `UP`/`DOWN` no `/healthcheck` (detalhes: nomes dos buckets, status HTTP e mensagem).
- ✅ **Não há** leitura (`GetObject`), listagem, exclusão nem URL assinada no código: a exclusão de arquivo/imagem não remove o objeto.
- ✅ `storage.public-url` existe só em `homolog` e **não é lida** pelo código.

## Falhas e dependências
- ✅ Se o MinIO estiver fora, `/healthcheck` fica `DOWN` (o `HEALTHCHECK` do Docker reinicia o contêiner após 3 falhas) e os uploads falham com `400`.
- ✅ Upload antes do `INSERT`: sem compensação (objeto órfão se o banco falhar).
- ✅ Logs `DEBUG` do AWS SDK/Apache HTTP em `homolog` (`logging.level.software.amazon.awssdk*`) podem expor cabeçalhos e requisições nos logs.

## Inferências e limitações
- 🔶 Provedor: a instância do `MinIO-CGDF` (`minio-infra`); os nomes `minio-sandbox`/`minio-production` não constam como tal no cofre — correspondência por nome e pela descrição da integração do Portal ([[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Portal]]).
- 🔶 Os mesmos buckets (`portal-arquivos`, `portal-imagens`) são lidos pelo Portal-Transparencia (via `/storage/url`); neste repositório só há a escrita.
- ❓ Política de bucket (público/privado), versionamento e ciclo de vida.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/MinIO-CGDF/Infra/MinIO-CGDF-Infra-Index|MinIO-CGDF]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-S3-Anexos-de-Denuncia|Integração SCI → S3]] (outro consumidor) · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Arquivos]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Imagens-do-Portal|Imagens]]

## Pendências e próximo passo
- Confirmar a instância do MinIO e quem apaga/limpa objetos antigos.
