---
type: module
system: SICI
repository: sici-backend
status: pendente
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tipo: modulo
sistema: SICI
commit: 1871e32
atualizado: 2026-10-18
cobertura: parcial
fontes:
  - api/ordemServicoGenerica/OrdemServicoGenericaController.java
  - application/usecase/ordemServicoGenerica/*
  - application/usecase/assinatura/AssinarOrdemServicoGenerica.java
  - domain/model/OrdemServicoGenerica.java
tags: [sici, modulo, os-generica]
---

# OS Genérica

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]], [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]]

> OS **sem ação de controle**: documento livre composto de **artigos**, **descrições de fase** com datas, **anexos**, equipe (coordenador e auditores), área executora e um texto de "OS vinculada". Usa o mesmo ciclo de status e a mesma assinatura das OS de ação de controle (modelo `GENERICA`, id 7).

## Endpoints — `/ordem-servico-generica` ✅
**Nenhum** endpoint tem `@PreAuthorize`: o import existe, mas não é usado. Todos exigem só autenticação.

| Método | Rota | Use case |
|---|---|---|
| POST | `/salvar-os` | `CriarOrdemServicoGenerica.criar` |
| GET | `/listar` | `ListarOrdemServicoGenerica` |
| GET | `/pesquisar` | `PesquisarOrdemServicoGenerica` |
| PUT | `/atualizar/{id}` | `AtualizarOrdemServicoGenerica.atualizar` |
| PUT | `/alterarStatusOs/{id}` | `AlterarStatusOrdemServicoGenerica` |
| DELETE | `/excluir/{id}` | `ExcluirOrdemServicoGenerica.excluir` |
| GET | `/gerar-pdf` | `GerarPdfOrdemServicoGenerica` (minuta via [[01-Sistemas/SICI/Backend/07-Integracoes/Integracoes-Externas|serviço de PDF]]) |

Assinatura e download: `POST /assinaturas/assinar-os-generica/{id}` e `GET /assinaturas/{id}/download-generica` — ver [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]].

## Regras ✅
- **Criação**: artigos obrigatórios (lista não vazia) e área executora obrigatória; trata coordenador e auditores (ramos para ausentes); grava artigos, descrições e anexos (tabelas V29, V30, V51).
- **Atualização** (`@Transactional`): artigos obrigatórios; bloqueia se já houver assinatura com data ou status ASSINADA (`OsAssinadaNaoPodeSerAtualizadaException`).
- **Status**: `OrdemServicoGenerica.alterarStatusOs`, a mesma máquina de [[01-Sistemas/SICI/Backend/02-Dominio/Enums-e-Estados|Enums-e-Estados]], com motivo obrigatório na devolução. `AlterarStatusOrdemServicoGenerica` tem o mesmo `if` vazio da OS comum.
- **Assinatura**: SUBCI titular ou substituto vigente; código `HMAC("OSG:"+id)`; numeração no **mesmo sequencial anual** das OS de ação.

## Lacunas ✅
- ⚠️ `ExcluirOrdemServicoGenerica.excluir` apaga direto, **sem verificar assinatura**, ao contrário de `ExcluirOrdemServico`. Uma OS genérica assinada pode ser excluída. Documento e numeração ficam órfãos, porque `TB_DOCUMENTO.ID_DOCUMENTO_RELACIONADO` não tem FK e a V44 removeu a FK da numeração.
- ⚠️ Mesma brecha de `PUT /alterarStatusOs` com `status = ASSINADA` sem assinatura (ver [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]], lacuna #2).
- `osVinculada` é texto livre e não referencia uma OS.

Cobertura parcial: os ramos de coordenador/auditores e o mapeamento de artigos e anexos não foram lidos linha a linha.
