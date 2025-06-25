# Weather AI Agent ADK

Agent that fetches accurate, up-to-date weather data for any location.

## Installation

1. Clone the repo:  
   ```bash
   git clone https://github.com/rivka14/weather-ai-agent-adk.git
   cd weather-ai-agent-adk
   ```
2. Create a virtual environment and install dependencies:  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy and configure environment variables:  
   ```bash
   cp .env.example .env
   # Open .env and add your API keys
   ```


## Project Structure

```text
weather-ai-agent-adk/
├── weather_agent/
│   ├── __init__.py
│   └── agent.py         # Core logic for fetching weather data
├── .env.example         # Sample environment file
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── .gitignore           # Git ignore rules
```

## Environment Variables

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=
OPENWEATHERMAP_API_KEY=
```
