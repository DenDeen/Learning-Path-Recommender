import numpy as np
from numpy.linalg import norm

import json

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

educations_path = "input/educations.csv"
embeddings_path = "input/embeddings_checkpoint_skills.pkl"

df = pd.read_csv(educations_path)
word_occurrence_matrix = pd.read_csv("input/word_matrix.csv")
with open(embeddings_path, "rb") as file:
    embeddings, _ = pickle.load(file)


def find_best_matches(input_embedding, input_text, n=5):
    # Calculate cosine similarities (or any other similarity measure)
    similarities = [
        np.dot(input_embedding, emb) / (norm(input_embedding) * norm(emb))
        for emb in embeddings
    ]

    # For each embedding index check if a word of the input text appears in word_occurrence_matrix
    for i in range(len(similarities)):
        for word in input_text.split():
            if word.lower() in word_occurrence_matrix.columns:
                if word_occurrence_matrix.iloc[i][word.lower()] > 0:
                    similarities[i] *= 1.05 ** word_occurrence_matrix.iloc[i][word.lower()]

    # Get the indexes of the top n matches
    best_match_indexes = sorted(
        range(len(similarities)), key=lambda i: similarities[i], reverse=True
    )[:n]

    # Get the best matches
    best_matches = df.iloc[best_match_indexes]

    # Add the similarity scores to the best matches, rounded to 2 decimals
    best_matches["similarity"] = [similarities[i] for i in best_match_indexes]

    # rename columns
    best_matches = best_matches.rename(
        columns={
            "EducationTitle": "title",
            "Description": "description",
            "SkillsAcquired": "skills",
            "Duration": "duration",
            "Level": "level",
        }
    )

    return best_matches


def convert_df_to_json(df):
    json_string = df.to_json(orient="records")
    return json.loads(json_string)


def compare_embeddings(embeddings):
    n = len(embeddings)
    similarity_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            similarity = np.dot(embeddings[i], embeddings[j]) / (
                norm(embeddings[i]) * norm(embeddings[j])
            )
            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity  # The matrix is symmetric

    return similarity_matrix


def compare_single_embedding_to_others(single_embedding, embeddings):
    similarities = [
        np.dot(single_embedding, emb) / (norm(single_embedding) * norm(emb))
        for emb in embeddings
    ]
    return similarities


def visualize_similarity_matrix(matrix, title="Similarity Matrix"):
    plt.figure(figsize=(20, 16))
    sns.heatmap(matrix, annot=False, cmap="coolwarm", square=True)
    plt.title(title)
    plt.ylabel("Embedding Index")
    plt.xlabel("Embedding Index")
    plt.show()


def visualize_embedding_similarity(
    similarities, title="Similarity to a Given Embedding"
):
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(similarities)), similarities, color="blue")
    plt.xlabel("Embedding Index")
    plt.ylabel("Similarity")
    plt.title(title)
    plt.show()
