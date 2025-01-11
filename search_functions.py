# search_functions.py

def search_single_word(inverted_index, word):
    """Recherche un mot unique dans l'index inversé."""
    word = word.lower()
    if word in inverted_index:
        return inverted_index[word]  # {doc_id: [positions], ...}
    else:
        return {}

def search_multiple_words_and(inverted_index, words_list):
    """Recherche AND : l'intersection des documents contenant tous les mots."""
    words_list = [w.lower() for w in words_list]
    if not words_list:
        return {}
    
    # Récupérer la liste des doc_id pour chaque mot
    list_of_dicts = []
    for w in words_list:
        if w in inverted_index:
            list_of_dicts.append(inverted_index[w])
        else:
            # Si un mot n'existe pas, l'intersection est vide
            return {}
    
    # Intersection des doc_ids
    common_doc_ids = set(list_of_dicts[0].keys())
    for d in list_of_dicts[1:]:
        common_doc_ids = common_doc_ids.intersection(d.keys())
    
    # Construire la structure finale
    result = {}
    for doc_id in common_doc_ids:
        result[doc_id] = {}
        for w in words_list:
            result[doc_id][w] = inverted_index[w][doc_id]
    return result





def search_phrase(inverted_index, phrase):
    """
    Recherche d'une phrase exacte (tokens consécutifs).
    Retourne {doc_id: [liste positions de départ], ...}
    """
    words = phrase.lower().split()
    if not words:
        return {}
    
    # Récupération des posting lists pour chaque mot
    posting_lists = []
    for w in words:
        if w in inverted_index:
            posting_lists.append(inverted_index[w])
        else:
            return {}
    
    # Intersection des doc_id
    common_doc_ids = set(posting_lists[0].keys())
    for pl in posting_lists[1:]:
        common_doc_ids = common_doc_ids.intersection(pl.keys())
    
    # Vérifier la séquence
    results = {}
    for doc_id in common_doc_ids:
        # Positions du premier mot
        positions_word1 = posting_lists[0][doc_id]
        for start_pos in positions_word1:
            match_found = True
            for i in range(1, len(words)):
                # On veut trouver le mot i à la position start_pos+i
                if (start_pos + i) not in posting_lists[i][doc_id]:
                    match_found = False
                    break
            if match_found:
                if doc_id not in results:
                    results[doc_id] = []
                results[doc_id].append(start_pos)
    return results
