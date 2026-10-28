---
type: technical-debt
aliases:
  - "PeoplesCheck Serviço — débitos técnicos"
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
sources:
  - src/main/java/br/gov/df/peoplescheckapi
  - src/main/resources
  - .docker/Dockerfile
  - .jenkins-pipelines
  - pom.xml
---
# PeoplesCheck Serviço — débitos técnicos

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Separar dos fatos os riscos e as melhorias recomendadas. Gravidade: 🔴 alta, 🟡 média, 🟢 baixa. Os itens são recomendações, não comportamento implementado.

## Evidências
- Cada linha aponta a nota com a evidência de código.

## Informações confirmadas
**A. Segurança**
| # | Fato | Evidência | Gravidade | Recomendação |
|---|---|---|---|---|
| A1 | ✅ O seletor do CouchDB é montado por concatenação do dado recebido. A pré-validação limpa os não dígitos só numa cópia local e o repositório recebe o texto original; uma entrada com aspas e dígitos que formem um CPF válido passa pela validação e chega ao seletor. 🔶 O alcance real depende do CouchDB. | [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco]] | 🔴 | Normalizar `data` para só dígitos antes de qualquer uso e montar o seletor com serialização JSON (Jackson). |
| A2 | ✅ TLS sem validação de certificado e de host no cliente do CouchDB. | [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-CouchDB|CouchDB]] | 🔴 | Instalar a cadeia interna no *truststore* e remover o *bypass*. |
| A3 | ✅ Chave de API, URI do MongoDB e licença do New Relic em arquivos versionados; chave de exemplo em teste. | [[01-Sistemas/PeoplesCheck/Servico/08-Seguranca/PeoplesCheck-Servico-Seguranca-e-Autorizacao|Segurança]] | 🔴 | Rotacionar, mover para secrets do cluster e remover do histórico. |
| A4 | ✅ Chave única compartilhada, sem papéis; rotas administrativas usam a mesma chave. | idem | 🔴 | Chave por consumidor, separar administração, comparar em tempo constante. |
| A5 | ✅ `AuthenticationFilter` continua a cadeia (`finally`) após escrever 401. | idem | 🟡 | Retornar após o erro; usar entry point do Spring. |
| A6 | ✅ `/healthcheck` com detalhes e `/prometheus` públicos. | [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Observabilidade-e-Logs|Observabilidade]] | 🟡 | Restringir por rede ou remover detalhes. |
| A7 | ✅ O desafio revela o comprimento do primeiro nome e do da mãe antes da prova. | [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação]] | 🟡 | Máscara de tamanho fixo. |
| A8 | 🔶 CPF/CNPJ em query string e sem log de auditoria de consultas. | [[01-Sistemas/PeoplesCheck/Servico/06-API/PeoplesCheck-Servico-Catalogo-de-Endpoints|Endpoints]] | 🟡 | Enviar no corpo (POST) e registrar consultas (sem dado pessoal em claro). |

**B. Correção e robustez**
| # | Fato | Evidência | Gravidade | Recomendação |
|---|---|---|---|---|
| B1 | ✅ Serviços de validação são singletons com lista de etapas em campo de instância (`addValidation` + `clear()`): requisições concorrentes se interferem. | [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Arquitetura|Arquitetura]] | 🔴 | Montar a lista de etapas por chamada (variável local) ou injetar a lista imutável. |
| B2 | ✅ Filtro de data da contagem de tentativas tem a chave `expirationDate` duplicada: a janela de 24 h não é aplicada; só vale a limpeza. | [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco]] | 🟡 | Usar um único `Document` com `$gte` e `$lt` na mesma chave; criar índice/TTL. |
| B3 | ✅ Falha de gravação do desafio vira `NullPointerException`; não há tratador global de exceções. | [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Consulta-e-Geracao-de-Desafio|Fluxo de consulta]] | 🟡 | `@ControllerAdvice` e erros tipados (503/500 com mensagem). |
| B4 | ✅ CNPJ associado inapto/inexistente cai silenciosamente nos dados da PF. | [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|Fluxo de resposta]] | 🟡 | Devolver erro explícito ou indicador do tipo de resposta. |
| B5 | ✅ Desafio reutilizável após o sucesso. | idem | 🟡 | Invalidar após resposta correta ou expirar de fato (campo de vencimento). |
| B6 | 🔶 Verificar contagem e incrementar não é atômico. | idem | 🟡 | Incremento condicional atômico no Mongo. |
| B7 | ✅ `keys` e `data` sem validação (índices, `null`); `JuridicalPersonRepository` usa `docs[0]` e `Integer.parseInt` sem proteção. | [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Comparacao-de-Respostas|Comparação]] | 🟡 | Validação de entrada (`@Valid`) e checagem de vazios. |
| B8 | ✅ Campo `expirationDate` guarda a data de criação; `solution` não é usado. | [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Modelo-de-Dominio|Domínio]] | 🟢 | Renomear (`createdAt`) ou implementar vencimento. |
| B9 | ✅ Sem timeout nem resiliência nos clientes CouchDB e Mongo. | [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-CouchDB|CouchDB]] | 🟡 | Timeouts e retry controlado. |

**C. Código e manutenção**
| # | Fato | Gravidade | Recomendação |
|---|---|---|---|
| C1 | ✅ Código sem uso aparente: `CacheXpto`, `ChallengeValidate`, `JuridicalPersonChallengeAnswerValidate`, `findAllChallenge`, parâmetro `IChallengeQuestionMapper` do `PeopleController`, `IValidationContract` com constantes. | 🟢 | Remover ou implementar o desafio de CNPJ. |
| C2 | ✅ Dependências sem uso aparente (`spring-boot-starter-cache`, `javaee-api`, `jaxb-api`, `jakarta.xml.bind-api`, `reactor-test`, `springloaded`) e `devtools` no runtime. | 🟢 | Limpar o `pom.xml`. |
| C3 | ✅ Spring Boot 2.7.13 e Java 11 (fora de suporte aberto). | 🟡 | Planejar migração (Boot 3 / Java 17+). |
| C4 | ✅ Duplicação de cliente HTTP: `CouchDBHealthCheck` cria cliente e pool a cada chamada; `CouchDbClient` monta o cabeçalho Basic à mão além do provider. | 🟢 | Reutilizar o cliente único. |
| C5 | ✅ `printStackTrace` em vez de logger; sem arquivo de log configurado. | 🟢 | Usar SLF4J. |
| C6 | ✅ `Dockerfile` ignora testes e passa `-P SPRING_PROFILES_ACTIVE` literal; `tzupdater` baixa dados da internet no build. | [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Deploy-e-Ambientes|Deploy]] | 🟡 | Rodar testes no pipeline; corrigir perfil; fixar a base de fuso em artefato interno. |
| C7 | ✅ Sem JaCoCo; testes `@SpringBootTest` pesados e sem testes de controllers. | [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Testes-e-Cobertura|Testes]] | 🟡 | Medir cobertura e criar testes de contrato/concorrência. |

## Inferências e limitações
- A1 é ✅ para o caminho de código e 🔶 para a exploração efetiva (não testada).
- Nenhum item foi corrigido nesta análise (o código não foi alterado).

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/08-Seguranca/PeoplesCheck-Servico-Seguranca-e-Autorizacao|Segurança]] · [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Pendências e próximo passo
- Priorizar A1, A3, B1 e A2 com o dono do serviço.
