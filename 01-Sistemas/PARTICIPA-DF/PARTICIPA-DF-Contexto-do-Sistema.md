---
type: system
aliases:
  - "PARTICIPA-DF — contexto do sistema"
system: PARTICIPA-DF
repository: participa-df-backend
status: inferido
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
sources:
  - src/OuvDF.sln
  - src/OuvDF.Api/Startup.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Enums
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Enums
---

# PARTICIPA-DF — contexto do sistema

Voltar: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|PARTICIPA-DF]] · Repositórios: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]]

> Visão de negócio **derivada só do backend**. Qualquer afirmação sobre finalidade legal ou organizacional é 🔶 até o time confirmar. O frontend não foi analisado.

## Objetivo
Dar o contexto mínimo para ler as notas técnicas: para que serve o sistema, quem o usa, o que ele faz e como se liga ao que está fora dele.

## Evidências
Backend `participa-df-backend`, commit `4901ad5`: nomes dos módulos, enums, perfis, mensagens de e-mail e de validação, jobs e integrações. Os nomes "Participa DF" e "OuvDF" aparecem como produto e como código (ver [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências]]).

## Informações confirmadas

### O que é
- ✅ Um sistema com **dois módulos** sobre a mesma base de usuários e unidades:
  1. **Ouvidoria (SO)**: cidadãos registram *manifestações* (denúncia, reclamação, solicitação, sugestão, informação, elogio), que são tramitadas entre unidades, respondidas e avaliadas. [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestacao]].
  2. **Serviço de Informação ao Cidadão (SIC)**: cidadãos registram *pedidos de acesso à informação*, com resposta, prorrogação, recursos em até três instâncias (a terceira na CGDF) e notificações de omissão de resposta. [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Pedido-e-Recurso|Pedido-e-Recurso]].
- ✅ "Participa DF" é o nome mostrado ao cidadão (e-mails, agente HTTP, produtor de eventos); o serviço de zeladoria é recusado "pelo Participa-DF"; `OuvDF` é o nome do código (🔶 histórico).

### Atores
| Ator | Como aparece no código | Nota |
|---|---|---|
| Cidadão (pessoa física) e pessoa jurídica | `PessoaFisica`, `PessoaJuridica`; manifestação pode ser anônima se a classificação permitir | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]] |
| Operador da Ouvidoria (SO) | `OperadorSO`, papel `OperadorSO`, perfil com funcionalidades 1 a 50 | idem |
| Operador do SIC | `OperadorSIC`, papel `OperadorSIC`, funcionalidades 201 a 220 | idem |
| Unidades (órgãos) | `Unidade` hierárquica, com tipos (ouvidoria-geral, controle de qualidade, unidade de ouvidoria, finalística, COACI, SIC superior) | [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] |
| Sistemas integrados | `OperadorWS` (API `v1`) | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]] |
| Rotinas automáticas | 10 jobs e um operador automático | [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]] |

### Ciclos principais
- Manifestação: registro → tramitação → resposta → avaliação, com prazos e prorrogação. [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Registro]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Tramitação e resposta]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-e-Prorrogacao|Prazos]].
- Pedido: registro (uma cópia por unidade) → resposta → recursos → omissão e CGDF. [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Registro]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Recursos]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Omissão]].
- Conta e acesso: cadastro, login, recuperação de senha, bloqueio por inconsistência/falecimento, exclusão de conta. [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Autenticação]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio]].
- Denúncias: uma IA (Iza) sugere se o relato é denúncia; a denúncia segue para triagem e interage com um sistema correcional por eventos. [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Atribuicao-e-Bloqueio-Externo|Bloqueio externo]].

### Contexto técnico
- API ASP.NET Core (.NET 5), SQL Server, NHibernate, MediatR; implantada em contêineres (Docker Swarm) por pipelines Jenkins. [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]] · [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Endpoints]].
- Riscos e dívidas: [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Debitos-Tecnicos]].

## Inferências e limitações
- 🔶 A base legal (por exemplo, a lei de acesso à informação) e o dono do sistema não constam no código.
- 🔶 O sistema parece pertencer à administração pública distrital (nomes CGDF, COACI, domínio de e-mail institucional), sem confirmação formal.
- ❓ Frontend, volumes, indicadores, usuários reais e a relação com o SICI (nenhuma evidência de relação).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Validar este contexto com o time e analisar o frontend (repositório a identificar).
