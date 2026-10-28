---
type: flow
aliases:
  - "SCI Frontend — fluxo da denúncia até a admissibilidade (visão do cliente)"
system: SCI
component: Frontend
repository: sci-frontend
status: inferido
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/pages/denuncias
  - src/app/pages/demanda
  - src/app/pages/jad
  - src/app/pages/encaminhados
  - src/app/store/services/perfil-entrada.service.ts
---
# SCI Frontend — fluxo da denúncia até a admissibilidade (visão do cliente)

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] · Visão do backend: [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo do backend]]

## Objetivo
Mostrar a sequência de telas e atores que o frontend oferece, da denúncia ao encaminhamento da admissibilidade. Só o lado do cliente foi verificado; o ponta a ponta com o backend não foi executado.

## Evidências
- Rotas e componentes de `pages/denuncias`, `pages/demanda`, `pages/jad`, `pages/encaminhados`; serviços `denuncia`, `demanda`, `jad`, `encaminhamento`.

## Informações confirmadas
1. **Denúncia.** `Apoio Correcional` abre `/pages/denuncias`, filtra, entra em `analisar/:id` e **aceita** ou **recusa** (motivo obrigatório). A denúncia vem do PARTICIPA-DF pelo backend (evento); o cliente só exibe e decide.
2. **Demanda.** `Autoridade Correcional` e `Apoio Correcional` trabalham demandas em `/pages/demanda` (cadastro, anexos, edição). O cliente **não** vincula a denúncia aceita a uma demanda na tela de análise.
3. **Tratar demanda.** A autoridade escolhe encaminhar ao processo de admissibilidade, ao MPTCE ou a ambos, com ou sem distribuir a um relator (`POST demanda/tratar`).
4. **Processo de admissibilidade (JAD).** A caixa de entrada por perfil mostra o processo; o cadastro (fatos, envolvidos, condutas, evidências) é concluído, o processo é distribuído a um analista, analisado, revisado (gestor, autoridade, revisor), a nota técnica é assinada e o processo é concluído ou encaminhado (`POST encaminhamento`) para outra unidade, com tela de recebidos, enviados e devolvidos. Detalhe em [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-JAD-Admissibilidade|JAD]] e [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Encaminhamento-e-Gerenciador|Encaminhamento]].
5. **Desfecho.** Estados finais no cliente: `PC` Processo concluído, `AE` Aguardando encaminhamento e `FES` Finalizado — encaminhado via SEI. A instauração de PIP sai de uma análise concluída (ver [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Ciclo-do-PIP|Ciclo do PIP]]).

## Inferências e limitações
- 🔶 A ordem acima é montada a partir de rotas, serviços e status; as transições reais estão no backend.
- 🔶 O histórico Git cita as branches `feat/analisar-denuncia-criar-demanda` e `ativar-denuncias`; o código atual de `analisar-denuncia` não cria demanda (aceitar/recusar apenas). Se a criação foi removida ou ficou em outra tela, não foi identificado.
- ❓ Como a denúncia aceita vira demanda (pendência 3 do backend) segue em aberto.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Denuncia-e-Demanda|Denúncia e demanda]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
