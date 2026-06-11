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
