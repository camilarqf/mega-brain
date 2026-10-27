---
type: analysis-log
system: SICI
repository: sici-frontend
status: pendente
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
created: 2026-10-18
updated: 2026-10-18
tags:
  - sici
  - frontend
  - pendencias
  - duvidas
---

# Pendências — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Registro-de-Analise|Registro-de-Analise]] · Backend: [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendências do Backend]]

## Perguntas de negócio
- [ ] O sistema é publicado como "Integra" (aplicação no pipeline, prefixo `/integra`, logotipo)? Qual é o nome oficial a usar no vault? ([[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Perfis-e-Ambientes|Perfis-e-Ambientes]])
- [ ] A validação por QR Code deve ser **pública**? Hoje a página `/validacao` é pública, mas o endpoint exige token; e o QR Code do backend envia `c`, a página lê `codigo`. ([[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]])
- [ ] O perfil `DIRETOR` deve poder excluir (inativar) ação de controle? O frontend permite (`EXCLUIR_ACAO`), o backend só SUBCI e COORDENADOR.
- [ ] A exclusão de OS genérica deve ter tela? Existe no backend, sem uso no frontend.
- [ ] A tela `template-editor` ainda é usada? ([[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]])

## Perguntas técnicas
- [ ] Qual é o perfil de id `1` vinculado ao titular/substituto SUBCI? O id é o mesmo em todos os ambientes? ([[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Gestao-SUBCI-e-Perfis|Gestao-SUBCI-e-Perfis]])
- [ ] `GET /ordem-servico/por-acao/{id}` e `GET /fase/descricao-fase/listar` existem no backend? Não constam no catálogo documentado. ([[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]])
- [ ] `GET /os-acao-controle/gerar-pdf?id=` recebe id da OS ou do documento assinado? O frontend usa o id do documento assinado em alguns caminhos (OS genérica).
- [ ] O backend é idempotente para a segunda chamada `PUT alterarStatusOs {status: ENVIADA}`? O frontend envia duas. ([[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]])
- [ ] `GET /os-acao-controle/pesquisar` (S/D no backend) retorna `403` para COORDENADOR e AUDITOR nas telas que o usam?
- [ ] Qual é o valor/parâmetro real de `assinatura.url.validacao` em cada ambiente?
- [ ] Qual mecanismo de entrega está ativo por ambiente (cópia de estáticos por Jenkinsfile ou contêiner por `deployment.params.yml`)? O prefixo `/integra-dev/` é tratado pelo nginx?
- [ ] Posso remover o código sem uso listado em [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]] (D8)?
- [ ] Registrar `Google Fonts` (folha de estilos de CDN) como serviço externo no catálogo ou ignorar?

## Verificações que exigem execução (fora da análise estática)
- [x] `ng build` (sucesso, com avisos) e `ng test` (não compila por `keycloak.service.ts`; 3 specs rodados: 1 passa, 2 falham) — executados em 2026-10-18, ver [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]].
- [ ] Decidir: remover/corrigir o `KeycloakService` e corrigir os 2 specs para a suíte rodar.
- [ ] `npm audit` e conferência de versões instaladas.
- [ ] Reproduzir D1 (URL sem barra) e D2 (envio duplicado) no navegador.
- [ ] Testar o fluxo de assinatura (popup, `postMessage`, fechamento antes de concluir).
- [ ] Comparar DTOs do frontend (`src/core/models`) com os do backend.
