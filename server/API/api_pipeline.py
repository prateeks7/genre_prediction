

from extract_song_feature_links import run_url_prob_pipeline
from recommendation_pipeline import new_song_recommendations


print("🟢 begin")


# your_notebook.py (after cleanup)
def run_pipeline(url):
    print("⭕️ run_pipeline loaded")
    get_new_song_genre_prob = run_url_prob_pipeline(url)
    recommendations = new_song_recommendations(get_new_song_genre_prob)
    return get_new_song_genre_prob



