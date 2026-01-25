from typing import List, Dict

class BaseRetriever:
    """
        Abstract retriever interface.
        All retrievers must implement this.
    """
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        raise NotImplementedError("Retriever must implement retrieve()")


def normalize_results(raw_results, retriever_name: str) -> List[Dict]:
    normalized = []

    for item in raw_results:
        normalized.append({
            "chunk_id": item.get("chunk_id"),
            "document": item.get("document"),
            "text": item.get("text"),
            "score": float(item.get("score", 0.0)),
            "retriever": retriever_name
        })

    return normalized
