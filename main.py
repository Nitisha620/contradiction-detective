from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import ValidationError
import time

from schemas import AnalysisRequest, AnalysisResponse

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from config import settings

from logger_config import logger

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


api_key = settings.GEMINI_API_KEY

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)

app = FastAPI(
    title="Contradiction Detective",
    description="An API that analyses two statements for contradictions.",
    version="1.0.0"
)

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
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
@limiter.limt("5/minute")
def analyse_statements(request: AnalysisRequest):

    start_time = time.perf_counter()

    logger.info("Analysis request received.")

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

        elapsed_time = time.perf_counter() - start_time

        logger.info(
            "Gemini response received in %.2f seconds",
            elapsed_time
        )

        return AnalysisResponse.model_validate_json(response.text)

    except ValidationError:
        logger.error("Gemini returned an invalid response.")

        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid response."
        )

    except Exception as error:

        elapsed_time = time.perf_counter() - start_time

        logger.error(
            "Gemini API request failed after %.2f seconds. Error: %s",
            elapsed_time,
            type(error).__name__
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to analyse the statements right now."
        )