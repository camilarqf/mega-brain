---
name: documentar-sistema
description: Analisa o código de um repositório e documenta o sistema no Mega Brain por lotes pequenos e rastreáveis, com plano aprovado antes de escrever. Use para documentar um repositório novo ou retomar uma análise interrompida.
---

# Documentar sistema

Regras e definições estão em `BRAIN-RULES.md` (seções citadas abaixo); não repeti-las aqui.

1. **Acesso e identificação.** Confirmar o caminho absoluto do vault e o repositório analisado (acesso ao vault: seção 11). Sem acesso, informar a limitação e pedir acesso; não presumir o conteúdo. Identificar sistema, componente e repositório no `Catalogo-de-Sistemas.md` e no índice pertinente (seção 6, N0–N1). Se o sistema não estiver cadastrado, propor o cadastro (ID) no plano; não deduzir associação pelo nome.
2. **Retomar.** Ler o registro de análise e as pendências do componente, se existirem, e o "próximo passo exato". Comparar `analyzed_commit` com `git rev-parse HEAD`; se mudou, verificar os arquivos de `sources` alterados (seção 5) e tratar as notas afetadas como desatualizadas, encaminhando-as à Skill `atualizar-documentacao`. Não refazer lotes concluídos.
3. **Inventário.** Stack, módulos, controllers e rotas, serviços, entidades, persistência, integrações e dependências, autenticação, validações, testes e fluxos. Nunca reproduzir segredos, credenciais ou dados reais (seção 10).
4. **Integrações.** Procurar clientes, adaptadores e configuração de chamadas a outros sistemas ou serviços; registrar consumidor, provedor, tecnologia, contrato e direção quando verificáveis (seção 7). Sem evidência, é hipótese.
5. **Plano.** Apresentar o plano de lotes pequenos: para cada nota, o `type` (seção 2), o nome (seção 3), as notas existentes que serão atualizadas em vez de duplicadas (seção 8) e os links previstos. **Obter aprovação antes de escrever.**
6. **Documentar um lote por vez**, com evidências (repositório, commit, arquivo, símbolos) e a distinção ✅/🔶/❓ (seção 5). Regra de negócio só com evidência no código.
7. **Gerar as notas** com frontmatter da seção 4, nomes da seção 3 e links da seção 8. Atualizar o `Mapa-de-Integracoes` quando houver integração (seção 7). Preservar o material existente e não alterar o código.
8. **Validar** com `python <vault>/scripts/validar-brain.py`; sem Python, conferir à mão tipo, campos, datas, links e nomes únicos. Corrigir antes de encerrar o lote.
9. **Fechar o lote:** atualizar índice, registro de análise, pendências e `coverage`, com o próximo passo exato (seção 8), e relatar o que não foi coberto.
10. Backend e frontend do mesmo sistema ficam em pastas próprias; integrar fluxos somente após verificar ambos.
11. Não executar `git add`, commit nem push; ao final, sugerir `sincronizar-brain` (seções 9 e 10).
