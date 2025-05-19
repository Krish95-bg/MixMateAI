🎧 MixMateAI
Note: This project is currently a work-in-progress and actively being improved.

MixMateAI is a powerful AI-driven music assistant capable of generating audio mashups and recommending songs based on user input. It integrates machine learning, signal processing, and natural language interaction via LLMs like Mistral running locally with Ollama.

🚀 Features

🔊 Mashup Generator (via AI Agent)

Accepts a natural language prompt like:

"Create a mashup of Kesariya.mp3 and Believer.mp3 from 0 to 30 seconds each, with 1500 milliseconds crossfade."

Uses Mistral LLM via Ollama to generate a mashup plan

Cuts and merges MP3 files using pydub

Returns a downloadable mashup_output.mp3

🎵 Song Recommendation Engine

Based on K-Nearest Neighbors (KNN) algorithm

Recommends similar tracks from the dataset (e.g. based on genres, tempo, etc.)

Can serve as a content-based recommendation tool for playlists or mood matching

🛠️ Tech Stack

FastAPI: For RESTful API interface

Python 3.11

Pydub: Audio processing

scikit-learn: KNN-based recommendation

Ollama + Mistral: Local LLM chat inference

JSON-based interaction for model control

📦 Installation & Setup

Clone the repo:

git clone https://github.com/YOUR-USERNAME/MixMateAI.git
cd MixMateAI

Create virtual environment:

python -m venv mixmateai/venv
source mixmateai/venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Ensure Ollama and Mistral are running:

ollama run mistral &

Start the API:

uvicorn mixmateai.api.mashup_api:app --reload --port 8001

🧠 How It Works

Mashup API:

Receives user prompt

Sends to Ollama's local LLM API (/api/chat)

Extracts segments and crossfade info

Uses pydub to merge clips

Recommender API:

Uses tracks.csv and vectorizes features

Applies KNN to find closest matches

🚧 Future Enhancements



📁 Project Structure

MixMateAI/
├── mixmateai/
│   ├── api/                # FastAPI route handlers
│   ├── agents/             # LLM + logic for mashup creation
│   ├── assets/             # MP3 files for mashup
│   ├── recommender/        # KNN recommender logic
│   ├── venv/               # Python virtual environment
└── outputs/             # Generated mashup audio files

🤝 Contributing

If you'd like to contribute features or ideas, feel free to open an issue or pull request!

📢 License

MIT License

✨ Created with love by @krishnarajoria

