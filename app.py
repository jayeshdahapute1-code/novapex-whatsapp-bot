import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "novapex_verify_2026")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")


MAIN_MENU = """👋 Welcome to NOVAPEX!
Digital Solutions for Your Business 🚀

Please select an option:
1️⃣ Novapex Information
2️⃣ Website Development
3️⃣ More Details

Reply with 1, 2, or 3.
Reply 0️⃣ anytime for the main menu."""

INFO = """🏢 *Novapex Information*

Novapex provides digital solutions for businesses:
• Website Development
• Web Applications
• Mobile Applications
• Custom Software Solutions

🌐 https://www.novapexhub.com

Reply 0️⃣ for Main Menu."""

WEBSITE = """💻 *Website Development*

We can develop:
• Business Websites
• Portfolio Websites
• E-commerce Websites
• Custom Websites
• Web Applications

🌐 https://www.novapexhub.com

Reply 0️⃣ for Main Menu."""

DETAILS = """📋 *Tell us about your requirement*

Please send:
1. Your Name
2. Mobile Number
3. Business/Company Name
4. Website/App requirement

Our Novapex team will contact you.

Reply 0️⃣ for Main Menu."""


@app.get("/")
def home():
    return "Novapex WhatsApp Bot is running."


@app.get("/webhook")
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


@app.post("/webhook")
def receive_webhook():
    data = request.get_json(silent=True) or {}

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for message in value.get("messages", []):
                    if message.get("type") != "text":
                        continue

                    sender = message.get("from")
                    text = message.get("text", {}).get("body", "").strip().lower()

                    if text in ("hi", "hello", "hey", "start"):
                        reply = MAIN_MENU
                    elif text == "1":
                        reply = INFO
                    elif text == "2":
                        reply = WEBSITE
                    elif text == "3":
                        reply = DETAILS
                    elif text == "0":
                        reply = MAIN_MENU
                    else:
                        reply = "Please reply with 1, 2, 3, or 0.\n\n" + MAIN_MENU

                    send_whatsapp_message(sender, reply)

    except Exception as exc:
        app.logger.exception("Webhook processing error: %s", exc)

    # Meta expects a quick 200 response.
    return "EVENT_RECEIVED", 200


def send_whatsapp_message(to, body):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        app.logger.warning("WHATSAPP_TOKEN or PHONE_NUMBER_ID is not configured.")
        return

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=20)
    response.raise_for_status()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
