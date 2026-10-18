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

## Schema de metadados

Todo frontmatter usa exatamente estas chaves, em inglês, nesta ordem. Incluir somente os campos aplicáveis ao tipo da nota e omitir os demais (nunca usar `""`). Não criar duplicatas em português (`tipo`, `sistema`, `cobertura`, `fontes`, `commit`, `atualizado`, `componente`).

| Campo | Formato | Valores / regra |
|---|---|---|
| `type` | texto | `system`, `architecture`, `module`, `flow`, `business-rule`, `integration`, `security`, `reference`, `analysis-log`; também `index` (MOC), `repository` e `decision`. Outro tipo só se nenhum destes servir. |
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
