import streamlit as st
import pickle
import pandas as pd

df = pickle.load(open("df.pkl", "rb"))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
tfidf_matrix = tfidf.fit_transform(df["combined_text"])
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_game(game_name):

    game_name = game_name.lower()

    matches = df[df["Title"].str.lower() == game_name]
    
    if matches.empty:
        return ["Game not found"]

    index = matches.index[0]

    similarity_scores = list(enumerate(similarity_matrix[index]))
    sorted_games = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_10 = sorted_games[1:11]

    recommendations = []
    for i in top_10:
        recommendations.append(df.iloc[i[0]]["Title"])

    return recommendations


st.title("🎮 AI Game Recommendation System")

game_list = df["Title"].values
selected_game = st.selectbox("Choose a game:", game_list)

if st.button("Recommend Games"):
    results = recommend_game(selected_game)

    st.subheader("✅ Top Recommended Games:")
    for game in results:
        st.write("🎯", game)
