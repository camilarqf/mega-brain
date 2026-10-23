---
type: analysis-log
system: SCI
component: Backend
repository: sci-backend
status: pendente
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
created: 2026-10-19
updated: 2026-10-23
tags:
  - sci
  - pendencias
---

# Pendências

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] · [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro de análise]]

## Perguntas ao time
| # | Pergunta | Origem |
|---|---|---|
| 1 | ~~Qual é o repositório do frontend do SCI~~ Respondida em 2026-10-19: `sci-frontend` (ver [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]). Falta a expansão da sigla SCI. | Lote 0 |
| 2 | `src/SCI.HtmlToPdfClient` (fora da solução) duplica `SCI.HtmlToPdf.Client`; pode ser removido? Qual o papel de `Legacy/`? | Lote 0 |
| 3 | ~~Denúncia aceita → demanda: não há vínculo no backend~~ **Resolvida em 2026-10-23** (`29989114`): o aceite cria a demanda `CR` e copia os anexos do S3. Texto original: usuário não sabia se a funcionalidade terminou (2026-10-19). | Lote 4 |
| 4 | Expansão de JAD, DODF, SIGRH, SIGGO e das siglas de recomendação (ROO, SPA, IPF, PAD, REF, DMC, TAC, PCT, RCG). | Lote 1 |
| 5 | Significado de "matriz" nas diligências do PIP. | Lote 4 |
| 6 | Como são cadastradas unidades novas e usuários em produção (não há endpoint de criação de unidade)? | Lote 4 |
| 7 | ~~`Support.GenerateDatabase` em homologação/produção~~ Respondida em 2026-10-19: só funciona em dev e local. Falta confirmar como isso é imposto (flag por ambiente). | Lote 2 |
| 8 | O `PARTICIPA-DF` usa `security/auth` para a autenticação chamada pelo SCI? Há reentrega/DLQ no consumidor de `denuncia-registrada`? | Lote 5 |
| 9 | Quem é o dono do BCadastro e do serviço HtmlToPdf? (HtmlToPdf: mesmo serviço para SCI, PARTICIPA-DF e SICI, informado; falta só o dono.) | Lote 5 |
| 10 | Validação pública por QR Code: qual a URL de `GEDSettings.UrlValidacao` e qual endpoint atende sem login? | Lote 4 |

## Perguntas abertas no lote 7 (2026-10-23)
| # | Pergunta | Origem |
|---|---|---|
| 11 | Por que aceitar/recusar denúncia passou de AutoridadeCorrecional para ApoioCorrecional? | Lote 7 |
| 12 | Falha na criação da demanda ou na cópia dos anexos após o aceite: há compensação/reprocessamento? Qual a ordem frente à remoção dos objetos pelo `PARTICIPA-DF`? | Lote 7 |
| 13 | `GET /denuncia/{id}/download` deveria checar a unidade? Recusar denúncia já aceita é permitido? | Lote 7 |
| 14 | Como os ambientes existentes migram o esquema (`TB_STATUS_DENUNCIA` → `TB_STATUS_ANALISE_DENUNCIA`, novas tabelas)? | Lote 7 |
| 15 | Os projetos de teste `SCI.Application.Tests` e `SCI.Api.Tests` (sem `.csproj`) serão adicionados à solução? | Lote 7 |

## Riscos para tratar fora do cofre
Itens 1 a 4 (e o 17) de [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]] (bypass, `generate-database`, `DELETE /unidade`, segredos versionados e rotação).

## Próximo passo exato
Responder as perguntas 11 a 15; lote 8 opcional (ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro de análise]]).
