---
name: sincronizar-brain
description: Verifica estado Git do cofre e orienta uma sincronização segura após revisão de conteúdo e conflitos.
---

# Sincronizar Brain

1. Verificar caminho do cofre e `git status --short`, branch, remoto e `git diff --stat`; não executar alterações de imediato.
2. Alertar se houver dados sensíveis, código interno, dumps, segredos, tokens, grandes binários ou documentação institucional sem autorização.
3. Conferir `.gitignore` e arquivos staged/unstaged, inclusive arquivos novos. Mostrar plano e pedir aprovação explícita para cada operação de alteração Git.
4. Se aprovado, obter alterações remotas com `git fetch`; inspecionar divergências, conflitos e risco de sobrescrita. Não usar `reset --hard`, `push --force` ou comandos destrutivos.
5. Somente após validação e aprovação: stage seletivo, commit, integração com remoto e push. Nunca prometer que sincronização foi concluída sem checar o resultado.
6. Informar hash de commit final, arquivos enviados e pendências. Não sincronizar material institucional com remoto pessoal.
