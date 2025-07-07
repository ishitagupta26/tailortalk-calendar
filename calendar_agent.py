# calendar_agent.py

import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytz
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Google Calendar API setup
service_account_info = {
    "type": os.environ["type"],
    "project_id": os.environ["project_id"],
    "private_key_id": os.environ["private_key_id"],
    "private_key": os.environ["private_key"].replace("\\n", "\n"),  # important fix
    "client_email": os.environ["client_email"],
    "client_id": os.environ["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": os.environ["token_uri"],
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ["client_x509_cert_url"],
}
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'c84a668e0342524fd101cf6f89513ef89194cadaf8bf2c66f314204f250151d6@group.calendar.google.com'

credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)

# Calendar Event Creator Function
def create_event_on_calendar(text: str):
    print("📌 Tool triggered with text:", text)
# Fix datetime handling and timezone
    IST = pytz.timezone("Asia/Kolkata")
    now = datetime.now(IST)

    # Date Extraction
# Date Extraction (support both "9 July" and "July 9")
    date_match = re.search(r'(\d{1,2})(?:[a-z]{2})?\s+(July|August|September)', text, re.IGNORECASE)
    if not date_match:
        date_match = re.search(r'(July|August|September)\s+(\d{1,2})', text, re.IGNORECASE)

    if date_match:
        if date_match.lastindex == 2:
            if date_match.group(1).isalpha():  # e.g., "July 9"
                month_str = date_match.group(1)
                day = int(date_match.group(2))
            else:  # e.g., "9 July"
                day = int(date_match.group(1))
                month_str = date_match.group(2)

            month = datetime.strptime(month_str, "%B").month
            year = now.year
        else:
            day, month, year = now.day, now.month, now.year

    # Time Extraction
    time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(AM|PM)', text, re.IGNORECASE)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        if time_match.group(3).upper() == "PM" and hour != 12:
            hour += 12
        elif time_match.group(3).upper() == "AM" and hour == 12:
            hour = 0
    else:
        hour, minute = now.hour + 1, 0

    # ✅ Timezone-aware datetime
    start_time = IST.localize(datetime(year, month, day, hour, minute))
    end_time = start_time + timedelta(hours=1)

    event = {
        "summary": "Meeting from TailorTalk",
        "description": f"Auto-created from chat: \"{text}\"",
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"📅 Event created successfully: [View on Calendar]({created_event.get('htmlLink')})"


# LLM setup using OpenRouter Gemini or other models
llm = ChatOpenAI(
    temperature=0,
    model_name=os.getenv("OPENAI_MODEL_NAME"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
)

# LangChain Tool wrapper
tools = [
    Tool(
        name="CreateGoogleCalendarEvent",
        func=create_event_on_calendar,
        description="Use this tool to create a meeting on Google Calendar. Input should contain time like '4 PM' and optionally a date like 'on July 7'."
    )
]

# Agent setup
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True  # 👈 Add this line
)


# Final callable function
def run_calendar_agent(query):
    result = agent.run(query)
    return result
