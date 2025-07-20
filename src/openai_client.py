"""
OpenAI Client with enhanced error handling and retry logic.
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Optional
from pathlib import Path

# Add the src directory to Python path for imports to work in both local and deployed environments
current_dir = Path(__file__).parent
if current_dir.name == 'src' and str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from openai import OpenAI

# Import error types from the new OpenAI library
from openai import (
    RateLimitError,
    AuthenticationError,
    BadRequestError,
    APIConnectionError,
    APIStatusError
)

# Import citation formatter at module level
try:
    from citation_formatter import CitationFormatter
except ImportError:
    try:
        from src.citation_formatter import CitationFormatter
    except ImportError:
        print("Warning: Could not import CitationFormatter")
        CitationFormatter = None

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Handles all calls to the OpenAI API for chat, analysis, suggestions, and drafting.
    Includes retry logic and comprehensive error handling.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        # Initialize the new OpenAI client with increased timeout for O4 models
        self.client = OpenAI(
            api_key=self.api_key,
            timeout=90.0,  # Increased timeout for O4 reasoning models
            max_retries=0  # We handle retries ourselves
        )
        self.model = os.getenv("OPENAI_MODEL", "o4-mini-2025-04-16")
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
        # Check if using a reasoning model (O1 or O4 series)
        self.is_reasoning_model = self.model.startswith(('o1-preview', 'o1-mini', 'o4-preview', 'o4-mini', 'o4-mini-2025'))

    def _handle_api_error(self, error: Exception, context: str) -> Dict:
        """Handle various OpenAI API errors with appropriate responses."""
        error_message = str(error)
        
        if isinstance(error, RateLimitError):
            logger.warning(f"Rate limit hit during {context}: {error_message}")
            return {"error": "Rate limit reached. Please try again in a moment."}
        
        elif isinstance(error, AuthenticationError):
            logger.error(f"Authentication error during {context}: {error_message}")
            return {"error": "Authentication failed. Please check API key configuration."}
        
        elif isinstance(error, BadRequestError):
            logger.error(f"Invalid request during {context}: {error_message}")
            return {"error": "Invalid request. Please check input data."}
        
        elif isinstance(error, APIConnectionError):
            logger.error(f"Connection error during {context}: {error_message}")
            return {"error": "Connection error. Please check your internet connection and try again."}
        
        elif isinstance(error, APIStatusError):
            logger.error(f"API error during {context}: {error_message}")
            return {"error": "OpenAI service error. Please try again later."}
        
        else:
            logger.error(f"Unexpected error during {context}: {error_message}", exc_info=True)
            return {"error": f"An unexpected error occurred: {error_message}"}

    def _make_api_call(self, messages: List[Dict], temperature: float = 0.7, 
                      max_tokens: Optional[int] = None, context: str = "API call") -> Dict:
        """Make an API call with retry logic."""
        # Prepare messages for reasoning models
        if self.is_reasoning_model:
            # O1 models don't support system messages, merge them into user messages
            processed_messages = []
            system_content = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    system_content += msg["content"] + "\n\n"
                else:
                    if system_content and msg["role"] == "user":
                        # Prepend system content to first user message
                        msg_copy = msg.copy()
                        msg_copy["content"] = f"{system_content}Instructions: {msg['content']}"
                        processed_messages.append(msg_copy)
                        system_content = ""
                    else:
                        processed_messages.append(msg)
            
            # If there's remaining system content, add it as a user message
            if system_content:
                processed_messages.insert(0, {"role": "user", "content": system_content})
            
            messages = processed_messages
            logger.info(f"Using reasoning model {self.model}, converted {len(messages)} messages")
            logger.debug(f"O4 model detected - temperature and max_tokens parameters will be omitted")
        else:
            logger.info(f"Using standard model {self.model}")
        
        for attempt in range(self.max_retries):
            try:
                kwargs = {
                    "model": self.model,
                    "messages": messages
                }
                
                # O1 models don't support temperature or max_tokens
                if not self.is_reasoning_model:
                    kwargs["temperature"] = temperature
                    if max_tokens:
                        kwargs["max_tokens"] = max_tokens
                
                # Log API call details
                logger.info(f"Making OpenAI API call (attempt {attempt + 1}/{self.max_retries}) for {context}")
                start_time = time.time()
                
                response = self.client.chat.completions.create(**kwargs)
                
                # Log successful response time
                elapsed_time = time.time() - start_time
                logger.info(f"OpenAI API call completed in {elapsed_time:.2f}s for {context}")
                
                return response.choices[0].message.model_dump()
                
            except RateLimitError as e:
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Rate limit hit, retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                return self._handle_api_error(e, context)
                
            except Exception as e:
                if attempt < self.max_retries - 1 and "timeout" in str(e).lower():
                    logger.info(f"Timeout on attempt {attempt + 1}, retrying...")
                    time.sleep(self.retry_delay)
                    continue
                return self._handle_api_error(e, context)
        
        return {"error": f"Failed after {self.max_retries} attempts"}

    def chat_completion(self, messages: List[Dict]) -> Dict:
        """Simple chat completion with error handling."""
        result = self._make_api_call(messages, temperature=0.7, context="chat")
        
        # Ensure we always return a properly formatted response
        if "error" in result:
            return {"role": "assistant", "content": result["error"]}
        
        return {
            "role": result.get("role", "assistant"),
            "content": result.get("content", "I understand. Please continue.")
        }

    def analyze_achievements(self, messages: List[Dict], awardee_info: Dict, 
                           refresh: bool = False) -> Dict:
        """
        Enhanced analysis with better conversation processing and comprehensive extraction.
        """
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
- PRIORITIZE achievements with quantifiable impacts and measurable results
- For each achievement, identify the ACTION (what was done), IMPACT (what changed), and RESULT (the measurable outcome)
- Link achievements to their specific impacts whenever possible
- Include ALL challenges: resource constraints, time pressure, difficult conditions, complex problems
- Look for scope indicators: individual/team/unit/sector/district/area/coast guard-wide/national/international
- Identify valor: life-saving, rescue operations, dangerous conditions, personal risk

IMPORTANT CONTEXT - Coast Guard Rank Expectations:
- Consider the awardee's rank when evaluating achievements
- Junior enlisted (E-1 to E-4) are not expected to lead large teams or have organization-wide impact
- Mid-level enlisted (E-5 to E-7) typically lead teams of 5-30 people and impact their unit
- Senior enlisted (E-8 to E-9) lead larger groups and may have sector/district impact
- Junior officers (O-1 to O-3) lead divisions/departments with unit-level impact
- Senior officers (O-4+) are expected to have sector/district/area-wide impact
- Be realistic about what constitutes exceptional performance for each rank level
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
            logger.info(f"Analyzing conversation with {len(conversation_flow)} exchanges")
            
            response = self._make_api_call(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert Coast Guard personnel analyst who extracts comprehensive achievement data from conversations. You must return valid JSON only with all specified fields populated."
                    },
                    {"role": "user", "content": base_prompt}
                ],
                temperature=0.1,  # Very low temperature for consistent extraction
                max_tokens=3000,  # Increased token limit for comprehensive response
                context="achievement analysis"
            )
            
            if "error" in response:
                raise Exception(response["error"])
            
            content = response.get("content", "").strip()
            
            # Clean up any markdown formatting (O4 models often add more formatting)
            content = content.replace('```json', '').replace('```', '').strip()
            
            # O4 models might add additional explanation - extract just the JSON
            if self.is_reasoning_model and '{' in content and '}' in content:
                # Find the JSON object in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    content = content[start_idx:end_idx]
                    logger.debug("Extracted JSON from O4 reasoning model response")
            
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
            logger.info(f"EXTRACTION RESULTS:")
            logger.info(f"  Achievements: {len(data.get('achievements', []))}")
            logger.info(f"  Impacts: {len(data.get('impacts', []))}")
            logger.info(f"  Leadership: {len(data.get('leadership_details', []))}")
            logger.info(f"  Innovation: {len(data.get('innovation_details', []))}")
            
            return data
            
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"ERROR in analyze_achievements: {e}")
            if 'content' in locals():
                logger.debug(f"Raw OpenAI response: {content[:500]}...")
            
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

    def generate_improvement_suggestions(self, award: str, achievement_data: Dict, 
                                       awardee_info: Dict) -> List[str]:
        """Generate specific improvement suggestions based on current data."""
        prompt = f"""
You are a Coast Guard award writing expert. Based on the current achievement data and recommended award level, provide specific, actionable suggestions for improvement.

CURRENT AWARD RECOMMENDATION: {award}

CURRENT ACHIEVEMENT DATA:
{json.dumps(achievement_data, indent=2)}

AWARDEE INFO:
{json.dumps(awardee_info, indent=2)}

Analyze the gaps and weaknesses in this achievement package and provide 5-7 specific, actionable suggestions for improvement. 

IMPORTANT: Be realistic about award thresholds AND consider the awardee's rank:

RANK-BASED EXPECTATIONS:
- Junior Enlisted (E-1 to E-4): Leading 2-5 people is significant; unit-level impact is exceptional
- Mid-level Enlisted (E-5 to E-7): Expected to lead 5-30 people; sector impact for higher awards
- Senior Enlisted (E-8 to E-9): Expected to lead 30+ people; district/area impact expected
- Junior Officers (O-1 to O-3): Expected to lead divisions; sector/district impact for higher awards
- Senior Officers (O-4+): Expected to have district/area/CG-wide impact; leadership of 50+ expected

GENERAL AWARD THRESHOLDS:
- Administrative/cost savings achievements rarely qualify for awards above Commendation Medal
- Life-saving actions, heroism, or combat achievements are required for Coast Guard Medal or higher
- Achievement Medal: Appropriate for exceptional performance at or slightly above rank expectations
- Commendation Medal: Requires performance significantly above rank expectations or broader impact
- MSM and above: Requires exceptional leadership AND organizational impact well above rank norm

Focus on:
1. Missing quantifiable impacts (numbers, percentages, dollar amounts)
2. Insufficient leadership details (how many people, what responsibilities)
3. Lack of scope clarity (unit/district/coast guard-wide impact)
4. Missing innovation or creative problem-solving examples
5. Insufficient challenge/obstacle details
6. Weak time period or duration information
7. Missing awards, recognitions, or special acknowledgments

Return a JSON array of suggestion strings. Each suggestion should be specific and actionable.
Example: ["Add specific numbers: How many personnel did you supervise?", "Quantify the cost savings or efficiency gains achieved"]

If the achievements have fundamental limitations (e.g., no life-saving, no leadership role, limited scope), acknowledge these realistic constraints in your suggestions.

Return ONLY the JSON array, no other text.
"""
        
        try:
            response = self._make_api_call(
                messages=[
                    {"role": "system", "content": "You provide specific, actionable improvement suggestions for Coast Guard award packages."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                context="improvement suggestions"
            )
            
            if "error" in response:
                raise Exception(response["error"])
            
            content = response.get("content", "").strip()
            
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
            logger.error(f"Error generating suggestions: {e}")
            
            # Fallback suggestions based on missing data
            return self._generate_fallback_suggestions(achievement_data)

    def _generate_fallback_suggestions(self, achievement_data: Dict) -> List[str]:
        """Generate fallback suggestions when API call fails."""
        suggestions = []
        
        impacts = achievement_data.get('impacts', [])
        leadership = achievement_data.get('leadership_details', [])
        innovations = achievement_data.get('innovation_details', [])
        
        if len(impacts) < 3:
            suggestions.append("Add more quantifiable impacts with specific numbers, percentages, or dollar amounts")
        
        if len(leadership) < 2:
            suggestions.append("Include more leadership details: How many people did you supervise or lead?")
        
        if not achievement_data.get('scope') or 'not specified' in achievement_data.get('scope', '').lower():
            suggestions.append("Clarify the scope of impact: Was this unit-level, district-level, or Coast Guard-wide?")
        
        if len(innovations) < 2:
            suggestions.append("Highlight any innovative approaches, creative solutions, or process improvements")
        
        if len(achievement_data.get('challenges', [])) < 2:
            suggestions.append("Describe specific challenges or obstacles that were overcome")
        
        suggestions.extend([
            "Include any awards, recognitions, or commendations received for this work",
            "Specify the time period over which these accomplishments occurred"
        ])
        
        return suggestions[:6]  # Return max 6 suggestions

    def draft_award(self, award: str, achievement_data: Dict, awardee_info: Dict) -> str:
        """Generate a formal award citation compliant with CG standards."""
        # Try to use the new citation generator for rich narratives
        try:
            from citation_generator import CitationGenerator
            generator = CitationGenerator()
            citation = generator.generate_citation(award, awardee_info, achievement_data)
            return citation
        except ImportError:
            logger.warning("CitationGenerator not available, falling back to CitationFormatter")
            
        # Check if CitationFormatter is available
        if CitationFormatter is None:
            # Fallback to the old method if CitationFormatter is not available
            return self._generate_condensed_citation(award, achievement_data, awardee_info)
            
        # Use the formatter to create a compliant citation
        formatter = CitationFormatter()
        citation = formatter.format_citation(award, awardee_info, achievement_data)
        
        # Validate the citation
        is_valid, issues = formatter.validate_citation(citation, award)
        
        if not is_valid:
            logger.warning(f"Citation validation issues: {issues}")
            # Try to fix common issues
            if any("exceeds limit" in issue for issue in issues):
                # Citation too long, need to condense
                return self._generate_condensed_citation(award, achievement_data, awardee_info)
        
        return citation
    
    def _generate_condensed_citation(self, award: str, achievement_data: Dict, awardee_info: Dict) -> str:
        """Generate a condensed citation when the standard one is too long."""
        # Check if operational device is authorized
        has_operational_device = awardee_info.get('operational_device', False)
        
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

{"IMPORTANT: At the very end of the citation, add the following sentence on a new line: 'The Operational Distinguishing Device is authorized.'" if has_operational_device else ""}

Return only the formatted citation text.
"""
        
        try:
            response = self._make_api_call(
                messages=[
                    {"role": "system", "content": "You draft official Coast Guard award citations in proper military format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                context="award citation drafting"
            )
            
            if "error" in response:
                return f"Unable to draft {award} citation at this time. Error: {response['error']}"
            
            return response.get("content", "").strip()
            
        except Exception as e:
            logger.error(f"Error drafting citation: {e}")
            return f"Unable to draft {award} citation at this time. Please try again or contact support."