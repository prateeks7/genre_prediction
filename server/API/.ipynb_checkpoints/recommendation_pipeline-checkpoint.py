


import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.preprocessing import MinMaxScaler
from pymongo import MongoClient
import os



MONGO_URI = "mongodb+srv://prateeks1110:prateeks.iu@recommendationdata.uywtlek.mongodb.net/?retryWrites=true&w=majority&appName=recommendationData"
client = MongoClient(MONGO_URI)
db = client["FMA_Recommendation"]
recommendation = db["recommendation"]
track_artist_genre = db["track_artist_genre"]


recommendation_data = pd.DataFrame(list(recommendation.find())).drop("_id",axis=1)
track_title_artist = pd.DataFrame(list(track_artist_genre.find())).drop("_id",axis=1)
recommendation_data.set_index("track_id",inplace=True)
track_title_artist.set_index("track_id",inplace=True)
track_title_artist = track_title_artist.replace([np.inf, -np.inf], np.nan).fillna("-")


def new_song_recommendations(url_gerne_prob):

    
    new_song_similarities = cosine_similarity(url_gerne_prob,recommendation_data[url_gerne_prob.columns])
    recommendation_data["cosine_similarity"] = new_song_similarities[0]

    

    top_recommendations = recommendation_data.nlargest(10, "cosine_similarity").copy()


    # top_recommendations["cosine_similarity"].mean()



    normalized_features = pd.DataFrame(columns=["normalized_listens","normalized_favorites","normalized_interest"],index=top_recommendations.index)




    

    scaler = MinMaxScaler()
    normalized_features['normalized_listens'] = scaler.fit_transform(top_recommendations[['listens']])[:, 0]
    normalized_features['normalized_favorites'] = scaler.fit_transform(top_recommendations[['favorites']])[:, 0]
    normalized_features['normalized_interest'] = scaler.fit_transform(top_recommendations[['interest']])[:, 0]



    top_recommendations["final_score"] = (0.5 * top_recommendations["cosine_similarity"]
                    + 0.3 * normalized_features["normalized_listens"]
                + 0.1 * normalized_features["normalized_favorites"]
                + 0.1 * normalized_features["normalized_interest"])


    # top_recommendations["final_score"].mean()


    final_recommendations = top_recommendations.sort_values("final_score", ascending=False)

    recommendation_list =  pd.DataFrame({"title" : track_title_artist["title"].loc[final_recommendations.index].values, "artist" : track_title_artist["artist"].loc[final_recommendations.index].values, "genre" : track_title_artist["genre_top"].loc[final_recommendations.index].values})

#     formatted_json = ',\n'.join([
#     f'{{ title: "{row.title}", artist: "{row.artist}", genre: "{row.genre}" }}'
#     for _, row in recommendation_list.iterrows()
# ])

    return recommendation_list.to_dict(orient='records')