from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import ValidationError

from schemas import AnalysisRequest, AnalysisResponse

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from config import settings


api_key = settings.GEMINI_API_KEY

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)

app = FastAPI(
    title="Contradiction Detective",
    description="An API that analyses two statements for contradictions.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/analyse", response_model=AnalysisResponse)
def analyse_statements(request: AnalysisRequest):

    prompt = f"""
    You are a Contradiction Detective.

    Analyse the following two statements.

    Statement A: {request.statement_a}
    Statement B: {request.statement_b}

    Classify them as one of:
    - direct_contradiction
    - partial_conflict
    - compatible
    - insufficient_information

    Explain your reasoning.
    Identify supporting evidence.
    Mention possible explanations if there is a conflict.

    Rules:
    - Do not invent facts.
    - Do not assume different statements contradict each other
      simply because they discuss different things.
    - If information is insufficient, say so.
    - Be concise and objective.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=AnalysisResponse.model_json_schema(),
                http_options=types.HttpOptions(
                    timeout=settings.REQUEST_TIMEOUT
                )
            )
        )

        return AnalysisResponse.model_validate_json(response.text)

    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid response."
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to analyse the statements right now."
        )