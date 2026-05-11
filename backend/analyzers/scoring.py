def compute_overall_score(visual: dict, copy: dict, dna: dict) -> dict:
    scores = {
        "visual": visual.get("score", 50),
        "copy": copy.get("copyScore", 50),
        "cta": dna.get("cta", {}).get("score", 50),
        "composition": dna.get("composition", {}).get("score", 50),
        "hierarchy": dna.get("visualHierarchy", {}).get("score", 50),
        "colors": dna.get("colors_harmony", {}).get("score", 50),
    }

    weights = {
        "visual": 0.25,
        "copy": 0.20,
        "cta": 0.15,
        "composition": 0.15,
        "hierarchy": 0.15,
        "colors": 0.10,
    }

    overall = sum(scores[k] * weights[k] for k in scores)
    overall = min(95, max(10, int(overall)))

    insights = []
    if scores["cta"] < 50:
        insights.append("Your CTA is weak. Add a clear button or text like 'Shop Now' or 'Get Started' in the bottom third.")
    if scores["composition"] < 50:
        insights.append("Composition could be improved. Align key elements to rule-of-thirds grid intersections.")
    if scores["colors"] < 50:
        insights.append("Color harmony is low. Use analogous colors (next to each other on the color wheel) for cohesion.")
    if scores["visual"] > 75:
        insights.append("Strong visual appeal. Your creative quality is above average.")
    if scores["copy"] > 75:
        insights.append("Excellent copy. Good use of emotion and power words.")
    if scores["hierarchy"] < 50:
        insights.append("Visual hierarchy is unclear. Guide the eye from headline → image → CTA.")
    if not insights:
        if overall >= 70:
            insights.append("Solid ad overall. Consider A/B testing minor variations to optimize further.")
        else:
            insights.append("This ad needs work. Focus on the weakest scoring elements first.")

    return {
        "overallScore": overall,
        "visualScore": scores["visual"],
        "copyScore": scores["copy"],
        "ctaScore": scores["cta"],
        "insights": insights,
        "breakdown": scores,
    }
