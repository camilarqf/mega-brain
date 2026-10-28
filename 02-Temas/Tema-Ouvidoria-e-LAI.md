---
type: index
aliases:
  - "Ouvidoria e LAI"
status: pendente
updated: 2026-10-28
---
# Ouvidoria e LAI

Voltar: [[Home]] · [[Mapa-de-Integracoes|Mapa de integrações]]

Tema transversal: manifestações de ouvidoria, pedidos de acesso à informação (SIC/LAI) e denúncias. Os fatos e a confirmação de cada relação vêm do [[Mapa-de-Integracoes|Mapa de integrações]]; aqui só se reúnem os caminhos.

## Visão geral
- ✅ O `PARTICIPA-DF` concentra o registro de manifestações e pedidos: backend e três frontends (Cidadão, Ouvidoria e SIC).
- ✅ O backend do `PARTICIPA-DF` pede ao `Iza` sugestões de triagem (4 operações `predict-*`). 🔶 O provedor é o repositório `cgdf-iza` (aceito pelo usuário).
- ✅ O `PARTICIPA-DF` valida identidade no `PeoplesCheck` e acessa o `SEI` no recurso de 3ª instância.
- 🔶 O `SCI` é a contraparte provável dos eventos de denúncia (`denuncia-registrada`, `denuncia-aceita`, `denuncia-recusada`) via `RabbitMQ` e lê os anexos de denúncia no S3.
- ✅ O `Gerenciador-Portal` administra os órgãos da LAI exibidos no Portal.

## Por sistema
- **PARTICIPA-DF:** [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestação]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Pedido-e-Recurso|Pedido e recurso]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Registro de manifestação]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Registro de pedido]] · [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas]]
- **Frontends do PARTICIPA-DF:** [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Cidadão]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Ouvidoria]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|SIC]]
- **Iza:** [[01-Sistemas/Iza/Api/05-Fluxos/Iza-Api-Fluxo-Triagem-de-Manifestacao|Triagem de manifestação]] · [[01-Sistemas/Iza/Api/03-Modulos/Iza-Api-Predicao-de-Triagem|Predição de triagem]]
- **SCI:** [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|Eventos SCI ⇄ PARTICIPA-DF]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-S3-Anexos-de-Denuncia|Anexos de denúncia]] · [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Denúncia até admissibilidade]]
- **Gerenciador-Portal:** [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Orgaos-LAI|Órgãos da LAI]]

## Módulos e fluxos de PARTICIPA-DF, SCI e Iza
```base
filters:
  and:
    - or:
        - system == "PARTICIPA-DF"
        - system == "SCI"
        - system == "Iza"
    - or:
        - type == "flow"
        - type == "module"
views:
  - type: table
    name: Ouvidoria e LAI
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
