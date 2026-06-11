# Contribuindo com o JurisBench-BR

Obrigado pelo interesse! Este projeto vive de comunidade — e as contribuições mais valiosas nem sempre são código.

## Formas de contribuir

### 1. ⭐ Divulgação
Estrele o repositório e compartilhe os resultados. Quanto mais gente souber que embeddings genéricos falham no domínio jurídico brasileiro, mais pressão existe para o ecossistema melhorar.

### 2. 🔱 Testar e submeter modelos
Faça um fork, adicione seu modelo ao dicionário `MODELS` em `jurisbench_v0.py`, rode e [submeta o resultado ao leaderboard](LEADERBOARD.md).

### 3. 🧠 Crítica metodológica
Issues questionando o desenho do benchmark (amostragem, métricas, vazamento lexical, vieses do corpus) são **contribuições de primeira classe**. Abra uma issue com o rótulo de discussão.

### 4. 📚 Novas tarefas, consultas e tribunais
A v1 precisa de:
- **Consultas em linguagem natural** (pergunta de leigo → jurisprudência relevante) — se você é da área jurídica, sua ajuda aqui vale ouro;
- **Novos tribunais** (TJSP, STF, TST...) com datasets públicos;
- **Julgados de relevância graduada** (mais de um documento relevante por consulta).

### 5. 💻 Código
Correções, otimizações e novas funcionalidades no harness de avaliação.

## Fluxo para PRs

1. Fork e branch a partir de `main`;
2. Mantenha o estilo do código existente (PEP 8, comentários em PT-BR);
3. Rode o lint antes de abrir o PR:
   ```bash
   pip install ruff
   ruff check .
   ```
4. Descreva **o que** muda e **por quê** — se alterar metodologia, explique o impacto nos números publicados;
5. PRs que alterem a metodologia de avaliação exigem discussão prévia em issue.

## Princípios do projeto

- **Honestidade primeiro** — limitações são documentadas, não escondidas;
- **Reprodutibilidade** — seed fixa, dados públicos, código aberto;
- **Dados públicos e legais** — apenas atos oficiais (Lei 9.610/98, art. 8º, IV) ou dados com licença explícita;
- **Test set privado** — parte da avaliação nunca é publicada, para manter o leaderboard confiável.

## Dúvidas?

Abra uma issue ou escreva para thalesandradees@gmail.com.
