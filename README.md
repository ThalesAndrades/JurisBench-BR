# JurisBench-BR ⚖️

**Benchmark de recuperação semântica jurídica em português brasileiro** — mantido pela [THM Tecnologia](APRESENTACAO-THM.md).

## O experimento (v0)

Tarefa realista de busca jurídica: dado o **cabeçalho temático** de uma ementa do STJ (ex.: *"DIREITO PENAL. AGRAVO REGIMENTAL. TRÁFICO PRIVILEGIADO..."*), recuperar o **corpo da decisão correspondente** (teses numeradas no padrão CNJ) em um corpus de 1.500 decisões reais. 200 consultas; métricas nDCG@10 e Recall@10.

Os dados são decisões judiciais públicas do Superior Tribunal de Justiça — atos oficiais, sem proteção autoral (Lei 9.610/98, art. 8º, IV).

## Resultados (v0 — 11/06/2026)

| Modelo | nDCG@10 | Recall@10 |
|---|---:|---:|
| **BM25 (busca lexical, anos 1990)** | **0,771** | **0,895** |
| bge-m3 (estado da arte multilíngue) | 0,441 | 0,620 |
| serafim-335m (estado da arte PT) | 0,170 | 0,260 |
| MiniLM-multilingual (embedding mais baixado do mundo) | 0,040 | 0,080 |

**Conclusão:** nenhum embedding aberto disponível supera a busca lexical no domínio jurídico brasileiro. O vocabulário, a morfologia e a estrutura documental do direito brasileiro estão fora da distribuição de treino de todos os modelos genéricos.

## Limitações conhecidas da v0 (honestidade primeiro)

- A sobreposição lexical entre cabeçalho e corpo favorece o BM25; a v1 incluirá consultas em linguagem natural (leigo → jurisprudência), onde a vantagem lexical desaparece.
- Fonte única (STJ) e corpus de 1.500 documentos; a v1 expandirá para TJSP/STF.
- `google/embeddinggemma-300m` ainda não avaliado (repositório gated).

## Test set privado e submissões

Para evitar overfitting e contaminação, **parte do conjunto de avaliação é privada**. Quer ver seu modelo no leaderboard? [Submeta pelo formulário](https://github.com/ThalesAndrades/jurisbench-br/issues/new?template=02-jurisbench-submissao.yml) — avaliamos e publicamos o resultado.

## Reproduzir a parte pública

```bash
pip install -r requirements.txt
python jurisbench_v0.py  # resultados em results/
```

Modelos e datasets via [hfdownloader](https://github.com/ThalesAndrades/HuggingFaceModelDownloader):

```bash
hfdownloader download BAAI/bge-m3
hfdownloader download celsowm/jurisprudencias_stj --dataset
```

## Roadmap

- [x] v0: tarefa cabeçalho→corpo, baselines BM25 + 3 embeddings
- [ ] v1: consultas em linguagem natural, mais tribunais, test set privado formalizado
- [ ] **JurisEmbed-BR**: modelo da THM com meta declarada de superar o BM25 nesta tarefa

## Licença

Código: Apache 2.0. Dados: decisões judiciais públicas (Lei 9.610/98, art. 8º, IV).

---

*THM Tecnologia — Thales Andrades · contato: thalesandradees@gmail.com*
