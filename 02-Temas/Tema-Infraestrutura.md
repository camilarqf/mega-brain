---
type: index
aliases:
  - "Infraestrutura"
status: pendente
updated: 2026-10-28
tags:
  - armazenamento-objetos
  - mensageria
---
# Infraestrutura

Voltar: [[Home]] · [[Mapa-de-Integracoes|Mapa de integrações]]

Tema transversal: roteamento, armazenamento de objetos e mensageria compartilhados entre os sistemas. Os fatos e a confirmação de cada relação vêm do [[Mapa-de-Integracoes|Mapa de integrações]]; aqui só se reúnem os caminhos.

## Visão geral
- ✅ O `INGRESS-CGDF` (Nginx) roteia por prefixo de path para serviços Swarm (19 rotas) e faz proxy TCP do `RabbitMQ`. 🔶 A correspondência das rotas com os sistemas é só pelo nome do serviço.
- ✅ O `MinIO-CGDF` expõe a API S3. Consumidores com cliente no código: `Gerenciador-Portal` (grava; 🔶 instância), `SCI` (lê anexos de denúncia; 🔶 provedor) e `Portal-Transparencia` (health e URLs; 🔶 provedor).
- ✅ No `RabbitMQ`: `PARTICIPA-DF` e `SCI` trocam eventos de denúncia; o `Gerenciador-Portal` publica e o `Portal-Transparencia` consome na exchange `medida-protetiva-topic`. ❓ Não se sabe se é o mesmo broker.

## Por sistema
- **INGRESS-CGDF:** [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Integracoes-com-Upstreams|Upstreams]] · [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Proxy-TCP-RabbitMQ|Proxy TCP RabbitMQ]]
- **MinIO-CGDF:** [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Arquitetura|Arquitetura]] · [[01-Sistemas/MinIO-CGDF/Infra/99-Controle/MinIO-CGDF-Infra-Pendencias|Pendências (consumidores)]]
- **Consumidores do S3:** [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MinIO-S3|Gerenciador → MinIO]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-S3-Anexos-de-Denuncia|SCI → S3]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Portal-Transparencia]]
- **Mensageria:** [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Eventos SCI ⇄ PARTICIPA-DF]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-RabbitMQ-Expirar-Cache|Gerenciador → RabbitMQ]] · [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Portal consome expirePortal]]

## Todas as notas com tag `armazenamento-objetos` ou `mensageria`
```base
filters:
  or:
    - file.hasTag("armazenamento-objetos")
    - file.hasTag("mensageria")
views:
  - type: table
    name: Infraestrutura
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
