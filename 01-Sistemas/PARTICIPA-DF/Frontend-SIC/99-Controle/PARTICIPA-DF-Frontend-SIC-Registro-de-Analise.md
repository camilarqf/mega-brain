---
type: analysis-log
aliases:
  - "Registro de análise — Frontend SIC"
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
created: 2026-10-18
updated: 2026-10-28
commit_data: 2026-10-14
branch: master
---

# Registro de análise — Frontend SIC

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]]

## Base analisada
- Repositório: `participa-df-sic-frontend` (endereço omitido); branch `master`; commit `5518a81` (2026-10-14); working tree limpa.
- Método: leitura estática. Testes não executados (não há), aplicação não iniciada, build não executado.

## Regras de proteção aplicadas
- Não foram reproduzidos endereços de ambiente, valores das variáveis do Jenkins nem a chave de aplicação encontrada no interceptor; só a existência e o arquivo.
- O código não foi alterado.

## Decisões de classificação
- Repositório associado ao `PARTICIPA-DF` por: caminho do remoto (grupo `participa-df`), uso dos mesmos pontos do backend (`security/token-retrieve/{sessionId}`, `configuration/front-end-urls`), consumo de `operador-sic/*` e `acesso-informacao/*` (todos presentes no catálogo do backend) e nome `Participa DF Sic Frontend` em `.jenkins-pipelines/deployment.params.yml`. Associação autorizada pela responsável ao aprovar o plano em 2026-10-18; segue como pendência a confirmação do nome oficial e da correspondência com `SistemaSicDF`.
- Componente nomeado `Frontend-SIC` (rótulo provisório). Pasta e prefixo `PARTICIPA-DF-Frontend-SIC-`.

## Mapeamento de verificação
- Caminho e verbo das chamadas `Api.GET/POST` comparados por script (texto) com as notas `Backend/05-API` (commit `4901ad5`): 77 caminhos distintos (67 de chamadas literais `Api.*` + 10 montados em *strings* dos controllers); 76 encontrados; `v2/usuario/true/false` só tem o prefixo `v2/usuario` no catálogo (mesma situação do front de Ouvidoria). Payloads e códigos de retorno não conferidos.
- Rotas de `app.routes.js` conferidas contra templates e controllers: 1 rota (`/bloquear-usuario`) sem template nem controller.

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Cadastro, retomada e esqueleto | ✅ concluído | 2026-10-18 | Index, este registro, Pendencias; atualizados Catálogo, Repositórios e Index do sistema |
| 1 | Fundamentos | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Stack-e-Dependencias|Stack]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Arquitetura|Arquitetura]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Perfis-e-Ambientes|Perfis-e-Ambientes]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Rotas-e-Telas|Rotas-e-Telas]] (todas parciais) |
| 2 | Segurança e sessão | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao|Fluxo-Autenticacao]] |
| 3 | Fluxos e módulos de negócio | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Caixa-de-Entrada-e-Detalhamento|Caixa-de-Entrada-e-Detalhamento]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Prorrogacao-e-Reencaminhamento|Prorrogacao-e-Reencaminhamento]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Registro-por-Operador|Registro-por-Operador]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Gerencial|Modulo-Gerencial]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Conta-por-Operador|Modulo-Conta-por-Operador]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Super-Busca|Modulo-Super-Busca]] |
| 4 | API consumida e integrações | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Integracoes-Externas|Integracoes-Externas]]; atualizado o `Mapa-de-Integracoes` |
| 5 | Qualidade | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]] |

## O que não foi coberto
- Templates `.html` lidos só por controller/títulos de etapa (detalhamento do pedido, registro por operador, conta, gerencial, super-busca); diretivas de formulário de `app/shared/*` e `views-dist.js` (gerado) não analisados.
- Cabeçalhos de versão de `assets/lib/*` (exceto AngularJS, `angular-route` e Bootstrap) e busca exaustiva de XSS nos templates.
- Comparação de **payloads** e códigos de retorno com os controllers do backend (só caminho e verbo foram conferidos por texto: 76 de 77).
- Regras de negócio do SIC no backend (prazos, situações, classificação, sigilo, perfis): fora do escopo deste repositório.
- Origem do `sessionId` e o front-end de login; nome oficial do front-end e correspondência com `SistemaSicDF`.
- Execução de build, aplicação e testes (não há testes). Valores dos `*.env.yml` e a chave de aplicação não foram lidos/reproduzidos.

## Próximo passo exato
Fim do plano aprovado (lotes 0 a 5). Próximos: (1) responder as Pendências com o time; (2) rodar `git diff 5518a81..HEAD --stat` e invocar `atualizar-documentacao` se houver mudanças; (3) lote 6 — ler os templates de conta/registro/detalhamento e as diretivas `shared/`; (4) lote 7 — confrontar payloads e códigos de ação com os controllers do backend; (5) sugerir `sincronizar-brain` (nenhum `git add`/commit/push foi executado).

## Histórico de estrutura
- 2026-10-27: pastas reorganizadas conforme a seção 1 do `BRAIN-RULES.md` (numeração fixa; melhorias do cofre, lote 3).
- 2026-10-28: frontmatter padronizado: título legível em `aliases` e tags reduzidas ao vocabulário controlado da seção 4 do `BRAIN-RULES.md` (melhorias do cofre, lote 5).
