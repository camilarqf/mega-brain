---
type: integration
aliases:
  - "Integração Gerenciador-Portal → MongoDB"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
consumer: Gerenciador-Portal
provider: MongoDB-Portal
tags:
  - busca
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/config/MongoConfiguration.java
  - src/main/java/br/gov/df/cgdf/gerenciador/model/PalavraChave.java
  - src/main/java/br/gov/df/cgdf/gerenciador/repository/PalavrasRepository.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/PalavraService.java
---
# Integração Gerenciador-Portal → MongoDB

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integrações externas do Gerenciador-Portal Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Gerenciador-Portal` (`gerenciador-portal-backend`) | `MongoDB-Portal` (🔶 banco do serviço de busca do Portal; dono não identificado) | Spring Data MongoDB (driver `MongoClient`, URI com usuário e senha) | coleção `indices`, documento `PalavraChave` | saída (leitura e escrita) |

## Evidências
`MongoConfiguration` (chaves `spring.data.mongodb.host|port|user|pass|database`), `PalavrasRepository`, `PalavraService`, `PalavraChave`.

## Informações confirmadas
- ✅ Leitura/escrita da coleção `indices`: `save`, `findOne`, `delete` e a consulta derivada `findByDatasetOrderByPalavraChaveDesc("CUSTOM-PALAVRA-CHAVE")`. Campos: `_id`, `descritivo` (palavra), `urlConsulta`, `descricao`, `prioridade=1`, `dataset`, `exercicio`.
- ✅ Só os documentos com `dataset="CUSTOM-PALAVRA-CHAVE"` são listados; documentos de outros `dataset` na mesma coleção não são alterados por esta API (excluir/editar usam o `_id` informado pelo cliente).
- ✅ Os perfis `dev` e `homolog` (e o `local`) apontam ao mesmo host e ao banco `superbuscaportal_hom`; o perfil `prod` usa o banco `superbuscaportal` (host omitido). Credenciais distintas por perfil.
- ✅ `MongoConfiguration` monta a URI `mongodb://` concatenando usuário, senha, host e porta, sem codificar caracteres especiais e sem TLS.

## Falhas e dependências
- ✅ Usuário/senha do Mongo versionados nos `application-*.properties` (valores não registrados).
- ✅ Se `user` for nulo usa conexão sem autenticação; com o `@Value` obrigatório isso só ocorre se a chave existir vazia.
- ✅ A indisponibilidade do Mongo derruba as rotas `/palavra/*`; as demais continuam.

## Inferências e limitações
- 🔶 A coleção `indices` e o campo `dataset` indicam o índice do serviço de busca do Portal (`apisuperbusca`); o Gerenciador acrescenta as "palavras-chave customizadas". Não confirmado.
- ❓ Dono do cluster MongoDB e política de backup.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Módulo de conteúdo do portal]] · [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Banco-e-Persistencia|Banco e persistência]]

## Pendências e próximo passo
- Confirmar o dono do cluster e o consumidor da coleção.
