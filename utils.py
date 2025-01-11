# utils.py

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

def get_excerpt(df, doc_id, start_pos, window=5, colonnes_textuelles=["ReviewHeader","ReviewBody"]):
    """Retourne un petit extrait autour de start_pos (± window mots)."""
    # Concaténer le texte
    row = df.iloc[doc_id]
    texte_document = ""
    for col in colonnes_textuelles:
        val = row[col] if pd.notnull(row[col]) else ""
        texte_document += str(val) + " "
        
    tokens = texte_document.lower().split()
    
    left_index = max(0, start_pos - window)
    right_index = min(len(tokens), start_pos + window + len(tokens))
    excerpt_tokens = tokens[left_index : right_index]
    return " ".join(excerpt_tokens)

def compute_distribution(results_dict):
    """
    Calcule la distribution du nombre d'apparitions par document.
    results_dict : {doc_id: list_of_positions, ...}
    Retourne une liste (doc_id, count_positions).
    """
    distribution = []
    for doc_id, positions in results_dict.items():
        distribution.append((doc_id, len(positions)))
    return distribution

def compute_average_occurrences(distribution_list):
    """
    Calcul de la moyenne des occurrences parmi les documents où l'expression est présente.
    distribution_list : liste de tuples (doc_id, count_occurrences)
    """
    if not distribution_list:
        return 0
    total_occ = sum([occ for (_, occ) in distribution_list])
    return total_occ / len(distribution_list)

def generate_word_cloud(neighbor_tokens):
    """
    Génère un Word Cloud sous forme d'image encodée en base64 à partir d'une liste de tokens.
    """
    text_joined = " ".join(neighbor_tokens)
    wordcloud = WordCloud(width=600, height=400, background_color="white").generate(text_joined)
    
    # Convertir en image base64
    buffer = io.BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_b64}"

def get_neighbors_for_expression(df, doc_id, start_pos, expression_tokens, window=1, colonnes_textuelles=["ReviewHeader","ReviewBody"]):
    """
    Récupère les mots qui précèdent (mot-1) et qui suivent (mot+1) l'expression dans un document.
    'expression_tokens' est la liste de mots de la requête.
    """
    row = df.iloc[doc_id]
    texte_document = ""
    for col in colonnes_textuelles:
        val = row[col] if pd.notnull(row[col]) else ""
        texte_document += str(val) + " "
    
    tokens = texte_document.lower().split()

    # Position de fin de l'expression
    end_pos = start_pos + len(expression_tokens) - 1
    
    neighbors = []
    
    # --- voisin précédent ---
    neighbor_left_index = start_pos - window
    if 0 <= neighbor_left_index < len(tokens):
        neighbors.append(tokens[neighbor_left_index])
    
    # --- voisin suivant ---
    neighbor_right_index = end_pos + window
    if 0 <= neighbor_right_index < len(tokens):
        neighbors.append(tokens[neighbor_right_index])
    
    return neighbors
