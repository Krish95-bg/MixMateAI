from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uvicorn
from mixmateai.agents import gpt_agent
import logging

app = FastAPI(title="MixMateAI Mashup API")
logger = logging.getLogger("uvicorn.error")

class MashupRequest(BaseModel):
    prompt: str

@app.on_event("startup")
async def startup_event():
    """Initialize service dependencies"""
    try:
        gpt_agent.validate_ollama_connection()
        logger.info("✅ Service initialization complete")
    except Exception as e:
        logger.critical("🚨 Service initialization failed: %s", str(e))
        raise

@app.post("/create-mashup")
async def create_mashup_api(request: MashupRequest):
    try:
        logger.info("Received request: %s", request.prompt)
        plan = gpt_agent.generate_mashup_plan(request.prompt)
        output_path = gpt_agent.create_mashup(plan)
        return FileResponse(
            path=output_path,
            media_type="audio/mpeg",
            filename="mashup_output.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "🎧 MixMateAI Mashup API is live!"}

if __name__ == "__main__":
    uvicorn.run("mixmateai.api.mashup_api:app", host="127.0.0.1", port=8001, reload=True) 