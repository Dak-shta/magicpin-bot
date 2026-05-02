from fastapi import FastAPI, Request
from compose import compose

app = FastAPI()

# In-memory context store
CONTEXT = {}

# --------------------------
# Helper functions
# --------------------------

AUTO_REPLY_PATTERNS = [
    "thank you for contacting",
    "we will get back",
    "auto reply",
    "out of office"
]

def is_auto_reply(msg):
    msg = msg.lower()
    return any(p in msg for p in AUTO_REPLY_PATTERNS)


def is_positive_intent(msg):
    msg = msg.lower()
    return any(x in msg for x in [
        "yes", "ok", "okay", "let's do", "go ahead", "sure", "sounds good"
    ])


def is_hostile(msg):
    msg = msg.lower()
    return any(x in msg for x in [
        "stop", "spam", "useless", "don't message", "dont message", "leave me"
    ])

# --------------------------
# Endpoints
# --------------------------

@app.get("/v1/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "Team Vera",
        "model": "ollama-llama3"
    }


@app.post("/v1/context")
async def context(req: Request):
    data = await req.json()

    key = f"{data['scope']}:{data['context_id']}"
    CONTEXT[key] = data["payload"]

    return {"accepted": True}


@app.post("/v1/tick")
async def tick(req: Request):
    data = await req.json()
    triggers = data.get("available_triggers", [])

    actions = []

    for tid in triggers:
        trigger = CONTEXT.get(f"trigger:{tid}", {})
        merchant_id = trigger.get("merchant_id")

        merchant = CONTEXT.get(f"merchant:{merchant_id}", {})
        category = CONTEXT.get(f"category:{merchant.get('category_slug')}", {})

        result = compose(category, merchant, trigger)

        actions.append({
            "trigger_id": tid,
            "merchant_id": merchant_id,
            "action": "send",
            "body": result["message"],
            "cta": result["cta"],
            "send_as": result["send_as"]
        })

    return {"actions": actions}


@app.post("/v1/reply")
async def reply(req: Request):
    data = await req.json()
    msg = data.get("message", "")

    # --------------------------
    # 1. Hostile → END
    # --------------------------
    if is_hostile(msg):
        return {
            "action": "end"
        }

    # --------------------------
    # 2. Auto-reply → END
    # --------------------------
    if is_auto_reply(msg):
        return {
            "action": "end"
        }

    # --------------------------
    # 3. Positive intent → ACTION mode
    # --------------------------
    if is_positive_intent(msg):
        return {
            "action": "send",
            "body": "Great — I’ll set this up and share results shortly. Proceed?",
            "cta": "YES",
            "send_as": "vera"
        }

    # --------------------------
    # 4. Default → normal compose
    # --------------------------
    merchant_id = data.get("merchant_id")

    merchant = CONTEXT.get(f"merchant:{merchant_id}", {})
    category = CONTEXT.get(f"category:{merchant.get('category_slug')}", {})

    # fallback trigger
    trigger = {
        "kind": "conversation",
        "merchant_id": merchant_id,
        "payload": {}
    }

    result = compose(category, merchant, trigger)

    if "action" in result:
        return result

    return {
    "action": "send",
    "body": result.get("message", ""),
    "cta": result.get("cta", "YES")
}

    return {
        "action": "send",
        "body": result["message"],
        "cta": result["cta"],
        "send_as": result["send_as"]
    }