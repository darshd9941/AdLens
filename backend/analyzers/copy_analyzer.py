import re
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_vader = SentimentIntensityAnalyzer()

POWER_WORDS = [
    "free", "new", "proven", "instant", "exclusive", "limited", "save",
    "discover", "secret", "unlock", "guarantee", "easy", "fast", "now",
    "you", "your", "today", "best", "top", "official",
    "sale", "discount", "offer", "bonus", "special", "premium",
    "revolutionary", "breakthrough", "results", "success", "win",
    "growth", "scale", "transform", "boost", "increase", "double",
    "skyrocket", "dominate", "crush", "no-brainer",
]

EMOTION_TRIGGERS = {
    "urgency": ["now", "today", "limited", "hurry", "last chance", "don't miss", "act fast", "ending soon", "only"],
    "trust": ["proven", "guarantee", "official", "certified", "trusted", "secure", "safe", "warranty"],
    "excitement": ["new", "exclusive", "secret", "unlock", "discover", "revolutionary", "breakthrough", "amazing"],
    "fear": ["miss out", "before it's gone", "warning", "don't wait", "risk-free", "no obligation"],
    "curiosity": ["secret", "hidden", "what they don't tell", "revealed", "discover", "unlock", "shocking"],
    "value": ["free", "save", "discount", "bonus", "extra", "more", "best price", "affordable"],
    "belonging": ["community", "join", "together", "our", "we", "family", "members"],
}


def analyze_sentiment_vader(text: str) -> dict:
    scores = _vader.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return {
        "label": label,
        "compound": round(compound, 3),
        "pos": round(scores["pos"], 3),
        "neu": round(scores["neu"], 3),
        "neg": round(scores["neg"], 3),
        "score": int(abs(compound) * 100),
    }


def detect_emotions(text: str) -> list:
    lower = text.lower()
    detected = []
    for emotion, triggers in EMOTION_TRIGGERS.items():
        hits = [t for t in triggers if t in lower]
        if hits:
            detected.append({"emotion": emotion, "triggers": hits, "strength": len(hits)})
    detected.sort(key=lambda x: -x["strength"])
    return detected


def find_power_words(text: str) -> list:
    lower = text.lower()
    return [w.strip() for w in POWER_WORDS if w.strip() in lower]


def analyze_readability(text: str) -> dict:
    flesch = textstat.flesch_reading_ease(text)
    grade = textstat.flesch_kincaid_grade(text)
    reading_time = textstat.reading_time(text, ms_per_char=14)

    if flesch >= 60:
        label = "Easy to read — great for ads"
    elif flesch >= 40:
        label = "Moderate — acceptable for most audiences"
    else:
        label = "Complex — simplify for ad copy"

    return {
        "flesch_ease": round(flesch, 1),
        "grade_level": round(grade, 1),
        "reading_time_sec": round(reading_time, 1),
        "label": label,
        "score": int(max(0, min(100, flesch))),
    }


def generate_suggestions(text: str, sentiment: dict, emotions: list, power_words: list, readability: dict) -> list:
    suggestions = []
    words = text.split()
    word_count = len(words)

    if word_count < 15:
        suggestions.append("Very short copy — add a benefit or unique value proposition")
    elif word_count > 40:
        suggestions.append(f"{word_count} words is long for ad copy — test a shorter version")

    if not power_words:
        suggestions.append("No power words found — add words like 'free', 'proven', 'exclusive' to boost engagement")
    elif len(power_words) >= 3:
        suggestions.append(f"Good use of {len(power_words)} power words")

    if sentiment["compound"] < -0.2:
        suggestions.append("Negative sentiment detected — ensure it creates urgency, not negativity")
    elif sentiment["compound"] > 0.5:
        suggestions.append("Strong positive sentiment — good for brand building")

    if not emotions:
        suggestions.append("No strong emotion detected — ads that trigger emotion perform 2x better")

    emotion_types = [e["emotion"] for e in emotions]
    if "urgency" not in emotion_types:
        suggestions.append("Add urgency — 'Limited time', 'Today only', 'Hurry' boost CTR")
    if "trust" not in emotion_types:
        suggestions.append("Add trust signals — 'Proven', 'Guaranteed', 'Official' build confidence")

    if readability["score"] < 40:
        suggestions.append("Hard to read — simplify language for faster comprehension")

    if "?" in text:
        suggestions.append("Question detected — good for engagement, ensure the answer is clear")

    if "!" not in text and text.isupper() is False:
        suggestions.append("Consider adding emphasis — exclamation marks increase energy")

    return suggestions[:6]


def analyze_copy(headline: str = "", body: str = "", cta: str = "") -> dict:
    full_text = f"{headline} {body} {cta}".strip()
    if not full_text:
        full_text = "No text provided"

    sentiment = analyze_sentiment_vader(full_text)
    emotions = detect_emotions(full_text)
    power_words = find_power_words(full_text)
    readability = analyze_readability(full_text)
    suggestions = generate_suggestions(full_text, sentiment, emotions, power_words, readability)

    char_count = len(full_text)
    word_count = len(full_text.split())

    copy_score = min(95, max(15, int(
        sentiment["score"] * 0.25 +
        readability["score"] * 0.20 +
        min(len(power_words) * 10, 30) +
        (15 if emotions else 0) +
        (10 if 10 <= word_count <= 30 else 0) +
        10
    )))

    return {
        "headline": headline,
        "bodyText": body,
        "charCount": char_count,
        "wordCount": word_count,
        "sentiment": sentiment["label"],
        "sentimentScore": sentiment["score"],
        "sentimentDetail": {
            "compound": sentiment["compound"],
            "positive": sentiment["pos"],
            "neutral": sentiment["neu"],
            "negative": sentiment["neg"],
        },
        "primaryEmotion": emotions[0]["emotion"].title() if emotions else "Neutral",
        "emotions": emotions,
        "powerWords": power_words[:8],
        "readability": readability["label"],
        "readabilityScore": readability["score"],
        "gradeLevel": readability["grade_level"],
        "readingTime": readability["reading_time_sec"],
        "suggestions": suggestions,
        "copyScore": copy_score,
    }
