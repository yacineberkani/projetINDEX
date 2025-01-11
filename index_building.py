# index_building.py

import pandas as pd
import re

def nettoyer_et_tokenizer(texte):
    """Nettoie et tokenize un texte en une liste de mots."""
    if not isinstance(texte, str):
        texte = str(texte)
    texte = texte.lower()
    texte = re.sub(r'[^a-zA-Z\s]', ' ', texte)
    tokens = texte.split()
    return tokens

def construire_index_inverse(df, colonnes_textuelles):
    """
    Construit un index inversé à partir des colonnes textuelles d'un DataFrame.
    Retourne un dictionnaire: { mot: {doc_id: [pos1, pos2, ...], ...}, ... } 
    """
    inverted_index = {}
    
    for doc_id, row in df.iterrows():
        # Concaténer le texte de plusieurs colonnes
        texte_document = ""
        for col in colonnes_textuelles:
            valeur_colonne = row[col] if pd.notnull(row[col]) else ""
            texte_document += str(valeur_colonne) + " "
        
        # Tokenizer
        tokens = nettoyer_et_tokenizer(texte_document)
        
        # Parcourir chaque token
        for pos, token in enumerate(tokens):
            if token not in inverted_index:
                inverted_index[token] = {}
            if doc_id not in inverted_index[token]:
                inverted_index[token][doc_id] = []
            inverted_index[token][doc_id].append(pos)
            
    return inverted_index
