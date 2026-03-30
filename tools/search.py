import re
from typing import List, Dict, Set, Tuple

# Simulated document store
DOCUMENTS = [
    {
        "id": "doc1",
        "title": "AI in Healthcare",
        "content": "AI improves diagnostic accuracy and reduces human error."
    },
    {
        "id": "doc2",
        "title": "Risks of AI",
        "content": "AI systems may introduce bias and lack interpretability."
    },
    {
        "id": "doc3",
        "title": "AI Efficiency",
        "content": "Automation reduces costs and improves efficiency in hospitals."
    }
]

# Keeps scoring focused on content words (not "the", "of", …).
_STOPWORDS: Set[str] = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "from",
    "of", "as", "by", "with", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "may", "might", "must", "can", "this", "that", "these", "those", "it", "its",
    "what", "which", "who", "whom", "how", "when", "where", "why",
})


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _query_terms(query: str) -> Set[str]:
    """Terms to match: drop stopwords and 1-char noise; keep short real words like 'ai'."""
    raw = _tokenize(query)
    terms = {t for t in raw if len(t) > 1 and t not in _STOPWORDS}
    if terms:
        return terms
    return {t for t in raw if len(t) > 1} or set(raw)


def search_documents(query: str) -> List[Dict]:
    """
    Lexical search over title + content: score by overlap of meaningful query terms.
    Matches the "sense" of a question better than requiring the full string as a substring.
    Results are sorted by relevance (overlap count), then id.
    """
    if not query.strip():
        return []

    q_terms = _query_terms(query)
    if not q_terms:
        return []

    scored: List[Tuple[int, Dict]] = []

    for doc in DOCUMENTS:
        blob = f"{doc['title']} {doc['content']}"
        doc_terms = set(_tokenize(blob))
        overlap = sum(1 for t in q_terms if t in doc_terms)
        if overlap > 0:
            scored.append((overlap, doc))

    scored.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [doc for _, doc in scored]
