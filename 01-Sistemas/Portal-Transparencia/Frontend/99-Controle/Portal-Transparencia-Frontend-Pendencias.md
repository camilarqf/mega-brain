---
type: analysis-log
aliases:
  - "Pendências"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: pendente
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-27
---

# Pendências

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]] · [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Registro-de-Analise|Registro de análise]]

## Perguntas ao time
| # | Pergunta | Origem |
|---|---|---|
| 1 | Qual é o perfil usado em produção e como são feitos o *build* e a implantação (o `Jenkinsfile.prod` foi removido em 2026-10-14)? Como o proxy mapeia `/api`, `/api-super-busca` e `/arquivos/*`? | Lote 1 |
| 2 | Quem é o dono do serviço `apisuperbusca` (índice de busca) e onde está o repositório? Deve ser cadastrado como sistema? | Lote 2 |
| 3 | Qual sistema é o "gerenciador" (`apiGerenciador`), usado em Quadros Temáticos e Setor Desejado? É o mesmo citado nas pendências do Backend (#18)? 🔶 Pode ser o `Gerenciador-Portal` ([[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Index|índice]]), informado pelo usuário como sistema à parte (2026-10-27); a URL `apiGerenciador` não foi comparada com o serviço dele. | Lote 2 |
| 4 | Os *buckets* `portal-imagens`, `portal-arquivos` e `portal-dados-abertos` são do `MinIO-CGDF`? A refatoração `feature/refatoracao-acesso-minio` pretende que o frontend use `/storage/url` do Backend em vez das constantes `caminho*`? | Lote 2 |
| 5 | `src/app/config.js` deve ficar versionado (contém endereços de infraestrutura)? Os endereços internos precisam ser trocados por caminhos relativos? | Lote 1 e 5 |
| 6 | As chamadas sem rota no Backend (`/despesa/porAcao/empenhado`, `/receita/multas/total`, `/servidor/listarDataReferenciaPorOutrosOrcamento`, `/prestando-contas/detalhamento-conselheiro`, `/licitacoes-contratos/{anos,licitacao/orgao,licitacao/situacao,grafico/*}`) estão em telas ativas? | Lote 2 |
| 7 | O formulário "Fale conosco" (`POST /contato/registro`) deve funcionar? O controller do Backend está comentado (Backend #11). | Lote 2 |
| 8 | Aceita-se CPF/CNPJ no caminho da URL na super busca (fica em *logs*)? Há política de retenção desses logs? | Lote 4 e 5 |
| 9 | Podem ser removidos `/old`, `todo-widget`, `upload.controller.js`, rotas comentadas (`restos-a-pagar`, `execucao-emendas`, `acao`, `servidores/tabela`) e `bolsa-alimentacao`? | Lote 1 e 4 |
| 10 | As telas de programas da pandemia (renda emergencial, prato cheio, auxílio União, COVID-19) continuam vigentes? | Lote 3 e 4 |
| 11 | Os textos de `sobre`, `faq`, `legislacao` e `linksuteis` têm dono/responsável de conteúdo? | Lote 4 |
| 12 | O Google Analytics (`gtag.js`, ID omitido) e os endpoints `/analytics/*` do Backend (Universal Analytics, Backend #7) ainda são usados? | Lote 2 |

## Lacunas de análise
- Templates HTML, SCSS e lógica interna de cada controller foram lidos por amostragem (cobertura `parcial`).
- Parâmetros e DTOs das chamadas não foram comparados campo a campo com o Backend.
- Testes e *build* não foram executados.
- Nenhuma nota de fluxo ou de regra de negócio do frontend foi escrita (sem evidência de regra além de filtros e formatação).

## Próximo passo exato
1. Responder as perguntas acima (principalmente #3, #4 e #6) e registrar a decisão.
2. Rodar `gulp test` em ambiente compatível (Node 6) e anotar a cobertura em [[01-Sistemas/Portal-Transparencia/Frontend/09-Qualidade/Portal-Transparencia-Frontend-Testes-e-Cobertura|Testes e cobertura]].
3. Aprofundar por módulo (parâmetros/DTO × Backend) começando por Despesas e Prestando Contas.
4. Atualizar com a skill `atualizar-documentacao` quando `git diff dca3e933..HEAD` mostrar mudanças.
