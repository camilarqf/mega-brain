---
type: index
system: Gerenciador-Portal
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - moc
  - sistema
---
# Gerenciador do Portal da Transparência — índice do sistema

## Objetivo
Ponto de entrada do sistema de negócio **Gerenciador-Portal** (nome no pipeline: "Gerenciador do Portal da Transparência"; `artifactId` `GerenciadorPortal`; descrição do `pom.xml`: "Gerenciador do portal da trasparencia"). Só o backend foi analisado (ver [[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Repositorios|Repositórios]]).

## Evidências
- Cadastro: [[Catalogo-de-Sistemas|Catálogo de sistemas]] (ID `Gerenciador-Portal`, cadastrado em 2026-10-27 com autorização do usuário; o ID usa hífen por causa da seção 3 do `BRAIN-RULES.md`).
- Documentação técnica do backend: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]] (commit `14b185f`).

## Informações confirmadas
- ✅ API REST (Spring Boot 1.5, Java 8) que **administra o conteúdo e os dados de apoio do Portal da Transparência**: cadastro e ativação de relatórios/arquivos por categoria, imagens do portal (slideshow, setores e fundos de painel), textos explicativos das consultas, palavras-chave de busca, órgãos da LAI, lista de pessoas com medida protetiva (ocultas no portal) e consulta ao controle de cargas.
- ✅ Grava arquivos e imagens em armazenamento S3-compatível (buckets `portal-arquivos` e `portal-imagens`) e registra tudo em SQL Server (`DB_PRT_TRANSPARENCIA`) e MongoDB.
- ✅ Autenticação do operador por SSO (Keycloak, fluxo de senha) e autorização por órgão/unidades configurados; o resto da API não valida o token (ver [[01-Sistemas/Gerenciador-Portal/Backend/06-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Segurança]]).

## Relação com o Portal-Transparencia
- 🔶 **Informado pelo usuário em 2026-10-27**: o Gerenciador tem ligação com o Portal da Transparência, mas é um **sistema à parte**. Não há chamada entre os dois no código deste repositório.
- ✅ Indícios no código: mesmo banco (`DB_PRT_TRANSPARENCIA`, esquemas `Portal`, `Servidor`, `Carga`), mesmos nomes de bucket do MinIO e a mesma exchange RabbitMQ `medida-protetiva-topic` que o backend do Portal consome. Ver [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integrações externas]].
- Responde em parte à pendência 18 do [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|Backend do Portal]] ("qual é o sistema gerenciador?"). Falta confirmar se ele chama `/storage/health` e `/storage/url` do Portal.

## Componentes
| Componente | Estado | Entrada |
|---|---|---|
| `gerenciador-portal-backend` | analisado (lotes 0 a 4, leitura estática, cobertura parcial) | [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]] |
| frontend | ❓ não identificado/não analisado (os parâmetros `usuarioLogado` e a ordenação por prioridade indicam um cliente web, 🔶) | — |

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]]
- [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Index|Portal-Transparencia]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Gerenciador-Portal/Backend/99-Controle/Gerenciador-Portal-Backend-Pendencias|Pendências]]. Próximo passo: localizar e documentar o frontend; confirmar com o time a relação com o Portal.
