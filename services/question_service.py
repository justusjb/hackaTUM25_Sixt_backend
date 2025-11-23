from groq import Groq
import json
from pathlib import Path
from config import get_settings
from models import CustomerData

settings = get_settings()
client = Groq(api_key=settings.groq_api_key)


def load_prompt(prompt_name: str) -> str:
    """Load prompt template from file."""
    prompt_path = Path(__file__).parent.parent / "prompts" / f"{prompt_name}.txt"
    with open(prompt_path, "r") as f:
        return f.read()


def parse_llm_response(response_text: str) -> dict:
    """Parse and clean LLM response."""
    response_text = response_text.strip()

    # Remove markdown code blocks if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    return json.loads(response_text)


def generate_decision_tree(customer_data: CustomerData) -> dict:
    """Generate a decision tree based on customer data."""
    prompt_template = load_prompt("decision_tree")
    prompt = prompt_template.format(
        customer_data=json.dumps(customer_data.model_dump(), indent=2)
    )

    completion = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=settings.model_temperature,
        seed=settings.model_seed,
    )

    response_text = completion.choices[0].message.content
    tree = parse_llm_response(response_text)

    return tree
