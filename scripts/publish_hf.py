# -*- coding: utf-8 -*-
"""Gera (e opcionalmente publica) o dataset público do JurisBench-BR no HF Hub.

Monta os pares congelados (cabeçalho → corpo) em hf_dataset/, com a dataset
card preenchida a partir de results/v0_results.json.

Uso:
  python scripts/publish_hf.py                  # só gera hf_dataset/
  HF_TOKEN=hf_xxx python scripts/publish_hf.py thm-tecnologia/jurisbench-br

Apenas a parte PÚBLICA do benchmark é publicada; o conjunto de teste
privado do leaderboard nunca sai da THM.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jurisbench_v0 as j  # noqa: E402

OUT_DIR = "hf_dataset"

CARD = """\
---
language: [pt]
license: other
license_name: atos-oficiais
license_details: >-
  Decisões judiciais públicas do STJ — atos oficiais, sem proteção autoral
  (Lei brasileira 9.610/98, art. 8º, IV). Código de avaliação: Apache 2.0.
task_categories: [text-retrieval]
tags: [legal, brazil, portuguese, benchmark, information-retrieval, rag]
size_categories: [1K<n<10K]
---

# JurisBench-BR (parte pública)

Primeiro benchmark aberto de recuperação semântica jurídica em português
brasileiro. Tarefa v0: dado o **cabeçalho temático** de uma ementa do STJ,
recuperar o **corpo de teses numeradas** (padrão CNJ) correspondente em um
corpus deduplicado de 1.500 decisões. 200 consultas; nDCG@10 e Recall@10.

First open benchmark for legal semantic retrieval in Brazilian Portuguese.
Task v0: given the thematic header of an STJ headnote, retrieve the matching
CNJ-standard numbered-theses body from a deduplicated corpus of 1,500 real
decisions. 200 queries; nDCG@10 and Recall@10.

- **Código, harness e regras:** https://github.com/ThalesAndrades/JurisBench-BR
- **Fonte dos dados:** [`celsowm/jurisprudencias_stj`](https://huggingface.co/datasets/celsowm/jurisprudencias_stj) (atos oficiais)
- **Leaderboard:** https://github.com/ThalesAndrades/JurisBench-BR/blob/main/LEADERBOARD.md
- ⚠️ Este é o conjunto **público**; o leaderboard usa também um conjunto
  **privado** para evitar contaminação/overfitting.

## Campos

| campo | descrição |
|---|---|
| `key` | chave única do documento (hash do corpo) |
| `id` | identificação da decisão no STJ (não é única) |
| `cabecalho` | cabeçalho temático da ementa (a consulta) |
| `corpo` | teses numeradas da ementa (o documento-alvo) |

As primeiras 200 linhas (na ordem do arquivo) são as consultas oficiais;
todas as 1.500 compõem o corpus de busca. O documento relevante de cada
consulta é o `corpo` de mesma `key`.

## Resultados v0

{tabela}

## Citação

```bibtex
@misc{{jurisbenchbr2026,
  author       = {{Andrades, Thales}},
  title        = {{JurisBench-BR: um benchmark aberto de recupera\\c{{c}}\\~ao
                  sem\\^antica jur\\'idica em portugu\\^es brasileiro}},
  year         = {{2026}},
  publisher    = {{GitHub}},
  howpublished = {{\\url{{https://github.com/ThalesAndrades/JurisBench-BR}}}}
}}
```

*THM Tecnologia — thalesandradees@gmail.com*
"""


def build():
    """Gera hf_dataset/ com data.jsonl e a dataset card."""
    rows = j.load_pairs(j.N_CORPUS)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "data.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    res = json.load(open(os.path.join(j.RESULTS_DIR, "v0_results.json")))
    linhas = ["| Modelo | nDCG@10 | Recall@10 |", "|---|---:|---:|"]
    for nome, (ndcg, rec) in sorted(res.items(), key=lambda kv: -kv[1][0]):
        linhas.append(f"| {nome} | {ndcg:.3f} | {rec:.3f} |")
    with open(os.path.join(OUT_DIR, "README.md"), "w") as f:
        f.write(CARD.format(tabela="\n".join(linhas)))
    print(f"{len(rows)} pares e dataset card gerados em {OUT_DIR}/")


def upload(repo_id):
    """Publica hf_dataset/ como dataset no HF Hub (requer HF_TOKEN)."""
    from huggingface_hub import HfApi

    api = HfApi(token=os.environ["HF_TOKEN"])
    api.create_repo(repo_id, repo_type="dataset", exist_ok=True)
    api.upload_folder(folder_path=OUT_DIR, repo_id=repo_id,
                      repo_type="dataset")
    print(f"Publicado em https://huggingface.co/datasets/{repo_id}")


if __name__ == "__main__":
    build()
    if len(sys.argv) > 1:
        if not os.environ.get("HF_TOKEN"):
            sys.exit("defina HF_TOKEN para publicar")
        upload(sys.argv[1])
