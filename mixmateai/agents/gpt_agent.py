# mixmateai/agents/gpt_agent.py
import requests
from pydub import AudioSegment
import os
import json
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_ollama_connection():
    """Verify Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434", timeout=5)
        if response.status_code != 200:
            raise ConnectionError("Ollama not responding properly")
        logger.info("Ollama connection verified")
    except Exception as e:
        logger.error("Ollama connection failed: %s", str(e))
        raise

def generate_mashup_plan(prompt: str) -> Dict:
    """Generate validated mashup plan using Ollama/Mistral"""
    validate_ollama_connection()

    system_prompt = """You are a music mashup assistant. Return ONLY JSON with:
- "songs": List of exact filenames from assets folder (case-sensitive)
- "segments": List of [start_ms, end_ms] for each song (numbers only)
- "crossfade_ms": Optional number between 500-3000 (default: 1000)

Example response:
{
  "songs": ["Believer.mp3", "Kesariya.mp3"],
  "segments": [[0, 30000], [0, 30000]],
  "crossfade_ms": 1500
}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "mistral",
                "messages": messages,
                "stream": False,
                "format": "json"
            },
            timeout=30
        )
        response.raise_for_status()
        
        # Clean and parse response
        content = response.json()["message"]["content"]
        content = content.strip().replace('```json', '').replace('```', '')
        logger.debug("Raw Ollama response: %s", content)
        
        plan = json.loads(content)
        
        # Validate structure
        if not isinstance(plan.get("songs", []), list) or \
           not isinstance(plan.get("segments", []), list):
            raise ValueError("Invalid plan structure")
            
        if len(plan["songs"]) != len(plan["segments"]):
            raise ValueError("Songs and segments count mismatch")

        # Convert all numbers to integers
        plan["segments"] = [
            [int(start), int(end)] for start, end in plan["segments"]
        ]
        
        if "crossfade_ms" in plan:
            plan["crossfade_ms"] = int(plan["crossfade_ms"])
        else:
            plan["crossfade_ms"] = 1000

        logger.info("Validated mashup plan: %s", plan)
        return plan

    except json.JSONDecodeError as e:
        logger.error("JSON parsing failed: %s\nContent: %s", e, content)
        raise ValueError("Invalid JSON response from AI model") from e
    except requests.exceptions.RequestException as e:
        logger.error("API request failed: %s", str(e))
        raise
    except Exception as e:
        logger.error("Plan generation failed: %s", str(e))
        raise

def create_mashup(plan: Dict, output_path: str = "outputs/mashup_output.mp3") -> str:
    """Create audio mashup from validated plan"""
    try:
        songs: List[str] = plan["songs"]
        segments: List[List[int]] = plan["segments"]
        crossfade_ms: int = plan["crossfade_ms"]

        if len(songs) < 2:
            raise ValueError("At least 2 songs required for mashup")

        mashup = AudioSegment.empty()
        logger.info("Starting mashup of %d songs", len(songs))

        for idx, song_file in enumerate(songs):
            full_path = os.path.join("mixmateai/assets", song_file.strip())
            
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Audio file not found: {full_path}")
                
            audio = AudioSegment.from_file(full_path)
            start, end = segments[idx]
            
            # Validate segment times
            if start < 0 or end <= start:
                raise ValueError(f"Invalid segment for {song_file}: {start}-{end}")
            if end > len(audio):
                raise ValueError(f"Segment end {end}ms exceeds {song_file} duration ({len(audio)}ms)")

            segment = audio[start:end]
            
            if idx == 0:
                mashup = segment
            else:
                mashup = mashup.append(segment, crossfade=crossfade_ms)
            
            logger.info("Added %s (%d-%d ms)", song_file, start, end)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        mashup.export(output_path, format="mp3")
        logger.info("Mashup saved to: %s", output_path)
        return output_path

    except Exception as e:
        logger.error("Mashup creation failed: %s", str(e))
        raise