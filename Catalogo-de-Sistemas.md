# Catálogo de sistemas

> Cadastre somente sistemas que tenham documentação aprovada para este cofre. Os **IDs** abaixo são os valores usados em `system`, `consumer` e `provider` (`BRAIN-RULES.md`, seção 4). Relações entre sistemas: [[Mapa-de-Integracoes|Mapa de integrações]].

| ID | Sistema | Repositórios | Estado | Índice |
|---|---|---|---|---|
| `SICI` | SICI (validar permissão antes de publicar) | `sici-backend`, `sici-frontend` | Backend analisado (commit `1871e32`; cobertura parcial em 2 notas); frontend não analisado | [[01-Sistemas/SICI/SICI-Index\|SICI-Index]] |

## Serviços externos (provedores)

Serviços consumidos pelos sistemas acima, sem repositório próprio neste cofre.

| ID | Descrição | Documentação |
|---|---|---|
| `Keycloak` | Provedor de identidade (OIDC) usado pelo backend do SICI. | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |
| `Servico-de-PDF` | Serviço de geração de PDF chamado pelo backend do SICI; tecnologia, dono e SLA não identificados. | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |

## Critério de classificação
Antes de documentar um novo repositório, verificar se ele pertence a sistema já catalogado. Não deduzir relação apenas pelo nome.
