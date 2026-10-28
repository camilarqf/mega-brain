---
type: analysis-log
aliases:
  - "Registro de análise"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-28
commit_data: 2026-10-21
branch: master
---

# Registro de análise

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]]

## Base analisada
- Repositório: `portal-transparencia-frontend` (pasta local `PT2016_FrontEnd`; GitLab interno, endereço omitido). Branch `master`, `HEAD` `dca3e933ffd7e5bbfd173133e88d14f94304cb52` (2026-10-21, merge de `feature/refatoracao-acesso-minio`). Árvore de trabalho limpa.
- Pertencimento ao sistema `Portal-Transparencia` **confirmado pelo usuário em 2026-10-21** (o nome do remoto e a pasta `PT2016_*` eram indícios).
- Método: leitura estática; chamadas HTTP extraídas por script dos `*.service.js`; caminhos comparados por texto com os mapeamentos do Backend no commit `e98fcc38`. Testes, build e aplicação **não** foram executados.
- 974 arquivos em `src/`; 1013 arquivos versionados; 3676 commits.

## Regras de proteção aplicadas
- Valores de `config.json`, `src/app/config.js`, `.bowerrc`, IDs de medição do Google e endereços de infraestrutura **não registrados** (só nomes de chaves).

## Cobertura por lote
| Lote | Escopo | Status | Data | Notas geradas |
|---|---|---|---|---|
| 0 | Índice, stack, controle, atualização de repositório/catálogo | ✅ concluído | 2026-10-21 | [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index\|Index]], [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Stack-e-Dependencias\|Stack]], este registro, [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias\|Pendências]] |
| 1 | Arquitetura, build e perfis | ✅ concluído | 2026-10-21 | [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Arquitetura-AngularJS\|Arquitetura]], [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Build-e-Perfis-de-Ambiente\|Build e perfis]] |
| 2 | API e integrações | ✅ concluído (parâmetros/DTO não comparados) | 2026-10-21 | [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend\|Integração com a API]], [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API\|Catálogo de chamadas]], [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas\|Integrações externas]] |
| 3 | Módulos: Despesas, Receitas, Servidores, Orçamento | ✅ concluído (parcial: lógica dos controllers por amostragem) | 2026-10-21 | [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Despesas\|Despesas]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Receitas\|Receitas]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Servidores\|Servidores]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Orcamento\|Orçamento]] |
| 4 | Módulos: Licitações, Convênios, Patrimônio, Prestando Contas, Super Busca, Institucionais | ✅ concluído (parcial) | 2026-10-21 | [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Licitacoes-e-Contratos\|Licitações]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Convenios\|Convênios]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Patrimonio\|Patrimônio]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Prestacao-de-Contas\|Prestando Contas]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Super-Busca\|Super Busca]], [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Paginas-Institucionais-e-Navegacao\|Institucionais]] |
| 5 | Segurança, testes e débitos | ✅ concluído | 2026-10-21 | [[01-Sistemas/Portal-Transparencia/Frontend/08-Seguranca/Portal-Transparencia-Frontend-Seguranca-e-Privacidade\|Segurança]], [[01-Sistemas/Portal-Transparencia/Frontend/09-Qualidade/Portal-Transparencia-Frontend-Testes-e-Cobertura\|Testes]], [[01-Sistemas/Portal-Transparencia/Frontend/09-Qualidade/Portal-Transparencia-Frontend-Debitos-Tecnicos\|Débitos]] |

## Alterações em notas existentes (lote 0 e 2)
- `Portal-Transparencia-Repositorios`: linha do frontend (analisado, commit `dca3e933`).
- `Portal-Transparencia-Index`: componente frontend e atalhos.
- `Catalogo-de-Sistemas`: repositório `portal-transparencia-frontend` e estado.
- `Mapa-de-Integracoes`: 2 linhas do frontend (API do Backend e Google Analytics) e 2 hipóteses (serviço de busca; objetos em armazenamento/gerenciador).

## Próximo passo exato
Ver "Próximo passo exato" em [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]]: responder #3, #4 e #6; depois comparar parâmetros/DTO por módulo (Despesas e Prestando Contas primeiro).

## Histórico de estrutura
- 2026-10-27: pastas reorganizadas conforme a seção 1 do `BRAIN-RULES.md` (numeração fixa; melhorias do cofre, lote 3).
- 2026-10-28: frontmatter padronizado: título legível em `aliases` e tags reduzidas ao vocabulário controlado da seção 4 do `BRAIN-RULES.md` (melhorias do cofre, lote 5).
