# -*- coding: utf-8 -*-
"""
JurisBench-BR v0 — benchmark de retrieval jurídico PT-BR (custo zero).

Roda no Google Colab gratuito (T4) ou em CPU local.
Constrói o conjunto de avaliação a partir de decisões do STJ (atos oficiais,
não protegidos por direito autoral — Lei 9.610/98, art. 8º, IV) e mede
modelos de embedding existentes. O resultado é a tabela-baseline que o
JurisEmbed-BR precisará bater — e o conteúdo do primeiro post de divulgação.

Uso (Colab):
  !pip install -q -r requirements.txt
  !python jurisbench_v0.py
"""
import json
import os
import random
import re

import numpy as np
import pandas as pd

SEED = 42
N_QUERIES = 200       # ementas usadas como consulta
N_CORPUS = 1500       # acórdãos no corpus de busca (inclui os 200 relevantes)
TOP_K = 10

random.seed(SEED)
np.random.seed(SEED)

# ---------------------------------------------------------------- dados
print("[1/4] Baixando decisões do STJ (streaming, só o necessário)...")
from datasets import load_dataset

ds = load_dataset("celsowm/jurisprudencias_stj", split="train", streaming=True)

rows = []
for r in ds:
    em, ac = (r.get("ementa_texto") or "").strip(), (r.get("acordao") or "").strip()
    # pares utilizáveis: ementa e acórdão substanciais e distintos
    if len(em) > 200 and len(ac) > 300 and em[:80] != ac[:80]:
        rows.append({"id": r["identificacao"], "ementa": em, "acordao": ac})
    if len(rows) >= N_CORPUS:
        break

random.shuffle(rows)
queries = rows[:N_QUERIES]
corpus = rows[:N_CORPUS]
print(f"  {len(queries)} consultas (ementas) | corpus de {len(corpus)} acórdãos")

corpus_texts = [c["acordao"][:2000] for c in corpus]
corpus_ids = [c["id"] for c in corpus]
query_texts = [q["ementa"][:1000] for q in queries]
query_gold = [q["id"] for q in queries]


def ndcg_recall(rankings):
    """rankings: lista (por consulta) dos ids ordenados por score."""
    ndcg, rec = [], []
    for gold, ranked in zip(query_gold, rankings):
        hits = [i for i, d in enumerate(ranked[:TOP_K]) if d == gold]
        ndcg.append(1.0 / np.log2(hits[0] + 2) if hits else 0.0)
        rec.append(1.0 if hits else 0.0)
    return float(np.mean(ndcg)), float(np.mean(rec))


results = {}

# ---------------------------------------------------------------- BM25
print("[2/4] Baseline lexical: BM25...")
from rank_bm25 import BM25Okapi

tok = lambda t: re.findall(r"\w+", t.lower())
bm25 = BM25Okapi([tok(t) for t in corpus_texts])
rankings = []
for qt in query_texts:
    scores = bm25.get_scores(tok(qt))
    order = np.argsort(scores)[::-1][:TOP_K]
    rankings.append([corpus_ids[i] for i in order])
results["BM25 (lexical)"] = ndcg_recall(rankings)

# ------------------------------------------------------- embeddings
print("[3/4] Baselines de embedding (CPU ok; GPU acelera)...")
from sentence_transformers import SentenceTransformer

MODELS = {
    "MiniLM-multilingual (224M dl/mês)": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "serafim-335m (SOTA PT atual)": "PORTULAN/serafim-335m-portuguese-pt-sentence-encoder-ir",
    "bge-m3 (SOTA multilíngue)": "BAAI/bge-m3",
    "embeddinggemma-300m (base do JurisEmbed)": "google/embeddinggemma-300m",
}

for name, repo in MODELS.items():
    try:
        m = SentenceTransformer(repo, trust_remote_code=True)
        ce = m.encode(corpus_texts, batch_size=16, show_progress_bar=True,
                      normalize_embeddings=True)
        qe = m.encode(query_texts, batch_size=16, normalize_embeddings=True)
        sims = qe @ ce.T
        rankings = [[corpus_ids[i] for i in np.argsort(s)[::-1][:TOP_K]] for s in sims]
        results[name] = ndcg_recall(rankings)
        del m, ce, qe
    except Exception as e:
        print(f"  !! {name}: {e}")

# ---------------------------------------------------------------- saída
print("[4/4] Resultados — JurisBench-BR v0 (ementa → acórdão, STJ)\n")
df = pd.DataFrame(
    [(k, f"{v[0]:.3f}", f"{v[1]:.3f}") for k, v in results.items()],
    columns=["Modelo", f"nDCG@{TOP_K}", f"Recall@{TOP_K}"],
)
print(df.to_markdown(index=False))
os.makedirs("results", exist_ok=True)
df.to_csv("results/v0_results.csv", index=False)
with open("results/v0_results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\nSalvo em results/v0_results.{csv,json} — essa tabela é o baseline a bater e o conteúdo do post de lançamento.")
