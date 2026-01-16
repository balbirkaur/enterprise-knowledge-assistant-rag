
# Enterprise Knowledge Assistant (Advanced RAG)

## Overview
This is a self-initiated portfolio project focused on building an end-to-end Enterprise Knowledge Assistant using Retrieval Augmented Generation (RAG) techniques.

The project starts from basic RAG fundamentals and progressively evolves into an advanced, production-style RAG system, all within a single codebase.

## Motivation
Modern enterprises store critical information across numerous internal documents such as HR policies, compliance guidelines, and IT security manuals. Traditional search systems often fail to provide accurate, context-aware answers.

## Use Case
An AI-powered assistant that allows users to ask natural language questions over internal enterprise documents and receive grounded, source-backed responses.

## Architecture
1. Document ingestion (PDFs)
2. Text chunking with overlap
3. Metadata enrichment
4. Embedding generation
5. Vector database storage
6. Hybrid retrieval (Vector + Keyword)
7. Query expansion
8. Re-ranking
9. Context compression
10. Answer generation
11. Evaluation & monitoring

## Tech Stack
- Python
- LangChain
- FAISS / Chroma
- OpenAI / Azure OpenAI
- SentenceTransformers
- BM25
- RAGAS
- Streamlit

## Dataset
Enterprise-style PDF documents including HR policies, banking guidelines, IT security documents, and compliance policies.

## RAG Progression
### Basic RAG
- PDF ingestion
- Chunking & embeddings
- Vector similarity search

### Intermediate RAG
- Metadata filtering
- Hybrid search
- Query expansion

### Advanced RAG
- Re-ranking
- Context compression
- Hallucination control
- Evaluation metrics

## Evaluation
RAG-specific metrics are used to measure answer relevance and faithfulness.

## UI
Streamlit-based chat interface for interactive Q&A.

## Resume Highlight
Built a self-driven enterprise-grade RAG system demonstrating advanced retrieval and evaluation techniques.
