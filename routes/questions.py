from fastapi import APIRouter
from models import TreeResponse, CustomerData
from services.question_service import generate_decision_tree

router = APIRouter(prefix="/api", tags=["questions"])


@router.post("/generate-questions", response_model=TreeResponse)
def generate_questions():
    """Generate personalized decision tree for car rental upgrades."""
    # Hardcoded customer data for now
    customer_data = CustomerData(
        name="John Doe",
        destination="Swiss Alps",
        party_size=3,
        previous_rentals=["SUV with ski rack", "4WD in winter"],
        booking_date="2024-12-15"
    )

    tree = generate_decision_tree(customer_data)
    return {"tree": tree}
