# 🏆 Leaderboard — JurisBench-BR

Tarefa v0: **cabeçalho de ementa → corpo de teses da ementa** (STJ) · 200 consultas · corpus de 1.500 decisões deduplicado · métricas nDCG@10 e Recall@10 · [conjunto de avaliação congelado](data/v0_eval_ids.json).

> ⚠️ **Retratação (12/06/2026):** a tabela de 11/06 foi retirada — o script original apontava para o campo errado do dataset (a certidão de julgamento, idêntica em todas as decisões) e seus números não eram reproduzíveis. Detalhes no [README](README.md). Os resultados abaixo saem do pipeline público atual.

## Resultados oficiais (v0 — 12/06/2026)

| # | Modelo | Tipo | nDCG@10 | Recall@10 | Avaliado em |
|---|---|---|---:|---:|---|
| 1 | **BM25** | Lexical (baseline, 1994) | **0,693** | **0,825** | 12/06/2026 |
| 2 | BM25 + MiniLM (RRF) | Híbrido | 0,613 | 0,760 | 12/06/2026 |
| 3 | [MiniLM-multilingual](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | Embedding multilíngue | 0,017 | 0,040 | 12/06/2026 |
| — | [bge-m3](https://huggingface.co/BAAI/bge-m3) · [serafim-335m](https://huggingface.co/PORTULAN/serafim-335m-portuguese-pt-sentence-encoder-ir) · [multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) | Embeddings | *em avaliação* | *em avaliação* | — |

> 🎯 **O desafio em aberto:** nenhum embedding superou o BM25 até hoje. O primeiro modelo que conseguir entra no **Hall da Fama** abaixo.

## 🏛 Hall da Fama

*Vazio. Seja o primeiro a vencer o BM25 no domínio jurídico brasileiro.*

## 📨 Como submeter seu modelo

1. Rode a parte pública localmente (`python jurisbench_v0.py` com seu modelo no dicionário `MODELS`) para validar a integração;
2. Abra uma [issue de submissão](https://github.com/ThalesAndrades/JurisBench-BR/issues/new?template=02-jurisbench-submissao.yml) com o link do modelo no HuggingFace;
3. Avaliamos no conjunto completo (incluindo a **parte privada**, para evitar overfitting/contaminação) e publicamos o resultado aqui, normalmente em até 7 dias.

### Regras

- O modelo precisa estar acessível (HuggingFace público ou gated com acesso concedido a nós);
- Aceitamos embeddings (bi-encoders) na v0; rerankers terão trilha própria na v1;
- O resultado publicado é o do conjunto completo — pode diferir do número que você obteve na parte pública;
- Resultados são publicados com data e hash de revisão do modelo, para reprodutibilidade;
- Modelos que exigem `trust_remote_code` são avaliados em ambiente isolado (sandbox) e podem ser recusados se o código do repositório não for auditável — veja a [política de segurança](SECURITY.md).

---

*Mantido pela [THM Tecnologia](APRESENTACAO-THM.md) · dúvidas: thalesandradees@gmail.com*
