# Scoper

Scoper is a scientific argument mining application that analyzes a single-sentence scientific claim and generates structured supporting and opposing arguments based strictly on a manually curated literature corpus.

The system uses a persistent FAISS vector database, OpenAI embeddings, GPT-5.2, and a claim-aware retrieval pipeline. It provides a minimalist Tkinter GUI with a two-column argument display.

---

## Overview

Scoper takes:

- A single scientific statement (one sentence)
- A local folder of PDF research papers (maximum ~100)

It produces:

- A structured list of supporting arguments
- A structured list of opposing arguments
- Citations in the format `(Author, Year)`

The system does not fabricate sources. All arguments are synthesized exclusively from the provided literature.

---

## Core Capabilities

- Persistent FAISS vector index
- Pre-chunked PDF corpus
- OpenAI embedding storage (locally saved)
- Claim-aware retrieval
- Passage-level stance classification
- Argument aggregation with citation enforcement
- Minimalist two-column Tkinter GUI
- Re-index button for rebuilding the literature database

---

## System Architecture

Scoper follows a claim-aware RAG (Retrieval-Augmented Generation) pipeline:

```
User Claim
↓
Claim Embedding
↓
FAISS Retrieval (top-k chunks)
↓
Passage-level Stance Classification
↓
Support/Oppose Grouping
↓
GPT-5.2 Argument Aggregation
↓
Two-column GUI Output
```

---

## How It Works

### 1. Literature Indexing (Offline Phase)

When **"Re-index Literature"** is pressed:

1. PDFs are loaded from the `literature/` folder.
2. Text is extracted using PyMuPDF.
3. Each document is chunked with overlap.
4. Metadata is attached:
    - Title
    - Author
    - Year
    - DOI
5. OpenAI embeddings are generated.
6. Embeddings are normalized and stored locally.
7. A persistent FAISS index is built and saved.
8. Chunk metadata is stored in JSON format.

Generated files:

- `data/vector.index`
- `data/embeddings.npy`
- `data/chunks.json`

Indexing only needs to be performed when new literature is added.

---

### 2. Claim Analysis (Runtime Phase)

When a user enters a single-sentence claim and clicks **Analyze**:

1. The claim is embedded using OpenAI embeddings.
2. FAISS retrieves the top-k most similar chunks.
3. Each retrieved chunk is sent to GPT-5.2 for stance classification:
    - Support
    - Oppose
    - Neutral
4. Neutral passages are discarded.
5. Supporting and opposing passages are grouped separately.
6. GPT-5.2 aggregates each group into structured bullet-point arguments.
7. Each bullet ends with citation formatting: `(Author, Year)`

Only retrieved passages are used for argument generation.

---

## Project Structure

```
scoper/
│
├── main.py
├── gui.py
├── scoper_engine.py
│
├── config/
│   └── config.json
│
├── literature/
│   └── *.pdf
│
├── data/
│   ├── vector.index
│   ├── embeddings.npy
│   └── chunks.json
│
├── core/
│   ├── config_loader.py
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embedding_manager.py
│   ├── faiss_manager.py
│   ├── retriever.py
│   ├── stance_classifier.py
│   ├── argument_aggregator.py
│   └── index_builder.py
│
└── requirements.txt
```

The architecture is modular and separation-of-concerns driven.

---

## Installation

1. Clone the repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key in:

```
config/config.json
```

4. Add scientific PDFs to:

```
literature/
```

---

## Running the Application

```bash
python main.py
```

Use the GUI to:

- Enter a single scientific claim
- Analyze the claim
- Re-index literature if new PDFs are added

---

## Design Decisions

### Why Persistent FAISS?

- Avoid recomputation of embeddings
- Enable fast repeated queries
- Reflect production-grade vector search workflow

### Why Claim-Aware Stance Classification?

Instead of simply summarizing retrieved passages, Scoper:

- Classifies each chunk relative to the claim
- Separates support and opposition before aggregation
- Produces clearer, structured scientific reasoning

This makes the system closer to argument mining than simple retrieval summarization.

### Why Pre-Chunking?

- Improves retrieval precision
- Prevents context overflow
- Enables granular stance detection

---

## Limitations

- Assumes well-formatted PDF metadata
- Works best with clean academic PDFs
- Designed for small-to-medium corpora (~100 papers)
- Stance classification depends on model interpretation quality

---

## Technical Stack

- Python
- Tkinter
- FAISS (IndexFlatIP)
- NumPy
- PyMuPDF
- OpenAI API (Embeddings + GPT-5.2)

---

## Intended Use

Scoper is designed as:

- A portfolio-level AI systems project
- A demonstration of retrieval-augmented argument mining
- A modular RAG architecture example
- A practical implementation of stance-aware aggregation

It is not intended for medical, legal, or high-stakes decision-making without expert validation.
