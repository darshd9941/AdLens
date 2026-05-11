import re

POWER_WORDS = [
    "free", "new", "proven", "instant", "exclusive", "limited", "save",
    "discover", "secret", "unlock", "guarantee", "easy", "fast", "now",
    "you", "your", "today", "best", "top", "official", "official",
    "sale", "discount", "offer", "bonus", "special", "premium",
    "revolutionary", " breakthrough", "results", "success", "win",
    "growth", "scale", "transform", "boost", "increase", "double",
    "skyrocket", "dominate", "crush", "slam dunk", "no-brainer",
]

EMOTION_MAP = {
    "urgency": ["now", "today", "limited", "hurry", "last chance", "don't miss", "act fast", "ending soon"],
    "trust": ["proven", "guarantee", "official", "certified", "trusted", "secure", "safe"],
    "excitement": ["new", "exclusive", "secret", "unlock", "discover", "revolutionary", "breakthrough"],
    "fear": ["miss out", "before it's gone", "warning", "don't wait", "risk-free", "no obligation"],
    "curiosity": ["secret", "hidden", "what they don't tell", "revealed", "discover", "unlock"],
    "value": ["free", "save", "discount", "bonus", "extra", "more", "best price"],
}


def analyze_sentiment(text: str) -> dict:
    positive_words = ["love", "great", "best", "amazing", "excellent", "perfect", "wonderful",
                      "fantastic", "beautiful", "happy", "enjoy", "win", "success", "good"]
    negative_words = ["bad", "worst", "hate", "terrible", "awful", "poor", "fail",
                      "wrong", "never", "problem", "risk", "fear", "worry", "difficult"]

    lower = text.lower()
    pos = sum(1 for w in positive_words if w in lower)
    neg = sum(1 for w in negative_words if w in lower)
    total = pos + neg

    if total == 0:
        return {"label": "Neutral", "score": 50}
    ratio = pos / total
    if ratio > 0.6:
        return {"label": "Positive", "score": int(60 + ratio * 30)}
    elif ratio < 0.4:
        return {"label": "Negative", "score": int(20 + ratio * 40)}
    return {"label": "Neutral", "score": 50}


def detect_emotions(text: str) -> list:
    lower = text.lower()
    detected = []
    for emotion, triggers in EMOTION_MAP.items():
        hits = [t for t in triggers if t in lower]
        if hits:
            detected.append({"emotion": emotion, "triggers": hits, "strength": len(hits)})
    detected.sort(key=lambda x: -x["strength"])
    return detected


def find_power_words(text: str) -> list:
    lower = text.lower()
    return [w.strip() for w in POWER_WORDS if w.strip() in lower]


def readability_score(text: str) -> dict:
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    syllables = sum(_count_syllables(w) for w in words)

    word_count = max(len(words), 1)
    sent_count = max(len(sentences), 1)

    flesch = 206.835 - 1.015 * (word_count / sent_count) - 84.6 * (syllables / word_count)
    flesch = max(0, min(100, flesch))

    if flesch >= 60:
        label = "Easy to read"
    elif flesch >= 40:
        label = "Moderately readable"
    else:
        label = "Complex — consider simplifying"

    return {"score": int(flesch), "label": label}


def generate_suggestions(text: str, sentiment: dict, emotions: list, power_words: list) -> list:
    suggestions = []
    word_count = len(text.split())

    if word_count < 20:
        suggestions.append("Consider adding more detail — short copy can miss context")
    elif word_count > 50:
        suggestions.append("Long copy detected — test a shorter version for mobile")

    if not power_words:
        suggestions.append("Add power words like 'free', 'proven', 'exclusive' to boost engagement")

    if sentiment["score"] < 40:
        suggestions.append("Negative sentiment detected — ensure it's intentional (urgency vs. negativity)")

    if not emotions:
        suggestions.append("No strong emotion detected — ads that trigger emotion perform 2x better")

    if "urgency" not in [e["emotion"] for e in emotions]:
        suggestions.append("Add urgency — 'Limited time', 'Today only', 'Hurry' boost CTR")

    if "trust" not in [e["emotion"] for e in emotions]:
        suggestions.append("Consider adding trust signals — 'Proven', 'Guaranteed', 'Official'")

    if text != text.upper() and not any(c == '!' for c in text):
        suggestions.append("Add an exclamation mark or CTA emphasis to increase energy")

    if "?" in text:
        suggestions.append("Question in copy — good for engagement, ensure answer is clear")

    return suggestions[:6]


def _count_syllables(word: str) -> int:
    word = word.lower().strip(".,!?;:'\"")
    if len(word) <= 3:
        return 1
    vowels = "aeiou"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e"):
        count -= 1
    return max(count, 1)


def analyze_copy(headline: str = "", body: str = "", cta: str = "") -> dict:
    full_text = f"{headline} {body} {cta}".strip()

    sentiment = analyze_sentiment(full_text)
    emotions = detect_emotions(full_text)
    power_words = find_power_words(full_text)
    readability = readability_score(full_text)
    suggestions = generate_suggestions(full_text, sentiment, emotions, power_words)

    char_count = len(full_text)
    word_count = len(full_text.split())

    copy_score = min(95, max(20,
        readability["score"] * 0.3 +
        min(len(power_words) * 12, 36) +
        (30 if emotions else 0) +
        (15 if 20 <= word_count <= 40 else 5)
    ))

    return {
        "headline": headline,
        "bodyText": body,
        "charCount": char_count,
        "wordCount": word_count,
        "sentiment": sentiment["label"],
        "sentimentScore": sentiment["score"],
        "primaryEmotion": emotions[0]["emotion"].title() if emotions else "Neutral",
        "emotions": emotions,
        "powerWords": power_words[:8],
        "readability": readability["label"],
        "readabilityScore": readability["score"],
        "suggestions": suggestions,
        "copyScore": int(copy_score),
    }
