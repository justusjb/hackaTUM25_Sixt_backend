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

You MUST return ONLY a valid JSON object with NO markdown formatting, NO code blocks, NO explanations.

CRITICAL REQUIREMENTS:
1. You MUST include these exact 3 questions with their exact images:
   - "gear" with image "/ski-gear.jpg"
   - "alpine" with image "/alpine-pass.jpg"  
   - "snow" with image "/snow-on-the-road.jpg"

2. You can EXTEND the tree by adding 2-5 additional questions
3. For any NEW questions you add, ALWAYS use the image "/empty.jpg"
4. null means END OF QUESTIONS - when a user reaches null, the questionnaire is complete
5. Create multiple paths through the tree with different endpoints (null values)

Example structure (you must extend this):
{{
    "snow": {{
    "id": 1,
    "key": "snow",
    "question": "Expecting snow on the roads?",
    "image": "/snow-on-the-road.jpg",
    "yes": "alpine",
    "no": null
  }}
  "alpine": {{
    "id": 2,
    "key": "alpine",
    "question": "Taking the high alpine passes?",
    "image": "/alpine-pass.jpg",
    "yes": "gear",
    "no": "gear",
  }},
  "gear": {{
    "id": 3,
    "key": "gear",
    "question": "All 3 of you bringing ski gear?",
    "image": "/ski-gear.jpg",
    "yes": null,
    "no": null,
  }},
}}

Rules:
- MUST include "gear", "alpine", and "snow" with their exact images
- New questions must use "/empty.jpg" as image
- Each key must match its "key" field value
- null means "end of questionnaire" - this is a terminal node
- Questions must be YES/NO format about car rental needs (space, terrain, weather, 4WD, comfort, passengers)
- Create logical paths based on the customer data
- Aim for 5-8 total questions

Return ONLY valid JSON. No markdown. No explanation. Just the JSON object."""

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
