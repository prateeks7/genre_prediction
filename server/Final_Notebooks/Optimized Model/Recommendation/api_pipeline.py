#!/usr/bin/env python
# coding: utf-8

# In[3]:


from extract_song_feature_links import run_url_prob_pipeline
from recommendation_pipeline import new_song_recommendations


# In[5]:


# your_notebook.py (after cleanup)
def run_pipeline(url):
    get_new_song_genre_prob = run_url_prob_pipeline(url)
    recommendations = new_song_recommendations(get_new_song_genre_prob)
    return recommendations


# In[7]:


# recommendations = run_pipeline()


# # In[8]:


# recommendations

