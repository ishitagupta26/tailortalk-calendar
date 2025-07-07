# TailorTalk Calendar Assistant

The TailorTalk Calendar Assistant is an intelligent conversational agent that allows users to book Google Calendar events using natural language. It leverages Streamlit for the chat UI, LangChain for tool-based agent logic, and OpenRouter's LLMs for interpreting user queries.

# Live Demo  
👉 [Try the App on Render](https://tailortalk-calendar.onrender.com)

local url 
http://localhost:8501/

---
# Features
- Book meetings via natural language
- Powered by LangChain ReAct agent + OpenRouter LLM
- Timezone-aware calendar entries (Asia/Kolkata)
- Tool-calling architecture with LangChain `Tool`
- Handles date and time parsing (e.g., "Book meeting on July 9 at 4 PM")
- Google Calendar integration via Service Account
- Deployed on Render using `render.yaml`

# Technologies Used

- Python
- Streamlit
- LangChain
- Google Calendar API
- OpenRouter (LLM)
- Render.com

# Project Structure
tailortalk-calendar-bot/
  app.py  (Main Streamlit UI)
  calendar_agent.py (Agent + Tool definitions)
  calendar-service-account.json (GCP service account key)    
  .env  (OpenRouter credentials)
  render.yaml  (Deployment config)
  README.md 
  requirements.txt   (Python dependencies)


# Setup Instructions (Local)

1. Clone the Repository

git clone https://github.com/your-username/tailortalk-calendar.git
cd tailortalk-calendar

2. Install Dependencies
pip install -r requirements.txt

3. Create a .env file

OPENAI_API_KEY=your-openrouter-key
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_MODEL_NAME=mistralai/mistral-7b-instruct

4. Add Google Service Account Key
Save your calendar-service-account.json file in the root directory.

5. Run the App
streamlit run app.py

# Google Calendar Integration
--Go to Google Cloud Console
--Enable the Google Calendar API
--Create a Service Account and download the JSON key
--Share your Google Calendar with the service account email with Editor access
--Replace CALENDAR_ID in calendar_agent.py with your calendar's ID

# Deployment on Render
--Push your code to GitHub
--Connect GitHub repo to Render
--Set the Environment Variables from .env
--Use render.yaml to deploy automatically

Sample render.yaml:

services:
  - type: web
    name: tailor-calendar-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py
    envVars:
      - key: OPENAI_API_KEY
        value: sk-or-...your_key...
      - key: OPENAI_API_BASE
        value: https://openrouter.ai/api/v1
      - key: OPENAI_MODEL_NAME
        value: mistralai/mistral-7b-instruct

# Sample Prompts
1. "Schedule a meeting tomorrow at 3 PM"

2. "Book an appointment on July 10 at 10:30 AM"

3. "Create event on 11 August at 4 PM"
