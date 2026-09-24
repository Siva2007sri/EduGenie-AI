from gemini_client import generate_text
from utils import validate_text


def get_learning_recommendations(text: str) -> str:
    """
    Generate a personalized learning path using Gemini.
    """

    text = validate_text(text)

    prompt = f"""
Create a personalized educational learning path for:

{text}

Organize the learning path from beginner to advanced.

Include:

1. Prerequisites
2. Beginner topics
3. Intermediate topics
4. Advanced topics
5. Practice projects
6. Suggested timeline
7. Types of learning resources to use

Requirements:
- Make the path suitable for a learner starting from the basics.
- Organize the topics clearly.
- Keep the recommendations practical.
- Do not invent specific URLs.
"""

    return generate_text(prompt)