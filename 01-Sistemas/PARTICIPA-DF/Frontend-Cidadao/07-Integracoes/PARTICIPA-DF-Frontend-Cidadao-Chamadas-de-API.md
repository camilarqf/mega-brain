---
type: api
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - participa-df
  - frontend-cidadao
  - api
  - consumo
sources:
  - src/app/core/services/api.service.ts
  - src/app/core/services/authentication.service.ts
  - src/app/core/services/usuario.service.ts
  - src/app/app.component.ts
  - src/app/pages
  - src/app/layout/components
---

# Frontend Cidadão — chamadas à API do backend

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Contrato do provedor: [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo de endpoints do Backend]]

## Objetivo
Listar, por área, os endpoints que o frontend **consome** (a nota `api` aqui descreve o uso, não o contrato; o contrato fica no backend).

## Evidências
Busca por `GET`, `POST`, `Download` da classe `Api` em todo `src/app` (commit `d250804`): 66 caminhos distintos. Todos os 66 aparecem (por correspondência de texto) nas notas de endpoints do backend ([[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Endpoints-Ouvidoria|Ouvidoria]], [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Endpoints-SIC|SIC]], [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo]]); a correspondência é textual, não confere verbo nem payload. Os três endpoints de recurso são montados dinamicamente (ver abaixo).

## Informações confirmadas
Todos os caminhos são relativos a `environment.apiUrl`. Verbo: **G** = GET, **P** = POST.

| Área | Verbo e caminho | Quem usa |
|---|---|---|
| Sessão | G `security/is-auth` · P `security/auth` · P `security/notify` | `AuthenticationService`, login, `AppComponent` |
| Desafio / bloqueio | G `security/count-try?data=` · G `security/check?data=` · P `security/challenge` · G `security/check-cpf-vinculado-pj?cpf&cnpj&aceiteResponsabilidade` | login, validar CPF/CNPJ, desafio |
| Configuração | G `configuration/front-end-urls` | `AppComponent` |
| Usuário | G `usuario` · G `usuario/detalhar` · G `v2/usuario` · P `usuario/alterar-senha` · P `usuario/recuperar-senha` · P `usuario/concluir-recuperacao-senha` | validação, conta, shell |
| Política LGPD | G `politica/vigente` · P `politica/aceitar-vigente` | validação |
| Conta PF | P `pessoa-fisica` · P `pessoa-fisica/existe` · P `pessoa-fisica/atualizar` · P `pessoa-fisica/desbloquear-dados-inconsistentes` · `necessidade-especial` | cadastro e desafio |
| Conta PJ | P `pessoa-juridica` · P `pessoa-juridica/existe` · P `pessoa-juridica/atualizar` · P `pessoa-juridica/atualizar-responsavel` · P `pessoa-juridica/desbloquear-dados-inconsistentes` · G `pessoa-juridica/historico-responsavel` · G `pessoa-juridica/tipo-entidade` | cadastro, desafio, histórico |
| Ouvidoria: registro | P `servico-ouvidoria/ia/assunto` · P `servico-ouvidoria/ia/classificacao` · G `servico-ouvidoria/assunto/por-palavra-chave/{termo}` · P `.../assunto/filtrar-por-palavra-chave-e-classificacao` (só na página de exemplo) · P `.../assunto/id` · P `.../classificacao/id` · P `.../tipo-entrada/id` · P `.../formulario/por-assunto` · G `.../regiao-administrativa` · P `.../arquivo/validar` · P `.../arquivo/enviar` · P `.../manifestacao` · P `.../manifestacao/integrada` · P `.../manifestacao/resumo` | fluxo de registro |
| Ouvidoria: acompanhamento | P `.../manifestacao/manifestante/itens-filtro` · P `.../manifestacao/manifestante/detalhe` · P `.../complementacao/responder` · P `.../complementacao/pro-ativa` · P `.../manifestacao/avaliar` · P `.../arquivo/download-manifestante` · P `.../manifestacao/exportar-pdf-manifestante` (PDF) · P `questionario` · P `questionario/responder` | caixa de entrada |
| SIC: registro | G `acesso-informacao/assunto` · P `acesso-informacao/pedido/unidades` · P `acesso-informacao/arquivo/validar` · P `acesso-informacao/pedido` · P `acesso-informacao/pedido/consultar-por-lote` | fluxo de pedido |
| SIC: acompanhamento | P `.../pedido/manifestante/itens-filtro` · P `.../pedido/manifestante/` · P `.../pedido/detalhar-por-manifestante` · P `.../pedido/acoes-autor` · P `.../pedido/detalhar-evento-pedido/` · P `.../pedido/exportar-pedido-usuario` (PDF) · P `.../arquivo/download` · G `.../recurso/justificativa` · P `.../questionario` · P `.../questionario/responder-pesquisa` | caixa de entrada |
| SIC: recursos (dinâmicos) | P `acesso-informacao/recurso/primeira-instancia/registrar` · `.../segunda-instancia/registrar` · `.../terceira-instancia/registrar` | `DetalharPedido` |

- ✅ Cabeçalhos: `Authorization: Bearer` (todas), `spinner` (controle do indicador de carregamento) e `Accept: application/pdf` no `Download`.
- ✅ Tratamento de erro: ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Arquitetura|Arquitetura]] (`400` → lista de notificações, `500` → modal).
- ✅ Contrato de erro esperado do backend: `ExceptionType`, `Notifications`, `ExceptionDetails` (`400`); `Message` (`500`); `Context` no `428`.
- ✅ Dados pessoais em URL: CPF/CNPJ sem máscara vão em query string nos GET de `security/*` (podem aparecer em logs de acesso).

## Inferências e limitações
- 🔶 Não há versionamento da API no frontend, exceto `v2/usuario`; as demais rotas usam o primeiro nível sem prefixo de versão.
- 🔶 `GET necessidade-especial` foi encontrado na busca textual; o chamador exato não foi aberto.
- ❓ Verbo e payload exatos de cada rota não foram comparados um a um com os controllers.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas|Integrações externas]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-Modulos/PARTICIPA-DF-Frontend-Cidadao-Rotas-e-Telas|Rotas-e-Telas]]

## Pendências e próximo passo
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]: comparar verbo e payload com os controllers quando o backend for atualizado.
