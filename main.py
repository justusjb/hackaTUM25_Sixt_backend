from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import json
import os
import dotenv

dotenv.load_dotenv()
app = FastAPI()

# CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class TreeResponse(BaseModel):
    tree: dict


@app.post("/generate-questions", response_model=TreeResponse)
def generate_questions():
    # Hardcoded customer data for now
    customer_data = {
        "name": "John Doe",
        "destination": "Swiss Alps",
        "party_size": 3,
        "previous_rentals": ["SUV with ski rack", "4WD in winter"],
        "booking_date": "2024-12-15"
    }

    prompt = f"""You are a car rental assistant. Based on this customer data, create a decision tree of YES/NO questions to determine the best car upgrade options.

Customer Data:
{json.dumps(customer_data, indent=2)}

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation):
{{
  "gear": {{
    "id": 1,
    "key": "gear",
    "question": "All 3 of you bringing ski gear?",
    "image": "/ski-gear.jpg",
    "yes": "alpine",
    "no": "snow"
  }},
  "alpine": {{
    "id": 2,
    "key": "alpine",
    "question": "Taking the high alpine passes?",
    "image": "/alpine-pass.jpg",
    "yes": "snow",
    "no": null
  }},
  "snow": {{
    "id": 3,
    "key": "snow",
    "question": "Expecting snow on the roads?",
    "image": "/snow-on-the-road.jpg",
    "yes": null,
    "no": null
  }}
}}

Rules:
- Create 2-4 relevant questions based on the customer data
- Each question must be a YES/NO question
- Use keys like "gear", "alpine", "snow", "luggage", "comfort", etc.
- Set "yes" and "no" to the key of the next question, or null if it's a terminal node
- Use placeholder images like "/ski-gear.jpg", "/alpine-pass.jpg", "/luggage.jpg", etc.
- Make questions relevant to car rental upgrades (space, terrain, weather, comfort)

Return ONLY the JSON object, nothing else."""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        seed=42,  # Fixed seed for deterministic results
    )

    response_text = completion.choices[0].message.content.strip()

    # Remove markdown code blocks if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    tree = json.loads(response_text)

    return {"tree": tree}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
