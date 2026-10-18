# Convenções do Mega Brain

- Um sistema de negócio vive em `01-Sistemas/<Sistema>/`.
- A documentação técnica de cada repositório vive em uma subpasta do sistema (`Backend/`, `Frontend/`, `Servico-X/`).
- A visão de negócio compartilhada fica na raiz do sistema e só deve ser consolidada quando houver evidências.
- Não criar pastas de componentes ainda não analisados: citá-los em `Repositorios.md` como `não analisado`.
- Links internos Obsidian: preferir `[[Caminho/Nota|Título]]` em caso de nomes ambíguos.
- Frontmatter recomendado: `type`, `system`, `repository`, `status`, `analyzed_commit`, `updated`.
- Estados: `confirmado`, `inferido`, `nao-identificado`, `pendente`.
- Separar fatos presentes no código de recomendações de melhoria.
- Sempre preservar o histórico e tornar o próximo lote retomável por outra sessão.
- Antes de sincronizar, classificar o conteúdo e confirmar se o remoto é autorizado.
