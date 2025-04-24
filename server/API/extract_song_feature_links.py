# pip install --upgrade yt_dlp
# pip install pytubefix


from pytubefix import YouTube
import os
import multiprocessing
import warnings
import numpy as np
from scipy import stats
import pandas as pd
import librosa
from tqdm import tqdm
import requests

import pickle
with open('final_optimized_classification_model.pkl', 'rb') as f:
    model = pickle.load(f)

def run_url_prob_pipeline(url):    
    

    api_url = "https://youtube-to-mp315.p.rapidapi.com/download"
    params = {"url": url}
    headers = {'x-rapidapi-key': os.getenv("RAPID_API"),'x-rapidapi-host': 'youtube-to-mp315.p.rapidapi.com'}
    
    r = requests.post(api_url, params=params, headers=headers)
    
    mp = requests.get(r.json()["downloadUrl"])
    with open("song.mp3", "wb") as f:
        f.write(mp.content)

    def columns():
        feature_sizes = dict(chroma_stft=12, chroma_cqt=12, chroma_cens=12,
                            tonnetz=6, mfcc=20, rmse=1, zcr=1,
                            spectral_centroid=1, spectral_bandwidth=1,
                            spectral_contrast=7, spectral_rolloff=1,mel_spec=128)
        moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

        columns = []
        for name, size in feature_sizes.items():
            for moment in moments:
                it = ((name, moment, '{:02d}'.format(i+1)) for i in range(size))
                columns.extend(it)

        names = ('feature', 'statistics', 'number')
        columns = pd.MultiIndex.from_tuples(columns, names=names)

        return columns.sort_values()


    def compute_features():

        features = pd.Series(index=columns(), dtype=np.float32)

        warnings.filterwarnings('error', module='librosa')

        def feature_stats(name, values):
            features[name, 'mean'] = np.mean(values, axis=1)
            features[name, 'std'] = np.std(values, axis=1)
            features[name, 'skew'] = stats.skew(values, axis=1)
            features[name, 'kurtosis'] = stats.kurtosis(values, axis=1)
            features[name, 'median'] = np.median(values, axis=1)
            features[name, 'min'] = np.min(values, axis=1)
            features[name, 'max'] = np.max(values, axis=1)

        try:
            x, sr = librosa.load("song.mp3", sr=None, mono=True)

            f = librosa.feature.zero_crossing_rate(x, frame_length=2048, hop_length=512)
            feature_stats('zcr', f)

            cqt = np.abs(librosa.cqt(x, sr=sr, hop_length=512, bins_per_octave=12,
                                    n_bins=7*12, tuning=None))
            
            assert cqt.shape[0] == 7 * 12
            assert np.ceil(len(x)/512) <= cqt.shape[1] <= np.ceil(len(x)/512)+1

            f = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)
            feature_stats('chroma_cqt', f)
            f = librosa.feature.chroma_cens(C=cqt, n_chroma=12, n_octaves=7)
            feature_stats('chroma_cens', f)
            f = librosa.feature.tonnetz(chroma=f)
            feature_stats('tonnetz', f)

            del cqt
            stft = np.abs(librosa.stft(x, n_fft=2048, hop_length=512))
            assert stft.shape[0] == 1 + 2048 // 2
            assert np.ceil(len(x)/512) <= stft.shape[1] <= np.ceil(len(x)/512)+1
            del x

            f = librosa.feature.chroma_stft(S=stft**2, n_chroma=12)
            feature_stats('chroma_stft', f)

            f = librosa.feature.rms(S=stft)
            feature_stats('rmse', f)

            f = librosa.feature.spectral_centroid(S=stft)
            feature_stats('spectral_centroid', f)
            f = librosa.feature.spectral_bandwidth(S=stft)
            feature_stats('spectral_bandwidth', f)
            f = librosa.feature.spectral_contrast(S=stft, n_bands=6)
            feature_stats('spectral_contrast', f)
            f = librosa.feature.spectral_rolloff(S=stft)
            feature_stats('spectral_rolloff', f)
            f = librosa.feature.melspectrogram(S=stft)
            feature_stats('mel_spec', f)
            
            
            
            mel = librosa.feature.melspectrogram(sr=sr, S=stft**2)
            del stft
            f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
            feature_stats('mfcc', f)


        except Exception as e:
            print('{}'.format( repr(e)))
        
        return features

    features = pd.DataFrame(compute_features())

    url_features = features.transpose()

    mel_spec = url_features['mel_spec']

    mel_spec.columns = pd.MultiIndex.from_tuples([
        ('mel_spec',) + col if isinstance(col, tuple) else ('mel_spec', col)
        for col in mel_spec.columns
    ])

    url_features = url_features.drop('mel_spec',axis=1).merge(mel_spec,left_index=True,right_index=True)
    
    # features.to_csv("song.csv")
    print(url_features)
    return pd.DataFrame(model.predict_proba(url_features),columns = ["Rock","Electronic","Pop","Hip-Hop","Folk"])

