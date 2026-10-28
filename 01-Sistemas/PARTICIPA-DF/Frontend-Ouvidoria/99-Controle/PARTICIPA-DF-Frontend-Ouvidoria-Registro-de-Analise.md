---
type: analysis-log
aliases:
  - "Registro de análise — Frontend Ouvidoria"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
created: 2026-10-18
updated: 2026-10-28
commit_data: 2026-09-09
branch: master
---

# Registro de análise — Frontend Ouvidoria

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]]

## Base analisada
- Repositório: `participa-df-ouv-frontend` (endereço omitido); branch `master`; commit `9d8ecdb` (2026-09-09); working tree limpa.
- Método: leitura estática. Testes não executados, aplicação não iniciada, build não executado.

## Regras de proteção aplicadas
- Não foram reproduzidos endereços de ambiente, hosts de serviços, chave de aplicação nem credenciais encontradas no código; só a existência e o arquivo.
- O código não foi alterado.

## Mapeamento de verificação
- Caminho e verbo das chamadas de `Api.GET/POST` comparados por script com as notas `Backend/05-API` (commit `4901ad5`): 127 combinações iguais; 7 caminhos legados sem correspondência; `v2/usuario/false/true` parcial.
- Rotas de `app.routes.js` conferidas contra templates e controllers existentes: 3 `templateUrl` ausentes e controllers `navegacaoCtrl`/`criarFormularioCtrl` inexistentes.

## Decisões de classificação
- Repositório associado ao `PARTICIPA-DF` por: README ("módulo de Ouvidoria do Participa DF"), caminho do remoto (`.../participa-df/participa-df-ouv-frontend`) e uso dos mesmos pontos do backend (`security/token-retrieve/{sessionId}`, `configuration/front-end-urls`, `servico-ouvidoria/*`). Associação autorizada pela responsável ao aprovar o plano em 2026-10-18; segue como pendência a confirmação do nome oficial.
- Componente nomeado `Frontend-Ouvidoria` (rótulo provisório). Pasta e prefixo `PARTICIPA-DF-Frontend-Ouvidoria-`.

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Cadastro, retomada e esqueleto | ✅ concluído | 2026-10-18 | Index, este registro, Pendencias; atualizados Catálogo, Repositórios e Index do sistema |
| 1 | Fundamentos | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Stack-e-Dependencias|Stack]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Arquitetura|Arquitetura]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Perfis-e-Ambientes|Perfis-e-Ambientes]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Rotas-e-Telas|Rotas-e-Telas]] (todas parciais) |
| 2 | Segurança e sessão | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/08-Seguranca/PARTICIPA-DF-Frontend-Ouvidoria-Seguranca-e-Sessao|Seguranca-e-Sessao]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Fluxo-Autenticacao]] |
| 3 | Fluxos e módulos de negócio | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Caixa-de-Entrada-e-Detalhamento|Fluxo-Caixa-de-Entrada-e-Detalhamento]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Registro-por-Operador|Fluxo-Registro-por-Operador]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Prorrogacao-de-Prazo|Fluxo-Prorrogacao-de-Prazo]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Gerencial|Modulo-Gerencial]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Dashboards-e-Relatorios|Modulo-Dashboards-e-Relatorios]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Conta-por-Operador|Modulo-Conta-por-Operador]] |
| 4 | API consumida e integrações | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas|Integracoes-Externas]] |
| 5 | Qualidade | ✅ concluído | 2026-10-18 | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Testes-e-Cobertura|Testes-e-Cobertura]], [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Debitos-Tecnicos]] |

## O que não foi coberto
- Telas e templates `.html` lidos só por controller/campos principais (detalhe da manifestação, registro, conta, gerencial, dashboards); os 8 relatórios `rel_*` sem rota e o `painel-interativo` por amostra; `app/shared/*` (diretivas de formulário) e `views-dist.js` (gerado).
- Cabeçalhos de versão de `assets/lib/*` e conteúdo dos `.pubxml` e dos estágios Jenkins linha a linha.
- Comparação de **payloads** e códigos de retorno com os controllers do backend (só caminho e verbo foram conferidos por texto: 99 de 107 caminhos iguais).
- Origem do `sessionId` e o front-end de login; o front-end SIC.
- Execução de build, aplicação e testes (não há testes).

## Próximo passo exato
Fim do plano aprovado (lotes 0 a 5). Próximos: (1) responder as Pendências com o time; (2) rodar `git diff 9d8ecdb..HEAD --stat` e invocar `atualizar-documentacao` se houver mudanças; (3) lote 6 — ler os templates de conta/registro e as diretivas `shared/`; (4) lote 7 — confrontar payloads e códigos de ação com o backend; (5) sugerir `sincronizar-brain` (nenhum `git add`/commit/push foi executado).

## Histórico de estrutura
- 2026-10-27: pastas reorganizadas conforme a seção 1 do `BRAIN-RULES.md` (numeração fixa; melhorias do cofre, lote 3).
- 2026-10-28: frontmatter padronizado: título legível em `aliases` e tags reduzidas ao vocabulário controlado da seção 4 do `BRAIN-RULES.md` (melhorias do cofre, lote 5).
