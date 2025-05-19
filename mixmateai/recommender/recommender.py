from sklearn.neighbors import NearestNeighbors
import pandas as pd
import os


csv_path = os.path.join(os.path.dirname(__file__), 'tracks.csv')
df = pd.read_csv(csv_path)

df = df.dropna(subset=['track_name', 'artist_name', 'danceability', 'energy', 'valence', 'tempo'])
df = df.reset_index(drop=True)

features = ['danceability', 'energy', 'valence', 'tempo']
X = df[features]


model = NearestNeighbors(n_neighbors=6, algorithm='auto', metric='euclidean')
model.fit(X)


def get_recommendations(song_title, top_n=5):
    if song_title not in df['track_name'].values:
        return f"'{song_title}' not found in dataset."
    
    idx = df[df['track_name'] == song_title].index[0]
    distances, indices = model.kneighbors([X.iloc[idx]], n_neighbors=top_n+1)
    recommended = [df.iloc[i]['track_name'] for i in indices.flatten()[1:]]
    return recommended


if __name__ == "__main__":
    song = "Keys of Love"
    recs = get_recommendations(song)
    print("🎵 Recommended songs for:", song)
    print(recs)