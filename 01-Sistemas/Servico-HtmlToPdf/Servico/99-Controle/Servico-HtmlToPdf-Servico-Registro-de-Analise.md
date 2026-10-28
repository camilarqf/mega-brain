---
type: analysis-log
aliases:
  - "Serviço HtmlToPdf — registro de análise"
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-28
commit_data: 2026-09-23
branch: master
tags:
  - geracao-pdf
---
# Serviço HtmlToPdf — registro de análise

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Controlar os lotes da análise de `cgdf-html-to-pdf`.

## Evidências
- `git rev-parse HEAD` = `1393a68d633ed2ecc7c2c6a287a2631389d86ade`, branch `master`, commit de 2026-09-23.
- Árvore de trabalho com `cgdf-html-to-pdf.iml` modificado e `locustfile.py`/`requirements-dev.txt` não versionados (fora do escopo).
- Análise por leitura estática; testes e a aplicação não foram executados.

## Informações confirmadas
| Lote | Escopo | Notas | Estado |
|---|---|---|---|
| 0 | Identificação e estrutura | [[01-Sistemas/Servico-HtmlToPdf/Servico-HtmlToPdf-Index|Index]], [[01-Sistemas/Servico-HtmlToPdf/Servico-HtmlToPdf-Contexto-do-Sistema|Contexto]], [[01-Sistemas/Servico-HtmlToPdf/Servico-HtmlToPdf-Repositorios|Repositórios]], [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]] | concluído |
| 1 | Stack, arquitetura, API, módulo, fluxo | [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Stack-e-Dependencias|Stack]], [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Arquitetura|Arquitetura]], [[01-Sistemas/Servico-HtmlToPdf/Servico/06-API/Servico-HtmlToPdf-Servico-Catalogo-de-Endpoints|Endpoints]], [[01-Sistemas/Servico-HtmlToPdf/Servico/03-Modulos/Servico-HtmlToPdf-Servico-Geracao-de-PDF|Módulo]], [[01-Sistemas/Servico-HtmlToPdf/Servico/05-Fluxos/Servico-HtmlToPdf-Servico-Fluxo-Geracao-de-PDF|Fluxo]] | concluído |
| 2 | Observabilidade, deploy, testes, segurança, débitos | [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Observabilidade-e-Logs|Observabilidade]], [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Deploy-e-Ambientes|Deploy]], [[01-Sistemas/Servico-HtmlToPdf/Servico/09-Qualidade/Servico-HtmlToPdf-Servico-Testes-e-Cobertura|Testes]], [[01-Sistemas/Servico-HtmlToPdf/Servico/08-Seguranca/Servico-HtmlToPdf-Servico-Seguranca|Segurança]], [[01-Sistemas/Servico-HtmlToPdf/Servico/09-Qualidade/Servico-HtmlToPdf-Servico-Debitos-Tecnicos|Débitos]] | concluído |
| 3 | Integrações e catálogo | [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Integrações]]; edições no `Catalogo-de-Sistemas`, no `Mapa-de-Integracoes` e links de volta nas 3 notas dos consumidores | concluído |

- Decisão de catálogo (aprovada pelo usuário em 2026-10-19): o ID `Servico-HtmlToPdf` passa de serviço externo a sistema, sem renomear os `provider` existentes.

## Inferências e limitações
- Não foram criadas notas de domínio, persistência ou regras de negócio: o código não tem entidades, banco nem regras além da validação da entrada.
- `Mapa-de-Integracoes`: correspondência com os consumidores confirmada pelo usuário em 2026-10-19.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/99-Controle/Servico-HtmlToPdf-Servico-Pendencias|Pendências]]

## Pendências e próximo passo
- 2026-10-19: o usuário confirmou que este repositório é o serviço chamado por PARTICIPA-DF, SCI e SICI; linhas do mapa promovidas a ✅.
- **Próximo passo exato:** dono registrado (CGDF); informar SLA e URLs por ambiente e resolver as pendências restantes (2 a 7). Se `HEAD` mudar, comparar `git diff --name-only 1393a68..HEAD` com os `sources` e acionar `atualizar-documentacao`.

## Histórico de estrutura
- 2026-10-27: pastas reorganizadas conforme a seção 1 do `BRAIN-RULES.md` (numeração fixa; melhorias do cofre, lote 3).
- 2026-10-28: frontmatter padronizado: título legível em `aliases` e tags reduzidas ao vocabulário controlado da seção 4 do `BRAIN-RULES.md` (melhorias do cofre, lote 5).
