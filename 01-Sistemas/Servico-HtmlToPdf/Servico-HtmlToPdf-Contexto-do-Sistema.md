---
type: system
system: Servico-HtmlToPdf
status: confirmado
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - html-to-pdf
  - contexto
sources:
  - README.md
  - app/pdf/routes.py
  - app/pdf/service.py
---
# Serviço HtmlToPdf — contexto do sistema

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico-HtmlToPdf-Index|Índice do sistema]]

## Objetivo
Converter um trecho de HTML recebido por HTTP em um arquivo PDF (A4), sem estado e sem persistência.

## Evidências
- `README.md`: "Serviço HTTP que converte um trecho de HTML em PDF usando WeasyPrint".
- `app/pdf/routes.py` (`html_to_pdf`) e `app/pdf/service.py` (`generate_pdf`).
- Nome da aplicação no pipeline: `HTML TO PDF` (`.jenkins-pipelines/deployment.params.yml`).

## Informações confirmadas
- ✅ Um único caso de uso: `POST /html-to-pdf/generate` com `{"HtmlString": "..."}` devolve `application/pdf`. Ver [[01-Sistemas/Servico-HtmlToPdf/Servico/06-API/Servico-HtmlToPdf-Servico-Catalogo-de-Endpoints|Catálogo de endpoints]].
- ✅ Não há banco, fila, autenticação nem chamadas a outros sistemas no código.
- ✅ Consumidores (conforme o vault, não este repositório): backends de `PARTICIPA-DF`, `SCI` e `SICI`, via [[Mapa-de-Integracoes|Mapa de integrações]].

## Inferências e limitações
- 🔶 O CSS base contém seletores específicos (`.logo-ouv`, `.card-left`), o que sugere origem no uso pelo PARTICIPA-DF (Ouvidoria); não há evidência direta no código.
- ✅ Dono: a CGDF (informado pelo usuário em 2026-10-19; o código não registra o dono).
- ❓ SLA e URLs por ambiente não identificados.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Integrações (consumidores)]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Servico-HtmlToPdf/Servico/99-Controle/Servico-HtmlToPdf-Servico-Pendencias|Pendências]].
