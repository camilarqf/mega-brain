---
type: index
aliases:
  - "Portal da Transparência"
status: pendente
updated: 2026-10-28
tags:
  - busca
  - dados-pessoais
---
# Portal da Transparência

Voltar: [[Home]] · [[Mapa-de-Integracoes|Mapa de integrações]]

Tema transversal: o Portal da Transparência e o sistema que administra o seu conteúdo. Os fatos e a confirmação de cada relação vêm do [[Mapa-de-Integracoes|Mapa de integrações]]; aqui só se reúnem os caminhos.

## Visão geral
- ✅ O `Portal-Transparencia` (backend e frontend) oferece as consultas públicas.
- ✅ O `Gerenciador-Portal` administra o conteúdo: grava no `SQL-Server-Portal` (`DB_PRT_TRANSPARENCIA`), nos buckets `portal-arquivos` e `portal-imagens` do `MinIO-CGDF` e as palavras-chave no `MongoDB-Portal`.
- 🔶 A ligação entre os dois foi informada pelo usuário; no código, os indícios são o banco comum, os buckets e a exchange `medida-protetiva-topic` (o Gerenciador publica `expirePortal`, o Portal consome).
- Dados pessoais no Portal: ver as notas de mascaramento e de segurança listadas abaixo.

## Por sistema
- **Portal-Transparencia:** [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Index|Índice]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integrações externas]] · [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Invalidação de cache de mascarados]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Super-Busca|Super busca]]
- **Gerenciador-Portal:** [[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Index|Índice]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integrações externas]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SQL-Server|SQL Server]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MongoDB|MongoDB]] · [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Expirar-Cache-Medida-Protetiva|Expirar cache da medida protetiva]]

## Notas dos dois sistemas com tag `busca` ou `dados-pessoais`
```base
filters:
  and:
    - or:
        - system == "Portal-Transparencia"
        - system == "Gerenciador-Portal"
    - or:
        - file.hasTag("busca")
        - file.hasTag("dados-pessoais")
views:
  - type: table
    name: Portal da Transparência
    groupBy:
      property: system
      direction: ASC
    order:
      - file.name
      - type
      - status
```

## Hipóteses
Ver a seção "Relações não confirmadas" do [[Mapa-de-Integracoes|Mapa de integrações]].
