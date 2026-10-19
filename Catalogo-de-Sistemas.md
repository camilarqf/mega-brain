# Catálogo de sistemas

> Cadastre somente sistemas que tenham documentação aprovada para este cofre. Os **IDs** abaixo são os valores usados em `system`, `consumer` e `provider` (`BRAIN-RULES.md`, seção 4). Relações entre sistemas: [[Mapa-de-Integracoes|Mapa de integrações]].

| ID | Sistema | Repositórios | Estado | Índice |
|---|---|---|---|---|
| `SICI` | SICI (validar permissão antes de publicar) | `sici-backend`, `sici-frontend` | Backend analisado (commit `1871e32`; cobertura parcial em 2 notas); frontend analisado por leitura estática (commit `418642f`; lotes 0 a 5, cobertura parcial) | [[01-Sistemas/SICI/SICI-Index\|SICI-Index]] · [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index\|Frontend SICI]] |
| `PARTICIPA-DF` | Participa DF (nome do app no pipeline; namespace `OuvDF`; nome oficial a validar; validar permissão antes de publicar) | `participa-df-backend`, `participa-df-frontend` (Cidadão), `participa-df-ouv-frontend` (Ouvidoria), `participa-df-sic-frontend` (SIC); 3 de 3 front-ends identificados | Backend analisado (commit `4901ad5`; lotes 0 a 8 concluídos, cobertura parcial); frontend `participa-df-frontend` analisado (commit `d250804`; lotes 0 a 5, cobertura parcial); frontend `participa-df-ouv-frontend` (AngularJS, Ouvidoria) analisado (commit `9d8ecdb`; lotes 0 a 5, cobertura parcial); frontend `participa-df-sic-frontend` (AngularJS, SIC) em análise (commit `5518a81`; lotes 0 a 5, cobertura parcial) | [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index\|PARTICIPA-DF-Index]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index\|Frontend Ouvidoria]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index\|Frontend SIC]] |

## Serviços externos (provedores)

Serviços consumidos pelos sistemas acima, sem repositório próprio neste cofre.

| ID | Descrição | Documentação |
|---|---|---|
| `Keycloak` | Provedor de identidade (OIDC) usado pelo backend do SICI. | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `Servico-de-PDF` | Serviço de geração de PDF chamado pelo backend do SICI; tecnologia, dono e SLA não identificados. | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `Iza` | Serviço de IA que sugere assunto, classificação, unidade e se o relato é denúncia; chamado pelo backend do PARTICIPA-DF; natureza e dono não identificados. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `MailService` | Serviço de envio de e-mail (API HTTP) usado pelo backend do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `PeoplesCheck` | Serviço de validação de identidade (CPF e vínculo CPF–CNPJ) usado pelo PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `SEI` | Sistema de processos eletrônicos, acessado por web service no recurso de 3ª instância do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `Servico-HtmlToPdf` | Serviço de geração de PDF a partir de HTML usado pelo PARTICIPA-DF; contrato igual ao de `Servico-de-PDF` (relação não confirmada). | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `RabbitMQ` | Broker de mensagens usado pelo PARTICIPA-DF para os eventos de denúncia. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `Servico-Geocodificacao` | Serviços de geocodificação e endereço consultados pelo PARTICIPA-DF por proxy. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `Servico-Localizacao-CGDF` | Serviço de localização (busca de endereço, endereço por coordenada e região administrativa) chamado direto pelo navegador nos frontends do PARTICIPA-DF (Cidadão e Ouvidoria); dono não identificado; relação com `Servico-Geocodificacao` não confirmada. | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas\|Integrações do Frontend Cidadão]] |
| `Google-Analytics` | Google Tag (`gtag.js`) usado pelo frontend do PARTICIPA-DF para métricas de navegação. | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas\|Integrações do Frontend Cidadão]] |
| `Perto-Digital` | Plugin de acessibilidade carregado por CDN no frontend do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas\|Integrações do Frontend Cidadão]] |
| `Grafana-Loki` | Destino de logs (Serilog) do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `NewRelic` | Monitoramento de desempenho (agente .NET) do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `OpenStreetMap` | Tiles de mapa (OSM) usados via OpenLayers pelo frontend de Ouvidoria do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/04-API-e-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas\|Integrações do Frontend Ouvidoria]] |
| `Servico-WMS-Ortofoto-DF` | Serviço WMS de ortofoto consumido direto do navegador no mapa de detalhe da manifestação (frontend de Ouvidoria); dono não identificado. | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/04-API-e-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas\|Integrações do Frontend Ouvidoria]] |

## Critério de classificação
Antes de documentar um novo repositório, verificar se ele pertence a sistema já catalogado. Não deduzir relação apenas pelo nome.
