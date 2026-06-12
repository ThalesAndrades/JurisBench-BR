# -*- coding: utf-8 -*-
"""
JurisBench-BR v0 — benchmark de retrieval jurídico PT-BR (custo zero).

Roda no Google Colab gratuito (T4) ou em CPU local.
Constrói o conjunto de avaliação a partir de ementas de decisões do STJ
(atos oficiais, não protegidos por direito autoral — Lei 9.610/98, art. 8º,
IV) e mede modelos de embedding existentes contra o baseline lexical BM25.

A tarefa: dado o CABEÇALHO temático de uma ementa (a parte em caixa alta,
ex. "DIREITO PENAL. AGRAVO REGIMENTAL. TRÁFICO..."), recuperar o CORPO
correspondente (as teses numeradas no padrão CNJ, "1. ... 2. ...") em um
corpus com os corpos de todas as decisões.

Uso (Colab ou local):
  pip install -r requirements.txt
  python jurisbench_v0.py

Configuração via variáveis de ambiente (padrões = execução v0 publicada):
  JURISBENCH_N_QUERIES          número de consultas (padrão: 200)
  JURISBENCH_N_CORPUS           tamanho do corpus de busca (padrão: 1500)
  JURISBENCH_TRUST_REMOTE_CODE  "1" permite modelos que executam código
                                próprio do repositório HuggingFace
                                (padrão: 0 — desabilitado por segurança)
"""
import hashlib
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
# Carregar um modelo com trust_remote_code executa código arbitrário do
# repositório HuggingFace na sua máquina. Só habilite para modelos que você
# auditou e nos quais confia.
TRUST_REMOTE_CODE = os.environ.get("JURISBENCH_TRUST_REMOTE_CODE", "0") == "1"

DATASET = "celsowm/jurisprudencias_stj"
# Conjunto de avaliação congelado: chaves de conteúdo (na ordem embaralhada)
# que reproduzem exatamente a execução publicada, mesmo que o dataset
# upstream mude. `identificacao` NÃO é única no dataset, então cada
# documento é identificado pelo hash do corpo.
FROZEN_IDS = os.path.join("data", "v0_eval_ids.json")

# Primeira tese numerada da ementa: separa cabeçalho temático do corpo.
SPLIT_RE = re.compile(r"\s1\s*\.\s")
MIN_CABECALHO = 100
MIN_CORPO = 300

# query_prefix/passage_prefix: instruções exigidas por modelos estilo E5.
MODELS = {
    "MiniLM-multilingual": {
        "repo": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"},
    "serafim-335m (SOTA PT)": {
        "repo": "PORTULAN/serafim-335m-portuguese-pt-sentence-encoder-ir"},
    "bge-m3 (SOTA multi)": {"repo": "BAAI/bge-m3"},
    "embeddinggemma-300m": {"repo": "google/embeddinggemma-300m"},
    "multilingual-e5-large": {
        "repo": "intfloat/multilingual-e5-large",
        "query_prefix": "query: ",
        "passage_prefix": "passage: ",
    },
}


def split_ementa(ementa):
    """Divide a ementa em (cabeçalho temático, corpo de teses numeradas).

    Retorna None quando a ementa não segue o padrão ou alguma das partes
    é curta demais para formar um par de avaliação útil.
    """
    m = SPLIT_RE.search(ementa)
    if not m:
        return None
    cab, corpo = ementa[:m.start()].strip(), ementa[m.start():].strip()
    if len(cab) < MIN_CABECALHO or len(corpo) < MIN_CORPO:
        return None
    return cab, corpo


def doc_key(corpo):
    """Chave única e estável de um documento: hash do conteúdo do corpo."""
    return hashlib.sha1(corpo.encode("utf-8")).hexdigest()[:16]


def load_pairs(n_corpus, seed=SEED):
    """Baixa ementas do STJ via streaming e monta pares (cabeçalho, corpo).

    Corpos duplicados são descartados (decisões quase idênticas são comuns
    no STJ). Se data/v0_eval_ids.json existir (e casar com n_corpus),
    reconstrói exatamente o conjunto congelado; senão, constrói pelo filtro
    + seed e salva o congelamento para as próximas execuções.
    """
    from datasets import load_dataset

    frozen = None
    if os.path.exists(FROZEN_IDS):
        with open(FROZEN_IDS) as f:
            keys = json.load(f)["doc_keys"]
        if len(keys) == n_corpus:
            frozen = keys
        else:
            print(f"  aviso: {FROZEN_IDS} tem {len(keys)} chaves != n_corpus="
                  f"{n_corpus}; reconstruindo dinamicamente")

    ds = load_dataset(DATASET, split="train", streaming=True)

    rows, by_key = [], {}
    wanted = set(frozen) if frozen is not None else None
    for r in ds:
        parts = split_ementa((r.get("ementa_texto") or "").strip())
        if not parts:
            continue
        cab, corpo = parts
        key = doc_key(corpo)
        if key in by_key:
            continue  # decisão duplicada/quase idêntica
        if wanted is not None and key not in wanted:
            continue
        by_key[key] = {"key": key, "id": r["identificacao"],
                       "cabecalho": cab, "corpo": corpo}
        if wanted is None:
            rows.append(by_key[key])
            if len(rows) >= n_corpus:
                break
        elif len(by_key) == len(wanted):
            break

    if frozen is not None:
        missing = wanted - set(by_key)
        if missing:
            raise RuntimeError(
                f"{len(missing)} chaves do conjunto congelado não existem "
                f"mais no dataset upstream (ex.: {sorted(missing)[:3]})")
        return [by_key[k] for k in frozen]

    random.Random(seed).shuffle(rows)
    os.makedirs(os.path.dirname(FROZEN_IDS), exist_ok=True)
    with open(FROZEN_IDS, "w") as f:
        json.dump({"dataset": DATASET, "seed": seed,
                   "doc_keys": [r["key"] for r in rows],
                   "ids": [r["id"] for r in rows]},
                  f, ensure_ascii=False)
    print(f"  conjunto de avaliação congelado em {FROZEN_IDS}")
    return rows


def ndcg_recall(query_gold, rankings, top_k=TOP_K):
    """nDCG@k e Recall@k para 1 documento relevante por consulta.

    rankings: lista (por consulta) das chaves ordenadas por score.
    """
    ndcg, rec = [], []
    for gold, ranked in zip(query_gold, rankings):
        hits = [i for i, d in enumerate(ranked[:top_k]) if d == gold]
        ndcg.append(1.0 / np.log2(hits[0] + 2) if hits else 0.0)
        rec.append(1.0 if hits else 0.0)
    return float(np.mean(ndcg)), float(np.mean(rec))


def run_bm25(query_texts, corpus_texts, corpus_ids):
    """Ranqueia o corpus para cada consulta com BM25 (baseline lexical)."""
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


def run_embedding(spec, query_texts, corpus_texts, corpus_ids):
    """Ranqueia o corpus por similaridade de cosseno com o modelo de `spec`."""
    from sentence_transformers import SentenceTransformer

    qp = spec.get("query_prefix", "")
    pp = spec.get("passage_prefix", "")
    m = SentenceTransformer(spec["repo"], trust_remote_code=TRUST_REMOTE_CODE)
    ce = m.encode([pp + t for t in corpus_texts], batch_size=16,
                  show_progress_bar=True, normalize_embeddings=True)
    qe = m.encode([qp + t for t in query_texts], batch_size=16,
                  normalize_embeddings=True)
    sims = qe @ ce.T
    return [[corpus_ids[i] for i in np.argsort(s)[::-1][:TOP_K]] for s in sims]


def rrf_fuse(rankings_a, rankings_b, k=60, top_k=TOP_K):
    """Reciprocal Rank Fusion: combina dois rankings por consulta."""
    fused = []
    for ra, rb in zip(rankings_a, rankings_b):
        scores = {}
        for ranked in (ra, rb):
            for pos, doc in enumerate(ranked):
                scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + pos + 1)
        fused.append(sorted(scores, key=scores.get, reverse=True)[:top_k])
    return fused


def main():
    """Executa o benchmark completo: dados → BM25 → embeddings → results/."""
    random.seed(SEED)
    np.random.seed(SEED)

    print(f"[1/4] Baixando decisões do STJ ({DATASET}, streaming)...")
    rows = load_pairs(N_CORPUS)
    queries = rows[:N_QUERIES]
    corpus = rows[:N_CORPUS]
    print(f"  {len(queries)} consultas (cabeçalhos) | corpus de "
          f"{len(corpus)} corpos de ementa")

    corpus_texts = [c["corpo"][:2000] for c in corpus]
    corpus_keys = [c["key"] for c in corpus]
    query_texts = [q["cabecalho"][:1000] for q in queries]
    query_gold = [q["key"] for q in queries]

    results = {}

    print("[2/4] Baseline lexical: BM25...")
    bm25_rankings = run_bm25(query_texts, corpus_texts, corpus_keys)
    results["BM25 (lexical)"] = ndcg_recall(query_gold, bm25_rankings)

    print("[3/4] Baselines de embedding (CPU ok; GPU acelera)...")
    for name, spec in MODELS.items():
        try:
            rankings = run_embedding(spec, query_texts, corpus_texts,
                                     corpus_keys)
            results[name] = ndcg_recall(query_gold, rankings)
            hybrid = rrf_fuse(bm25_rankings, rankings)
            results[f"BM25 + {name} (RRF)"] = ndcg_recall(query_gold, hybrid)
        except Exception as e:
            print(f"  !! {name}: {e}")

    print("[4/4] Resultados — JurisBench-BR v0 (cabeçalho → corpo, STJ)\n")
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
