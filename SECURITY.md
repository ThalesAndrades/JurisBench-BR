# Política de Segurança

## Reportando vulnerabilidades

Encontrou uma vulnerabilidade no código do benchmark ou no processo de avaliação?

- **Preferencial:** use o [relato privado de vulnerabilidade do GitHub](https://github.com/ThalesAndrades/JurisBench-BR/security/advisories/new) (*Security → Report a vulnerability*);
- **Alternativa:** e-mail para thalesandradees@gmail.com com o assunto `[SECURITY] JurisBench-BR`.

**Não abra issue pública** para vulnerabilidades — issues são públicas e expõem o problema antes da correção. Respondemos em até 7 dias.

## Execução de código remoto de modelos (`trust_remote_code`)

Carregar um modelo do HuggingFace com `trust_remote_code=True` **executa código arbitrário do repositório do modelo na sua máquina**. Por isso:

- O `jurisbench_v0.py` roda com `trust_remote_code` **desabilitado por padrão**. Para modelos que exigem código próprio, habilite explicitamente com `JURISBENCH_TRUST_REMOTE_CODE=1` — apenas se você auditou e confia no repositório do modelo;
- Submissões ao leaderboard que exijam `trust_remote_code` são avaliadas **em ambiente isolado (sandbox), sem acesso ao conjunto de teste privado em disco nem a credenciais**, e podem ser recusadas se o código do repositório não for auditável.

## Escopo

Este repositório contém apenas código de avaliação e dados públicos (decisões judiciais — atos oficiais, Lei 9.610/98, art. 8º, IV). Não há segredos, credenciais ou dados pessoais sensíveis no repositório nem no histórico git. O conjunto de teste privado é mantido fora deste repositório.
