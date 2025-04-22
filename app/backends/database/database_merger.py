#==========================================================================================
# Import necessary modules and libraries from the application's utility helpers.

# Import the pandas library as 'pd' for working with structured data such as DataFrames.
# Pandas is commonly used for data manipulation and analysis.

# Import the numpy library as 'np' for numerical computations and handling arrays.
# Numpy provides support for multi-dimensional arrays and mathematical functions.

# Import the cosine_similarity function, typically used to measure similarity between vectors.
# This function is often used in natural language processing or machine learning to calculate
# how similar two vectors are in terms of their cosine angle.

# Import the AgglomerativeClustering class for performing hierarchical clustering.
# Agglomerative clustering is a bottom-up clustering method where each data point starts as its own cluster,
# and pairs of clusters are merged iteratively based on their similarity.

# Import the SentenceTransformer class, a model used for embedding sentences into high-dimensional vector space.
# SentenceTransformer is often used for tasks like semantic similarity, clustering, or search,
# enabling efficient handling of textual data.

from app.utils.import_helpers import pd, np, cosine_similarity, AgglomerativeClustering, SentenceTransformer
#==========================================================================================

def merge_category_dataframes(dataframes: list) -> pd.DataFrame:
    """
    Merge multiple DataFrames within a category, aligning and merging columns intelligently.

    :param dataframes: List of pandas DataFrames to be merged.
    :return: A single merged DataFrame.
    """
    if not dataframes:
        return pd.DataFrame()  # Return empty DataFrame if no input
    
    # Concatenate all DataFrames row-wise (keep all columns for alignment)
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Extract column names
    column_names = list(combined_df.columns)

    # Load sentence-transformers model for embedding generation
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Generate embeddings for column names
    column_embeddings = model.encode(column_names, convert_to_tensor=True)

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(column_embeddings.cpu().numpy())

    # Perform clustering to group similar columns
    clustering = AgglomerativeClustering(
        n_clusters=None,  # Auto-detect number of clusters
        metric="precomputed", # Use precomputed distance matrix
        linkage="average",
        distance_threshold=0.3  # Tune threshold for merging columns
    )
    column_clusters = clustering.fit_predict(1 - similarity_matrix)  # Use 1-similarity as distance

    # Map cluster IDs to columns
    cluster_map = {}
    for cluster_id, column_name in zip(column_clusters, column_names):
        cluster_map.setdefault(cluster_id, []).append(column_name)

    # Merge columns in the same cluster
    merged_columns = {}
    for cluster_id, columns in cluster_map.items():
        merged_columns[columns[0]] = combined_df[columns].apply(
            lambda row: row.dropna().iloc[0] if not row.dropna().empty else np.nan, axis=1
        )

    # Create final merged DataFrame
    merged_df = pd.DataFrame(merged_columns)

    # Clean and normalize column names for downstream ML workloads
    merged_df.columns = [normalize_column_name(col) for col in merged_df.columns]

    return merged_df

def normalize_column_name(column_name: str) -> str:
    """
    Normalize column names for ML compatibility (e.g., lowercase, underscores).

    :param column_name: Original column name.
    :return: Normalized column name.
    """
    return column_name.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")

def merge_databases(databases: dict) -> dict:
    """
    Merge DataFrames within each category in the databases dictionary.

    :param databases: Dictionary where keys are categories and values contain DataFrames.
    :return: Dictionary with merged DataFrames for each category.
    """
    for category, data in databases.items():
        if data["dataframes"]:
            print(f"Merging {len(data['dataframes'])} DataFrames in category: {category}")
            databases[category]["merged"] = merge_category_dataframes(data["dataframes"])
        else:
            databases[category]["merged"] = pd.DataFrame()  # Empty if no data
    
    return databases
