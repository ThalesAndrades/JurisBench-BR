<div align="center">

# ⚖️ JurisBench-BR

### O primeiro benchmark aberto de busca semântica jurídica em português brasileiro

**Um algoritmo de 1994 vence todos os embeddings de IA modernos na jurisprudência brasileira — por margens enormes.**

[![Licença](https://img.shields.io/badge/licen%C3%A7a-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/ThalesAndrades/JurisBench-BR/actions/workflows/ci.yml/badge.svg)](https://github.com/ThalesAndrades/JurisBench-BR/actions/workflows/ci.yml)
[![PRs bem-vindos](https://img.shields.io/badge/PRs-bem--vindos-brightgreen.svg)](CONTRIBUTING.md)
[![Leaderboard](https://img.shields.io/badge/%F0%9F%8F%86-leaderboard-orange.svg)](LEADERBOARD.md)

🇧🇷 Português · [🇺🇸 English](README-en.md)

</div>

---

## 💥 TL;DR

Testamos embeddings abertos numa tarefa real de busca jurídica brasileira (recuperar a decisão correta do STJ entre 1.500 documentos). **O BM25, um algoritmo de busca por palavra-chave de 30 anos atrás, segue imbatível:**

![Resultados JurisBench-BR v0](assets/results_v0.svg)

| Modelo | nDCG@10 | Recall@10 |
|---|---:|---:|
| 🥇 **BM25 (busca lexical, 1994)** | **0,693** | **0,825** |
| BM25 + MiniLM (híbrido RRF) | 0,613 | 0,760 |
| MiniLM-multilingual *(embedding mais baixado do mundo)* | 0,017 | 0,040 |
| bge-m3, serafim-335m, multilingual-e5-large | *em avaliação* | *em avaliação* |

*Resultados de 12/06/2026 no [conjunto congelado](data/v0_eval_ids.json); reproduza com `python jurisbench_v0.py`.*

> **Se o seu RAG jurídico usa embeddings genéricos, ele provavelmente está pior do que a busca por palavra-chave que você substituiu.**

> ⚠️ **Correção (12/06/2026):** a tabela publicada em 11/06 foi **retratada**. O script original usava o campo `acordao` do dataset como documento-alvo, mas esse campo contém apenas a certidão de julgamento padrão ("Vistos e relatados... acordam os Ministros..."), quase idêntica em todas as decisões — a tarefa era insolúvel e os números não eram reproduzíveis pelo código publicado. A tarefa foi reimplementada exatamente como descrita (cabeçalho → corpo de teses da ementa), o conjunto de avaliação foi congelado e todos os números desta tabela saem do pipeline público. *Honestidade primeiro.*

⭐ **Esse resultado te surpreendeu?** Deixe uma estrela para acompanhar as próximas versões e [compartilhe no X](https://twitter.com/intent/tweet?text=Um%20algoritmo%20de%201994%20vence%20todos%20os%20embeddings%20de%20IA%20na%20busca%20jur%C3%ADdica%20brasileira.%20Benchmark%20aberto%3A&url=https%3A%2F%2Fgithub.com%2FThalesAndrades%2FJurisBench-BR) ou no [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fgithub.com%2FThalesAndrades%2FJurisBench-BR).

---

## 🔍 Por que isso importa

Milhares de lawtechs, escritórios e tribunais brasileiros estão construindo sistemas de RAG (Retrieval-Augmented Generation) sobre embeddings **treinados majoritariamente em inglês e em texto genérico**. O vocabulário, a morfologia e a estrutura documental do direito brasileiro (ementas, acórdãos, teses numeradas no padrão CNJ) estão **fora da distribuição de treino** de todos esses modelos.

O JurisBench-BR existe para:

1. **Medir** — quantificar, com metodologia aberta e reproduzível, o quão ruim a busca semântica genérica é no domínio jurídico BR;
2. **Comparar** — dar à comunidade um leaderboard público para qualquer modelo novo;
3. **Melhorar** — servir de meta objetiva para modelos especializados (o primeiro alvo: **superar o BM25**, coisa que nenhum embedding aberto consegue hoje).

## 🧪 A tarefa (v0)

Busca jurídica realista: dado o **cabeçalho temático** de uma ementa do STJ (ex.: *"DIREITO PENAL. AGRAVO REGIMENTAL. TRÁFICO PRIVILEGIADO..."*), recuperar o **corpo da ementa correspondente** (as teses numeradas no padrão CNJ, *"1. ... 2. ..."*) em um corpus de **1.500 decisões reais**, deduplicado por conteúdo. São **200 consultas**, avaliadas com **nDCG@10** e **Recall@10**. O conjunto de avaliação é **congelado** em [`data/v0_eval_ids.json`](data/v0_eval_ids.json) — qualquer pessoa reproduz exatamente os mesmos números, mesmo que o dataset upstream mude.

Os dados são decisões judiciais públicas do Superior Tribunal de Justiça — atos oficiais, sem proteção autoral (Lei 9.610/98, art. 8º, IV), via dataset [`celsowm/jurisprudencias_stj`](https://huggingface.co/datasets/celsowm/jurisprudencias_stj).

## ⚡ Reproduza em 3 comandos

Roda no Colab gratuito (T4) ou em CPU local:

```bash
git clone https://github.com/ThalesAndrades/JurisBench-BR.git && cd JurisBench-BR
pip install -r requirements.txt
python jurisbench_v0.py   # resultados em results/
```

Quer testar **seu próprio modelo**? Adicione o repositório HuggingFace ao dicionário `MODELS` em [`jurisbench_v0.py`](jurisbench_v0.py) e rode. Depois [submeta ao leaderboard](LEADERBOARD.md) 🏆.

> 🔒 Modelos que exigem `trust_remote_code` (código próprio no repositório do modelo) ficam **desabilitados por padrão**: habilite com `JURISBENCH_TRUST_REMOTE_CODE=1` apenas para repositórios que você auditou — veja a [política de segurança](SECURITY.md).

Dica: baixe modelos e datasets antecipadamente com o [hfdownloader](https://github.com/ThalesAndrades/HuggingFaceModelDownloader):

```bash
hfdownloader download BAAI/bge-m3
hfdownloader download celsowm/jurisprudencias_stj --dataset
```

## 🏆 Leaderboard e test set privado

Para evitar overfitting e contaminação, **parte do conjunto de avaliação é privada**. Submissões são avaliadas por nós e publicadas no [LEADERBOARD.md](LEADERBOARD.md).

👉 **[Submeta seu modelo pelo formulário](https://github.com/ThalesAndrades/JurisBench-BR/issues/new?template=02-jurisbench-submissao.yml)** — leva 2 minutos.

## 🧭 Limitações conhecidas da v0 (honestidade primeiro)

- A sobreposição lexical entre cabeçalho e corpo favorece o BM25; a **v1 incluirá consultas em linguagem natural** (pergunta de leigo → jurisprudência), onde a vantagem lexical desaparece.
- Consulta e documento vêm da **mesma ementa** (cabeçalho → teses); é uma tarefa de pareamento intra-documento, não de busca entre documentos distintos.
- Fonte única (STJ) e corpus de 1.500 documentos; a v1 expandirá para TJSP/STF.
- 1 documento relevante por consulta (a v1 terá julgados de relevância graduada).
- `google/embeddinggemma-300m` ainda não avaliado (repositório gated); bge-m3, serafim-335m e multilingual-e5-large estão em avaliação após a correção de 12/06.

Achou outra limitação? [Abra uma issue](https://github.com/ThalesAndrades/JurisBench-BR/issues) — crítica metodológica é contribuição de primeira classe aqui.

## 🗺 Roadmap

- [x] **v0** — tarefa cabeçalho→corpo, baselines BM25 + 3 embeddings *(jun/2026)*
- [ ] **v1** — consultas em linguagem natural, mais tribunais (TJSP/STF), test set privado formalizado
- [ ] **Leaderboard automatizado** — submissões via PR com avaliação no test set privado
- [ ] **JurisEmbed-BR** — modelo aberto da THM com meta pública declarada: **superar o BM25 nesta tarefa**

## 🤝 Como contribuir

Toda contribuição conta — e as mais valiosas nem exigem código:

- ⭐ **Estrela e divulgação** — quanto mais gente souber que embeddings genéricos falham no jurídico BR, melhor para o ecossistema;
- 🔱 **Fork e teste seu modelo** — depois submeta o resultado;
- 🧠 **Crítica metodológica** — issues questionando o desenho do benchmark são bem-vindas;
- 📚 **Novas tarefas e tribunais** — veja o [guia de contribuição](CONTRIBUTING.md).

## 📖 Como citar

```bibtex
@misc{jurisbenchbr2026,
  author       = {Andrades, Thales},
  title        = {JurisBench-BR: um benchmark aberto de recupera{\c{c}}{\~a}o sem{\^a}ntica jur{\'i}dica em portugu{\^e}s brasileiro},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/ThalesAndrades/JurisBench-BR}}
}
```

Ou use o arquivo [`CITATION.cff`](CITATION.cff) (o GitHub gera a citação automaticamente no botão *"Cite this repository"*).

## 📜 Licença

- **Código:** [Apache 2.0](LICENSE)
- **Dados:** decisões judiciais públicas — atos oficiais, sem proteção autoral (Lei 9.610/98, art. 8º, IV)

---

<div align="center">

Mantido pela [**THM Tecnologia**](APRESENTACAO-THM.md) — IA local e soberania de dados para o mercado brasileiro.

*Thales Andrades · thalesandradees@gmail.com*

[![Star History Chart](https://api.star-history.com/svg?repos=ThalesAndrades/JurisBench-BR&type=Date)](https://star-history.com/#ThalesAndrades/JurisBench-BR&Date)

</div>
