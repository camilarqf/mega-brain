---
type: analysis-log
aliases:
  - "SCI Frontend — pendências"
system: SCI
component: Frontend
repository: sci-frontend
status: pendente
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
---
# SCI Frontend — pendências

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] · [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Registro-de-Analise|Registro de análise]]

## Perguntas ao time
| # | Pergunta | Origem |
|---|---|---|
| 1 | Os endpoints chamados pelo cliente e ausentes no `sci-backend` (denúncia por id, download de anexo da denúncia, `pessoa/processos`, `pessoa-juridica/pesquisar`, `unidade/has-assessor-autoridade`, `processo-admissibilidade/encaminhar`, `pip/recuperar-admissibilidade`, `revisao-pip/admitir-revisao-preliminar`) existem em outra branch, repositório ou implantação? Quais são código morto? | Lote 3 |
| 2 | Quem pode aceitar e recusar denúncia: Apoio Correcional (cliente) ou Autoridade Correcional (política do backend)? | Lote 2 |
| 3 | As rotas `denuncias` e `encaminhados` devem ter restrição de perfil no cliente? | Lote 1 |
| 4 | A página pública `/validacao` deve funcionar sem login? O endpoint `POST documento/validar` exige autenticação. Como o QR Code chega à página? | Lote 2 |
| 5 | A que sistema `participaUrl` aponta em cada ambiente (frontend do `PARTICIPA-DF`)? | Lote 3 |
| 6 | Quem é o dono do painel Power BI e o link é público? A URL pode ir para `environment`? | Lote 3 |
| 7 | O vínculo denúncia aceita → demanda é feito em alguma tela? (branches `feat/analisar-denuncia-criar-demanda` e `ativar-denuncias` no histórico.) Repete a pergunta 3 do backend. | Lote 4 |
| 8 | Siglas `AAS` e `AG` na lista do investigador: de qual status vêm? | Lote 2 |
| 9 | Expansão de SCI, JAD, MPTCE e significado de "matriz" e "providências adicionais". Repete perguntas 1, 4 e 5 do backend. | Lote 2 |
| 10 | A API é servida só por HTTPS? `apiUrl` termina com `/` nos três ambientes (as URLs são concatenadas sem barra)? | Lote 3 |

## Respondidas
- Pergunta 1 do backend (repositório do frontend): é o `sci-frontend` (2026-10-19, confirmado pelo usuário).

## Riscos para tratar fora do cofre
Itens 1 a 5 de [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Debitos-Tecnicos|Débitos técnicos]] (contrato desalinhado, autorização só no cliente, sessão, painel BI, ausência de testes).

## Próximo passo exato
Lote 5 opcional (ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Registro-de-Analise|Registro de análise]]).
