---
type: analysis-log
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: pendente
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - pendencias
---
# Pendências — Gerenciador-Portal Backend

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]] · [[01-Sistemas/Gerenciador-Portal/Backend/99-Controle/Gerenciador-Portal-Backend-Registro-de-Analise|Registro de análise]]

## Objetivo
Dúvidas a confirmar com o time e lacunas da análise.

## Evidências
Origem em cada linha (lote/nota).

## Informações confirmadas
### Perguntas ao time
| # | Pergunta | Origem |
|---|---|---|
| 1 | Onde está o **frontend** do Gerenciador (repositório) e como ele usa `usuarioLogado`/`x-client-id`? O token do SSO chega ao backend? | Lote 1 |
| 2 | Qual a relação exata com o Portal-Transparencia? O Gerenciador chama `/storage/health` e `/storage/url` do Portal (pendência 18 do Portal) ou é o cliente web que o faz? | Lote 3 |
| 3 | A API está atrás de gateway/WAF/rede restrita? O ingress (`gerenciador-portal-transparencia`) exige algo além do `x-client-id`? | Lote 1 |
| 4 | O **Spring Data REST** realmente expõe os repositórios em execução? | Lote 1 |
| 5 | As credenciais versionadas (banco, MongoDB, RabbitMQ, usuário de desenvolvimento) já foram rotacionadas? O login de desenvolvimento deve existir em `prod`? | Lote 1/4 |
| 6 | Por que a exclusão apaga no disco local e não no MinIO? Quem limpa os objetos antigos? `salvar-sem-ordenar` ainda é usado? | Lote 2 |
| 7 | Quem consome `expireSuperbusca` e `expirePortal`? O cliente chama `expirar-cache` depois de cada alteração? O broker é o mesmo do PARTICIPA-DF/SCI? | Lote 3 |
| 8 | Qual o dono do banco `DB_PRT_TRANSPARENCIA` (DDL) e os privilégios do usuário da aplicação? | Lote 2 |
| 9 | Quem alimenta `Carga.Controle` e o significado de `SEM ALTER.`/`REALIZADO`? | Lote 2 |
| 10 | Qual o significado das categorias de arquivo único (50 a 59) e de 55/56 (imagens)? | Lote 2 |
| 11 | O Staging recebe credenciais do MinIO por qual meio (o pipeline só monta o secret do SSO)? | Lote 0 |
| 12 | O perfil Maven `producao` e o perfil Spring `prod` são o mesmo? Como o Jenkins define `SPRING_PROFILES_ACTIVE` no build? | Lote 0 |
| 13 | A instância do Keycloak é a do `KEYCLOAK-CGDF`? O endpoint `http` é interno? | Lote 3 |

### Lacunas da análise
- ❓ Frontend não analisado; comportamento em execução e DDL não verificados.
- ❓ Diff do commit `14b185f` (corrige usuário logado) não lido.
- ❓ Testes não versionados (`HealthcheckTest`, `ClientIdFilterTest`) fora do escopo; o segundo parece depender de uma mudança do filtro ainda não commitada.

## Inferências e limitações
Todas as ligações com o Portal-Transparencia são 🔶 (informadas pelo usuário, sem chamada direta no código).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
Resolver primeiro as perguntas 1, 2, 4 e 5.
