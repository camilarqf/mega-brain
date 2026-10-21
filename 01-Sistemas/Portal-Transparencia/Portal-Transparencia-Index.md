---
type: index
system: Portal-Transparencia
status: pendente
updated: 2026-10-21
tags:
  - portal-transparencia
  - moc
  - sistema
---
# Portal da Transparência — índice do sistema

## Objetivo
Ponto de entrada do sistema de negócio **Portal-Transparencia** (Portal da Transparência; o pacote Java é `br.gov.df.transparencia` e o PDF gerado se identifica como "Portal da Transparência"). Só o backend foi analisado (ver [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Repositorios|Repositórios]]).

## Evidências
- Cadastro: [[Catalogo-de-Sistemas|Catálogo de sistemas]] (ID `Portal-Transparencia`, cadastrado em 2026-10-19 conforme o nome informado pelo usuário).
- Documentação técnica do backend: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] (commit `e98fcc38`; módulos de negócio no commit `9434e58f`).

## Informações confirmadas
| Componente | Estado | Entrada |
|---|---|---|
| `portal-transparencia-backend` (pasta local `PT2016_BackEnd`) | analisado (lotes 0 a 8 e atualização para `e98fcc38`; leitura estática; cobertura parcial) | [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] |
| frontend | não analisado; repositório não identificado | — |

Atalhos do backend:
- [[01-Sistemas/Portal-Transparencia/Backend/08-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Débitos técnicos e riscos]]
- [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]] (inclui `/storage/*`)
- Segurança aprofundada: [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]] · [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]
- Módulos por área: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Receita|Receita]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Servidores-e-Remuneracao|Servidores-e-Remuneracao]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Licitacoes-e-Contratos|Licitacoes-e-Contratos]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Convenios|Convenios]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Patrimonio|Patrimonio]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Prestacao-de-Contas|Prestacao-de-Contas]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Orcamento-e-Documentos-Publicados]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados|Apoio-e-Atualizacao-de-Dados]]
- [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Registro-de-Analise|Registro de análise]] · [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|Pendências]]

## Inferências e limitações
- 🔶 O backend serve consultas públicas (despesa, receita, servidores e remuneração, licitações e contratos, convênios, patrimônio, prestação de contas) a um frontend não identificado; os cabeçalhos CORS e o `x-client-id` obrigatório indicam consumo por navegador.
- ❓ Frontend e demais componentes do sistema não foram identificados; o contexto de negócio (atores, objetivo oficial) não foi consolidado por falta de evidência no código.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]] · [[Home|Home]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|Pendências]].
