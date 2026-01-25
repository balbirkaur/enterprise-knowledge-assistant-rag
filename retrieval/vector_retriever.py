from typing import List, Dict

# Import the base retriever interface and normalization helper
# BaseRetriever ensures all retrievers follow the same contract
# normalize_results ensures consistent output format for evaluation
from retrieval.retriever import BaseRetriever, normalize_results


class VectorRetriever(BaseRetriever):
    """
    VectorRetriever implements semantic (embedding-based) retrieval.

    Conceptually, this retriever does the following:
    1. Converts the query text into an embedding (numbers)
    2. Compares the query embedding with stored document embeddings
    3. Retrieves the most semantically similar document chunks
    4. Returns them with similarity scores

    NOTE:
    - Steps 1 and 2 are handled internally by the vector store
    - This class orchestrates the retrieval and formats the output
    """

    def __init__(self, vector_store):
        """
        Constructor.

        vector_store:
        - This is a pre-built vector database (FAISS / Chroma etc.)
        - It ALREADY contains:
            • document chunks
            • embeddings for each chunk
            • metadata (document name, chunk_id, etc.)

        IMPORTANT:
        - Text → embeddings conversion for documents
          DOES NOT happen here.
        - It happens during ingestion/indexing.
        """
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """
        Perform vector-based retrieval.

        Parameters:
        - query: user question in plain text
        - k: number of top similar chunks to retrieve

        Returns:
        - A list of standardized retrieval results (list of dicts)
        """

        # ------------------------------------------------------------
        # STEP 1: Convert query text → embedding
        # ------------------------------------------------------------
        # This step is NOT explicitly visible in code.
        # Internally, the vector store:
        #   - Takes the query string
        #   - Passes it to the embedding model
        #   - Converts it into a numerical vector
        #
        # You do NOT manually write embedding logic here.
        # ------------------------------------------------------------

        # ------------------------------------------------------------
        # STEP 2: Compare query embedding with stored embeddings
        # ------------------------------------------------------------
        # similarity_search_with_score does ALL of the following internally:
        #   - Computes query embedding
        #   - Compares it with all stored document embeddings
        #   - Calculates similarity/distance scores
        #   - Selects top-k most similar chunks
        #
        # Output format:
        #   [
        #     (Document, score),
        #     (Document, score),
        #     ...
        #   ]
        # ------------------------------------------------------------
        results = self.vector_store.similarity_search_with_score(query, k=k)

        # ------------------------------------------------------------
        # STEP 3: Extract raw results
        # ------------------------------------------------------------
        # At this stage:
        # - We have Document objects + similarity scores
        # - But the format is NOT suitable for evaluation or hybrid fusion
        #
        # So we convert them into a simple dictionary format
        # ------------------------------------------------------------
        raw_results = []

        for doc, score in results:
            # doc.page_content  -> actual text chunk
            # doc.metadata      -> metadata added during ingestion
            # score             -> similarity score from vector search

            raw_results.append({
                # Unique identifier for the chunk (used for debugging)
                "chunk_id": doc.metadata.get("chunk_id"),

                # Original document name (CRITICAL for Recall@K evaluation)
                "document": doc.metadata.get("document"),

                # The actual text that matched the query semantically
                "text": doc.page_content,

                # Similarity score between query embedding and chunk embedding
                # Lower or higher = better depending on vector DB implementation
                "score": score
            })

        # ------------------------------------------------------------
        # STEP 4: Normalize results
        # ------------------------------------------------------------
        # normalize_results ensures:
        # - Same output structure across all retrievers (vector, BM25, hybrid)
        # - Retriever name is attached for comparison
        #
        # This makes:
        # - Evaluation easy
        # - Hybrid fusion possible
        # - Debugging transparent
        # ------------------------------------------------------------
        return normalize_results(raw_results, retriever_name="vector")
