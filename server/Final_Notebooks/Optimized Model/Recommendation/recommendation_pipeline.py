


import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from sklearn.preprocessing import MinMaxScaler

recommendation_data = pd.read_csv("final_recommendation_data.csv",index_col=[0])
track_title_artist = pd.read_csv("track_title_artist.csv",index_col=[0])

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

    recommendation_list =  pd.DataFrame({"title" : track_title_artist["title"].loc[final_recommendations.index], "artist" : track_title_artist["artist"].loc[final_recommendations.index], "genre" : track_title_artist["genre_top"].loc[final_recommendations.index]})

    return recommendation_list