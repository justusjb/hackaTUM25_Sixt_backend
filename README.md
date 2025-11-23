# Car Rental Decision Tree API

AI-powered backend that generates personalized car rental upgrade questionnaires.

## What It Does

Takes customer booking data → Calls Groq/Llama 3 → Returns a custom decision tree of yes/no questions to determine optimal car upgrades.

## Tech Stack

- **FastAPI** - REST API
- **Groq API** - LLM inference (Llama 3.3 70B)
- **Deterministic** - Fixed seed for consistent results
