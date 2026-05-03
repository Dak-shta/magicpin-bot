# 🚀 Vera AI Bot — Magicpin AI Challenge

An intelligent, high-conversion AI bot designed to optimize merchant performance using contextual insights, strategic messaging, and real-time decision making.

---

## 📌 Overview

**Vera AI Bot** analyzes merchant data (CTR, views, engagement signals) and generates **high-impact, conversion-focused messages** to:

- Increase bookings, orders, or memberships
- Recover inactive merchants
- Improve listing performance
- Maximize ROI before subscription expiry

Built using **FastAPI + Rule Engine + LLM fallback (Groq)**.

---

## 🧠 Core Features

### 🔹 Smart Strategy Engine
Automatically detects merchant state:
- Performance Drop → Fix conversions  
- High Demand → Scale growth  
- Inactive Listing → Re-engage  
- Expiring Plan → Urgent renewal  

---

### 🔹 Category-Aware Messaging
Custom actions per category:
- 🦷 Dentist → Appointments  
- 🏋️ Gym → Memberships  
- 🍽️ Restaurant → Orders  
- 💇 Salon → Bookings  
- 💊 Pharmacy → Repeat Orders  

---

### 🔹 Conversion-Optimized Messaging
Every message includes:
- Merchant-specific data (CTR, views, calls)  
- Urgency signals  
- Clear CTA  
- Business impact focus  

---

### 🔹 Intelligent Conversation Handling
Handles:
- ✅ Auto-replies → Ends conversation  
- ✅ Hostile users → Stops messaging  
- ✅ Positive intent → Moves to action mode  

---

### 🔹 LLM Enhancement (Groq)
- Uses Groq API as fallback for smarter responses  
- Ensures structured JSON output  
- Keeps responses fast and relevant  

---

## 🏗️ Tech Stack

- **Backend:** FastAPI  
- **LLM:** Groq (LLaMA 3)  
- **Deployment:** Render  
- **Language:** Python  

---

## 🌐 Live API

Base URL:
```
https://dkodes-magicpin-bot.onrender.com
```

---

## 🔌 API Endpoints

### ✅ Health Check
```
GET /v1/healthz
```

### 📊 Metadata
```
GET /v1/metadata
```

### 🧠 Context Ingestion
```
POST /v1/context
```

### ⚡ Trigger Execution
```
POST /v1/tick
```

### 💬 Reply Handling
```
POST /v1/reply
```

---

## 🧪 Sample Request

### POST `/v1/reply`

```json
{
  "message": "yes let's do it",
  "merchant_id": "001"
}
```

---

### ✅ Sample Response

```json
{
  "action": "send",
  "body": "Great — I’ll set this up and share results shortly. Proceed?",
  "cta": "YES",
  "send_as": "vera"
}
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repo
```
git clone https://github.com/your-username/vera-ai-bot.git
cd vera-ai-bot
```

---

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

---

### 3️⃣ Run Locally
```
uvicorn main:app --host 0.0.0.0 --port 8050
```

---

### 4️⃣ Environment Variables (Optional - for Groq)

Create `.env` file or add in Render:

```
GROQ_API_KEY=your_api_key_here
```

---

## 🚀 Deployment (Render)

- Create a **Web Service**
- Connect your GitHub repo
- Set start command:

```
uvicorn main:app --host 0.0.0.0 --port 10000
```

- Add environment variable:
  - `GROQ_API_KEY`

---

## 🧩 Architecture

```
Incoming Trigger → Strategy Engine → Category Logic → Message Builder
                                      ↓
                                  (Fallback)
                                      ↓
                                   Groq LLM
```

---

## 📈 Scoring Optimization

Designed to maximize:
- Specificity  
- Category Fit  
- Merchant Fit  
- Decision Quality  
- Engagement  

---

## 👥 Team

**Team Vera**

---

## 📬 Notes

- Keep the service live during evaluation  
- Ensure endpoints are stable  
- Avoid redeploying during judge run  

---

## ✨ Future Improvements

- Advanced personalization  
- Multi-language support  
- Better LLM prompt tuning  
- Real-time analytics dashboard  
