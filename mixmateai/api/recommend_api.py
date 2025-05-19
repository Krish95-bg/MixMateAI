from fastapi import FastAPI, Query
import pandas as pd
import os
from sklearn.neighbors import NearestNeighbors

app = FastAPI()

@app.get("/")
def root():
    return {"message": "🎧 MixMateAI KNN Recommender API is running!"}

# ✅ Load dataset
csv_path = os.path.join(os.path.dirname(__file__), '../recommender/tracks.csv')
df = pd.read_csv(csv_path)

# ✅ Clean & prepare data
df = df.dropna(subset=['track_name', 'artist_name', 'danceability', 'energy', 'valence', 'tempo'])
df = df.reset_index(drop=True)

# ✅ Use audio features only
features = ['danceability', 'energy', 'valence', 'tempo']
X = df[features]

# ✅ Fit KNN model
model = NearestNeighbors(n_neighbors=6, algorithm='auto', metric='euclidean')
model.fit(X)

# ✅ Recommendation logic
def get_recommendations(song_title, top_n=5):
    if song_title not in df['track_name'].values:
        return []
    
    idx = df[df['track_name'] == song_title].index[0]
    distances, indices = model.kneighbors([X.iloc[idx]], n_neighbors=top_n+1)
    recommended = [df.iloc[i]['track_name'] for i in indices.flatten()[1:]]
    return recommended

# ✅ API endpoint
@app.get("/recommend")
def recommend(song: str = Query(..., description="Enter song title")):
    recs = get_recommendations(song)
    if not recs:
        return {"message": f"'{song}' not found in dataset."}
    return {"recommendations": recs}