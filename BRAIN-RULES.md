# Convenções do Mega Brain

- Um sistema de negócio vive em `01-Sistemas/<Sistema>/`.
- A documentação técnica de cada repositório vive em uma subpasta do sistema (`Backend/`, `Frontend/`, `Servico-X/`).
- A visão de negócio compartilhada fica na raiz do sistema e só deve ser consolidada quando houver evidências.
- Não criar pastas de componentes ainda não analisados: citá-los em `Repositorios.md` como `não analisado`.
- Links internos Obsidian: preferir `[[Caminho/Nota|Título]]` em caso de nomes ambíguos.
- Metadados YAML: seguir o schema da seção "Schema de metadados" abaixo.
- Estados de confirmação (`status`): `confirmado`, `inferido`, `nao-identificado`, `pendente`.
- Separar fatos presentes no código de recomendações de melhoria.
- Sempre preservar o histórico e tornar o próximo lote retomável por outra sessão.
- Antes de sincronizar, classificar o conteúdo e confirmar se o remoto é autorizado.

## Tipos de nota

Esta tabela é a **única fonte** dos valores de `type`. Escolher o tipo mais específico que descreva o objetivo principal da nota; `reference` só quando nenhum outro servir. Um tipo novo exige, antes, atualizar esta tabela e os grupos de cor do grafo (`.obsidian/graph.json`).

| `type` | Usar quando a nota… | Grupo do grafo (RGB) |
|---|---|---|
| `system` | descreve o sistema de negócio como um todo: objetivo, atores, contexto. | 196, 70, 255 |
| `index` | é um índice (MOC) de navegação, sem análise própria. | 196, 70, 255 |
| `architecture` | descreve estrutura, camadas e padrões de um componente. | 0, 170, 255 |
| `decision` | registra uma decisão com contexto e alternativas, somente se houver evidência. | 0, 170, 255 |
| `module` | documenta uma capacidade funcional coesa (controllers, casos de uso e modelos de uma área). | 255, 136, 0 |
| `business-rule` | descreve uma regra de negócio específica e verificável no código (condição → efeito); hipótese baseada em nomes vai em "inferências". | 255, 221, 0 |
| `flow` | descreve uma sequência ponta a ponta de passos, estados e atores. | 57, 255, 20 |
| `integration` | descreve a comunicação com sistema ou serviço externo: adaptadores, contratos, falhas. | 0, 245, 255 |
| `api` | descreve o contrato exposto: endpoints, verbos, payloads, códigos HTTP. | 0, 245, 255 |
| `security` | trata de autenticação, autorização, perfis, proteção de dados e riscos de segurança (sem segredos). | 255, 64, 180 |
| `technical-debt` | lista débitos, riscos e melhorias recomendadas, separados dos fatos. | 255, 64, 180 |
| `repository` | descreve um repositório de código: stack, estado da análise, relação com o sistema. | 200, 210, 255 |
| `analysis-log` | controla o processo de análise: lotes, pendências, cobertura. | 200, 210, 255 |
| `reference` | nenhuma categoria acima se aplica (glossário, enums, stack, ambientes, modelo de dados). | 200, 210, 255 |

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
