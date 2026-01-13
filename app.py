from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuration - Get values from environment variables
HFM_AFFILIATE_LINK = os.environ.get("HFM_AFFILIATE_LINK", "https://www.hfm.com/?refid=YOUR_ID")
PIPS_LAB_LINK = os.environ.get("PIPS_LAB_LINK", "https://t.me/pipslab")
JOSE_EMAIL = os.environ.get("JOSE_EMAIL", "josekamau@example.com")

# In-memory storage for user conversations (in production, use a database)
user_sessions = {}

class JosekamauTradingAgent:
    def __init__(self, hfm_link, pips_lab_link, jose_email):
        self.hfm_link = hfm_link
        self.pips_lab_link = pips_lab_link
        self.jose_email = jose_email

    def handle_message(self, user_id, message):
        """Process user message and return appropriate response"""
        
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                "step": "initial",
                "created_at": datetime.now().isoformat(),
                "conversation": []
            }
            response = "Hello! Thank you for reaching out to Josekamau Trading. 🎯\n\nTo help me understand how I can best assist you, could you please tell me your name and briefly explain why you reached out today?"
            user_sessions[user_id]["conversation"].append({
                "role": "agent",
                "message": response,
                "timestamp": datetime.now().isoformat()
            })
            return response

        step = user_sessions[user_id]["step"]
        
        # Log user message
        user_sessions[user_id]["conversation"].append({
            "role": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

        if step == "initial":
            user_sessions[user_id]["name_reason"] = message
            user_sessions[user_id]["step"] = "service_interest"
            response = f"Thank you! I\\'ve noted that. Are you looking for information on **copy trading** services or our **educational classes**? (Or both?)"
            
        elif step == "service_interest":
            user_sessions[user_id]["interest"] = message
            user_sessions[user_id]["step"] = "hfm_status"
            response = "Great! To proceed, do you currently have an **HFM (HotForex) trading account**? (Reply: Yes or No)"
            
        elif step == "hfm_status":
            if "no" in message.lower():
                user_sessions[user_id]["hfm_status"] = "no"
                user_sessions[user_id]["step"] = "pips_lab"
                response = f"""No problem at all! 👍 You can easily open an HFM account using Josekamau Trading\\'s official affiliate link here:\n\n🔗 {self.hfm_link}\n\nPlease use this link to ensure you\\'re linked to our services. Once you\\'ve created your account, feel free to let me know. In the meantime, here\\'s the link to our **Pips Lab Telegram channel** for exclusive insights and updates:\n\n📱 {self.pips_lab_link}\n\nAnd don\\'t forget - we host a **live webinar every Sunday** in the group! It\\'s a great opportunity to learn and ask questions directly. 📚"""
                
            elif "yes" in message.lower():
                user_sessions[user_id]["hfm_status"] = "yes"
                user_sessions[user_id]["step"] = "hfm_verification"
                response = f"""Excellent! 🎉 To verify your account and link it with Josekamau Trading, please provide:\n\n1️⃣ **Email address** you used to register your HFM account\n2️⃣ **Screenshot** of your HFM account dashboard (showing both account creation date and current status)\n\nYou can send these details to: **{self.jose_email}**\n\nOr reply here with the information and we\\'ll process it."""
            else:
                response = "I didn\\'t quite catch that. Could you please reply with **Yes** or **No** to whether you have an HFM account?"
                return response

        elif step == "hfm_verification":
            user_sessions[user_id]["verification_info"] = message
            user_sessions[user_id]["step"] = "pips_lab"
            response = f"""Thank you for providing that information! ✅ We\\'ll verify your account shortly.\n\nNow, to get access to exclusive insights and updates, here\\'s the link to our **Pips Lab Telegram channel**:\n\n📱 {self.pips_lab_link}\n\nMake sure to join! \n\nAlso, remember we have a **live webinar every Sunday** in the group. It\\'s a perfect opportunity to learn trading strategies and ask questions directly. Don\\'t miss it! 📚"""

        elif step == "pips_lab":
            response = """You\\'re all set! 🚀 \n\nIf you have any more questions, feel free to reach out anytime. \n\n📌 **Quick Reminders:**\n• Join our **Pips Lab Telegram channel** for daily insights\n• Attend our **Sunday webinars** for live training\n• Contact us at **{email}** if you need any assistance\n\nLooking forward to trading with you! 💪""".format(email=self.jose_email)

        else:
            response = "I apologize, I didn\\'t quite catch that. Could you please rephrase or provide the information I requested?"

        # Log agent response
        user_sessions[user_id]["conversation"].append({
            "role": "agent",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })

        return response


# Initialize the agent
agent = JosekamauTradingAgent(HFM_AFFILIATE_LINK, PIPS_LAB_LINK, JOSE_EMAIL)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Josekamau Trading AI Agent",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/webhook", methods=["POST"])
def webhook():
    """Main webhook endpoint for receiving messages from ManyChat or other platforms"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract user ID and message
        # Adjust these field names based on your platform (ManyChat, Instagram, etc.)
        user_id = data.get("user_id") or data.get("subscriber_id") or data.get("from_id")
        user_message = data.get("message") or data.get("text") or data.get("body")
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        if not user_message:
            return jsonify({"error": "message is required"}), 400
        
        # Get response from agent
        response = agent.handle_message(str(user_id), user_message)
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "reply": response,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route("/conversation/<user_id>", methods=["GET"])
def get_conversation(user_id):
    """Retrieve conversation history for a specific user"""
    if user_id not in user_sessions:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user_id": user_id,
        "conversation": user_sessions[user_id],
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/stats", methods=["GET"])
def get_stats():
    """Get agent statistics"""
    return jsonify({
        "total_users": len(user_sessions),
        "users": list(user_sessions.keys()),
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/config", methods=["GET"])
def get_config():
    """Get current configuration (for verification)"""
    return jsonify({
        "hfm_link": HFM_AFFILIATE_LINK,
        "pips_lab_link": PIPS_LAB_LINK,
        "jose_email": JOSE_EMAIL,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/", methods=["GET"])
def index():
    """Welcome endpoint"""
    return jsonify({
        "service": "Josekamau Trading AI Agent",
        "version": "1.0.0",
        "description": "Automated AI agent for handling DMs and comments on Josekamau Trading accounts",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook (POST)",
            "conversation": "/conversation/<user_id> (GET)",
            "stats": "/stats (GET)",
            "config": "/config (GET)"
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=False)
