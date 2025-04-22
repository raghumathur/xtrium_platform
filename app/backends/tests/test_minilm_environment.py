def test_environment():
    try:
        import pandas as pd
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        from sklearn.cluster import AgglomerativeClustering
        from sentence_transformers import SentenceTransformer

        # Test pandas
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        print("Pandas: Successfully created DataFrame")

        # Test NumPy
        arr = np.array([1, 2, 3])
        print("NumPy: Successfully created NumPy array")

        # Test sentence-transformers
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(["test"])
        print(f"Sentence-Transformers: Successfully generated embeddings of shape {embeddings.shape}")

        # Test cosine similarity
        sim = cosine_similarity([[1, 0]], [[0, 1]])
        print(f"Sklearn Cosine Similarity: Successfully computed similarity = {sim[0][0]}")

        # Test clustering
        clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=1.0)
        clustering.fit([[1], [2], [3]])
        print("Sklearn Clustering: Successfully performed clustering")

        print("\nEnvironment Test Passed!")
    except Exception as e:
        print(f"Environment Test Failed: {e}")


if __name__ == "__main__":
    test_environment()