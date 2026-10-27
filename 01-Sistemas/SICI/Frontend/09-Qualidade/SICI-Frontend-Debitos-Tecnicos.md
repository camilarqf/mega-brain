---
type: technical-debt
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - debito-tecnico
  - riscos
sources:
  - src/core/services/ordem-servico.service.ts
  - src/app/pages/ordem-servico/ordem-servico-listar/acao-controle-os.component.ts
  - src/app/pages/ordem-servico/visualizar-pdf/visualizar-pdf.component.ts
  - src/app/app-routing.module.ts
  - src/app/pages/acao-controle/acao-controle-routing.module.ts
  - src/app/app.module.ts
  - src/core/services/auth/auth.service.ts
  - src/core/services/pdf-hash.service.ts
  - src/app/pages/gestao-subci/gestao-subci-cadastrar/gestao-subci-cadastrar.component.ts
---

# Débitos técnicos e riscos — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]], [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]] · Backend: [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Debitos-Tecnicos|Debitos do Backend]]

> Esta nota separa **fatos do código** (✅, coluna Evidência) de **recomendações**. `ng build` e `ng test` foram executados (ver [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]]); a aplicação não foi executada, então os efeitos em tempo de execução continuam 🔶.

## Objetivo
Listar débitos, riscos e melhorias do frontend, com evidência e recomendação.

## Evidências
Arquivos em `sources` e as demais notas do componente.

## Achados
| # | Severidade | Achado (fato no código) | Evidência | Efeito provável 🔶 | Recomendação |
|---|---|---|---|---|---|
| D1 | 🟠 Alta | URLs montadas sem barra: `${urlApi}os-acao-controle/pesquisar` em `buscarOrdemServicoBase` e `getById` | `ordem-servico.service.ts` | com `urlApi=/api`, a chamada vai a `/apios-acao-controle/pesquisar`; prorrogação e `visualizarOrdemServicoPorId` podem falhar ou receber o `index.html` do fallback do nginx | corrigir para `/os-acao-controle/...`; teste de serviço |
| D2 | 🟠 Alta | Envio de OS dispara `PUT alterarStatusOs` duas vezes (efeito NgRx e chamada direta no componente) | `acao-controle-os.component.ts` (`enviarOrdemServico`), `visualizar-pdf.component.ts`, `ordem-servico.effects.ts` (`enviarOrdemServico$`) | requisições duplicadas; resultado depende da idempotência do backend | manter uma só via (o efeito) |
| D3 | 🟠 Alta | Rota pública `validacao` chama endpoint que exige token; o `401` leva ao login | `app-routing.module.ts`, `validar-assinatura-os.component.ts`, `auth-error.interceptor.ts`, catálogo do backend | o QR Code não valida para quem não está logado; parâmetro do QR (`c`) difere do lido (`codigo`) | decidir validação pública (backend + frontend) e alinhar o parâmetro |
| D4 | 🟡 Média | Rota `cadastrar-acao-controle` declara `permissions` sem `canActivate: [GuardPerfil]` | `acao-controle-routing.module.ts` | qualquer autenticado abre a tela por URL | adicionar o guard (o backend já restringe a criação) |
| D5 | 🟡 Média | Token, conta e perfis em `localStorage` e `sessionStorage`; contexto da assinatura (inclui corpo de OS genérica) em `localStorage` | `auth.service.ts`, `assinatura-popup-context.service.ts` | exposição a XSS; dados que sobram se o popup fecha | avaliar `sessionStorage` somente, cookie `HttpOnly` via backend ou BFF; limpar contexto ao fechar |
| D6 | 🟡 Média | Restrições de perfil do frontend não coincidem com o backend (ex.: `EXCLUIR_ACAO` inclui DIRETOR; `GET /os-acao-controle/pesquisar` é S/D no backend e usado por todos os perfis) e o backend deixa 46 endpoints abertos | [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]], catálogo do backend | botões que dão `403`; falsa sensação de proteção | gerar a matriz de permissões de uma fonte única (backend) e revisar S1/S4 |
| D7 | 🟡 Média | `gestao-subci` vincula o perfil de id **fixo `1`** ao cadastrar titular/substituto | `gestao-subci-cadastrar.component.ts` | perfil errado se ids mudarem por ambiente; cadastro sem perfil se a 2ª chamada falhar | enviar o perfil por nome/código ou criar endpoint atômico |
| D8 | 🟡 Média | Código sem uso: `KeycloakService`, `TokenService`, `UserInfoService`, `DescricaoFaseService`, `HeaderService`/`HeaderServiceService`, `abrirModalAssinar`/`AssinarOrdemServico`/`assinarOs` (assina sem reautenticação) | buscas textuais por referência | confusão sobre o fluxo real; `KeycloakService` não compila se incluído (falta `environment.keycloak`) | remover ou isolar; validar com o time |
| D9 | 🟡 Média | Lista geral carrega **todas** as OS e genéricas (`size: 10000`) e pagina no cliente; também recarrega tudo após cada assinatura | `ordens-servico-listagem.component.ts` | lentidão e consumo de memória com o crescimento da base | paginação e filtros no servidor (como na lista de genéricas) |
| D10 | 🟢 Baixa | Registro duplicado de store/efeitos (`StoreModule.forRoot` + `provideStore`; `EffectsModule.forRoot` + `provideEffects`); `acoesControle` e `acaoControle` usam o mesmo reducer | `app.module.ts` | efeitos podem rodar em dobro; estado redundante | unificar no padrão *standalone* ou NgModule |
| D11 | 🟢 Baixa | `PdfHashService.validarAssinatura` usa `window.location.origin + '/validacao'` e ignora o *base href* | `pdf-hash.service.ts` | link quebrado em `/integra/` e `/integra-dev/` | usar `document.baseURI`/Router |
| D12 | 🟢 Baixa | `setTimeout` de 300 ms entre gravar dados da ação no estado e navegar | `acao-controle-listar.component.ts` | corrida se o estado demorar | navegar após a confirmação do estado ou passar por parâmetros |
| D13 | 🟠 Alta | **`ng test` não roda** (erro TS em `keycloak.service.ts`); dos 3 specs que compilam, 2 falham (`pTooltip`, `HttpClient` sem provider); 4 specs de uma asserção; cobertura medida 5%; guards, assinatura e transições sem teste | [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]] | regressões não detectadas (ex.: D1, D2) | cobrir serviços, guards e fluxo de assinatura primeiro |
| D14 | 🟢 Baixa | Tipagem fraca: ~187 ocorrências de `any`/`as any` fora dos testes; componentes de 1600 e 790 linhas (`ordem-servico-cadastrar`, `-atualizar`) | busca textual; contagem de linhas | manutenção difícil | extrair serviços/estado do formulário e tipar os DTOs |
| D15 | 🟢 Baixa | Nomes inconsistentes: pasta `reducers/ordem-servico-generica.reducer.ts/` (diretório com extensão de arquivo), `header.service.service.ts`, `ordem-serviço-editar-cancelamento` (acento), `unidade-aditoria.*`, mistura PT/EN | árvore de `src` | dificulta busca | padronizar nomes |
| D16 | 🟢 Baixa | `npm ci --legacy-peer-deps` no build; `ng build` emite avisos (orçamento da folha de fontes, módulos CommonJS do CKEditor, 9 regras CSS ignoradas) | `.docker/Dockerfile`; execução do build | conflitos de dependências ocultos; otimização reduzida | resolver *peer deps* e tirar a flag |
| D17 | 🟢 Baixa | `nginx.conf` sem cabeçalhos de segurança (CSP, HSTS, X-Frame-Options); mapa de *base href* só trata `/integra` | `nginx.conf` | menor defesa em profundidade; `/integra-dev/` sem tratamento | revisar cabeçalhos e o mapa |
| D18 | 🟢 Baixa | Pipelines versionam caminhos de servidores de deploy e dependem de credencial do Jenkins por montagem CIFS (valores não reproduzidos aqui) | `.jenkins-pipelines/Jenkinsfile.*` | informação de infraestrutura no repositório | mover parâmetros sensíveis para o Jenkins/variáveis |
| D19 | 🟢 Baixa | Arquivo de falha da JVM (`hs_err_pid*.log`) aparece como não rastreado na raiz | `git status` | risco de commit acidental | adicionar ao `.gitignore` |

## Inferências e limitações
- Severidade é avaliação desta análise (impacto × probabilidade estimados sem execução); validar com o time.
- Débitos que dependem do backend (S1 a S5) estão no [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Debitos-Tecnicos|débito do Backend]].
- Cobertura parcial: templates, SCSS e a maior parte da lógica dos componentes grandes não foram revisados linha a linha.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]] · [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]] · [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Gestao-SUBCI-e-Perfis|Gestao-SUBCI-e-Perfis]] · [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
