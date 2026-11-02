# Contradiction Detective 🔍

An AI-powered application that analyses two statements and identifies whether they contradict each other, partially conflict, are compatible, or contain insufficient information.

## Overview

Contradiction Detective uses Google's Gemini API to compare two statements and generate a structured analysis.

The application provides a FastAPI backend and a simple web interface. It uses Pydantic for input validation and structured AI responses.

## Features

- Compare two statements using AI.
- Classify statements into four categories:
  - `direct_contradiction`
  - `partial_conflict`
  - `compatible`
  - `insufficient_information`
- Generate explanations and supporting evidence.
- Identify possible explanations for conflicting statements.
- Provide a confidence level: low, medium, or high.
- Return structured JSON responses.
- Validate user inputs before sending them to Gemini.
- Apply API rate limiting to reduce excessive requests.
- Provide a simple web interface.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| Pydantic | Input validation and response schemas |
| Google Gemini API | AI-powered statement analysis |
| Google GenAI SDK | Communication with Gemini |
| HTML, CSS, JavaScript | Frontend |
| Docker | Application containerization |
| Render | Cloud deployment |
| Git and GitHub | Version control |
| GitHub Actions | Continuous integration |
| SlowAPI | API rate limiting |

## Architecture

The application follows a simple client-server architecture.

1. The user enters two statements in the web interface.
2. JavaScript sends a POST request to the FastAPI backend.
3. Pydantic validates the incoming data.
4. FastAPI sends valid statements to the Gemini API.
5. Gemini returns a structured response.
6. FastAPI validates the AI response and returns it to the frontend.
7. JavaScript displays the analysis to the user.

```text
             User
               |
               v
       HTML / CSS / JavaScript
               |
               | POST /analyse
               v
          FastAPI Backend
               |
        +------+------+
        |             |
        v             v
   Pydantic       SlowAPI
   Validation   Rate Limiting
        |
        v
    Gemini API
        |
        v
 Structured AI Response
        |
        v
   FastAPI Response
        |
        v
   Frontend Display
```

## Project Structure

```text
ai-engineering-week4/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py
├── schemas.py
├── config.py
├── logger_config.py
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Nitisha620/contradiction-detective.git
cd ai-engineering-week4
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
APP_ENV=development
REQUEST_TIMEOUT=20000
```

Replace the placeholder with your Gemini API key.

### 5. Start the application

```bash
uvicorn main:app --reload
```

Open the application:

- Web interface: http://localhost:8000
- Swagger API documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `APP_ENV` | Application environment |
| `REQUEST_TIMEOUT` | Gemini request timeout in milliseconds |

**Security:** Never commit `.env` or expose API keys in frontend JavaScript. Configure production secrets through your hosting provider's environment settings.

## Running with Docker

### 1. Build the Docker image

```bash
docker build -t contradiction-detective .
```

### 2. Run the container

```bash
docker run -d \
  --name contradiction-detective \
  -p 8000:8000 \
  --env-file .env \
  contradiction-detective
```

On Windows PowerShell, you can use backticks instead of backslashes for multiline commands.

### 3. Access the application

http://localhost:8000

### 4. Stop the container

```bash
docker stop contradiction-detective
docker rm contradiction-detective
```

## API Endpoints

### GET /

Returns the application's frontend.

### POST /analyse

Accepts two statements and returns their AI-generated analysis.

**Request body:**

```json
{
  "statement_a": "The Earth revolves around the Sun.",
  "statement_b": "The Earth does not revolve around the Sun."
}
```

**Response structure:**

```json
{
  "classification": "direct_contradiction",
  "explanation": "The statements make opposing claims.",
  "evidence": [
    "Statement A says the Earth revolves around the Sun.",
    "Statement B denies that claim."
  ],
  "possible_explanations": [],
  "confidence": "high"
}
```

The actual response depends on the statements and the AI analysis.

## Continuous Integration

The project uses GitHub Actions for basic continuous integration.

The workflow runs when code is pushed to the `main` branch or a pull request targeting `main` is created or updated.

It performs the following checks:

- Checks out the repository.
- Sets up Python 3.12.
- Installs dependencies.
- Checks Python syntax.
- Verifies that the FastAPI application initializes.

## Deployment

The application is deployed using Render as a Docker Web Service.

Deployment configuration:

- Source: GitHub repository
- Runtime: Docker
- Dockerfile: `./Dockerfile`
- Branch: `main`

Production environment variables are configured through the Render dashboard.

## Known Limitations

- AI-generated classifications and explanations may not always be factually correct.
- Confidence levels are model-generated estimates, not calibrated probabilities.
- Gemini API availability and free-tier quotas can affect application availability.
- The application does not currently have user login or authentication.
- Rate limiting currently uses the default in-memory storage and requires additional configuration for multi-instance production deployments.
- The GitHub Actions workflow performs basic checks, not comprehensive automated application testing.
- The application is designed for comparing two statements and is not a general-purpose fact-checking system.

## Future Improvements

- Add user authentication and authorization.
- Introduce persistent storage for analysis history.
- Improve automated testing.
- Add monitoring and more detailed application metrics.
- Improve error handling and AI response quality.
- Introduce shared rate-limit storage for scalable deployments.

## License

This project is currently intended for learning and educational purposes.