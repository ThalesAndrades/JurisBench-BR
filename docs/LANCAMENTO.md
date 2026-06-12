# 📣 Kit de lançamento — JurisBench-BR

Textos prontos para divulgar o benchmark. Copie, ajuste o tom se quiser e poste. A imagem para anexar é [`assets/social_preview.png`](../assets/social_preview.png).

> **Ordem sugerida:** LinkedIn (manhã de terça a quinta) → X no mesmo dia → Hacker News e Reddit em inglês 1–2 dias depois, aproveitando a tração inicial.

---

## LinkedIn (PT-BR)

> Testamos os modelos de embedding mais usados do mundo numa tarefa real de busca jurídica brasileira: recuperar a decisão correta do STJ entre 1.500 acórdãos.
>
> Todos perderam — por margens enormes — para o BM25, um algoritmo de busca por palavra-chave de 1994:
>
> 🥇 BM25 (1994): nDCG@10 de 0,771
> 🤖 bge-m3 (estado da arte multilíngue): 0,441
> 🤖 serafim-335m (estado da arte em português): 0,170
> 🤖 MiniLM (embedding mais baixado do mundo): 0,040
>
> A conclusão prática é desconfortável: se o seu RAG jurídico usa embeddings genéricos, ele provavelmente está PIOR do que a busca por palavra-chave que você substituiu.
>
> Por isso publicamos o JurisBench-BR — o primeiro benchmark aberto de busca semântica jurídica em português brasileiro. Metodologia aberta, dados públicos do STJ, reproduzível em 3 comandos no Colab gratuito.
>
> E deixamos um desafio em aberto: o leaderboard tem um Hall da Fama vazio esperando o primeiro modelo que vencer o BM25 no domínio jurídico brasileiro.
>
> Código, dados e leaderboard: https://github.com/ThalesAndrades/JurisBench-BR
>
> #IA #NLP #Direito #Lawtech #RAG #MachineLearning

---

## X / Twitter (PT-BR — thread)

**1/5**
> Um algoritmo de 1994 vence TODOS os embeddings de IA modernos na busca jurídica brasileira.
>
> Não é clickbait — é o resultado do JurisBench-BR, benchmark aberto que acabamos de publicar. 🧵

**2/5**
> A tarefa: dado o cabeçalho de uma ementa do STJ, achar a decisão correspondente entre 1.500 acórdãos reais.
>
> BM25 (palavra-chave, 1994): 0,771 nDCG@10
> bge-m3 (SOTA multilíngue): 0,441
> serafim-335m (SOTA PT): 0,170
> MiniLM (o + baixado do mundo): 0,040

**3/5**
> Por quê? O vocabulário, a morfologia e a estrutura documental do direito brasileiro estão fora da distribuição de treino de todos os modelos genéricos.
>
> Se o seu RAG jurídico usa embeddings genéricos, ele provavelmente está pior que a busca por palavra-chave que substituiu.

**4/5**
> Tudo aberto e reproduzível em 3 comandos no Colab gratuito. Dados públicos do STJ (atos oficiais, sem direito autoral).
>
> E tem leaderboard com test set privado: o Hall da Fama está vazio esperando o primeiro modelo que vencer o BM25.

**5/5**
> Código, metodologia, limitações (documentadas, não escondidas) e formulário de submissão:
>
> https://github.com/ThalesAndrades/JurisBench-BR
>
> RT ajuda a comunidade jurídica e de ML a parar de construir RAG sobre fundações quebradas. ⚖️

---

## Hacker News (Show HN, EN)

**Título:**
> Show HN: A 1994 algorithm beats every modern embedding on Brazilian case law

**URL:** `https://github.com/ThalesAndrades/JurisBench-BR/blob/main/README-en.md` *(aponta direto para o README em inglês — público do HN não lê PT)*

**Primeiro comentário (do autor):**
> Author here. We built JurisBench-BR, the first open benchmark for legal semantic retrieval in Brazilian Portuguese: 200 queries over 1,500 real rulings from Brazil's Superior Court of Justice (public domain by law).
>
> Every open embedding we tested — including bge-m3 (multilingual SOTA) and the most-downloaded sentence-transformer in the world — loses badly to plain BM25. Best embedding: 0.441 nDCG@10. BM25: 0.771.
>
> Known limitations are documented in the README (e.g., lexical overlap between header and body favors BM25 in v0; v1 adds natural-language queries). Methodological criticism is explicitly welcome — it's listed as a first-class contribution.
>
> There's a leaderboard with a private test set and an empty Hall of Fame waiting for the first model to beat BM25 on this domain.

---

## Reddit (EN — r/MachineLearning ou r/LanguageTechnology)

**Título:**
> [P] JurisBench-BR: every open embedding loses to BM25 on Brazilian legal retrieval (open benchmark)

**Corpo:**
> We released an open benchmark for legal semantic retrieval in Brazilian Portuguese. Task: given the thematic header of a court headnote, retrieve the corresponding ruling among 1,500 real decisions (nDCG@10 / Recall@10, 200 queries, fixed seed, public-domain data).
>
> Results: BM25 0.771 · bge-m3 0.441 · serafim-335m 0.170 · MiniLM-multilingual 0.040.
>
> v0 limitations are documented (lexical overlap favors BM25; v1 adds natural-language queries and more courts). Reproducible in 3 commands on free Colab. Leaderboard with private test set accepts submissions.
>
> Repo: https://github.com/ThalesAndrades/JurisBench-BR (English README inside)

---

## Comunidades BR (grupos de lawtech, Telegram/Discord de NLP-PT)

> Acabamos de publicar o JurisBench-BR — primeiro benchmark aberto de busca semântica jurídica em PT-BR. Spoiler: nenhum embedding aberto vence o BM25 (1994) no domínio jurídico brasileiro. Se você constrói RAG jurídico, vale os 5 minutos de leitura: https://github.com/ThalesAndrades/JurisBench-BR — e se você treina modelos, o Hall da Fama do leaderboard está vazio te esperando. 😉

---

## Checklist de configuração do repositório (manual, 5 min)

- [ ] **About → Description:** `⚖️ O primeiro benchmark aberto de busca semântica jurídica em PT-BR. Nenhum embedding vence o BM25 (1994) — ainda. Leaderboard aberto.`
- [ ] **About → Website:** link para o leaderboard ou futura página
- [ ] **About → Topics:** `benchmark` `legal-nlp` `information-retrieval` `portuguese` `brasil` `embeddings` `rag` `direito` `nlp` `bm25`
- [ ] **Settings → Social preview:** subir [`assets/social_preview.png`](../assets/social_preview.png)
- [ ] **Settings → Features:** ativar **Discussions**
- [ ] Fixar o repositório no perfil (Customize your pins)
