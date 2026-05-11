import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4"

INDIA_BENCHMARKS = {
    "ecommerce": {"ctr": 1.5, "cpm": 80, "cpc": 5.5, "conv_rate": 2.0, "avg_order": 1200},
    "saas": {"ctr": 0.8, "cpm": 120, "cpc": 15, "conv_rate": 3.5, "avg_order": 5000},
    "education": {"ctr": 2.0, "cpm": 60, "cpc": 3, "conv_rate": 4.0, "avg_order": 800},
    "food": {"ctr": 2.5, "cpm": 50, "cpc": 2, "conv_rate": 3.0, "avg_order": 400},
    "fashion": {"ctr": 1.8, "cpm": 70, "cpc": 4, "conv_rate": 2.5, "avg_order": 1500},
    "real_estate": {"ctr": 0.6, "cpm": 150, "cpc": 25, "conv_rate": 1.0, "avg_order": 50000},
    "health": {"ctr": 1.2, "cpm": 90, "cpc": 7.5, "conv_rate": 2.8, "avg_order": 600},
    "local_business": {"ctr": 3.0, "cpm": 40, "cpc": 1.3, "conv_rate": 5.0, "avg_order": 500},
    "default": {"ctr": 1.5, "cpm": 80, "cpc": 5.5, "conv_rate": 2.5, "avg_order": 1000},
}

PLATFORM_CPM = {
    "facebook_feed": 1.0,
    "facebook_stories": 0.7,
    "instagram_feed": 1.2,
    "instagram_reels": 0.8,
    "instagram_stories": 0.9,
    "audience_network": 0.4,
}


def simulate_india_performance(analysis: dict, industry: str = "default", daily_budget: int = 1000) -> dict:
    base = INDIA_BENCHMARKS.get(industry, INDIA_BENCHMARKS["default"])

    overall = analysis.get("overallScore", 50)
    copy_score = analysis.get("copyScore", 50)
    cta_score = analysis.get("ctaScore", 50)
    visual_score = analysis.get("visualScore", 50)

    quality_multiplier = (overall / 50.0)
    cta_boost = 1.0 + (cta_score - 50) / 200.0
    copy_boost = 1.0 + (copy_score - 50) / 200.0

    ctr = base["ctr"] * quality_multiplier * cta_boost * copy_boost
    ctr = max(0.1, min(8.0, ctr))

    cpm = base["cpm"] / quality_multiplier
    cpm = max(15, min(300, cpm))

    cpc = cpm / (ctr * 10)
    cpc = max(0.5, min(50, cpc))

    daily_impressions = (daily_budget / cpm) * 1000
    daily_clicks = daily_impressions * (ctr / 100)
    daily_spend = daily_budget

    conv_rate = base["conv_rate"] * quality_multiplier * copy_boost
    conv_rate = max(0.5, min(10, conv_rate))
    daily_conversions = daily_clicks * (conv_rate / 100)

    avg_order = base["avg_order"]
    daily_revenue = daily_conversions * avg_order
    roas = daily_revenue / daily_spend if daily_spend > 0 else 0
    roas = max(0.1, min(20, roas))

    engagement_rate = ctr * 3.5
    likes = int(daily_impressions * (engagement_rate / 100) * 0.6)
    comments = int(daily_impressions * (engagement_rate / 100) * 0.08)
    shares = int(daily_impressions * (engagement_rate / 100) * 0.05)
    saves = int(daily_impressions * (engagement_rate / 100) * 0.03)

    monthly_clicks = daily_clicks * 30
    monthly_spend = daily_spend * 30
    monthly_conversions = daily_conversions * 30
    monthly_revenue = daily_revenue * 30

    platform_performance = {}
    for platform, multiplier in PLATFORM_CPM.items():
        p_cpm = cpm * multiplier
        p_ctr = ctr * (1.0 + (multiplier - 0.7) * 0.3)
        p_clicks = (daily_budget / p_cpm) * 1000 * (p_ctr / 100)
        platform_performance[platform] = {
            "cpm": round(p_cpm, 2),
            "ctr": round(p_ctr, 2),
            "daily_clicks": round(p_clicks),
        }

    best_platforms = sorted(platform_performance.items(), key=lambda x: x[1]["ctr"], reverse=True)[:3]

    return {
        "industry": industry,
        "dailyBudget": daily_budget,
        "monthlyBudget": daily_budget * 30,
        "daily": {
            "impressions": int(daily_impressions),
            "clicks": int(daily_clicks),
            "spend": daily_spend,
            "conversions": round(daily_conversions, 1),
            "revenue": round(daily_revenue),
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "saves": saves,
        },
        "monthly": {
            "impressions": int(daily_impressions * 30),
            "clicks": int(monthly_clicks),
            "spend": int(monthly_spend),
            "conversions": round(monthly_conversions),
            "revenue": round(monthly_revenue),
        },
        "metrics": {
            "ctr": round(ctr, 2),
            "cpm": round(cpm, 2),
            "cpc": round(cpc, 2),
            "roas": round(roas, 2),
            "convRate": round(conv_rate, 2),
            "engagementRate": round(engagement_rate, 2),
        },
        "platformPerformance": {k: v for k, v in platform_performance.items()},
        "bestPlatforms": [{"name": p, **d} for p, d in best_platforms],
    }


def generate_ab_tests(analysis: dict) -> list:
    tests = []
    overall = analysis.get("overallScore", 50)
    copy_score = analysis.get("copyScore", 50)
    cta_score = analysis.get("ctaScore", 50)

    if cta_score < 70:
        tests.append({
            "test": "CTA Text",
            "variant_a": "Current CTA",
            "variant_b": "Add action verb: 'Shop Now', 'Get 50% Off', 'Buy Today'",
            "expected_impact": "15-30% increase in CTR",
            "priority": "High",
        })

    if copy_score < 60:
        tests.append({
            "test": "Ad Copy Length",
            "variant_a": "Current copy",
            "variant_b": "Shorter version — under 15 words with one clear benefit",
            "expected_impact": "10-20% improvement in engagement",
            "priority": "High",
        })

    extracted = analysis.get("extractedText", "")
    if "?" not in extracted:
        tests.append({
            "test": "Headline Style",
            "variant_a": "Current headline (statement)",
            "variant_b": "Question headline: 'Tired of [problem]?'",
            "expected_impact": "12-18% higher CTR",
            "priority": "Medium",
        })

    emotions = analysis.get("emotions", [])
    emotion_types = [e.get("emotion", "") for e in emotions] if isinstance(emotions, list) else []
    if "urgency" not in emotion_types:
        tests.append({
            "test": "Urgency Trigger",
            "variant_a": "Current ad (no urgency)",
            "variant_b": "Add 'Limited time' or 'Only today' or countdown",
            "expected_impact": "20-35% increase in conversion rate",
            "priority": "High",
        })

    if overall < 70:
        tests.append({
            "test": "Visual Style",
            "variant_a": "Current creative",
            "variant_b": "UGC-style or lifestyle shot instead of product-focused",
            "expected_impact": "25-40% higher engagement on Reels/Stories",
            "priority": "Medium",
        })

    tests.append({
        "test": "Audience Targeting",
        "variant_a": "Current targeting",
        "variant_b": "Test Lookalike Audience (1-3%) from website visitors",
        "expected_impact": "15-25% lower CPA",
        "priority": "Medium",
    })

    return tests


def get_best_posting_times(industry: str = "default") -> dict:
    times = {
        "weekday": [
            {"time": "7:00-9:00 AM", "score": 85, "note": "Morning commute — high mobile usage"},
            {"time": "12:00-2:00 PM", "score": 70, "note": "Lunch break browsing"},
            {"time": "6:00-9:00 PM", "score": 95, "note": "Peak engagement hours"},
            {"time": "9:00-11:00 PM", "score": 60, "note": "Late night browsing"},
        ],
        "weekend": [
            {"time": "10:00 AM-12:00 PM", "score": 80, "note": "Weekend morning leisure"},
            {"time": "2:00-4:00 PM", "score": 65, "note": "Afternoon relaxed browsing"},
            {"time": "7:00-10:00 PM", "score": 90, "note": "Evening peak"},
        ],
        "best_days": ["Tuesday", "Wednesday", "Thursday"],
        "worst_days": ["Sunday", "Saturday morning"],
        "recommended_schedule": [
            "Run ads daily 7AM-11PM",
            "Increase budget 20% on Tue-Thu 6-9PM",
            "Reduce spend on Sunday mornings",
            "Test weekend Stories/Reels placements",
        ],
    }
    return times


def generate_report(analysis: dict, simulation: dict, ab_tests: list, posting: dict) -> dict:
    overall = analysis.get("overallScore", 50)
    metrics = simulation.get("metrics", {})

    if overall >= 80:
        verdict = "Strong ad — ready to scale"
    elif overall >= 60:
        verdict = "Good ad with room for improvement"
    elif overall >= 40:
        verdict = "Average — needs optimization before scaling"
    else:
        verdict = "Weak — major changes needed"

    return {
        "summary": {
            "score": overall,
            "verdict": verdict,
            "industry": simulation.get("industry", "default"),
            "dailyBudget": simulation.get("dailyBudget", 1000),
        },
        "performance": {
            "ctr": metrics.get("ctr"),
            "cpm": metrics.get("cpm"),
            "cpc": metrics.get("cpc"),
            "roas": metrics.get("roas"),
            "convRate": metrics.get("convRate"),
        },
        "dailyEstimate": simulation.get("daily", {}),
        "monthlyEstimate": simulation.get("monthly", {}),
        "topPlatforms": simulation.get("bestPlatforms", []),
        "abTests": ab_tests[:4],
        "postingSchedule": posting.get("recommended_schedule", []),
        "bestTimes": posting.get("weekday", [])[:2],
        "suggestions": analysis.get("insights", []),
    }
