# Catálogo de sistemas

> Cadastre somente sistemas que tenham documentação aprovada para este cofre. Os **IDs** abaixo são os valores usados em `system`, `consumer` e `provider` (`BRAIN-RULES.md`, seção 4). Relações entre sistemas: [[Mapa-de-Integracoes|Mapa de integrações]].

| ID | Sistema | Repositórios | Estado | Índice |
|---|---|---|---|---|
| `SICI` | SICI (validar permissão antes de publicar) | `sici-backend`, `sici-frontend` | Backend analisado (commit `1871e32`; cobertura parcial em 2 notas); frontend não analisado | [[01-Sistemas/SICI/SICI-Index\|SICI-Index]] |
| `PARTICIPA-DF` | Participa DF (nome do app no pipeline; namespace `OuvDF`; nome oficial a validar; validar permissão antes de publicar) | `participa-df-backend`; frontend não identificado | Backend analisado (commit `4901ad5`; lotes 0 a 8 concluídos, cobertura parcial); frontend não analisado | [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index\|PARTICIPA-DF-Index]] |

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
| `Grafana-Loki` | Destino de logs (Serilog) do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `NewRelic` | Monitoramento de desempenho (agente .NET) do PARTICIPA-DF. | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |

## Critério de classificação
Antes de documentar um novo repositório, verificar se ele pertence a sistema já catalogado. Não deduzir relação apenas pelo nome.
