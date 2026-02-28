"""Claude-powered review response generation."""
from __future__ import annotations
import os

try:
    import anthropic
    _CLIENT = None

    def _get_client():
        global _CLIENT
        if _CLIENT is None:
            _CLIENT = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        return _CLIENT

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


SENTIMENT_PROMPTS = {
    "positive": (
        "The customer left a glowing review. Write a warm, genuine, and brief thank-you response "
        "that feels personal and encourages them to return. Do not use generic phrases like "
        "'We appreciate your feedback'. Reference specifics from their review if possible."
    ),
    "neutral": (
        "The customer left a mixed review with some praise and some concerns. Write a professional "
        "response that thanks them for the honest feedback, acknowledges any issues mentioned "
        "without being defensive, and shows commitment to improvement."
    ),
    "negative": (
        "The customer left a negative review. Write a calm, empathetic, and professional response. "
        "Apologise sincerely for their experience, do not make excuses, offer to make it right "
        "(invite them to reach out directly), and show that the feedback is taken seriously. "
        "Never argue or be defensive."
    ),
}


def generate_response(
    business_name: str,
    business_category: str | None,
    reviewer_name: str,
    rating: int,
    review_text: str | None,
    brand_voice: str | None = None,
) -> str:
    """Generate an AI review response using Claude.

    Falls back to a template-based response if the Anthropic SDK is not
    installed or the API key is missing.
    """
    sentiment = "positive" if rating >= 4 else ("neutral" if rating == 3 else "negative")

    if not ANTHROPIC_AVAILABLE or not os.environ.get("ANTHROPIC_API_KEY"):
        return _template_fallback(business_name, reviewer_name, rating, review_text, sentiment)

    system_prompt = _build_system_prompt(business_name, business_category, brand_voice)
    user_prompt = _build_user_prompt(reviewer_name, rating, review_text, sentiment)

    try:
        client = _get_client()
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=300,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text.strip()
    except Exception as exc:
        return _template_fallback(business_name, reviewer_name, rating, review_text, sentiment)


def _build_system_prompt(
    business_name: str,
    business_category: str | None,
    brand_voice: str | None,
) -> str:
    parts = [
        f"You are a review response writer for {business_name}"
        + (f", a {business_category}" if business_category else "")
        + ".",
        "Write concise responses (2-4 sentences). Be authentic, never robotic.",
        "Do NOT include subject lines or sign-offs — just the response body.",
    ]
    if brand_voice:
        parts.append(f"Brand voice instructions: {brand_voice}")
    return " ".join(parts)


def _build_user_prompt(
    reviewer_name: str,
    rating: int,
    review_text: str | None,
    sentiment: str,
) -> str:
    lines = [
        f"Review from: {reviewer_name}",
        f"Star rating: {rating}/5",
    ]
    if review_text:
        lines.append(f"Review text: {review_text}")
    lines.append("")
    lines.append(SENTIMENT_PROMPTS[sentiment])
    return "\n".join(lines)


def _template_fallback(
    business_name: str,
    reviewer_name: str,
    rating: int,
    review_text: str | None,
    sentiment: str,
) -> str:
    """Basic template response used when AI is unavailable."""
    first_name = reviewer_name.split()[0] if reviewer_name else "there"
    if sentiment == "positive":
        return (
            f"Thank you so much, {first_name}! We're thrilled you had such a great experience at "
            f"{business_name}. Your kind words mean the world to our team. We can't wait to see "
            "you again soon!"
        )
    elif sentiment == "neutral":
        return (
            f"Thank you for your honest feedback, {first_name}. We're glad parts of your visit to "
            f"{business_name} met your expectations, and we take your comments seriously as we "
            "continuously work to improve. We hope to exceed your expectations next time!"
        )
    else:
        return (
            f"We sincerely apologise that your experience at {business_name} fell short of your "
            f"expectations, {first_name}. This is not the standard we hold ourselves to. Please "
            "reach out to us directly so we can make this right — your satisfaction is our "
            "top priority."
        )
