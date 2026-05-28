import json
import os
import uuid

from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

def try_provider(provider_name: str, provider_function, text: str) -> list[dict]:
    try: 
        tasks = provider_function(text)

        if tasks:
            print(f"Using {provider_name} AI parser")
            return tasks
        
    except Exception as error:
        print(f"{provider_name} AI parsing failed: {error}")

    return []

def extract_tasks_with_ai(text: str) -> list[dict]:
    provider = os.getenv("AI_PROVIDER", "groq").lower()

    try:
        if provider == "groq":
            groq_tasks = try_provider("groq", extract_tasks_with_groq, text)

            if groq_tasks:
                return groq_tasks
            
            gemini_tasks = try_provider("gemini", extract_tasks_with_groq, text)

            if gemini_tasks:
                return gemini_tasks
            
            return []
        
        if provider == "gemini":
            gemini_tasks = try_provider("gemini", extract_tasks_with_gemini, text)

            if gemini_tasks:
                return gemini_tasks
            
            return []
        
        return []
    
    except Exception as error:
        print(f"AI parsing failed: {error}")
        return []
    
def extract_tasks_with_groq(text: str) -> list[dict]:
    """Uses Groq to extract structured tasks from a brain dump."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return []
    
    client = Groq(api_key=api_key)

    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    prompt = f"""
Return ONLY raw JSON. No intro. No markdown. No explanation.

Format:
{{"tasks":[{{"title":"Finish resume","due_date":"Friday","urgency":"medium"}}]}}

Extract tasks from:
{text}
"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You extract productivity tasks and return only valid compact JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=2000,
    )

    raw_text = response.choices[0].message.content or ""
    raw_text = raw_text.strip()

    print("RAW GROQ RESPONSE:", repr(raw_text))

    if not raw_text:
        return []
    
    start = raw_text.find("{")
    end = raw_text.rfind("}") + 1

    if start == -1 or end == 0:
        return []
    
    clean_json = raw_text[start:end]

    data = json.loads(clean_json)

    return normalize_ai_tasks(data)

def extract_tasks_with_gemini(text: str) -> list[dict]:
    """Uses Gemini to extract structured tasks from a brain dump."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return []

    
    client = genai.Client(api_key=api_key)

    prompt = f"""
Return ONLY raw JSON. No intro. No markdown. No explanation.

Format:
{{"tasks":[{{"title":"Finish resume","due_date":"Friday","urgency":"medium"}}]}}

Extract tasks from:
{text}
"""


    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "max_output_tokens": 2000,
            "temperature": 0.1
        }
    )

    raw_text = (response.text or "").strip()

    print("RAW GEMINI RESPONSE:", repr(raw_text))

    if not raw_text:
        return []

    start = raw_text.find("{")
    end = raw_text.find("}")

    if start == -1 or end == 0:
        return []

    data = json.loads(raw_text)

    return normalize_ai_tasks(data)
    
def normalize_ai_tasks(data: dict) -> list[dict]:
    tasks = []

    for item in data.get("tasks", []):
        title = item.get("title")

        if not title:
            continue

        tasks.append({
            "id": str(uuid.uuid4()),
            "title": title.strip().capitalize(),
            "due_date": item.get("due_date"),
            "urgency": item.get("urgency", "normal"),
            "completed": False
        })

    return tasks
