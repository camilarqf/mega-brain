---
type: integration
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
created: 2026-10-23
updated: 2026-10-23
consumer: SCI
provider: MinIO-CGDF
tags:
  - sci
  - integracao
  - s3
  - minio
  - denuncia
  - anexos
sources:
  - SCI.S3.Client
  - src/SCI.Api/Program.cs
  - src/SCI.Api/Controllers/DenunciaController.cs
  - src/SCI.IntegrationServices/EventConsumers/DemandaCriadaPorDenunciaConsumer.cs
  - Directory.Packages.props
  - .docker/Dockerfile
---
# Integração SCI → armazenamento S3 (anexos de denúncia)

Voltar: [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas do SCI Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `SCI` (`sci-backend`) | `MinIO-CGDF` 🔶 (armazenamento S3-compatível) | pacote `Minio` `4.0.7`, via `HttpClient` com Polly | leitura do objeto `denuncias/{IdentificadorExterno}/{nomeArquivo}` em um bucket configurado | saída (somente leitura) |

## Evidências
- Projeto novo `SCI.S3.Client` (na solução, copiado no `Dockerfile`): `IS3Client.DownloadByDenunciaIdAsync(denunciaId, fileName)`, `S3Client`, `S3ClientSettings`, `AddS3Client` (registrado em `Program.cs`).
- Usos: `GET /denuncia/{denunciaId}/download` (`DenunciaController`) e `DemandaCriadaPorDenunciaConsumer`.

## Informações confirmadas
- ✅ **Chave do objeto**: prefixo constante `denuncias/{0}/` (com o `IdentificadorExterno` da denúncia) + nome do arquivo; se o nome já vier com o prefixo, não duplica. Barra invertida vira `/`; segmentos `.` e `..` são rejeitados ("O nome do arquivo é inválido."); `denunciaId <= 0` é rejeitado.
- ✅ **Operação**: `StatObject` (para o `ContentType`) e `GetObject` copiado para memória; retorna `DownloadObjectResponse` {nome, tipo, bytes}. Não há escrita nem remoção pelo SCI. Existe o tipo `S3ObjectInfo` (listagem), mas a interface não expõe método de listagem.
- ✅ **Resiliência**: `S3ClientSettings` herda `ResilienceSettings` (timeout, retry, circuit breaker, mensagem de fallback); o `HttpLoggingHandler` novo (em `SCI.DefaultHttpClient`) registra as chamadas.
- ✅ **Configuração** (só nomes de chaves, seção `S3ClientSettings`): `Uri`, `AccessKey`, `SecretKey`, `BucketName`, `Timeout`, `UserAgent`, `RetryCount`, `RetryIntervalInSeconds`, `HandledEventsAllowedBeforeBreaking`, `DurationOfBreakInSeconds`, `FallbackMessage`. Valores não registrados; `.jenkins-pipelines/deployment.params.yml` ganhou mapeamentos de secrets (não lidos).
- ✅ **Correspondência**: o `PARTICIPA-DF` grava relatório e anexos no S3 (cliente `OuvDF.S3.Client`, mesmo pacote, segundo o cofre) e o evento `denuncia-registrada` leva os nomes ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Eventos]]).

## Falhas e dependências
- ✅ Falha do S3 no download manual propaga como erro da requisição; no consumidor, nenhum tratamento específico foi visto (interrompe a cópia dos anexos restantes; os já copiados não se repetem).
- ✅ `GET /denuncia/{denunciaId}/download` só exige usuário autenticado e, pelo código lido, **não verifica** se a denúncia pertence à unidade do usuário (diferente de `get-all`). Ver [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]].

## Inferências e limitações
- 🔶 Provedor `MinIO-CGDF`: inferido pelo pacote `Minio`, pelo nome do serviço de armazenamento na configuração de homologação e pelo cofre; endereço e bucket reais não registrados.
- ❓ Se os objetos são apagados pelo `PARTICIPA-DF` após aceite/recusa (informação do cofre) e como isso afeta um download tardio.
- Cobertura parcial: nenhum teste do cliente encontrado.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denúncia e Demanda]] · [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações do PARTICIPA-DF Backend]]

## Pendências e próximo passo
- Confirmar o ambiente/bucket com o time e a política de retenção dos objetos.
