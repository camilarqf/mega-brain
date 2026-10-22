---
type: security
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - seguranca
sources:
  - src/main.py
  - src/Queries/query_hash_modelo.py
  - deploy/Jenkinsfile
  - deploy/Jenkinsfile.hom
  - Dockerfile
---
# Iza Api — segurança

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Registrar controles e riscos de segurança verificáveis no código, **sem reproduzir segredos, endereços ou dados reais** (BRAIN-RULES, seção 10).

## Evidências
- `src/main.py` (ausência de dependências de segurança, CORS ou middleware), `deploy/Jenkinsfile*`, `Dockerfile`.

## Informações confirmadas
- ✅ **Sem autenticação nem autorização:** nenhum endpoint exige credencial; `/docs`, `/openapi.json`, `/prometheus`, `/health-check`, `/assuntos` e os `hash_modelo_*` são abertos. A proteção depende da rede (ingress e rede interna; o ingress também não autentica, conforme [[01-Sistemas/INGRESS-CGDF/Nginx/06-Seguranca/INGRESS-CGDF-Nginx-Seguranca-e-Exposicao|Segurança do ingress]]).
- ✅ **Dados pessoais:** o `relato` é texto livre de cidadão e pode conter dados pessoais; a API não o grava nem o registra em log (o log de acesso não inclui o corpo). O relato é recebido por HTTP; TLS não é tratado na aplicação.
- ✅ **Validação de entrada:** só tipos (Pydantic); não há limite de tamanho do `relato`.
- ✅ **Metadados públicos:** o Swagger expõe nome e e-mail de um contato individual (`contact` em `FastAPI(...)`); dado pessoal em endpoint aberto.
- 🔴 **Segredo no repositório:** `deploy/Jenkinsfile` contém a URL completa de um webhook do Discord (com token) escrita no código; no `Jenkinsfile.hom` a linha está comentada, mas permanece no histórico. Valor omitido aqui. Recomenda-se revogar/rotacionar e mover para uma credencial do Jenkins.
- ✅ **Pipeline legado:** `allowAnyHosts = true` nas conexões SSH, registry por HTTP sem TLS e uso de credencial de usuário privilegiado de deploy (`root-…`, identificador do Jenkins); IPs de servidores fixos no código (omitidos).
- ✅ **Carga de modelos:** `joblib.load` desserializa arquivos de `/mnt/iza-modelos`; 🔶 quem escreve nesse diretório pode executar código na inicialização (os arquivos são tratados como confiáveis).
- ✅ **Imagem:** executa como o usuário padrão da imagem (sem `USER` no `Dockerfile`) e a base `python:3.12` não é fixada por resumo.
- 🔶 `GET /hash_modelo_*` lê e calcula MD5 do arquivo inteiro a cada chamada anônima; custo repetível por qualquer cliente com acesso à rede.

## Inferências e limitações
- ❓ Exposição de rede real (quem alcança `iza-api`), existência de TLS entre o consumidor e o serviço e base legal/consentimento para o envio do relato (já sinalizado na nota do `PARTICIPA-DF`).
- ❓ Se o webhook do Discord ainda é válido.

## Relacionamentos
- [[01-Sistemas/Iza/Api/05-API/Iza-Api-Catalogo-de-Endpoints|Catálogo de endpoints]] · [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Deploy-e-Ambientes|Deploy e ambientes]] · [[01-Sistemas/Iza/Api/08-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Tratar o webhook exposto (ação do dono do pipeline) e decidir se a API precisa de autenticação; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
