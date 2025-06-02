import openai
import os
import json
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from award_engine import AwardEngine
from dotenv import load_dotenv
load_dotenv()

# Configure Flask app with proper static/template folders
app = Flask(__name__, 
           static_folder='static',
           static_url_path='/static',
           template_folder='templates')

app.secret_key = os.urandom(24)

class OpenAIClient:
    def __init__(self, api_key=None):
        # Use environment variable - NEVER hardcode API keys
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        openai.api_key = self.api_key

    def chat_completion(self, messages):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini-2024-07-18", # Use the latest model for best results
                messages=messages
            )
            return response.choices[0].message
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return {"role": "assistant", "content": f"Error: {str(e)}"}

    def analyze_achievements(self, messages, awardee_info, refresh=False):
        """Enhanced analysis with better conversation processing and comprehensive extraction"""
        
        # Separate user content from assistant responses
        user_content = []
        conversation_flow = []
        user_inputs = []
        
        for i, msg in enumerate(messages):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '').strip()
            
            if role == 'user' and content:
                user_content.append(content)
                user_inputs.append(content)
                conversation_flow.append(f"USER {i}: {content}")
            elif role == 'assistant' and content:
                conversation_flow.append(f"ASSISTANT {i}: {content}")
        
        # Build comprehensive conversation text
        conversation_text = '\n'.join(conversation_flow)
        
        # Enhanced prompt with comprehensive extraction
        base_prompt = f"""
        You are an expert Coast Guard personnel analyst. Analyze this complete conversation 
        to extract ALL achievements, impacts, and award-relevant details.

        AWARDEE INFORMATION:
        {json.dumps(awardee_info, indent=2)}

        FULL CONVERSATION:
        {conversation_text}

        Extract comprehensive data and return ONLY valid JSON with this EXACT structure:
        {{
            "achievements": [
                "List ALL significant accomplishments, projects, initiatives, and responsibilities mentioned"
            ],
            "impacts": [
                "List ALL quantifiable results, outcomes, improvements, and benefits mentioned"
            ],
            "leadership_details": [
                "List ALL leadership roles, supervision, training provided, and management responsibilities"
            ],
            "innovation_details": [
                "List ALL creative solutions, new processes, improvements, and first-time initiatives"
            ],
            "challenges": [
                "List ALL obstacles, difficulties, constraints, and complex situations overcome"
            ],
            "scope": "Detailed description of organizational reach (individual/unit/sector/district/area/coast guard-wide/national/international)",
            "time_period": "Duration or timeframe of accomplishments (be specific: days/weeks/months/years)",
            "valor_indicators": [
                "List ANY life-saving actions, rescue operations, dangerous situations, or heroic acts"
            ],
            "quantifiable_metrics": [
                "List ALL specific numbers, percentages, dollar amounts, time savings, or measurable results"
            ],
            "awards_received": [
                "List ANY awards, commendations, recognitions, or formal acknowledgments mentioned"
            ],
            "collaboration": [
                "List inter-agency work, joint operations, multi-unit coordination, or external partnerships"
            ],
            "training_provided": [
                "List training delivered to others, knowledge transfer, mentoring, or skill development activities"
            ],
            "above_beyond_indicators": [
                "List ANY voluntary overtime, extra duties, personal sacrifice, or exceptional effort beyond normal duties"
            ],
            "emergency_response": [
                "List ANY emergency situations, crisis response, urgent missions, or time-critical operations"
            ],
            "justification": "Comprehensive summary explaining why these accomplishments are significant and noteworthy for Coast Guard awards"
        }}

        CRITICAL EXTRACTION INSTRUCTIONS:
        - Extract EVERY achievement mentioned, regardless of size or perceived importance
        - Include ALL quantifiable data: exact numbers, percentages, dollar amounts, timeframes, personnel counts
        - Capture leadership at ANY level: formal supervision, informal leadership, project management, team coordination
        - Note ANY innovation, process improvement, creative solution, or new approach
        - Include ALL challenges: resource constraints, time pressure, difficult conditions, complex problems
        - Look for scope indicators: individual/team/unit/sector/district/area/coast guard-wide/national/international
        - Identify valor: life-saving, rescue operations, dangerous conditions, personal risk
        - Extract collaboration: inter-agency, joint operations, partnerships, coordination efforts
        - Find training activities: instruction given, mentoring provided, knowledge transfer
        - Identify above-and-beyond: voluntary work, extra hours, personal sacrifice, exceptional effort
        - Note emergency response: crisis situations, urgent missions, disaster response
        - Pay attention to IMPLIED accomplishments from context and follow-up details
        - Be specific and detailed - avoid generic statements
        
        Return ONLY the JSON object with no additional text, formatting, or explanations.
        """
        
        if refresh:
            base_prompt += "\n\nIMPORTANT: This is a REFRESH analysis. Provide alternative phrasing and extract any additional details that may have been missed in previous analysis. Look for subtle details, implied accomplishments, and context clues."

        try:
            print(f"Analyzing conversation with {len(conversation_flow)} exchanges")
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert Coast Guard personnel analyst who extracts comprehensive achievement data from conversations. You must return valid JSON only with all specified fields populated."
                    },
                    {"role": "user", "content": base_prompt}
                ],
                temperature=0.1,  # Very low temperature for consistent extraction
                max_tokens=3000   # Increased token limit for comprehensive response
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up any markdown formatting
            content = content.replace('```json', '').replace('```', '').strip()
            
            # Parse the JSON response
            data = json.loads(content)
            
            # Validate and ensure all required fields exist with proper defaults
            required_fields = {
                'achievements': [],
                'impacts': [],
                'leadership_details': [],
                'innovation_details': [],
                'challenges': [],
                'scope': 'Not specified',
                'time_period': 'Not specified',
                'valor_indicators': [],
                'quantifiable_metrics': [],
                'awards_received': [],
                'collaboration': [],
                'training_provided': [],
                'above_beyond_indicators': [],
                'emergency_response': [],
                'justification': 'Based on the provided accomplishments and their significance to Coast Guard operations'
            }
            
            # Ensure all fields exist and have proper values
            for field, default_value in required_fields.items():
                if field not in data:
                    data[field] = default_value
                elif not data[field] and isinstance(default_value, list):
                    data[field] = []
                elif not data[field] and isinstance(default_value, str):
                    data[field] = default_value
            
            # Enhanced fallback if no achievements extracted
            if not data.get('achievements') or len(data['achievements']) == 0:
                if user_inputs:
                    data['achievements'] = user_inputs[:5]  # Limit to first 5 user inputs
                else:
                    data['achievements'] = ["No specific achievements identified from conversation"]
            
            # Log extraction results
            print(f"EXTRACTION RESULTS:")
            print(f"  Achievements: {len(data.get('achievements', []))}")
            print(f"  Impacts: {len(data.get('impacts', []))}")
            print(f"  Leadership: {len(data.get('leadership_details', []))}")
            print(f"  Innovation: {len(data.get('innovation_details', []))}")
            print(f"  Challenges: {len(data.get('challenges', []))}")
            print(f"  Valor Indicators: {len(data.get('valor_indicators', []))}")
            print(f"  Quantifiable Metrics: {len(data.get('quantifiable_metrics', []))}")
            print(f"  Scope: {data.get('scope', 'Not specified')}")
            print(f"  Time Period: {data.get('time_period', 'Not specified')}")
            
            return data
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"ERROR in analyze_achievements: {e}")
            if 'content' in locals():
                print(f"Raw OpenAI response: {content[:500]}...")
            
            # Comprehensive fallback structure
            fallback_data = {
                "achievements": user_inputs if user_inputs else ["No achievements specified"],
                "impacts": [],
                "leadership_details": [],
                "innovation_details": [],
                "challenges": [],
                "scope": "Individual level",
                "time_period": "Not specified",
                "valor_indicators": [],
                "quantifiable_metrics": [],
                "awards_received": [],
                "collaboration": [],
                "training_provided": [],
                "above_beyond_indicators": [],
                "emergency_response": [],
                "justification": "Analysis failed - using basic extraction from user inputs. Please try generating the recommendation again."
            }
            
            return fallback_data

    def generate_improvement_suggestions(self, award, achievement_data, awardee_info):
        """Generate specific improvement suggestions based on current data."""
        
        # Analyze what's missing or weak
        achievements = achievement_data.get('achievements', [])
        impacts = achievement_data.get('impacts', [])
        leadership = achievement_data.get('leadership_details', [])
        innovations = achievement_data.get('innovation_details', [])
        
        prompt = f"""
        You are a Coast Guard award writing expert. Based on the current achievement data and recommended award level, provide specific, actionable suggestions for improvement.

        CURRENT AWARD RECOMMENDATION: {award}
        
        CURRENT ACHIEVEMENT DATA:
        {json.dumps(achievement_data, indent=2)}
        
        AWARDEE INFO:
        {json.dumps(awardee_info, indent=2)}

        Analyze the gaps and weaknesses in this achievement package and provide 5-7 specific, actionable suggestions for improvement. Focus on:

        1. Missing quantifiable impacts (numbers, percentages, dollar amounts)
        2. Insufficient leadership details (how many people, what responsibilities)
        3. Lack of scope clarity (unit/district/coast guard-wide impact)
        4. Missing innovation or creative problem-solving examples
        5. Insufficient challenge/obstacle details
        6. Weak time period or duration information
        7. Missing awards, recognitions, or special acknowledgments

        Return a JSON array of suggestion strings. Each suggestion should be specific and actionable.
        Example: ["Add specific numbers: How many personnel did you supervise?", "Quantify the cost savings or efficiency gains achieved"]

        Return ONLY the JSON array, no other text.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": "You provide specific, actionable improvement suggestions for Coast Guard award packages."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up markdown if present
            if content.startswith('```'):
                content = content.split('\n', 1)[1] if '\n' in content else content[3:]
            if content.endswith('```'):
                content = content.rsplit('\n', 1)[0] if '\n' in content else content[:-3]
            
            suggestions = json.loads(content)
            
            if isinstance(suggestions, list):
                return suggestions
            else:
                return list(suggestions.values()) if isinstance(suggestions, dict) else [str(suggestions)]
                
        except Exception as e:
            print(f"Error generating suggestions: {e}")
            
            # Fallback suggestions based on missing data
            fallback_suggestions = []
            
            if len(impacts) < 3:
                fallback_suggestions.append("Add more quantifiable impacts with specific numbers, percentages, or dollar amounts")
            
            if len(leadership) < 2:
                fallback_suggestions.append("Include more leadership details: How many people did you supervise or lead?")
            
            if not achievement_data.get('scope') or 'not specified' in achievement_data.get('scope', '').lower():
                fallback_suggestions.append("Clarify the scope of impact: Was this unit-level, district-level, or Coast Guard-wide?")
            
            if len(innovations) < 2:
                fallback_suggestions.append("Highlight any innovative approaches, creative solutions, or process improvements")
            
            if len(achievement_data.get('challenges', [])) < 2:
                fallback_suggestions.append("Describe specific challenges or obstacles that were overcome")
            
            fallback_suggestions.extend([
                "Include any awards, recognitions, or commendations received for this work",
                "Specify the time period over which these accomplishments occurred"
            ])
            
            return fallback_suggestions[:6]  # Return max 6 suggestions

    def draft_award(self, award, achievement_data, awardee_info):
        """Generate a formal award citation."""
        prompt = f"""
        Draft a formal Coast Guard {award} citation using the following information:

        ACHIEVEMENT DATA:
        {json.dumps(achievement_data, indent=2)}

        AWARDEE INFORMATION:
        {json.dumps(awardee_info, indent=2)}

        Create a professional, formal citation that follows Coast Guard standards. Include:
        - Formal opening with awardee information
        - Specific accomplishments and their impacts
        - Leadership demonstrated
        - Scope and significance of contributions
        - Formal closing appropriate for this award level

        Return only the formatted citation text.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You draft official Coast Guard award citations in proper military format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error drafting citation: {e}")
            return f"Unable to draft {award} citation at this time. Please try again or contact support."

# Initialize award engine and OpenAI client
award_engine = AwardEngine()
openai_client = OpenAIClient()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/session/clear', methods=['POST'])
def clear_session():
    """Clear the current session data"""
    try:
        # Clear all session data
        session.clear()
        
        # You might also want to clear any stored data if you're using a database
        # For example, if you store sessions in a database:
        # session_id = session.get('session_id')
        # if session_id:
        #     # Delete from database
        #     pass
        
        return jsonify({
            'success': True,
            'message': 'Session cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Handle chat messages and store conversation history."""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "Empty message"}), 400
        
        # Get existing messages from session
        messages = session.get('messages', [])
        
        # Add the new user message
        messages.append({
            "role": "user", 
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Prepare messages for OpenAI (only role and content, no timestamp)
        openai_messages = [
            {"role": "system", "content": "You are a helpful assistant helping to document Coast Guard achievements for award recommendations. Acknowledge the user's input and encourage them to continue sharing details."}
        ]
        
        # Add conversation history in proper format for OpenAI
        for msg in messages:
            if msg.get('role') in ['user', 'assistant'] and msg.get('content'):
                openai_messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Debug logging
        print(f"Sending {len(openai_messages)} messages to OpenAI")
        print(f"Latest message: {message[:100]}...")
        
        # Generate AI response using conversation context
        ai_response = openai_client.chat_completion(openai_messages)
        
        # Add AI response to messages
        messages.append({
            "role": "assistant",
            "content": ai_response.get("content", "I understand. Please continue."),
            "timestamp": datetime.now().isoformat()
        })
        
        # Store updated messages in session
        session['messages'] = messages
        
        # Debug: Print message count
        print(f"Total messages in session: {len(messages)}")
        
        return jsonify({
            "success": True,
            "response": ai_response.get("content", "I understand. Please continue."),
            "message_count": len(messages)
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": f"Chat error: {str(e)}"}), 500

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """Generate award recommendation based on conversation."""
    try:
        data = request.get_json()
        awardee_info = data.get('awardee_info', {})
        
        # Get ALL messages from the session
        messages = session.get('messages', [])
        
        if not messages:
            return jsonify({
                "error": "No achievements have been added yet. Please describe some achievements using the chat interface first, then click 'Generate Recommendation'."
            }), 400
        
        # Filter to only user messages for verification
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        
        if not user_messages:
            return jsonify({
                "error": "No achievement descriptions found. Please describe your accomplishments using the chat interface."
            }), 400
        
        print(f"Analyzing {len(user_messages)} user messages with {len(messages)} total messages")
        
        # Analyze ALL messages using improved method
        achievement_data = openai_client.analyze_achievements(messages, awardee_info)
        
        # Store the analysis in session for later use
        session['achievement_data'] = achievement_data
        
        # Score the achievements using enhanced data
        scores = award_engine.score_achievements(achievement_data)
        
        # Get award recommendation
        recommendation = award_engine.recommend_award(scores)
        award = recommendation["award"]
        
        # Generate explanation
        explanation = award_engine.generate_explanation(award, achievement_data, scores)
        
        # Store recommendation in session
        session['recommendation'] = {
            'award': award,
            'explanation': explanation,
            'achievement_data': achievement_data,
            'scores': scores
        }
        
        return jsonify({
            "success": True,
            "award": award,
            "explanation": explanation,
            "scores": scores,
            "achievement_data": achievement_data,
            "message_count": len(messages)
        })
        
    except Exception as e:
        app.logger.error(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": f"Failed to generate recommendation: {str(e)}"}), 500

@app.route('/api/improve', methods=['POST'])
def api_improve():
    """Generate improvement suggestions for the current award recommendation"""
    try:
        data = request.get_json()
        current_award = data.get('current_award', '')
        
        # Debug logging
        print(f"Improve endpoint received data: {data}")
        print(f"Current award: {current_award}")
        print(f"Session keys: {list(session.keys())}")
        
        # Get current award from session if not provided in request
        if not current_award:
            recommendation = session.get('recommendation', {})
            current_award = recommendation.get('award', '')
            print(f"Retrieved award from session: {current_award}")
        
        if not current_award:
            return jsonify({
                'success': False,
                'error': 'No current award found. Please generate a recommendation first.'
            }), 400
        
        # Get current session data
        achievement_data = session.get('achievement_data', {})
        awardee_info = data.get('awardee_info', {})
        
        print(f"Achievement data keys: {list(achievement_data.keys()) if achievement_data else 'None'}")
        
        if not achievement_data:
            return jsonify({
                'success': False,
                'error': 'No achievement data found. Please generate a recommendation first.'
            }), 400
        
        # Generate improvement suggestions using OpenAI
        suggestions = openai_client.generate_improvement_suggestions(
            current_award, achievement_data, awardee_info
        )
        
        print(f"Generated {len(suggestions)} suggestions")
        
        # Get current scores for reference
        current_scores = award_engine.score_achievements(achievement_data)
        
        # Store improvement suggestions in session
        session['improvement_suggestions'] = {
            'current_award': current_award,
            'suggestions': suggestions,
            'current_scores': current_scores
        }
        
        return jsonify({
            'success': True,
            'current_award': current_award,
            'suggestions': suggestions,
            'current_scores': current_scores
        })
        
    except Exception as e:
        print(f"Error in improve endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/finalize', methods=['POST'])
def api_finalize():
    """Generate final award citation."""
    try:
        data = request.get_json()
        award = data.get('award')
        awardee_info = data.get('awardee_info', {})
        
        # Debug logging
        print(f"Finalize endpoint received data: {data}")
        print(f"Award from request: {award}")
        print(f"Session keys: {list(session.keys())}")
        
        # Get award from session if not provided in request
        if not award:
            recommendation = session.get('recommendation', {})
            award = recommendation.get('award', '')
            print(f"Retrieved award from session: {award}")
        
        if not award:
            return jsonify({
                'success': False,
                'error': 'No award specified. Please generate a recommendation first.'
            }), 400
        
        # Get current achievement data from session
        achievement_data = session.get('achievement_data', {})
        
        print(f"Achievement data keys: {list(achievement_data.keys()) if achievement_data else 'None'}")
        
        if not achievement_data:
            return jsonify({
                'success': False,
                'error': 'No achievement data found. Please generate a recommendation first.'
            }), 400
        
        print(f"Generating citation for award: {award}")
        
        # Generate final citation
        citation = openai_client.draft_award(award, achievement_data, awardee_info)
        
        print(f"Generated citation length: {len(citation)} characters")
        
        # Store finalized award in session
        session['finalized_award'] = {
            'award': award,
            'citation': citation
        }
        
        return jsonify({
            'success': True,
            'award': award,
            'citation': citation
        })
        
    except Exception as e:
        print(f"Error in finalize endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Failed to finalize award: {str(e)}'
        }), 500

# Keep all other routes the same
@app.route('/api/export', methods=['POST'])
def api_export():
    data = request.get_json()
    awardee_info = data.get('awardee_info', {})
    
    # Get current state
    finalized = session.get('finalized_award')
    recommendation = session.get('recommendation')
    
    if finalized:
        return jsonify({
            'award': finalized['award'],
            'citation': finalized['citation']
        })
    elif recommendation:
        return jsonify({
            'award': recommendation['award'],
            'explanation': recommendation['explanation']
        })
    else:
        return jsonify({
            'award': 'No Award',
            'explanation': 'No recommendation available'
        })

@app.route('/api/session', methods=['GET'])
def get_session():
    session_data = {
        "session_id": session.get('session_id', 'default'),
        "session_name": session.get('session_name', ''),
        "messages": session.get('messages', []),
        "awardee_info": session.get('awardee_info', {}),
        "recommendation": session.get('recommendation'),
        "finalized_award": session.get('finalized_award')
    }
    return jsonify(session_data)

@app.route('/api/session', methods=['POST'])
def save_session():
    data = request.get_json()
    # Save relevant fields to session
    for key in ['session_id', 'session_name', 'messages', 'awardee_info']:
        if key in data:
            session[key] = data[key]
    return jsonify({"status": "success", "message": "Session data saved.", "session_id": session.get('session_id', 'default')})

@app.route('/api/session/<session_id>', methods=['GET'])
def load_session(session_id):
    # For now, just return current session data
    session_data = {
        "session_id": session_id,
        "session_name": session.get('session_name', ''),
        "messages": session.get('messages', []),
        "awardee_info": session.get('awardee_info', {}),
        "recommendation": session.get('recommendation'),
        "finalized_award": session.get('finalized_award')
    }
    return jsonify(session_data)

@app.route('/api/debug/session', methods=['GET'])
def debug_session():
    """Debug endpoint to check session state"""
    return jsonify({
        "session_keys": list(session.keys()),
        "messages_count": len(session.get('messages', [])),
        "has_achievement_data": 'achievement_data' in session,
        "has_recommendation": 'recommendation' in session,
        "session_id": session.get('session_id', 'No ID'),
        "recent_messages": [
            {
                "role": msg.get('role'),
                "content": msg.get('content', '')[:100] + "..." if len(msg.get('content', '')) > 100 else msg.get('content', ''),
                "timestamp": msg.get('timestamp')
            }
            for msg in session.get('messages', [])[-5:]  # Last 5 messages
        ]
    })
    
if __name__ == "__main__":
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For production (Railway will use this)
    app.config['DEBUG'] = False