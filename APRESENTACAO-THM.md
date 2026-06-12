<div align="center">

# THM Tecnologia

**IA local e soberania de dados para o mercado brasileiro**

*Thales Andrades — Fundador*

[Soluções](#-soluções) • [JurisBench-BR](#-jurisbench-br--o-benchmark) • [Resultados](#-resultados-que-sustentam-a-tese) • [Contato](#-fale-com-a-thm)

</div>

---

## 🎯 Nossa tese

A IA generativa global resolve problemas genéricos em inglês. **O mercado brasileiro precisa de IA especializada, em português, que respeite a LGPD** — rodando dentro da infraestrutura do cliente, sem que um único byte sensível saia da rede.

Os números provam a lacuna:

| Evidência | Fonte |
|---|---|
| O modelo jurídico PT-BR mais usado tem **1,09 milhão de downloads/mês** — e é de 2022, tecnologicamente obsoleto | HuggingFace Hub, jun/2026 |
| O ASR em português mais usado tem **2,77 milhões de downloads/mês** — e é de 2021 | HuggingFace Hub, jun/2026 |
| O embedding mais baixado do mundo acerta só **4%** das buscas em jurisprudência brasileira | JurisBench-BR v0 (nosso benchmark) |

**Milhões de sistemas em produção consomem modelos defasados porque ninguém construiu os sucessores. Nós estamos construindo.**

---

## 🛠 Soluções

### 1. Escriba — transcrição e atas 100% on-premise

Produto para escritórios de advocacia, clínicas e empresas reguladas: transcrição de reuniões, audiências e consultas com geração de atas e busca semântica no histórico — **com o áudio permanecendo na rede do cliente, do início ao fim**.

- Transcrição em tempo real em PT-BR (streaming, latência de milissegundos)
- Atas, resumos e itens de ação gerados automaticamente
- Busca semântica em todo o histórico de gravações
- Implantação em 1 GPU local — sem mensalidade de nuvem americana, sem exposição LGPD

> **💬 Interessado?** [Entre na lista de interesse →](https://github.com/ThalesAndrades/jurisbench-br/issues/new?template=01-escriba-interesse.yml) (2 minutos, sem compromisso)

### 2. JurisEmbed-BR — busca semântica jurídica que funciona

Modelo de embeddings treinado especificamente para o domínio jurídico brasileiro, em desenvolvimento com meta pública: **superar o BM25 no JurisBench-BR** — coisa que nenhum modelo aberto consegue hoje (veja os resultados abaixo).

- Versão aberta (300M) para a comunidade
- Versão comercial: reranker de alta precisão + **re-treino mensal com a jurisprudência do mês**

> **💬 Quer acesso antecipado ou avaliar seu RAG jurídico?** [Cadastre seu interesse →](https://github.com/ThalesAndrades/jurisbench-br/issues/new?template=02-jurisbench-submissao.yml)

### 3. hfdownloader — infraestrutura aberta

[github.com/ThalesAndrades/HuggingFaceModelDownloader](https://github.com/ThalesAndrades/HuggingFaceModelDownloader): a ferramenta de download de modelos do HuggingFace usada pela comunidade, que a THM mantém e evolui — incluindo análise de quantizações GGUF, estimativa de RAM e (em desenvolvimento) verificação automática de licenças comerciais.

---

## 📊 JurisBench-BR — o benchmark

Construímos o primeiro benchmark de recuperação semântica jurídica em português brasileiro: 200 consultas temáticas sobre um corpus deduplicado de 1.500 decisões reais do STJ (dados públicos — atos oficiais, Lei 9.610/98, art. 8º, IV), com conjunto de avaliação congelado e reproduzível.

### 📉 Resultados que sustentam a tese (12/06/2026)

| Modelo | nDCG@10 | Recall@10 |
|---|---:|---:|
| **BM25 (busca lexical, 1994)** | **0,693** | **0,825** |
| BM25 + MiniLM (híbrido RRF) | 0,613 | 0,760 |
| MiniLM-multilingual (224M downloads/mês) | 0,017 | 0,040 |
| bge-m3 · serafim-335m · multilingual-e5-large | *em avaliação* | *em avaliação* |

**Leitura:** toda a busca semântica disponível perde — por margens enormes — para um algoritmo de 30 anos atrás quando o domínio é o jurídico brasileiro. Se o seu RAG jurídico usa embeddings genéricos, ele provavelmente está pior do que a busca por palavra-chave que você substituiu.

Detalhes, código e limitações: [README do benchmark](README.md) · Conjunto de teste oculto: submissões de modelos são bem-vindas via [formulário](https://github.com/ThalesAndrades/jurisbench-br/issues/new?template=02-jurisbench-submissao.yml).

---

## 🗺 Roadmap público

| Quando | Entrega |
|---|---|
| Jun/2026 | JurisBench-BR v0 publicado (✅ você está aqui) |
| Jul/2026 | JurisEmbed-BR v1 aberto + leaderboard com test set privado |
| Jul/2026 | Escriba: pilotos com primeiros clientes (vagas limitadas) |
| Ago/2026 | JurisRerank-BR comercial + assinatura de re-treino mensal |
| S2/2026 | Expansão vertical: contábil/tributário e regulatório |

---

## 📬 Fale com a THM

- **Interesse no Escriba (transcrição on-premise):** [formulário de 2 minutos](https://github.com/ThalesAndrades/jurisbench-br/issues/new?template=01-escriba-interesse.yml)
- **JurisEmbed-BR / submeter modelo ao benchmark:** [formulário](https://github.com/ThalesAndrades/jurisbench-br/issues/new?template=02-jurisbench-submissao.yml)
- **E-mail direto (assuntos comerciais ou dados sensíveis):** thalesandradees@gmail.com
- **Referência:** THM Tecnologia — Thales Andrades

> *Privacidade: os formulários acima são issues públicas do GitHub — não inclua dados confidenciais neles. Para informações sensíveis, use o e-mail.*
