# Convenções do Mega Brain

- Um sistema de negócio vive em `01-Sistemas/<Sistema>/`.
- A documentação técnica de cada repositório vive em uma subpasta do sistema (`Backend/`, `Frontend/`, `Servico-X/`).
- A visão de negócio compartilhada fica na raiz do sistema e só deve ser consolidada quando houver evidências.
- Não criar pastas de componentes ainda não analisados: citá-los em `<Sistema>-Repositorios.md` como `não analisado`.
- Links internos Obsidian: preferir `[[Caminho/Nota|Título]]` em caso de nomes ambíguos.
- Metadados YAML: seguir o schema da seção "Schema de metadados" abaixo.
- Estados de confirmação (`status`): `confirmado`, `inferido`, `nao-identificado`, `pendente`.
- Separar fatos presentes no código de recomendações de melhoria.
- Sempre preservar o histórico e tornar o próximo lote retomável por outra sessão.
- Antes de sincronizar, classificar o conteúdo e confirmar se o remoto é autorizado.

## Tipos de nota

Esta tabela é a **única fonte** dos valores de `type`, usada por Claude Code, Codex e pelo grafo do Obsidian. Os tipos novos só entram aqui, junto com o grupo de cor em `.obsidian/graph.json`.

| `type` | Usar quando a nota… | Exemplo | Cor no grafo (RGB) |
|---|---|---|---|
| `system` | descreve o sistema de negócio: objetivo, atores, contexto. | `SICI-Contexto-do-Sistema` | 196, 70, 255 |
| `index` | é um índice (MOC) de navegação, sem análise própria. | `SICI-Index`, `SICI-Backend-Index` | 196, 70, 255 |
| `architecture` | descreve estrutura, camadas e padrões de um componente. | `SICI-Backend-Arquitetura-Hexagonal` | 0, 170, 255 |
| `decision` | registra uma decisão com contexto e alternativas, somente se houver evidência. | — | 0, 170, 255 |
| `module` | documenta uma capacidade funcional coesa (controllers, casos de uso e modelos de uma área). | `Ordem-de-Servico`, `POAC` | 255, 136, 0 |
| `flow` | descreve uma sequência ponta a ponta de passos, estados e atores. | `Fluxo-Assinatura-OS` | 57, 255, 20 |
| `business-rule` | descreve uma regra de negócio específica e verificável no código (condição → efeito); hipótese baseada em nomes vai em "inferências". | — | 255, 221, 0 |
| `integration` | descreve a comunicação com sistema ou serviço externo: adaptadores, contratos, falhas. | `SICI-Backend-Integracoes-Externas` | 0, 245, 255 |
| `api` | descreve o contrato exposto: endpoints, verbos, payloads, códigos HTTP. | `SICI-Backend-Catalogo-de-Endpoints` | 0, 245, 255 |
| `security` | trata de autenticação, autorização, perfis, proteção de dados e controles de segurança (sem segredos). | `SICI-Backend-Seguranca-e-Autorizacao` | 255, 64, 180 |
| `technical-debt` | lista débitos, riscos e melhorias recomendadas, separados dos fatos. | `SICI-Backend-Debitos-Tecnicos` | 255, 64, 180 |
| `domain` | descreve modelos de domínio, entidades conceituais, value objects, enums e estados. | `SICI-Backend-Modelo-de-Dominio`, `SICI-Backend-Enums-e-Estados` | 65, 105, 255 |
| `persistence` | descreve banco de dados, mapeamento de entidades, constraints e migrations. | `SICI-Backend-Banco-e-Migrations` | 25, 70, 220 |
| `quality` | descreve testes, cobertura e estratégias de qualidade. | `SICI-Backend-Testes-e-Cobertura` | 255, 105, 180 |
| `repository` | descreve um repositório de código: estado da análise e relação com o sistema. | `SICI-Repositorios` | 200, 210, 255 |
| `analysis-log` | controla o processo de análise: lotes, pendências, cobertura. | `SICI-Backend-Registro-de-Analise`, `SICI-Backend-Pendencias` | 200, 210, 255 |
| `reference` | nenhuma categoria acima representa a natureza predominante (glossário, stack, ambientes e configuração). | `SICI-Backend-Glossario`, `SICI-Backend-Stack-e-Dependencias`, `SICI-Backend-Perfis-e-Ambientes` | 200, 210, 255 |

Como escolher:
- Classificar pelo **conteúdo**, não pelo nome do arquivo nem pela pasta. Em caso de dúvida, vale a natureza predominante da nota.
- `reference` é o último recurso; documentação técnica não é `reference` automaticamente.
- Antes de criar uma nota, verificar se já existe nota sobre o assunto e atualizá-la em vez de duplicar o conhecimento.
- Não propor tipo novo sem necessidade real (várias notas que nenhum tipo atual represente).

## Nomenclatura de arquivos

O nome do arquivo é o rótulo da nota no grafo do Obsidian, por isso deve ser único e autoexplicativo:
- Índices: `<Sistema>-<Componente>-Index.md` (índice do sistema: `<Sistema>-Index.md`). Ex.: `SICI-Backend-Index`.
- Documentação de um componente: `<Sistema>-<Componente>-<Assunto>.md`. Ex.: `SICI-Backend-Pendencias`.
- Documentação geral do sistema: `<Sistema>-<Assunto>.md`. Ex.: `SICI-Repositorios`.
- Módulos e fluxos de negócio com nome já específico podem manter `<Assunto>.md` (ex.: `POAC`, `Ordem-de-Servico`).
- Sem acentos, com hífens e sem prefixo numérico.
- **Antes de criar uma nota, verificar se já existe arquivo com o mesmo nome em qualquer pasta do vault** (inclusive `99-Templates/`). Em caso de colisão, usar o prefixo `<Sistema>-<Componente>-`; nunca manter dois arquivos com o mesmo nome.
- Ao renomear, usar `git mv`, atualizar todos os links `[[…]]` e referências em regras e Skills, e preservar o histórico: registros de análise e decisões mantêm o texto original, e o mapeamento nome antigo → novo fica no `SICI-Backend-Registro-de-Analise`.

## Schema de metadados

Todo frontmatter usa exatamente estas chaves, em inglês, nesta ordem. Incluir somente os campos aplicáveis ao tipo da nota e omitir os demais (nunca usar `""`). Não criar duplicatas em português (`tipo`, `sistema`, `cobertura`, `fontes`, `commit`, `atualizado`, `componente`).

| Campo | Formato | Valores / regra |
|---|---|---|
| `type` | texto | Um dos valores da seção "Tipos de nota" abaixo, que é a única lista oficial. |
| `system` | texto | Sistema de negócio (ex.: `SICI`). |
| `component` | texto | Parte lógica do sistema. Só se houver evidência; não deduzir. |
| `repository` | texto ou lista | Nome do repositório; lista se a nota abranger vários. |
| `status` | texto | **Confirmação**: `confirmado`, `inferido`, `nao-identificado`, `pendente`. |
| `coverage` | texto | **Abrangência da análise**: `completa`, `parcial`, `nao-analisado`. Independe de `status`. |
| `analyzed_commit` | texto | Hash completo (40 caracteres) do commit analisado. |
| `created` | data `YYYY-MM-DD` | Só quando a data de criação for conhecida e diferente de `updated`. |
| `updated` | data `YYYY-MM-DD` | Sem aspas. |
| `tags` | lista em bloco | Minúsculas, sem `#`. |
| `sources` | lista em bloco | Caminhos relativos ao repositório analisado, como no código. |

Campos específicos de `analysis-log`: `commit_data` (data do commit, `YYYY-MM-DD`) e `branch`.

Regras:
- `status` e `coverage` são independentes: uma nota pode estar `confirmado` e `parcial`.
- Preservar fontes, commits, tags e datas originais; não inventar valores para campos ausentes.
- Ao atualizar uma nota, alterar `updated`, `analyzed_commit` e `coverage` conforme o caso, sem apagar `created`.
- Consultas Obsidian (Bases/Dataview) podem filtrar por qualquer chave acima, ex.: `status = "confirmado" AND coverage = "parcial"`.
