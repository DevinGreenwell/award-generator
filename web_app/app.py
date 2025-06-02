from flask import Flask, render_template, request, jsonify, session
import os
import json
import uuid
from datetime import datetime
import logging

# Import our custom modules
from openai_client import OpenAIClient
from award_engine import AwardEngine

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client and award engine
openai_client = OpenAIClient()
award_engine = AwardEngine()

@app.route('/')
def index():
    # Initialize session if needed
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['messages'] = []
        session['data'] = {
            "nominee_info": {},
            "achievements": [],
            "impacts": []
        }
    
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Add user message to session
    if 'messages' not in session:
        session['messages'] = []
    
    session['messages'].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Get response from OpenAI
    ai_response = openai_client.chat_completion(session['messages'])
    
    # Add AI response to session
    session['messages'].append({
        "role": "assistant",
        "content": ai_response["content"],
        "timestamp": datetime.now().isoformat()
    })
    
    # Save session
    session.modified = True
    
    return jsonify({
        "message": ai_response["content"],
        "session_id": session.get('session_id')
    })

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        # Use session data to generate recommendation
        messages = session.get('messages', [])
        
        # Analyze achievements using OpenAI
        analysis_text = openai_client.analyze_achievements(messages)
        logger.info(f"Achievement analysis: {analysis_text[:100]}...")
        
        # Process achievement data
        achievement_data = award_engine.process_achievement_data(analysis_text)
        
        # Score achievements
        scores = award_engine.score_achievements(achievement_data)
        
        # Get recommendation
        recommendation = award_engine.recommend_award(scores)
        
        # Generate explanation
        explanation = award_engine.generate_explanation(
            recommendation["award"], 
            achievement_data, 
            scores
        )
        
        # Store recommendation in session
        session['recommendation'] = {
            "award": recommendation["award"],
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }
        session.modified = True
        
        return jsonify({
            "award": recommendation["award"],
            "explanation": explanation,
            "session_id": session.get('session_id')
        })
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        return jsonify({
            "error": "Error generating recommendation",
            "details": str(e)
        }), 500

@app.route('/api/session', methods=['GET'])
def get_session():
    return jsonify({
        "session_id": session.get('session_id'),
        "messages": session.get('messages', []),
        "recommendation": session.get('recommendation', None)
    })

@app.route('/api/session', methods=['POST'])
def save_session():
    # In a production environment, this would save to a database
    # For now, just return the session ID
    return jsonify({
        "session_id": session.get('session_id'),
        "status": "saved"
    })

@app.route('/api/session/<session_id>', methods=['GET'])
def load_session(session_id):
    # In a production environment, this would load from a database
    # For now, just check if current session matches
    if session.get('session_id') == session_id:
        return jsonify({
            "session_id": session_id,
            "messages": session.get('messages', []),
            "recommendation": session.get('recommendation', None),
            "status": "loaded"
        })
    else:
        return jsonify({
            "error": "Session not found",
            "status": "error"
        }), 404

@app.route('/api/export', methods=['GET'])
def export_recommendation():
    recommendation = session.get('recommendation', {})
    if not recommendation:
        return jsonify({
            "error": "No recommendation available",
            "status": "error"
        }), 404
    
    export_data = {
        "award": recommendation.get("award", ""),
        "explanation": recommendation.get("explanation", ""),
        "timestamp": recommendation.get("timestamp", ""),
        "session_id": session.get('session_id')
    }
    
    return jsonify(export_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
