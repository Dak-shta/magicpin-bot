import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


# -------------------------------
# STRATEGY DECISION
# -------------------------------
def decide_strategy(trigger, merchant):
    kind = (trigger or {}).get("kind", "")
    signals = (merchant or {}).get("signals", [])

    signals_str = " ".join(signals)

    if "ctr_below_peer_median" in signals_str or "perf_dip" in kind:
        return "performance_fix"

    if "stale_posts" in signals_str:
        return "content_refresh"

    if "renewal_due_soon" in signals_str:
        return "subscription_renewal"

    if "dormant" in signals_str:
        return "re_engagement"

    if "high_engagement" in signals_str or "spike" in kind:
        return "growth_push"

    return "generic"


# -------------------------------
# CATEGORY-SPECIFIC ACTION
# -------------------------------
def category_action(category_name):
    category_name = category_name.lower()

    if "dentist" in category_name:
        return "increase bookings by highlighting top treatments, adding patient reviews, and improving trust signals"

    if "gym" in category_name:
        return "convert visitors into paid members using free trial offers and limited-time discounts"

    if "restaurant" in category_name:
        return "boost orders by promoting best-selling dishes, combo meals, and peak-hour offers"

    if "salon" in category_name:
        return "increase bookings by showcasing trending services, before-after results, and service packages"

    if "pharmacy" in category_name:
        return "drive more orders by highlighting fast delivery, medicine availability, and urgent needs"

    return "improve conversions by optimizing visibility and customer engagement"

# -------------------------------
# FALLBACK (SAFE)
# -------------------------------
def fallback():
    return {
        "message": "I can improve your listing performance using recent data and increase conversions quickly. Want me to do it?",
        "cta": "YES",
        "send_as": "vera",
        "suppression_key": "fallback",
        "rationale": "Safe fallback"
    }

def build_response(message, strategy, merchant_id):
    return {
        "message": message,
        "cta": "YES",
        "send_as": "vera",
        "suppression_key": f"{strategy}_{merchant_id}",
        "rationale": f"{strategy} with category-specific conversion optimization"
    }

def get_goal(category_name):
    category_name = category_name.lower()

    if "dentist" in category_name:
        return "appointments"
    if "gym" in category_name:
        return "memberships"
    if "restaurant" in category_name:
        return "orders"
    if "salon" in category_name:
        return "appointments"
    if "pharmacy" in category_name:
        return "repeat orders"

    return "customers"


# -------------------------------
# MAIN COMPOSE FUNCTION
# -------------------------------
def compose(category, merchant, trigger, customer=None):
    try:
        # -------------------------------
        # 🚀 FAST RULE SHORTCUTS
        # -------------------------------

        # Auto-reply detection
        if customer is None and (trigger or {}).get("kind") == "":
            return {"action": "end"}

        # Hostile detection
        if customer and any(word in str(customer).lower() for word in ["spam", "stop", "useless"]):
            return {"action": "end"}

        # Intent commit
        if customer and "do it" in str(customer).lower():
            return {
                "message": "Great — I’ll set this up and share results shortly. Proceed?",
                "cta": "YES",
                "send_as": "vera",
                "suppression_key": "intent_action",
                "rationale": "User committed"
            }

        # -------------------------------
        # SAFE INPUTS
        # -------------------------------
        category = category or {}
        merchant = merchant or {}
        trigger = trigger or {}

        strategy = decide_strategy(trigger, merchant)

        identity = merchant.get("identity", {})
        perf = merchant.get("performance", {})

        business = identity.get("name", "")
        locality = identity.get("locality", "")
        owner = identity.get("owner_first_name", "Owner")

        ctr = round(perf.get("ctr", 0) * 100, 1)
        views = perf.get("views", 0)
        calls = perf.get("calls", 0)

        merchant_id = merchant.get("merchant_id", "unknown")

        category_name = (category.get("name") or "")
        goal = get_goal(category_name)
        action_line = category_action(category_name)

        # -------------------------------
        # 🎯 STRATEGY-BASED RESPONSES
        # -------------------------------

        if strategy == "performance_fix":
            msg = (
        f"{owner}, {business} in {locality} is getting {views} views but only {ctr}% CTR and {calls} calls.\n"
        f"You're missing high-intent {goal} — I can increase {goal} by 20–30% this week by optimizing your listing. Want me to fix this today?"
    )
            return build_response(msg, strategy, merchant_id)
        

        if strategy == "growth_push":
            msg = (
        f"{business} in {locality} is getting strong demand ({views} views).\n"
        f"I can convert this into 20–30% more {goal} using targeted optimization. Want me to scale this now?"
    )
            return build_response(msg, strategy, merchant_id)
        
        if strategy == "content_refresh":
            msg = (
    f"Your listing in {locality} has CTR {ctr}% — content isn’t converting.\n"
    f"I can refresh it and boost {goal} by 20%+. Want me to update it now?"
)
    
            return build_response(msg, strategy, merchant_id)
       
        if strategy == "re_engagement":
            msg = (
    f"{owner}, {business} in {locality} is inactive — you're losing potential {goal} daily.\n"
    f"I can reactivate your listing and recover traffic fast. Want me to restart this today?"
)
            return build_response(msg, strategy, merchant_id)

       
        if strategy == "subscription_renewal":
            msg = (
    f"{owner}, your plan is ending while {business} still gets {views} views.\n"
    f"You risk losing {goal} — I can secure and grow them before expiry. Want me to act now?"
)
            return build_response(msg, strategy, merchant_id)

        # -------------------------------
        # GENERIC (still strong)
        # -------------------------------
        msg = (
    f"{owner}, {business} in {locality} is getting {views} views with {ctr}% CTR.\n"
    f"I can increase {goal} by 20%+ using targeted optimization. Want me to do it?"
)
        return build_response(msg, strategy, merchant_id)

    except Exception as e:
        print("ERROR:", e)
        return fallback()