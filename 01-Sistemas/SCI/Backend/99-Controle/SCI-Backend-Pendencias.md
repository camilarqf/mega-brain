---
type: analysis-log
system: SCI
component: Backend
repository: sci-backend
status: pendente
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
created: 2026-10-19
updated: 2026-10-19
tags:
  - sci
  - pendencias
---

# Pendências

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] · [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro de análise]]

## Perguntas ao time
| # | Pergunta | Origem |
|---|---|---|
| 1 | Qual é o repositório do frontend do SCI e a expansão da sigla SCI? | Lote 0 |
| 2 | `src/SCI.HtmlToPdfClient` (fora da solução) duplica `SCI.HtmlToPdf.Client`; pode ser removido? Qual o papel de `Legacy/`? | Lote 0 |
| 3 | Denúncia aceita → demanda: não há vínculo no backend. Usuário não sabe se a funcionalidade terminou (2026-10-19). Confirmar se está prevista. | Lote 4 |
| 4 | Expansão de JAD, DODF, SIGRH, SIGGO e das siglas de recomendação (ROO, SPA, IPF, PAD, REF, DMC, TAC, PCT, RCG). | Lote 1 |
| 5 | Significado de "matriz" nas diligências do PIP. | Lote 4 |
| 6 | Como são cadastradas unidades novas e usuários em produção (não há endpoint de criação de unidade)? | Lote 4 |
| 7 | ~~`Support.GenerateDatabase` em homologação/produção~~ Respondida em 2026-10-19: só funciona em dev e local. Falta confirmar como isso é imposto (flag por ambiente). | Lote 2 |
| 8 | O `PARTICIPA-DF` usa `security/auth` para a autenticação chamada pelo SCI? Há reentrega/DLQ no consumidor de `denuncia-registrada`? | Lote 5 |
| 9 | Quem é o dono do BCadastro e do serviço HtmlToPdf? (HtmlToPdf: mesmo serviço para SCI, PARTICIPA-DF e SICI, informado; falta só o dono.) | Lote 5 |
| 10 | Validação pública por QR Code: qual a URL de `GEDSettings.UrlValidacao` e qual endpoint atende sem login? | Lote 4 |

## Riscos para tratar fora do cofre
Itens 1 a 4 de [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]] (bypass, `generate-database`, `DELETE /unidade`, segredos versionados e rotação).

## Próximo passo exato
Lote 7 opcional (ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro de análise]]).
