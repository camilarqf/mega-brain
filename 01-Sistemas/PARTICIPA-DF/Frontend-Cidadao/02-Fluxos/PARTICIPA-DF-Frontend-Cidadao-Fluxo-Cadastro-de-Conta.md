---
type: flow
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - participa-df
  - frontend-cidadao
  - fluxo
  - conta
  - pessoa-fisica
  - pessoa-juridica
sources:
  - src/app/pages/conta/conta-routing.module.ts
  - src/app/pages/conta/validar-cpf/validar-cpf.component.ts
  - src/app/pages/conta/validar-cnpj/validar-cnpj.component.ts
  - src/app/pages/conta/desafio-pesssoa-fisica/desafio-pesssoa-fisica.component.ts
  - src/app/pages/conta/criar-conta-pessoa-fisica/criar-conta-pessoa-fisica.component.ts
  - src/app/pages/conta/criar-conta-juridica/criar-conta-juridica.component.ts
  - src/app/pages/conta/atualizar-dados/atualizar-dados.component.ts
  - src/app/pages/conta/historico-cpf-vinculado/historico-cpf-vinculado.component.ts
---

# Frontend Cidadão — fluxo de cadastro e manutenção de conta

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]]

## Objetivo
Descrever como o cidadão cria conta (pessoa física ou jurídica), atualiza dados e vincula CPF a CNPJ.

## Evidências
Arquivos em `sources`, commit `d250804`. Cobertura `parcial`: lidas as telas de validação de CPF, desafio, criação de PF e as chamadas das demais.

## Informações confirmadas
```mermaid
flowchart TD
    A[direcionar-usuario: PF ou PJ] -->|PF| B[validar-cpf modo 0]
    A -->|PJ| C[validar-cnpj] --> D[validar-cpf modo 2 + aceite de responsabilidade]
    B -->|POST pessoa-fisica/existe| E{Existe?}
    E -->|não| F[desafio-pessoa-fisica]
    F -->|desafio resolvido| G[criar-conta-pessoa-fisica: POST pessoa-fisica]
    E -->|sim| H[Backend notifica a existência: notificarExistencia = true]
    D -->|GET security/check-cpf-vinculado-pj| I[desafio] --> J[criar-conta-pessoa-juridica: POST pessoa-juridica]
```
- ✅ **PF:** `validar-cpf` verifica se o CPF já tem conta (`pessoa-fisica/existe`) e as tentativas (`security/count-try`); o desafio pessoal (`security/check`/`security/challenge`) precede o formulário; o cadastro envia `POST pessoa-fisica` (inclui `necessidadeEspecial`; senha com opções de visibilidade e aceite da política LGPD em modal).
- ✅ **PJ:** `validar-cnpj` (`pessoa-juridica/existe`, `security/check`, `security/count-try`), depois `validar-cpf` em modo PJ com `aceiteResponsabilidade` obrigatório (`requiredTrue`) e `security/check-cpf-vinculado-pj?cpf&cnpj&aceiteResponsabilidade`. O cadastro usa `GET pessoa-juridica/tipo-entidade` e `POST pessoa-juridica`.
- ✅ **Manutenção:** `conta/atualizar-dados` lê `GET usuario/detalhar` e grava em `pessoa-fisica/atualizar` ou `pessoa-juridica/atualizar`; `historico-cpf-vinculado` lista `pessoa-juridica/historico-responsavel`; a troca do CPF responsável usa o modo 4 do desafio (`pessoa-juridica/atualizar-responsavel`).
- ✅ **Home:** exibe um aviso às empresas de que é obrigatório vincular um CPF válido ao CNPJ.
- ✅ Todos os modos usam `ValidarCPFEnum` e `returnUrl` (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/02-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Autenticacao|Fluxo-Autenticacao]]).
- ✅ CPF/CNPJ são formatados e "limpos" por `FormataDocumentoService` antes de ir à URL (`security/count-try?data=`, `security/check?data=`): o documento trafega em **query string**.

## Inferências e limitações
- 🔶 As regras de validação do CPF/CNPJ (algoritmo) e de força de senha estão em validadores locais não lidos; o backend valida de novo (PeoplesCheck, ver [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas do Backend]]).
- ❓ O que o backend faz ao receber `notificarExistencia: true` (por exemplo, enviar e-mail ao titular) não está neste repositório; conferir no Backend.
- ❓ Telas `mensagem-conta`, `direcionar-usuario` e `atualizar-dados/:id` não foram lidas em detalhe.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/04-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-API-e-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas-de-API]]

## Pendências e próximo passo
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]].
