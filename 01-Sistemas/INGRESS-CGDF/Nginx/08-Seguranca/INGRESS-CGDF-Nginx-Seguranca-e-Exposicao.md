---
type: security
aliases:
  - "INGRESS-CGDF — segurança e exposição"
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
sources:
  - nginx.conf
  - nginx-nonprod.conf
  - locations/
---
# INGRESS-CGDF — segurança e exposição

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Registrar o que o ingress controla (e o que não controla) em segurança. Sem segredos.

## Evidências
- Busca por `ssl`, `auth`, `allow`, `deny`, `limit_*` e `proxy_*_timeout` em toda a configuração: nenhuma ocorrência.

## Informações confirmadas
- ✅ Todo o tráfego é HTTP puro; não há `listen … ssl` nem certificados no repositório.
- ✅ O ingress não autentica nem autoriza: nenhuma rota tem `auth_*`, `allow`/`deny` ou limite de requisições. A proteção fica em cada serviço.
- ✅ Todas as rotas de teste de produção (`-test`) são servidas pelo mesmo ingress de produção, sem diferença de controle.
- ✅ `/minio/` aceita corpos de até 5 GB; as demais rotas, 50 MB.
- ✅ O health do Keycloak (porta de gestão 9000, caminho `/health/`) fica acessível pelo ingress em todos os ambientes.
- ✅ Repasse do IP do cliente em `X-Real-IP` e `X-Forwarded-For`.
- ✅ `X-Forwarded-Proto` fixo em `http` no Keycloak (todos os ambientes) e no IBS (nonprod); nas demais rotas vale `$scheme`.
- ✅ Nenhum segredo, senha ou token no repositório; os arquivos do pipeline guardam apenas identificadores de credencial (não reproduzidos).

## Inferências e limitações
- 🔶 O `X-Forwarded-Proto: http` fixo pode fazer o Keycloak gerar URLs `http` se o acesso externo for HTTPS, a menos que a camada à frente corrija o cabeçalho. Não verificado.
- ❓ Onde ocorre a terminação TLS, e se há firewall/WAF ou restrição de rede, não consta no repositório.
- ❓ Se a exposição do health do Keycloak e do MinIO pelo ingress é pública ou restrita à rede interna.

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/09-Qualidade/INGRESS-CGDF-Nginx-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/INGRESS-CGDF/Nginx/06-API/INGRESS-CGDF-Nginx-Catalogo-de-Rotas|Catálogo de rotas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
