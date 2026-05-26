import json
import os
import uuid

from dotenv import load_dotenv
from google import genai

load_dotenv()


def extract_tasks_with_ai(text: str) -> list[dict]:
    """Uses Gemini to extract structured tasks from a brain dump."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return []

    try:
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
    
    except Exception as error:
        print(f"AI parsing failed: {error}")
        return []