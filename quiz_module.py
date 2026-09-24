from gemini_client import generate_text
from utils import parse_json_response, validate_text


def validate_quiz(data: dict, expected_count: int) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Quiz response must be a JSON object.")

    questions = data.get("questions")

    if not isinstance(questions, list):
        raise ValueError("Quiz response must contain a questions list.")

    if len(questions) != expected_count:
        raise ValueError(
            f"Expected {expected_count} questions, got {len(questions)}."
        )

    for index, question in enumerate(questions, start=1):

        if not isinstance(question, dict):
            raise ValueError(f"Question {index} is invalid.")

        if not question.get("question"):
            raise ValueError(
                f"Question {index} is missing its text."
            )

        options = question.get("options")

        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(
                f"Question {index} must have exactly 4 options."
            )

        correct_answer = question.get("correct_answer")

        if correct_answer not in options:
            raise ValueError(
                f"Question {index} has an invalid correct answer."
            )

        if not question.get("explanation"):
            raise ValueError(
                f"Question {index} is missing an explanation."
            )

    return data


def generate_quiz(text: str, count: int = 3) -> dict:
    text = validate_text(text)

    if count < 1 or count > 10:
        raise ValueError("Quiz count must be between 1 and 10.")

    prompt = (
        "Create an educational multiple-choice quiz about:\n\n"
        + text
        + "\n\n"
        + "Generate exactly "
        + str(count)
        + " questions.\n\n"
        + "Return ONLY valid JSON in this exact structure:\n\n"
        + "{\n"
        + '  "questions": [\n'
        + "    {\n"
        + '      "question": "Question text",\n'
        + '      "options": [\n'
        + '        "Option A",\n'
        + '        "Option B",\n'
        + '        "Option C",\n'
        + '        "Option D"\n'
        + "      ],\n"
        + '      "correct_answer": "One of the four options exactly",\n'
        + '      "explanation": "Short explanation of why the answer is correct."\n'
        + "    }\n"
        + "  ]\n"
        + "}\n\n"
        + "Rules:\n"
        + "- Generate exactly "
        + str(count)
        + " questions.\n"
        + "- Each question must have exactly 4 options.\n"
        + "- Only one option should be correct.\n"
        + "- correct_answer must exactly match one of the four options.\n"
        + "- Keep the questions educational and clear.\n"
        + "- Provide a short explanation for every answer."
    )

    raw_response = generate_text(
        prompt,
        response_mime_type="application/json",
        temperature=0.3,
    )

    data = parse_json_response(raw_response)

    return validate_quiz(data, count)