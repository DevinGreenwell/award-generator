# Coast Guard Award Writing Tool - OpenAI API Integration

import os
import openai
from flask import current_app

class OpenAIClient:
    """
    Client for interacting with the OpenAI API for the Coast Guard Award Writing Tool.
    Handles chat completions and manages conversation context.
    """
    
    def __init__(self, api_key=None):
        """Initialize the OpenAI client with the provided API key."""
        # Use provided API key or get from environment
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY', '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')
        openai.api_key = self.api_key
        
        # System prompt that guides the AI's behavior
        self.system_prompt = """
        You are an AI assistant for the Coast Guard Award Writing Tool. Your purpose is to help gather information about service members' accomplishments and recommend appropriate awards based on objective criteria from the Coast Guard Military Medals and Awards Manual (COMDTINST M1650.25E) and the Coast Guard Civilian Awards Manual (COMDTINST M12451.1C).

        Important guidelines:
        1. Focus on collecting quantitative data and action-impact-results information
        2. Make award recommendations based on accomplishments, NOT on rank
        3. Ask follow-up questions to gather specific details about achievements
        4. Help quantify qualitative statements when possible
        5. Maintain a professional, helpful tone
        6. Structure your data collection to cover:
           - Basic nominee information (rank/grade, position)
           - Specific actions taken
           - Quantifiable impacts and results
           - Scope of impact (individual, unit, Coast Guard-wide)
           - Challenges or unusual circumstances
        
        Remember that the goal is to ensure awards are based on objective criteria rather than rank.
        """
    
    def chat_completion(self, messages):
        """
        Send the conversation history to OpenAI and get a response.
        
        Args:
            messages: List of message objects with 'role' and 'content'
            
        Returns:
            Dict containing the assistant's response
        """
        try:
            # Prepare messages with system prompt
            formatted_messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            for msg in messages:
                if msg.get('role') in ['user', 'assistant']:
                    formatted_messages.append({
                        "role": msg.get('role'),
                        "content": msg.get('content', '')
                    })
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Using GPT-4 for best results
                messages=formatted_messages,
                temperature=0.7,  # Balanced between creativity and consistency
                max_tokens=800,  # Reasonable response length
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # Extract and return the assistant's message
            return {
                "role": "assistant",
                "content": response.choices[0].message.content
            }
            
        except Exception as e:
            current_app.logger.error(f"OpenAI API error: {str(e)}")
            return {
                "role": "assistant",
                "content": "I'm sorry, I encountered an error processing your request. Please try again or contact support if the issue persists."
            }
    
    def analyze_achievements(self, messages):
        """
        Analyze the conversation to extract achievement data for award recommendation.
        
        Args:
            messages: List of message objects with conversation history
            
        Returns:
            Dict containing structured achievement data
        """
        try:
            # Create a prompt for achievement analysis
            analysis_prompt = """
            Based on the conversation, please analyze the service member's accomplishments and provide structured data in JSON format with these fields:
            1. nominee_info: Basic information about the nominee (rank, position)
            2. achievements: List of specific actions and accomplishments
            3. impacts: List of quantifiable impacts and results
            4. scope: Scope of impact (individual, unit, Coast Guard-wide, etc.)
            5. challenges: Any unusual circumstances or challenges
            6. recommended_award: Your recommendation based on Coast Guard award criteria
            7. justification: Brief explanation of why this award is appropriate
            
            Provide ONLY the JSON response without additional text.
            """
            
            # Prepare messages for analysis
            formatted_messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": analysis_prompt}
            ]
            
            # Add conversation history as context
            conversation_text = "\n\n".join([
                f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" 
                for msg in messages if msg.get('role') in ['user', 'assistant']
            ])
            formatted_messages.append({
                "role": "user", 
                "content": f"Here is the conversation to analyze:\n\n{conversation_text}"
            })
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=formatted_messages,
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # Extract and return the analysis
            analysis_text = response.choices[0].message.content
            
            # In a production environment, we would parse the JSON here
            # For now, we'll return the raw text for the award engine to handle
            return analysis_text
            
        except Exception as e:
            current_app.logger.error(f"OpenAI analysis error: {str(e)}")
            return "Error analyzing achievements"
