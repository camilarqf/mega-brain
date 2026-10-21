---
type: system
system: INGRESS-CGDF
status: confirmado
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
tags:
  - ingress
  - nginx
  - contexto
sources:
  - Dockerfile
  - nginx.conf
  - nginx-nonprod.conf
  - .jenkins-pipelines/deployment.params.yml
---
# INGRESS-CGDF — contexto do sistema

Voltar: [[01-Sistemas/INGRESS-CGDF/INGRESS-CGDF-Index|Índice do sistema]]

## Objetivo
Ponto de entrada HTTP (e TCP para o RabbitMQ) das aplicações da CGDF em Docker Swarm: um Nginx que recebe as requisições, escolhe o serviço pelo prefixo do path e repassa a requisição. Não contém regra de negócio.

## Evidências
- Repositório `ingress-controller`, commit `a51459e` (ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Registro-de-Analise|Registro de análise]]).
- `Dockerfile` (imagem `nginx:alpine`), `nginx.conf` (produção), `nginx-nonprod.conf` (sandbox e staging) e `locations/**`.

## Informações confirmadas
- ✅ O repositório contém só configuração: um Dockerfile, duas configurações principais do Nginx, os arquivos `location` por aplicação e os parâmetros do pipeline Jenkins. Não há código de aplicação nem testes.
- ✅ O `ENVIRONMENT` do contêiner escolhe a configuração: `production`/`prod` usa `nginx.conf`; `nonprod`, `nonproduction`, `staging`, `sandbox`, `homolog` e `homologacao` usam `nginx-nonprod.conf`; qualquer outro valor encerra o contêiner com erro.
- ✅ Roteamento por prefixo de path para serviços Swarm resolvidos por DNS interno. Ver [[01-Sistemas/INGRESS-CGDF/Nginx/05-API/INGRESS-CGDF-Nginx-Catalogo-de-Rotas|Catálogo de rotas]] e [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Arquitetura|Arquitetura]].
- ✅ Proxy TCP na porta 5672 para dois nós RabbitMQ. Ver [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Proxy-TCP-RabbitMQ|Proxy TCP RabbitMQ]].

## Inferências e limitações
- ❓ Dono do serviço, SLA, domínios/URLs públicos e quem está na frente deste Nginx (balanceador, TLS) não constam no repositório; o usuário não informou o dono.
- 🔶 Os sistemas atrás de cada rota foram associados pelo nome do serviço, sem acesso às stacks que os definem. Ver [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Integracoes-com-Upstreams|Integrações com upstreams]].

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
