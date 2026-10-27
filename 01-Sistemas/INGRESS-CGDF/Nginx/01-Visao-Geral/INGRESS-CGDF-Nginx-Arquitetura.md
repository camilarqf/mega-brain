---
type: architecture
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
tags:
  - ingress
  - nginx
  - arquitetura
sources:
  - Dockerfile
  - nginx.conf
  - nginx-nonprod.conf
  - locations/common/health-check.conf
---
# INGRESS-CGDF — arquitetura do Nginx

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Descrever como a configuração está organizada e como a imagem escolhe o que executar.

## Evidências
- `Dockerfile`: copia `locations/common/` para `/etc/nginx/locations/`, `locations/prod/` e `locations/nonprod/` para subpastas, e as duas configurações principais para `/etc/nginx/nginx-production.conf` e `/etc/nginx/nginx-nonproduction.conf`.
- `nginx.conf` e `nginx-nonprod.conf`: blocos `stream` e `http`.

## Informações confirmadas
- ✅ **Seleção da configuração na partida**: o `CMD` copia uma das duas configurações para `/etc/nginx/nginx.conf` conforme `ENVIRONMENT` (padrão da imagem: `nonprod`) e inicia o `nginx` em primeiro plano. Valor não suportado imprime erro e sai com código 1. Mapa dos valores em [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Build-Deploy-e-Ambientes|Build, deploy e ambientes]].
- ✅ **Bloco `http`** (igual nas duas configurações, exceto a porta): `resolver` apontando para o DNS interno do Docker (`ipv6=off valid=10s`), um `map` de `Upgrade` para `Connection` (usado pelo WebSocket do `painel-ouvidoria`) e um único `server` que inclui `health-check.conf` e `locations/<ambiente>/*.conf`.
  - Produção escuta em `8080`; nonprod escuta em `80`.
- ✅ **Bloco `stream`**: porta `5672` para um upstream `rabbitmq_cluster`. Ver [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Proxy-TCP-RabbitMQ|Proxy TCP RabbitMQ]].
- ✅ **Um arquivo `location` por aplicação**, com duas variantes de rota (principal e teste em produção; staging e sandbox em nonprod). Ver [[01-Sistemas/INGRESS-CGDF/Nginx/06-API/INGRESS-CGDF-Nginx-Catalogo-de-Rotas|Catálogo de rotas]] e [[01-Sistemas/INGRESS-CGDF/Nginx/05-Fluxos/INGRESS-CGDF-Nginx-Fluxo-de-Roteamento-de-Requisicao|Fluxo]].
- ✅ **Health check próprio**: `GET /healthcheck` responde `200 ok` sem log de acesso, sem consultar upstream.
- ✅ `EXPOSE 80` e `EXPOSE 8080` no Dockerfile; o `HEALTHCHECK` do Dockerfile está comentado.

## Inferências e limitações
- 🔶 O uso de `set $upstream` com `proxy_pass http://$upstream` faz o Nginx resolver o nome em tempo de requisição (via `resolver`), então o contêiner sobe mesmo que um serviço não exista. Comportamento padrão do Nginx; não executado aqui.
- ❓ Quem fica à frente deste Nginx (TLS, domínio, balanceador) não consta no repositório.

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Stack-e-Dependencias|Stack e dependências]] · [[01-Sistemas/INGRESS-CGDF/Nginx/09-Qualidade/INGRESS-CGDF-Nginx-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
