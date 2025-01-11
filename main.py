# main.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd

from index_building import construire_index_inverse
from search_functions import search_single_word, search_phrase
from utils import (
    get_excerpt,
    compute_distribution,
    compute_average_occurrences,
    generate_word_cloud,
    get_neighbors_for_expression
)

# 1) Charger les données
df = pd.read_csv("BA_AirlineReviews.csv")

# 2) Construire l'index inversé
colonnes_textuelles = ["ReviewHeader", "ReviewBody"]
inverted_index = construire_index_inverse(df, colonnes_textuelles)

# 3) Initialiser l'application Dash
app = dash.Dash(__name__)
app.title = "Recherche British Airways"

app.layout = html.Div([
    html.H1(children="Système de Recherche - British Airways Reviews", style={'textAlign':'center'}),
    
    # Zone de saisie
    html.Div([
        dcc.Input(
            id='input-search',
            type='text',
            placeholder='Tapez un mot ou une expression...',
            style={'width': '50%'}
        ),
        html.Button('Rechercher', id='button-search', n_clicks=0)
    ], style={'marginBottom': '20px'}),
    
    # Zone d'affichage des résultats
    html.Div(id='results-stats', style={'marginTop': '20px'}),
    html.Div(id='results-distribution'),
    html.Div(id='results-excerpts'),
    html.Div(id='results-wordcloud')
])

# ---- Callbacks ----

@app.callback(
    [
        Output('results-stats', 'children'),
        Output('results-distribution', 'children'),
        Output('results-excerpts', 'children'),
        Output('results-wordcloud', 'children')
    ],
    [Input('button-search', 'n_clicks')],
    [State('input-search', 'value')]
)
def handle_search(n_clicks, input_value):
    if not input_value:
        return ["", "", "", ""]
    
    query = input_value.strip()
    if not query:
        return ["", "", "", ""]
    
    # 1) Recherche phrase (exact match) OU simple mot ?
    #    => On va considérer tout input comme "phrase" pour avoir la position exacte.
    results = search_phrase(inverted_index, query)
    
    # 2) Statistiques (nombre d'apparitions total, distribution, moyenne)
    #    results = {doc_id: [list_of_start_positions], ...}
    nb_docs = len(results)
    total_occurrences = sum(len(pos_list) for pos_list in results.values())
    
    # Distribution : (doc_id, occurrences)
    distribution_list = [(doc_id, len(pos_list)) for doc_id, pos_list in results.items()]
    average_occ = compute_average_occurrences(distribution_list)
    
    stats_text = [
        html.Div(f"Nombre de documents contenant '{query}': {nb_docs}"),
        html.Div(f"Nombre total d'occurrences: {total_occurrences}"),
        html.Div(f"Moyenne d'apparition (sur docs présents): {average_occ:.2f}")
    ]
    
    # 3) Distribution : affichons un bar chart (doc_id vs occurrences)
    if distribution_list:
        # Convertir en DataFrame pour plotly
        dist_df = pd.DataFrame(distribution_list, columns=["doc_id", "occurrences"])
        fig_dist = px.bar(dist_df, x="doc_id", y="occurrences", title="Distribution des occurrences par document")
        distribution_graph = dcc.Graph(figure=fig_dist)
    else:
        distribution_graph = html.Div("Aucune occurrence trouvée, pas de distribution")
    
    # 4) Extraits (afficher quelques extraits pour chaque doc trouvé)
    #    Pour ne pas surcharger, on peut limiter le nombre de doc affichés.
    max_docs = 5
    excerpt_children = []
    doc_count = 0
    
    for doc_id, start_positions in results.items():
        doc_count += 1
        if doc_count > max_docs:
            excerpt_children.append(html.Div(f"... affichage limité à {max_docs} documents ..."))
            break
        
        # On affiche un titre
        excerpt_children.append(html.H3(f"Document {doc_id}"))
        
        # Afficher chaque occurrence (limitons à 2 par doc)
        for i, start_pos in enumerate(start_positions[:2]):
            excerpt = get_excerpt(df, doc_id, start_pos, window=5, colonnes_textuelles=colonnes_textuelles)
            excerpt_children.append(html.Div(f"Position {start_pos} : {excerpt}"))
    
    # 5) Word Cloud : récupérer les mots -1 et +1 autour de chaque occurrence
    #    (Ceci est un exemple simple, on peut l’étoffer).
    
    neighbor_tokens = []
    query_tokens = query.lower().split()
    for doc_id, start_positions in results.items():
        for start_pos in start_positions:
            neighbors = get_neighbors_for_expression(df, doc_id, start_pos, query_tokens, window=1, colonnes_textuelles=colonnes_textuelles)
            neighbor_tokens.extend(neighbors)
    
    if neighbor_tokens:
        img_b64 = generate_word_cloud(neighbor_tokens)
        wc_image = html.Img(src=img_b64, style={'maxWidth':'600px'})
    else:
        wc_image = html.Div("Aucun voisin trouvé pour générer un Word Cloud.")
    
    return [
        stats_text,           # results-stats
        distribution_graph,   # results-distribution
        excerpt_children,     # results-excerpts
        wc_image              # results-wordcloud
    ]

# --- Lancer l'app ---
if __name__ == "__main__":
    # Pour tester en local
    app.run_server(debug=True, port=8050)
