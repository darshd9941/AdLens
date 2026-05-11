INDIA_BENCHMARKS = {
    "ecommerce": {"ctr": 1.2, "cpm": 90, "cpc": 7.5, "conv_rate": 1.5, "avg_order": 1200},
    "saas": {"ctr": 0.6, "cpm": 150, "cpc": 25, "conv_rate": 2.0, "avg_order": 5000},
    "education": {"ctr": 1.8, "cpm": 65, "cpc": 3.5, "conv_rate": 2.5, "avg_order": 800},
    "food": {"ctr": 2.0, "cpm": 55, "cpc": 2.8, "conv_rate": 2.0, "avg_order": 400},
    "fashion": {"ctr": 1.5, "cpm": 80, "cpc": 5.5, "conv_rate": 1.8, "avg_order": 1500},
    "real_estate": {"ctr": 0.5, "cpm": 180, "cpc": 35, "conv_rate": 0.5, "avg_order": 50000},
    "health": {"ctr": 1.0, "cpm": 100, "cpc": 10, "conv_rate": 1.5, "avg_order": 600},
    "local_business": {"ctr": 2.5, "cpm": 45, "cpc": 1.8, "conv_rate": 3.0, "avg_order": 500},
    "default": {"ctr": 1.2, "cpm": 85, "cpc": 7, "conv_rate": 1.5, "avg_order": 1000},
}

PLATFORM_CPM = {
    "facebook_feed": 1.0,
    "facebook_stories": 0.75,
    "instagram_feed": 1.15,
    "instagram_reels": 0.85,
    "instagram_stories": 0.9,
    "audience_network": 0.45,
}


def simulate_india_performance(analysis: dict, industry: str = "default", daily_budget: int = 1000) -> dict:
    base = INDIA_BENCHMARKS.get(industry, INDIA_BENCHMARKS["default"])

    overall = analysis.get("overallScore", 50)

    quality_mult = 0.7 + (overall / 100) * 0.6

    ctr = base["ctr"] * quality_mult
    ctr = max(0.3, min(5.0, ctr))

    cpm = base["cpm"] / quality_mult
    cpm = max(20, min(300, cpm))

    cpc = cpm / (ctr * 10) if ctr > 0 else 10
    cpc = max(1, min(60, cpc))

    daily_impressions = int((daily_budget / cpm) * 1000)
    daily_clicks = int(daily_impressions * (ctr / 100))

    conv_rate = base["conv_rate"] * (0.8 + quality_mult * 0.4)
    conv_rate = max(0.3, min(5.0, conv_rate))
    daily_conversions = round(daily_clicks * (conv_rate / 100), 1)

    avg_order = base["avg_order"]
    daily_revenue = round(daily_conversions * avg_order)
    roas = round(daily_revenue / daily_budget, 2) if daily_budget > 0 else 0
    roas = max(0.2, min(12, roas))

    engagement_rate = ctr * 2.5
    likes = int(daily_clicks * 2.1)
    comments = int(daily_clicks * 0.08)
    shares = int(daily_clicks * 0.04)
    saves = int(daily_clicks * 0.02)

    platform_performance = {}
    for platform, multiplier in PLATFORM_CPM.items():
        p_cpm = cpm * multiplier
        p_ctr = ctr * (0.9 + (multiplier - 0.5) * 0.4)
        p_clicks = int((daily_budget / p_cpm) * 1000 * (p_ctr / 100))
        platform_performance[platform] = {
            "cpm": round(p_cpm, 2),
            "ctr": round(p_ctr, 2),
            "daily_clicks": p_clicks,
        }

    best_platforms = sorted(platform_performance.items(), key=lambda x: x[1]["ctr"], reverse=True)[:3]

    return {
        "industry": industry,
        "dailyBudget": daily_budget,
        "monthlyBudget": daily_budget * 30,
        "daily": {
            "impressions": daily_impressions,
            "clicks": daily_clicks,
            "spend": daily_budget,
            "conversions": daily_conversions,
            "revenue": daily_revenue,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "saves": saves,
        },
        "monthly": {
            "impressions": daily_impressions * 30,
            "clicks": daily_clicks * 30,
            "spend": daily_budget * 30,
            "conversions": round(daily_conversions * 30),
            "revenue": daily_revenue * 30,
        },
        "metrics": {
            "ctr": round(ctr, 2),
            "cpm": round(cpm, 2),
            "cpc": round(cpc, 2),
            "roas": roas,
            "convRate": round(conv_rate, 2),
            "engagementRate": round(engagement_rate, 2),
        },
        "platformPerformance": platform_performance,
        "bestPlatforms": [{"name": p, **d} for p, d in best_platforms],
    }


def generate_ab_tests(analysis: dict) -> list:
    tests = []
    cta_score = analysis.get("ctaScore", 50)
    copy_score = analysis.get("copyScore", 50)
    overall = analysis.get("overallScore", 50)

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

    tests.append({
        "test": "Offer Framing",
        "variant_a": "Current offer presentation",
        "variant_b": "Add specific discount % or savings amount",
        "expected_impact": "20-35% higher conversion rate",
        "priority": "High",
    })

    return tests


def get_best_posting_times(industry: str = "default") -> dict:
    return {
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


def generate_report(simulation: dict, ab_tests: list, posting: dict) -> dict:
    metrics = simulation.get("metrics", {})
    daily = simulation.get("daily", {})
    return {
        "summary": {
            "dailyBudget": simulation.get("dailyBudget", 1000),
            "monthlyBudget": simulation.get("monthlyBudget", 30000),
            "industry": simulation.get("industry", "default"),
        },
        "metrics": metrics,
        "dailyEstimate": daily,
        "monthlyEstimate": simulation.get("monthly", {}),
        "topPlatforms": simulation.get("bestPlatforms", []),
        "abTests": ab_tests[:4],
        "postingSchedule": posting.get("recommended_schedule", []),
    }
