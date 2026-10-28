---
type: analysis-log
aliases:
  - "Pendências — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: pendente
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
---
# Pendências — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]] · [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Registro-de-Analise|Registro de análise]]

## Objetivo
Dúvidas a confirmar com o time e lacunas da análise do frontend.

## Evidências
Origem em cada linha (lote/nota).

## Informações confirmadas
### Perguntas ao time
| # | Pergunta | Origem |
|---|---|---|
| 1 | Qual o desenho pretendido da autenticação? O arquivo não versionado `src/app/sessao-sso.service.js` (`sessaoSso`) é a refatoração em andamento? O backend passará a validar token? | Lote 2/3 |
| 2 | O `UsuarioDTO` devolvido pelo login expõe `nome`? (`ArquivoController` usa `vm.usuario.nome`; a claim do SSO é `nomePessoa`) | Lote 2 |
| 3 | Como a SPA é publicada (servidor web, proxy de `/api` e `/arquivos/<bucket>`, escolha do `--profile`)? O `INGRESS-CGDF` é o proxy? | Lote 0/1 |
| 4 | `apiPortal` e `apiSuperbusca` são usadas em algum lugar (injetadas em `exclusoesAPI`, sem chamada)? São resquício? | Lote 1 |
| 5 | A tela "Textos Portal" (fora do menu) foi desativada de vez? | Lote 2 |
| 6 | Quais validações de formulário os HTML aplicam (campos obrigatórios, tamanho máximo de imagem, máscaras)? | Lote 2 |
| 7 | Significado de negócio das categorias de arquivo 43–47 ("saibaMais"), 50–59 (URL única) e 55/56 (imagens)? (mesma pergunta 10 do backend) | Lote 2 |
| 8 | A tela de arquivos funciona sem categoria/ano filtrados (a URL de upload leva `null`)? | Lote 2 |
| 9 | O Portal (`portal-transparencia-frontend`) usa o Gerenciador pelo `apiGerenciador` (🔶) ou só se liga por banco e buckets? | Lote 1 |

### Lacunas da análise
- ❓ HTML das telas (formulários, tabelas, modais), `index.scss`, `login.css` e `assets/` não foram lidos em detalhe.
- ❓ Comportamento em execução: nada foi compilado nem executado.
- ❓ `src/app/sessao-sso.service.js` (não versionado) fora do escopo por decisão do usuário.
- ❓ Histórico do Git (motivos de `fix: corrige roteamento…`, `feat:alterando caminho`) não lido.

## Inferências e limitações
O frontend é consumidor do backend do mesmo sistema; as ligações com o `Portal-Transparencia` continuam 🔶.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Gerenciador-Portal/Backend/99-Controle/Gerenciador-Portal-Backend-Pendencias|Pendências do Backend]]

## Pendências e próximo passo
Resolver primeiro as perguntas 1, 3 e 4.
