# -*- coding: utf-8 -*-
"""
JurisBench-BR v0 — benchmark de retrieval jurídico PT-BR (custo zero).

Roda no Google Colab gratuito (T4) ou em CPU local.
Constrói o conjunto de avaliação a partir de decisões do STJ (atos oficiais,
não protegidos por direito autoral — Lei 9.610/98, art. 8º, IV) e mede
modelos de embedding existentes contra o baseline lexical BM25.

Uso (Colab ou local):
  pip install -r requirements.txt
  python jurisbench_v0.py

Configuração via variáveis de ambiente (padrões = execução v0 publicada):
  JURISBENCH_N_QUERIES  número de consultas (padrão: 200)
  JURISBENCH_N_CORPUS   tamanho do corpus de busca (padrão: 1500)
"""
import json
import os
import random
import re

import numpy as np

SEED = 42
N_QUERIES = int(os.environ.get("JURISBENCH_N_QUERIES", 200))
N_CORPUS = int(os.environ.get("JURISBENCH_N_CORPUS", 1500))
TOP_K = 10
RESULTS_DIR = "results"

DATASET = "celsowm/jurisprudencias_stj"

MODELS = {
    "MiniLM-multilingual": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "serafim-335m (SOTA PT)": "PORTULAN/serafim-335m-portuguese-pt-sentence-encoder-ir",
    "bge-m3 (SOTA multi)": "BAAI/bge-m3",
    "embeddinggemma-300m": "google/embeddinggemma-300m",
}


def load_pairs(n_corpus, seed=SEED):
    """Baixa pares (ementa, acórdão) do STJ via streaming — só o necessário."""
    from datasets import load_dataset

    ds = load_dataset(DATASET, split="train", streaming=True)
    rows = []
    for r in ds:
        em = (r.get("ementa_texto") or "").strip()
        ac = (r.get("acordao") or "").strip()
        # pares utilizáveis: ementa e acórdão substanciais e distintos
        if len(em) > 200 and len(ac) > 300 and em[:80] != ac[:80]:
            rows.append({"id": r["identificacao"], "ementa": em, "acordao": ac})
        if len(rows) >= n_corpus:
            break
    random.Random(seed).shuffle(rows)
    return rows


def ndcg_recall(query_gold, rankings, top_k=TOP_K):
    """nDCG@k e Recall@k para 1 documento relevante por consulta.

    rankings: lista (por consulta) dos ids ordenados por score.
    """
    ndcg, rec = [], []
    for gold, ranked in zip(query_gold, rankings):
        hits = [i for i, d in enumerate(ranked[:top_k]) if d == gold]
        ndcg.append(1.0 / np.log2(hits[0] + 2) if hits else 0.0)
        rec.append(1.0 if hits else 0.0)
    return float(np.mean(ndcg)), float(np.mean(rec))


def run_bm25(query_texts, corpus_texts, corpus_ids):
    from rank_bm25 import BM25Okapi

    def tok(t):
        return re.findall(r"\w+", t.lower())

    bm25 = BM25Okapi([tok(t) for t in corpus_texts])
    rankings = []
    for qt in query_texts:
        scores = bm25.get_scores(tok(qt))
        order = np.argsort(scores)[::-1][:TOP_K]
        rankings.append([corpus_ids[i] for i in order])
    return rankings


def run_embedding(repo, query_texts, corpus_texts, corpus_ids):
    from sentence_transformers import SentenceTransformer

    m = SentenceTransformer(repo, trust_remote_code=True)
    ce = m.encode(corpus_texts, batch_size=16, show_progress_bar=True,
                  normalize_embeddings=True)
    qe = m.encode(query_texts, batch_size=16, normalize_embeddings=True)
    sims = qe @ ce.T
    return [[corpus_ids[i] for i in np.argsort(s)[::-1][:TOP_K]] for s in sims]


def main():
    random.seed(SEED)
    np.random.seed(SEED)

    print(f"[1/4] Baixando decisões do STJ ({DATASET}, streaming)...")
    rows = load_pairs(N_CORPUS)
    queries = rows[:N_QUERIES]
    corpus = rows[:N_CORPUS]
    print(f"  {len(queries)} consultas (ementas) | corpus de {len(corpus)} acórdãos")

    corpus_texts = [c["acordao"][:2000] for c in corpus]
    corpus_ids = [c["id"] for c in corpus]
    query_texts = [q["ementa"][:1000] for q in queries]
    query_gold = [q["id"] for q in queries]

    results = {}

    print("[2/4] Baseline lexical: BM25...")
    rankings = run_bm25(query_texts, corpus_texts, corpus_ids)
    results["BM25 (lexical)"] = ndcg_recall(query_gold, rankings)

    print("[3/4] Baselines de embedding (CPU ok; GPU acelera)...")
    for name, repo in MODELS.items():
        try:
            rankings = run_embedding(repo, query_texts, corpus_texts, corpus_ids)
            results[name] = ndcg_recall(query_gold, rankings)
        except Exception as e:
            print(f"  !! {name}: {e}")

    print("[4/4] Resultados — JurisBench-BR v0 (ementa → acórdão, STJ)\n")
    import pandas as pd

    df = pd.DataFrame(
        [(k, f"{v[0]:.3f}", f"{v[1]:.3f}") for k, v in results.items()],
        columns=["Modelo", f"nDCG@{TOP_K}", f"Recall@{TOP_K}"],
    )
    print(df.to_markdown(index=False))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "v0_results.csv"), index=False)
    with open(os.path.join(RESULTS_DIR, "v0_results.json"), "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSalvo em {RESULTS_DIR}/v0_results.{{csv,json}}")


if __name__ == "__main__":
    main()
