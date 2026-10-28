---
type: technical-debt
aliases:
  - "INGRESS-CGDF — débitos técnicos"
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
sources:
  - Dockerfile
  - nginx.conf
  - nginx-nonprod.conf
  - locations/
  - .jenkins-pipelines/
  - README.md
---
# INGRESS-CGDF — débitos técnicos

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Listar riscos e melhorias, separados dos fatos.

## Evidências
- Arquivos citados em cada linha; commit `a51459e`.

## Informações confirmadas
Fatos observados (✅):

| # | Fato | Onde |
|---|---|---|
| 1 | Imagem `nginx:alpine` sem versão fixa | `Dockerfile` |
| 2 | `HEALTHCHECK` do Dockerfile comentado | `Dockerfile` |
| 3 | 18 arquivos prod e 19 nonprod repetem os mesmos blocos, com duas variantes cada; sem `include` de modelo | `locations/` |
| 4 | Sem TLS, autenticação, limite de taxa nem timeouts configurados | [[01-Sistemas/INGRESS-CGDF/Nginx/08-Seguranca/INGRESS-CGDF-Nginx-Seguranca-e-Exposicao|Segurança]] |
| 5 | `X-Forwarded-Proto` e `X-Forwarded-Port` fixos em `http`/`80` no Keycloak e no IBS (nonprod); demais usam `$scheme` | `keycloak.conf`, `identity-broker-service.conf` |
| 6 | Health do Keycloak em nonprod usa o nome do serviço direto no `proxy_pass`, ao contrário das demais rotas (`set $upstream`) | `nonprod/keycloak.conf` |
| 7 | `deployment.params copy.yml` e dois arquivos de ambiente sem uso (`sandbox.env.yml`, `staging.env.yml`) versionados | `.jenkins-pipelines/` |
| 8 | Nomes inconsistentes: `sisconep.conf` (nonprod) × `sisconep-client.conf` (prod); `sedoc` só em nonprod; staging e sandbox com mesmo nome de contêiner | `locations/`, `deployment.params.yml` |
| 9 | Rotas de teste (`-test`) servidas pelo ingress de produção | `locations/prod/` |
| 10 | README é o modelo padrão do GitLab, sem descrição do projeto | `README.md` |
| 11 | Sem testes nem validação (`nginx -t`) no repositório | [[01-Sistemas/INGRESS-CGDF/Nginx/09-Qualidade/INGRESS-CGDF-Nginx-Testes-e-Cobertura|Testes]] |
| 12 | Blocos `stream` e health nonprod usam nomes literais, resolvidos na partida | `nginx*.conf`, `nonprod/keycloak.conf` |

## Inferências e limitações
Recomendações (🔶, não são fatos):
- Fixar a versão da imagem e habilitar o `HEALTHCHECK` (itens 1 e 2).
- Gerar os `location` a partir de um modelo ou usar `include` com variáveis, reduzindo a repetição (3).
- Alinhar `X-Forwarded-*` (5) e padronizar `set $upstream` no health do Keycloak (6).
- Remover arquivos sem uso e documentar o README (7 e 10).
- Rodar `nginx -t` no pipeline (11).
- Avaliar o impacto de um serviço ausente impedir a partida do Nginx (12), que é 🔶 não executado.

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
