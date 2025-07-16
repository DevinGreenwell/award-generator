# Coast Guard Award Writing Tool Implementation

## Overview
This document outlines the implementation plan for the Coast Guard Award Writing Tool, a Python-based application with a GUI interface that uses AI to gather information about service members' accomplishments and recommend appropriate awards based on objective criteria from the Coast Guard Military Medals and Awards Manual and Civilian Awards Manual.

## Project Structure
```
coast_guard_award_tool/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py   # Main application window
│   │   ├── chat_panel.py    # Chat interface panel
│   │   ├── award_panel.py   # Award display panel
│   │   └── styles.py        # GUI styling
│   ├── core/
│   │   ├── __init__.py
│   │   ├── chat_manager.py  # Manages chat conversation flow
│   │   ├── openai_client.py # Handles OpenAI API integration
│   │   ├── award_engine.py  # Award recommendation algorithm
│   │   └── explanation.py   # Award explanation generation
│   ├── data/
│   │   ├── __init__.py
│   │   ├── award_criteria.py # Award criteria database
│   │   ├── manual_references.py # Manual reference database
│   │   └── user_data.py     # User data management
│   └── utils/
│       ├── __init__.py
│       ├── text_processing.py # Text analysis utilities
│       └── export.py        # Export functionality
├── tests/
│   ├── __init__.py
│   ├── test_award_engine.py
│   ├── test_explanation.py
│   └── test_validation.py
├── resources/
│   ├── manuals/             # Reference manual excerpts
│   ├── templates/           # Award templates
│   └── sample_cases/        # Sample award scenarios
└── requirements.txt         # Project dependencies
```

## Implementation Steps

### 1. Environment Setup
- Create Python virtual environment
- Install required packages:
  - PyQt6 for GUI
  - OpenAI for API integration
  - NLTK for text processing
  - Pandas for data management
  - Pytest for testing

### 2. Core Components Implementation

#### OpenAI Integration
- Implement OpenAI client with provided API key
- Create system prompts based on award criteria
- Develop conversation management system
- Implement error handling and retry logic

#### Award Engine
- Implement scoring system from algorithm design
- Create criteria matching functions
- Develop award threshold verification
- Build recommendation generation system

#### Explanation Module
- Implement template-based explanation generation
- Create manual reference lookup system
- Develop evidence-to-criteria mapping
- Build natural language generation for explanations

### 3. GUI Implementation

#### Main Window
- Create application main window
- Implement navigation panel
- Design responsive layout

#### Chat Interface
- Implement chat message display
- Create text input with wrapping
- Design message bubbles and styling
- Build attachment handling

#### Award Display
- Create award recommendation cards
- Implement explanation display
- Build export functionality
- Design criteria checklist display

### 4. Data Management

#### Award Criteria Database
- Extract and structure criteria from manuals
- Create searchable database of requirements
- Implement scoring thresholds

#### User Data Management
- Create session management
- Implement save/load functionality
- Build export to standard formats

### 5. Testing and Validation

#### Unit Testing
- Test award engine scoring accuracy
- Validate explanation generation
- Verify OpenAI integration

#### Validation Testing
- Implement validation framework
- Create test scenarios
- Verify rank neutrality
- Confirm manual alignment

#### User Experience Testing
- Test GUI responsiveness
- Verify text wrapping
- Validate conversation flow

## Integration Plan

### OpenAI API Integration
```python
# Example implementation of OpenAI client
import openai

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        
    def generate_chat_response(self, messages, system_prompt):
        try:
            full_messages = [
                {"role": "system", "content": system_prompt}
            ]
            full_messages.extend(messages)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=full_messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return "I'm having trouble processing that. Could you try again?"
```

### Award Engine Implementation
```python
# Example implementation of award scoring
class AwardEngine:
    def __init__(self, criteria_db):
        self.criteria_db = criteria_db
        
    def score_achievement(self, achievement_data):
        scores = {
            "scope": self._score_scope(achievement_data),
            "duration": self._score_duration(achievement_data),
            "efficiency": self._score_efficiency(achievement_data),
            "initiative": self._score_initiative(achievement_data),
            "complexity": self._score_complexity(achievement_data),
            "risk": self._score_risk(achievement_data)
        }
        
        total_score = sum(scores.values())
        return total_score, scores
    
    def recommend_award(self, total_score, achievement_data):
        # Map score to award recommendations based on thresholds
        if total_score >= 46:
            return "Distinguished Service Medal"
        elif total_score >= 36:
            return "Legion of Merit"
        elif total_score >= 26:
            return "Meritorious Service Medal"
        elif total_score >= 16:
            return "Commendation Medal"
        elif total_score >= 10:
            return "Achievement Medal"
        else:
            return "Letter of Commendation"
```

### GUI Implementation
```python
# Example implementation of chat interface
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class ChatPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        self.text_input = QTextEdit()
        self.text_input.setAcceptRichText(False)
        self.text_input.setPlaceholderText("Type your message here...")
        self.text_input.setMaximumHeight(100)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(send_button)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
        
    def send_message(self):
        message = self.text_input.toPlainText().strip()
        if message:
            self.add_user_message(message)
            self.text_input.clear()
            # Signal to process message would be emitted here
            
    def add_user_message(self, message):
        self.chat_display.append(f'<div style="text-align: right;"><p style="background-color: #DCF8C6; display: inline-block; padding: 8px; border-radius: 8px; max-width: 70%;">{message}</p></div>')
        
    def add_ai_message(self, message):
        self.chat_display.append(f'<div style="text-align: left;"><p style="background-color: #F1F0F0; display: inline-block; padding: 8px; border-radius: 8px; max-width: 70%;">{message}</p></div>')
```

## Validation Implementation
```python
# Example implementation of validation testing
class ValidationTester:
    def __init__(self, award_engine, explanation_module):
        self.award_engine = award_engine
        self.explanation_module = explanation_module
        
    def test_rank_neutrality(self, scenario, ranks):
        results = {}
        
        for rank in ranks:
            # Create copy of scenario with different rank
            test_scenario = scenario.copy()
            test_scenario["rank"] = rank
            
            # Get recommendation
            score, score_breakdown = self.award_engine.score_achievement(test_scenario)
            recommendation = self.award_engine.recommend_award(score, test_scenario)
            explanation = self.explanation_module.generate_explanation(recommendation, score_breakdown, test_scenario)
            
            results[rank] = {
                "recommendation": recommendation,
                "score": score,
                "explanation": explanation
            }
        
        # Check if all recommendations are the same
        recommendations = [r["recommendation"] for r in results.values()]
        is_neutral = all(r == recommendations[0] for r in recommendations)
        
        return is_neutral, results
```

## Next Steps
1. Set up development environment with required dependencies
2. Implement core components (OpenAI integration, award engine, explanation module)
3. Develop GUI components
4. Create comprehensive test suite
5. Validate against sample scenarios
6. Refine based on validation results
7. Package for distribution
