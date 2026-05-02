import requests
import os
import json

# -------------------------------
# GROQ CONFIG
# -------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"


# -------------------------------
# GROQ CALL (SAFE)
# -------------------------------
def call_groq(prompt):
    try:
        if not GROQ_API_KEY:
            return None

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Vera, a strict conversion assistant. "
                        "Return ONLY valid JSON with keys: message, cta, send_as, suppression_key, rationale."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 120
        }

        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=3)

        if res.status_code != 200:
            return None

        data = res.json()

        return data.get("choices", [{}])[0].get("message", {}).get("content")

    except Exception:
        return None


# -------------------------------
# SAFE JSON PARSER
# -------------------------------
def extract_json(text):
    try:
        if not text:
            return None

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return None

        return json.loads(text[start:end+1])

    except Exception:
        return None


# -------------------------------
# STRATEGY ENGINE
# -------------------------------
def decide_strategy(trigger, merchant):
    kind = (trigger or {}).get("kind", "")
    signals = " ".join((merchant or {}).get("signals", []))

    if "ctr_below_peer_median" in signals or "perf_dip" in kind:
        return "performance_fix"

    if "stale_posts" in signals:
        return "content_refresh"

    if "renewal_due_soon" in signals:
        return "subscription_renewal"

    if "dormant" in signals:
        return "re_engagement"

    if "high_engagement" in signals or "spike" in kind:
        return "growth_push"

    return "generic"


# -------------------------------
# CATEGORY INTELLIGENCE
# -------------------------------
def category_action(category_name):
    category_name = (category_name or "").lower()

    if "dentist" in category_name:
        return "increase bookings via trust signals"
    if "gym" in category_name:
        return "convert visits into memberships"
    if "restaurant" in category_name:
        return "increase orders via combos"
    if "salon" in category_name:
        return "boost bookings via transformations"
    if "pharmacy" in category_name:
        return "increase urgent orders via availability"

    return "improve conversions via optimization"


def get_goal(category_name):
    category_name = (category_name or "").lower()

    if "dentist" in category_name:
        return "appointments"
    if "gym" in category_name:
        return "memberships"
    if "restaurant" in category_name:
        return "orders"
    if "salon" in category_name:
        return "bookings"
    if "pharmacy" in category_name:
        return "repeat orders"

    return "customers"


# -------------------------------
# RESPONSE BUILDER
# -------------------------------
def build_response(message, strategy, merchant_id):
    return {
        "message": message,
        "cta": "YES",
        "send_as": "vera",
        "suppression_key": f"{strategy}_{merchant_id}",
        "rationale": f"{strategy} optimized message"
    }


# -------------------------------
# FALLBACK
# -------------------------------
def fallback(strategy="generic", merchant_id="unknown"):
    return {
        "message": "I can improve your listing performance using insights and increase conversions quickly. Want me to do it?",
        "cta": "YES",
        "send_as": "vera",
        "suppression_key": f"{strategy}_{merchant_id}",
        "rationale": "safe fallback"
    }


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def compose(category, merchant, trigger, customer=None):
    try:

        # -----------------------
        # FAST RULES
        # -----------------------
        if customer is None and (trigger or {}).get("kind") == "":
            return {"action": "end"}

        if customer and any(w in str(customer).lower() for w in ["spam", "stop", "useless"]):
            return {"action": "end"}

        if customer and "do it" in str(customer).lower():
            return {
                "message": "Great — I’ll set this up and share results shortly. Proceed?",
                "cta": "YES",
                "send_as": "vera",
                "suppression_key": "intent_action",
                "rationale": "user intent commit"
            }

        # -----------------------
        # INPUT SAFE
        # -----------------------
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

        category_name = category.get("name", "")
        goal = get_goal(category_name)
        action = category_action(category_name)

        # -----------------------
        # STRATEGY RESPONSES
        # -----------------------
        def msg(text):
            return build_response(text, strategy, merchant_id)

        if strategy == "performance_fix":
            return msg(
                f"{owner}, {business} has {views} views but low CTR ({ctr}%).\n"
                f"You’re losing {goal}. I can {action} and improve conversions fast. Want me to fix it?"
            )

        if strategy == "growth_push":
            return msg(
                f"{business} is getting strong demand ({views} views).\n"
                f"I can {action} and convert into more {goal}. Want me to scale?"
            )

        if strategy == "content_refresh":
            return msg(
                f"CTR is {ctr}% — listing underperforming.\n"
                f"I can {action} and improve {goal}. Want update?"
            )

        if strategy == "re_engagement":
            return msg(
                f"{owner}, {business} is inactive — losing {goal}.\n"
                f"I can {action} and bring customers back. Want restart?"
            )

        if strategy == "subscription_renewal":
            return msg(
                f"{owner}, plan ending while traffic exists ({views}).\n"
                f"I can {action} and protect {goal}. Want to secure?"
            )

        # -----------------------
        # GROQ FALLBACK (SMART)
        # -----------------------
        prompt = f"""
Business: {business}
Location: {locality}
CTR: {ctr}%
Views: {views}
Calls: {calls}
Goal: {goal}
Strategy: {strategy}

Write a 2-line high-conversion message.
Include urgency + CTA.
Return JSON only.
"""

        raw = call_groq(prompt)
        parsed = extract_json(raw)

        if parsed and isinstance(parsed, dict) and "message" in parsed:
            parsed["cta"] = "YES"
            parsed["send_as"] = "vera"
            parsed["suppression_key"] = f"{strategy}_{merchant_id}"
            return parsed

        return fallback(strategy, merchant_id)

    except Exception:
        return fallback()