from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Credentials from Environment
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return "ARCHITECT_AI_ONLINE", 200
        
    try:
        data = request.json
        # The Predator Logic
        prompt = f"""
        COMMAND: ARCHITECT AI - GLOBAL ARBITRAGE PROTOCOL
        INPUT_DEAL: {data}
        
        MISSION (English Only):
        1. DETECT: Identify why this deal is a 'ripe fruit' (liquidation, distress, overstock).
        2. NEGOTIATE: Define the predatory entry price.
        3. MATCH: Identify global B2B buyers for immediate flipping (Heavy machinery, Tech, Cars).
        4. ACTION: Draft the final offer message to secure the deal.
        
        TONE: Cold, Analytical, Sovereign.
        """

        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        res = requests.post(gemini_url, json=payload)
        analysis = res.json()['candidates'][0]['content']['parts'][0]['text']

        # Telegram Alert
        tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(tg_url, json={
            "chat_id": CHAT_ID,
            "text": f"🏛️ **ARCHITECT AI: GLOBAL STRIKE**\n\n{analysis}",
            "parse_mode": "Markdown"
        })

        return "DEAL_CAPTURED", 200
    except Exception as e:
        return f"CRITICAL_ERROR", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
