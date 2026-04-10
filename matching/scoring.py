import uuid


def compute_score(user_a_id: uuid.UUID, user_b_id: uuid.UUID, db) -> float:
    # Cosine similarity on answer embeddings + consistency weighting
    raise NotImplementedError
