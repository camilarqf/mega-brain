# Convenções do Mega Brain

Fonte única das regras do vault, usada por Claude Code, Codex, Skills e pelo Obsidian. `CLAUDE.md`, `AGENTS.md` e as Skills apenas referenciam estas seções: **não copiar definições para eles**. Ler somente a seção necessária.

| Seção | Assunto |
|---|---|
| 1 | Estrutura: sistema, componente e repositório |
| 2 | Tipos de nota |
| 3 | Nomenclatura de arquivos |
| 4 | Schema de metadados |
| 5 | Evidência, confiança e validade |
| 6 | Recuperação progressiva de contexto |
| 7 | Relações entre sistemas e integrações |
| 8 | Criar, atualizar e relacionar notas |
| 9 | Aprovação e Git |
| 10 | Segurança, confidencialidade e remotos |
| 11 | Skills, agentes e ferramentas de terceiros |

## 1. Estrutura

- Um sistema de negócio vive em `01-Sistemas/<Sistema>/`. **Sistema de negócio não é sinônimo de repositório**: vários repositórios podem compor um sistema, e um componente (`Backend`, `Frontend`, `Servico-X`) corresponde a um repositório.
- Pastas da raiz: `00-Paineis/` (consultas Bases), `01-Sistemas/`, `02-Temas/` (notas de tema que ligam vários sistemas) e `99-Templates/`.
- A documentação técnica de cada repositório vive em uma subpasta do sistema (`Backend/`, `Frontend/`, `Servico-X/`).
- O índice do componente (`<Sistema>-<Componente>-Index`) fica na raiz da pasta do componente; as demais notas usam numeração fixa, igual em todos os componentes. Criar só as pastas necessárias, deixando lacunas na numeração:

| Pasta | Conteúdo |
|---|---|
| `01-Visao-Geral` | arquitetura, stack, deploy, ambientes, glossário |
| `02-Dominio` | modelo de domínio, enums e estados, banco e persistência |
| `03-Modulos` | módulos; rotas e telas (frontends) |
| `04-Regras-de-Negocio` | regras de negócio |
| `05-Fluxos` | fluxos |
| `06-API` | contrato exposto pelo componente (endpoints) |
| `07-Integracoes` | o que o componente consome, inclusive chamadas de API dos frontends |
| `08-Seguranca` | autenticação, autorização, sessão |
| `09-Qualidade` | testes, cobertura, débitos técnicos |
| `99-Controle` | registro de análise e pendências |
- Requisitos (US e solicitações de mudança) ficam em `01-Sistemas/<Sistema>/Requisitos/`, no sistema dono do requisito.
- A visão de negócio compartilhada fica na raiz do sistema e só deve ser consolidada quando houver evidências.
- Não criar pastas de componentes ainda não analisados: citá-los em `<Sistema>-Repositorios.md` como `não analisado`.
- `Catalogo-de-Sistemas.md` é o ponto de entrada: IDs de sistemas e de serviços externos, repositórios e índices. Os IDs do catálogo são os valores de `system`, `consumer` e `provider`.
- Links internos Obsidian: preferir `[[Caminho/Nota|Título]]` em caso de nomes ambíguos.
- Sempre preservar o histórico e tornar o próximo lote retomável por outra sessão.

## 2. Tipos de nota

Esta tabela é a **única fonte** dos valores de `type`, usada por Claude Code, Codex e pelo grafo do Obsidian. Tipos novos só entram aqui, junto com o grupo de cor em `.obsidian/graph.json`.

| `type` | Usar quando a nota… | Exemplo | Família e cor no grafo |
|---|---|---|---|
| `system` | descreve o sistema de negócio: objetivo, atores, contexto. | `SICI-Contexto-do-Sistema` | Navegação · `#C084FC` |
| `index` | é um índice (MOC) de navegação, sem análise própria. | `SICI-Index`, `SICI-Backend-Index`, `Mapa-de-Integracoes` | Navegação · `#C084FC` |
| `architecture` | descreve estrutura, camadas e padrões de um componente. | `SICI-Backend-Arquitetura-Hexagonal` | Estrutura · `#60A5FA` |
| `decision` | registra uma decisão com contexto e alternativas, somente se houver evidência. | — | Estrutura · `#60A5FA` |
| `module` | documenta uma capacidade funcional coesa (controllers, casos de uso e modelos de uma área). | `Ordem-de-Servico`, `POAC` | Funcional · `#FB923C` |
| `flow` | descreve uma sequência ponta a ponta de passos, estados e atores. | `Fluxo-Assinatura-OS` | Fluxo · `#4ADE80` |
| `business-rule` | descreve uma regra de negócio específica e verificável no código (condição → efeito); hipótese baseada em nomes vai em "inferências". | — | Regra · `#FACC15` |
| `integration` | descreve a comunicação entre um consumidor e um provedor (sistema ou serviço externo): cliente, contrato, direção, falhas. | `SICI-Backend-Integracoes-Externas` | Contratos · `#22D3EE` |
| `api` | descreve o contrato exposto: endpoints, verbos, payloads, códigos HTTP. | `SICI-Backend-Catalogo-de-Endpoints` | Contratos · `#22D3EE` |
| `security` | trata de autenticação, autorização, perfis, proteção de dados e controles de segurança (sem segredos). | `SICI-Backend-Seguranca-e-Autorizacao` | Risco · `#F43F5E` |
| `technical-debt` | lista débitos, riscos e melhorias recomendadas, separados dos fatos. | `SICI-Backend-Debitos-Tecnicos` | Risco · `#F43F5E` |
| `domain` | descreve modelos de domínio, entidades conceituais, value objects, enums e estados. | `SICI-Backend-Modelo-de-Dominio`, `SICI-Backend-Enums-e-Estados` | Estrutura · `#60A5FA` |
| `persistence` | descreve banco de dados, mapeamento de entidades, constraints e migrations. | `SICI-Backend-Banco-e-Migrations` | Estrutura · `#60A5FA` |
| `quality` | descreve testes, cobertura e estratégias de qualidade. | `SICI-Backend-Testes-e-Cobertura` | Apoio · `#94A3B8` |
| `requirement` | registra o que foi **solicitado**: US ou mudança, critérios de aceite, regras pretendidas e análise de impacto. Não descreve comportamento implementado. | `<Sistema>-US-<ID>-<Resumo>` | Requisito · `#F472B6` |
| `repository` | descreve um repositório de código: estado da análise e relação com o sistema. | `SICI-Repositorios` | Apoio · `#94A3B8` |
| `analysis-log` | controla o processo de análise: lotes, pendências, cobertura. | `SICI-Backend-Registro-de-Analise`, `SICI-Backend-Pendencias` | Apoio · `#94A3B8` |
| `reference` | nenhuma categoria acima representa a natureza predominante (glossário, stack, ambientes e configuração). | `SICI-Backend-Glossario`, `SICI-Backend-Stack-e-Dependencias`, `SICI-Backend-Perfis-e-Ambientes` | Apoio · `#94A3B8` |

Como escolher:
- Classificar pelo **conteúdo**, não pelo nome do arquivo nem pela pasta. Em caso de dúvida, vale a natureza predominante da nota.
- `reference` é o último recurso; documentação técnica não é `reference` automaticamente.
- Não propor tipo novo sem necessidade real (várias notas que nenhum tipo atual represente), e justificar antes de alterar esta tabela.

## 3. Nomenclatura de arquivos

O nome do arquivo é o rótulo da nota no grafo do Obsidian, por isso deve ser único e autoexplicativo:
- Índices: `<Sistema>-<Componente>-Index.md` (índice do sistema: `<Sistema>-Index.md`). Ex.: `SICI-Backend-Index`.
- Documentação de um componente: `<Sistema>-<Componente>-<Assunto>.md`. Ex.: `SICI-Backend-Pendencias`.
- Documentação geral do sistema: `<Sistema>-<Assunto>.md`. Ex.: `SICI-Repositorios`.
- Requisitos: `<Sistema>-US-<ID>-<Resumo>.md`.
- Toda nota de sistema leva o prefixo `<Sistema>-` (e `<Componente>-` quando for de um componente), mesmo com assunto já específico; não há exceção para módulos ou fluxos.
- Temas: `02-Temas/Tema-<Assunto>.md`. Painéis: `00-Paineis/<Assunto>.base`.
- Notas de vault inteiro (ex.: `Mapa-de-Integracoes`) ficam na raiz.
- Sem acentos, com hífens e sem prefixo numérico. O título legível, com acentos, vai em `aliases` (seção 4).
- IDs de sistema já cadastrados não mudam (são chaves de `system`, `consumer` e `provider`). IDs novos: inicial maiúscula e hífens (ex.: `Portal-Transparencia`); sufixo `-CGDF` só para infraestrutura própria da casa (ex.: `MinIO-CGDF`).
- **Antes de criar uma nota, verificar se já existe arquivo com o mesmo nome em qualquer pasta do vault** (inclusive `99-Templates/`). Em caso de colisão, usar o prefixo `<Sistema>-<Componente>-`; nunca manter dois arquivos com o mesmo nome.
- Ao renomear, usar `git mv`, atualizar todos os links `[[…]]` e referências em regras e Skills, incluir o nome antigo em `aliases` e preservar o histórico: registros de análise e decisões mantêm o texto original, e o mapeamento nome antigo → novo fica no registro de análise do componente.

## 4. Schema de metadados

Todo frontmatter usa exatamente estas chaves, em inglês, nesta ordem. Incluir somente os campos aplicáveis ao tipo da nota e omitir os demais (nunca usar `""`). Não criar duplicatas em português (`tipo`, `sistema`, `cobertura`, `fontes`, `commit`, `atualizado`, `componente`).

| Campo | Aplica-se a | Formato | Valores / regra |
|---|---|---|---|
| `type` | todas | texto | Um valor da seção 2. |
| `aliases` | opcional | lista em bloco | Título legível com acentos (ex.: `Registro de manifestação (Cidadão)`) e nomes antigos após renomeação. |
| `system` | todas, exceto notas de vault inteiro (raiz e `02-Temas/`) | texto | ID do sistema no catálogo (ex.: `SICI`). |
| `component` | opcional | texto | Parte lógica do sistema. Só se houver evidência; não deduzir. |
| `repository` | opcional | texto ou lista | Nome do repositório; lista se a nota abranger vários. |
| `status` | todas | texto | **Confirmação**: `confirmado`, `inferido`, `nao-identificado`, `pendente`. |
| `lifecycle` | **somente** `requirement` | texto | **Ciclo de vida do requisito**: `proposed`, `approved`, `in-progress`, `implemented`, `validated`, `rejected`, `cancelled`. Independe de `status`. |
| `coverage` | notas de análise de código | texto | **Abrangência da análise**: `completa`, `parcial`, `nao-analisado`. Independe de `status`. |
| `analyzed_commit` | opcional | texto | Hash completo (40 caracteres) do commit analisado. |
| `created` | opcional | data `YYYY-MM-DD` | Só quando a data de criação for conhecida e diferente de `updated`. |
| `updated` | todas | data `YYYY-MM-DD` | Sem aspas. |
| `commit_data`, `branch` | **somente** `analysis-log` | data / texto | Data do commit analisado e branch. |
| `consumer`, `provider` | **somente** `integration` (opcionais) | texto | ID do catálogo (sistema ou serviço externo). Preencher apenas com evidência; se desconhecido, omitir. |
| `tags` | opcional | lista em bloco | Somente do vocabulário controlado abaixo; minúsculas, sem `#`. |
| `sources` | opcional | lista em bloco | Caminhos relativos ao repositório analisado, como no código. |

Regras:
- `status`, `coverage` e `lifecycle` são independentes: um requisito pode ter `lifecycle: approved` e `status: inferido`; uma nota pode estar `confirmado` e `parcial`.
- Preservar fontes, commits, tags e datas originais; não inventar valores para campos ausentes.
- Ao atualizar uma nota, alterar `updated`, `analyzed_commit` e `coverage` conforme o caso, sem apagar `created`.
- Consultas Obsidian (Bases/Dataview) podem filtrar por qualquer chave acima, ex.: `status = "confirmado" AND coverage = "parcial"`.
- A validação automática está em `scripts/validar-brain.py`; ela lê os valores válidos desta tabela, do vocabulário de tags e da seção 2.

Vocabulário controlado de tags. Tags marcam **temas transversais** que cruzam sistemas; não repetir o que já está em `type`, `system`, no componente ou na pasta. Tag nova só entra nesta tabela com aprovação do usuário.

| Tag | Usar quando a nota trata de… |
|---|---|
| `autenticacao` | login, identidade, tokens, SSO, LDAP |
| `dados-pessoais` | tratamento de dados pessoais (LGPD), CPF, cadastro de pessoas |
| `geracao-pdf` | geração de documentos PDF |
| `armazenamento-objetos` | MinIO, S3, arquivos e anexos |
| `mensageria` | filas, eventos, RabbitMQ |
| `busca` | índices e mecanismos de busca |
| `geolocalizacao` | endereços, mapas, coordenadas |
| `observabilidade` | logs, métricas, monitoramento |

## 5. Evidência, confiança e validade

- Diferenciar sempre: **fato confirmado** (✅, verificado no código/contrato/teste), **inferência ou hipótese** (🔶, deduzida de nomes, padrões ou indícios), **lacuna** (❓, não identificado) e **dado desatualizado**. No frontmatter, `status` usa `confirmado`, `inferido`, `nao-identificado` ou `pendente`.
- Preservar rastreabilidade: registrar repositório, commit, caminho de arquivo e classe/método quando possível.
- Não inventar funcionalidades, decisões ou integrações não verificadas.
- Separar fatos presentes no código de recomendações de melhoria.
- Separar **requisito solicitado**, **comportamento implementado** e **documentação histórica**. Uma US aprovada não é funcionalidade implementada sem evidência no código.
- **Validade de uma nota**: comparar `analyzed_commit` com o `HEAD` do repositório e listar `git diff --name-only <analyzed_commit>..HEAD -- <sources>`. Se algum arquivo de `sources` mudou, a nota está potencialmente desatualizada e não prova o comportamento atual. Sem `analyzed_commit` ou `sources`, a validade é desconhecida.
- Documentação do Brain não é verdade absoluta: confrontar com o código atual, testes e contratos antes de afirmar comportamento. Decisões anteriores podem ser questionadas com justificativa técnica; novas funcionalidades não precisam seguir soluções antigas só por estarem documentadas. Apresentar alternativas e trade-offs quando a decisão for relevante.
- Conflitos entre requisito, documentação e código devem ser relatados, nunca resolvidos por suposição.
- Ao mudar uma regra, preservar a versão anterior em um bloco datado "Histórico" (regra anterior + commit); não sobrescrever o histórico.

## 6. Recuperação progressiva de contexto

Não carregar todas as notas de um sistema. Seguir os níveis, parando assim que houver informação suficiente:
1. **Tarefa e sistema**: identificar o assunto e o sistema envolvido. Se o vault não estiver acessível, informar a limitação e pedir acesso; não presumir que foi consultado.
2. **N0 — catálogo**: `Catalogo-de-Sistemas.md`.
3. **N1 — índices**: `<Sistema>-Index` e o índice do componente.
4. **N2 — notas-alvo**: localizar por `type`, `tags`, `sources` e títulos; ler primeiro o frontmatter e os títulos, e apenas as seções necessárias.
5. **N3 — vizinhas**: seguir links só quando houver dependência relevante.
6. **N4 — outros sistemas**: somente pelo `Mapa-de-Integracoes` ou por uma nota de `02-Temas/`, e quando a relação for relevante à tarefa.
7. **Verificação**: checar a validade (seção 5) e confirmar o que for importante no código atual, testes e contratos.

Evitar recuperar contexto do Brain em tarefas triviais sem relação com o conhecimento documentado. Informações do Brain são ponto de partida, não prova.

## 7. Relações entre sistemas e integrações

- Distinguir **sistema de negócio**, **componente** e **repositório**. Provedores externos (ex.: serviços de identidade) entram no catálogo como "serviços externos".
- Uma integração tem **uma única nota canônica** (`type: integration`, modelo `99-Templates/Integracao.md`), na pasta do componente que contém o cliente/adaptador (o consumidor). Registrar consumidor, provedor, tecnologia, contrato, direção da comunicação e dependências **quando verificáveis**. O lado provedor só recebe um link de volta; não duplicar a documentação.
- `Mapa-de-Integracoes.md` é o índice de todas as integrações (consumidor → provedor), com link para a nota canônica e a confirmação de cada linha. Toda integração nova ou alterada deve atualizar o mapa.
- Identificar integrações por evidência de código, configuração, contratos ou documentação confiável. Relações não confirmadas entram como hipótese (`status: inferido` ou `pendente`) em seção própria do mapa, nunca como fato.
- Análises de impacto transversais partem do mapa; consultar outro sistema apenas quando houver relação relevante.

## 8. Criar, atualizar e relacionar notas

- Antes de criar, verificar se já existe nota sobre o assunto e o nome (seção 3); atualizar em vez de duplicar conhecimento.
- Escolher o `type` pelo conteúdo (seção 2) e gerar frontmatter válido (seção 4).
- Criar links internos que reflitam **relações reais** (módulo ↔ regras ↔ fluxos ↔ arquitetura ↔ integrações). Toda nota nova deve ser linkada a partir do índice do componente e linkar de volta a ele; evitar links decorativos.
- Preservar material existente; não sobrescrever, mover ou excluir notas preexistentes sem plano e aprovação.
- Ao concluir cada lote, atualizar `<Sistema>-<Componente>-Registro-de-Analise.md`, `<Sistema>-<Componente>-Pendencias.md` e o índice, indicando o próximo passo exato (a análise deve ser retomável sem repetir o trabalho).
- Registrar no registro de análise somente alterações de classificação, padronização ou estrutura, não cada correção simples de YAML.

## 9. Aprovação e Git

- Toda escrita em notas parte de um **plano apresentado e aprovado** (escopo, arquivos, alterações).
- Não executar `git add`, `commit`, `push`, `reset` ou rebase automaticamente: mostrar o diff e solicitar aprovação explícita para cada operação. Commit e push são aprovados separadamente.
- Nunca usar `reset --hard`, `push --force` ou comandos destrutivos automaticamente.
- `.obsidian/graph.json` é versionado por causa dos grupos de cor (seção 2). Mudanças só de visualização (`scale`, `*Strength`, `linkDistance`, `*Multiplier`, `collapse-*`, `close`) não são commitadas: apontar e, com aprovação, descartar.
- A sincronização (Skill `sincronizar-brain`) nunca é consequência automática de outra Skill.
- Não alterar código-fonte como consequência de atividades de documentação.

## 10. Segurança, confidencialidade e remotos

- Nunca copiar credenciais, tokens, segredos, dados pessoais ou material institucional para destinos externos não autorizados, nem para as notas.
- O Git é o único meio de sincronização do cofre. Obsidian Sync e outros serviços de nuvem não são destinos autorizados; o plugin core `sync` fica desativado.
- Nunca reproduzir valores de configuração sensíveis; registrar apenas nomes de chaves e endereços omitidos.
- Antes de sincronizar, classificar o conteúdo por categoria: (a) conhecimento técnico genérico, (b) documentação derivada de código institucional, (c) requisitos, US e análises de impacto, (d) dados pessoais e segredos (nunca publicar).
- **Remoto configurado**: `origin` → `https://github.com/camilarqf/mega-brain.git`, uma conta pessoal do GitHub. Estar configurado **não** significa autorizado: a autorização deve ser confirmada pelo usuário **para cada categoria de conteúdo** antes de cada sincronização. Documentação institucional (categorias b e c) não é sincronizada sem autorização adequada; se não houver, interromper e propor ambiente institucional.
- Se a configuração atual não permitir uma operação autorizada, informar o bloqueio e propor alternativa segura.
- Não enviar código, documentos ou requisitos a serviços externos (inclusive outros agentes de IA) sem autorização; testes de Skills usam apenas cofres fictícios com dados sintéticos.

## 11. Skills, agentes e ferramentas de terceiros

- As Skills do Mega Brain são `SKILL.md` com `name` e `description`, autossuficientes e curtas; referenciam seções deste arquivo em vez de repeti-las. Responsabilidades: `documentar-sistema` (documentar código existente), `consultar-conhecimento` (responder, somente leitura), `atualizar-documentacao` (sincronizar notas com mudanças), `sincronizar-brain` (Git do cofre), `analisar-us` (analisar requisito, sem código), `implementar-us` (implementar escopo aprovado).
- O cofre é a fonte oficial e única das Skills (`.claude/skills/`). Claude Code e Codex as usam pelas instalações globais (`~/.claude/skills`, `~/.codex/skills`), criadas como junctions por `scripts/sincronizar-skills.py` (rodar em máquina nova); não há cópias a manter em sincronia. Nunca editar fora de `.claude/skills/`.
- Uma Skill não executa automaticamente outra: o agente indica a próxima Skill e o usuário (ou o mecanismo do agente) a invoca.
- Skills de terceiros: não modificar, não duplicar suas funções e usá-las quando forem adequadas e estiverem disponíveis na sessão; se o agente não conseguir invocá-las, pedir ao usuário. Instruções incompatíveis (por exemplo, commit/push/PR automáticos) exigem decisão do usuário.
- Plugins do Obsidian: os core (inclusive Bases) e, da comunidade, somente o Graph Styler (tema `Mega-Brain-Galaxy`, que altera fundo e linhas, não os grupos de cor). Plugin novo só com aprovação do usuário.
- Claude Code: acesso ao vault com `/add-dir` ou `claude --add-dir`. Codex: conferir caminho e permissões da sessão; não presumir que o cofre está montado.
