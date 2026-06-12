# -*- coding: utf-8 -*-
"""Testes das métricas do JurisBench-BR (não exigem download de dados/modelos)."""
import numpy as np
import pytest

from jurisbench_v0 import ndcg_recall


def test_acerto_na_primeira_posicao():
    ndcg, rec = ndcg_recall(["doc1"], [["doc1", "x", "y"]])
    assert ndcg == pytest.approx(1.0)
    assert rec == pytest.approx(1.0)


def test_acerto_na_segunda_posicao():
    ndcg, rec = ndcg_recall(["doc1"], [["x", "doc1", "y"]])
    assert ndcg == pytest.approx(1.0 / np.log2(3))
    assert rec == pytest.approx(1.0)


def test_documento_fora_do_top_k():
    ranked = [f"x{i}" for i in range(10)] + ["doc1"]
    ndcg, rec = ndcg_recall(["doc1"], [ranked], top_k=10)
    assert ndcg == 0.0
    assert rec == 0.0


def test_media_entre_consultas():
    gold = ["a", "b"]
    rankings = [["a"], ["x"]]  # uma consulta acerta no topo, outra erra
    ndcg, rec = ndcg_recall(gold, rankings)
    assert ndcg == pytest.approx(0.5)
    assert rec == pytest.approx(0.5)


def test_rrf_fusao_promove_consenso():
    from jurisbench_v0 import rrf_fuse
    a = [["d1", "d2", "d3"]]
    b = [["d3", "d4", "d1"]]
    fused = rrf_fuse(a, b)[0]
    # d1 e d3 aparecem nas duas listas; devem liderar a fusão
    assert set(fused[:2]) == {"d1", "d3"}


def test_split_ementa_padrao_cnj():
    from jurisbench_v0 import split_ementa
    em = ("DIREITO PENAL. AGRAVO REGIMENTAL. " + "TEMA. " * 20 +
          " 1. Primeira tese com fundamentação suficiente. " * 10 +
          "2. Segunda tese igualmente longa para o corte mínimo. " * 5)
    parts = split_ementa(em)
    assert parts is not None
    cab, corpo = parts
    assert cab.startswith("DIREITO PENAL")
    assert corpo.startswith("1.")


def test_split_ementa_sem_teses_numeradas():
    from jurisbench_v0 import split_ementa
    assert split_ementa("EMENTA CURTA SEM TESES. " * 20) is None


def test_doc_key_estavel_e_distinto():
    from jurisbench_v0 import doc_key
    assert doc_key("texto a") == doc_key("texto a")
    assert doc_key("texto a") != doc_key("texto b")
