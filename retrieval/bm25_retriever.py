from typing import List, Dict

# BM25 implementation (pure keyword-based retrieval)
# This library handles the BM25 math internally
from rank_bm25 import BM25Okapi

# Import base retriever contract and normalization helper
from retrieval.retriever import BaseRetriever, normalize_results


class BM25Retriever(BaseRetriever):
    """
    BM25Retriever implements exact keyword-based retrieval.

    Conceptually, this retriever:
    1. Tokenizes document chunks into words (during ingestion)
    2. Builds BM25 statistics (term frequency, rarity, length)
    3. Tokenizes the query into words (at query time)
    4. Scores each chunk based on keyword overlap
    5. Returns the highest-scoring chunks

    IMPORTANT:
    - No embeddings are used
    - No semantic understanding
    - Pure lexical (word-based) matching
    """

    def __init__(self, documents: List[Dict]):
        """
        Constructor.

        documents:
        - List of chunk dictionaries
        - Each item MUST contain:
            • chunk_id
            • document (document name)
            • text (chunk content)

        Example:
        {
          "chunk_id": "chunk_12",
          "document": "Finance_Reimbursement_Policy.pdf",
          "text": "CFO approval required for expenses above 50,000"
        }
        """

        # Store original documents for later reference
        self.documents = documents

        # ------------------------------------------------------------
        # STEP 1: Tokenize document text
        # ------------------------------------------------------------
        # BM25 works on tokens (words), not embeddings
        # Lowercasing is important for consistency
        self.tokenized_corpus = [
            doc["text"].lower().split()
            for doc in documents
        ]

        # ------------------------------------------------------------
        # STEP 2: Build BM25 index (INGESTION TIME)
        # ------------------------------------------------------------
        # This computes:
        # - term frequency
        # - inverse document frequency
        # - document length normalization
        #
        # This happens ONCE
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """
        Perform BM25 retrieval.

        Parameters:
        - query: user question (plain text)
        - k: number of top results to return

        Returns:
        - List of standardized retrieval results
        """

        # ------------------------------------------------------------
        # STEP 3: Tokenize query (QUERY TIME)
        # ------------------------------------------------------------
        # No meaning inference
        # Just exact word tokens
        tokenized_query = query.lower().split()

        # ------------------------------------------------------------
        # STEP 4: Score all documents using BM25
        # ------------------------------------------------------------
        # Returns one score per document chunk
        scores = self.bm25.get_scores(tokenized_query)

        # ------------------------------------------------------------
        # STEP 5: Rank documents by score
        # ------------------------------------------------------------
        # Higher BM25 score = better keyword match
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        # ------------------------------------------------------------
        # STEP 6: Select top-K results
        # ------------------------------------------------------------
        raw_results = []

        for idx in ranked_indices[:k]:
            raw_results.append({
                "chunk_id": self.documents[idx]["chunk_id"],
                "document": self.documents[idx]["document"],
                "text": self.documents[idx]["text"],
                "score": scores[idx]
            })

        # ------------------------------------------------------------
        # STEP 7: Normalize output
        # ------------------------------------------------------------
        # Makes BM25 results comparable with vector & hybrid retrieval
        return normalize_results(raw_results, retriever_name="bm25")
