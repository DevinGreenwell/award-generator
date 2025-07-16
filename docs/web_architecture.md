# Coast Guard Award Writing Tool - Web Application Architecture

## Overview
This document outlines the architecture for the web-based implementation of the Coast Guard Award Writing Tool. The application will provide a chat interface for gathering information about service members' accomplishments and recommend appropriate awards based on objective criteria from the Coast Guard manuals.

## System Architecture

### High-Level Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Web Frontend   │◄───►│  Flask Backend  │◄───►│   OpenAI API    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │                 │
                        │  Session Store  │
                        │                 │
                        └─────────────────┘
```

### Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript (with optional Vue.js for reactivity)
- **Backend**: Python with Flask framework
- **Session Management**: Flask-Session with filesystem storage
- **API Integration**: OpenAI Python client library
- **Deployment**: Flask application deployed to a cloud platform

## Component Design

### 1. Frontend Components

#### Chat Interface
- **Chat Display Area**: Shows conversation history between user and AI
- **Input Area**: Text input with wrapping for user messages
- **Send Button**: Submits user input to backend
- **Progress Indicator**: Shows chat progress and data collection status

#### Award Display
- **Recommendation Card**: Shows recommended award with justification
- **Explanation Section**: Displays detailed reasoning for recommendation
- **Export Options**: Allows saving or printing the recommendation

#### Session Management
- **Session Controls**: Save, resume, or start new session
- **Local Storage**: Backup of session data in browser storage

### 2. Backend Components

#### Flask Application
- **Routes**:
  - `/`: Main application page
  - `/api/chat`: Endpoint for chat messages
  - `/api/recommend`: Endpoint for award recommendations
  - `/api/session`: Endpoint for session management
  - `/api/export`: Endpoint for exporting recommendations

#### Chat Manager
- Manages conversation flow and context
- Tracks collected information
- Determines when sufficient data is gathered

#### Award Engine
- Processes collected data
- Applies scoring algorithm based on manual criteria
- Generates award recommendations

#### Explanation Module
- Creates detailed justifications for recommendations
- References specific manual criteria
- Formats explanation for display

#### Session Handler
- Creates and manages user sessions
- Stores conversation history and collected data
- Allows resuming previous sessions

### 3. External Integrations

#### OpenAI API Integration
- Handles API authentication and requests
- Manages conversation context
- Processes natural language responses

## Data Flow

### Chat Flow
1. User enters information in chat interface
2. Frontend sends message to backend API
3. Backend processes message and updates session data
4. Backend sends message to OpenAI API if needed
5. Response is returned to frontend
6. Frontend updates chat display

### Recommendation Flow
1. Chat Manager determines sufficient data is collected
2. Award Engine processes data and generates recommendation
3. Explanation Module creates justification
4. Results are sent to frontend
5. Frontend displays recommendation and explanation

### Session Management Flow
1. User session is created on first visit
2. Session data is updated throughout interaction
3. Session can be saved for later resumption
4. Session data is stored server-side with client reference

## Technical Considerations

### Scalability
- Stateless design where possible
- Session data stored efficiently
- Minimal dependencies on external services

### Security
- No authentication required (per requirements)
- No PII stored permanently
- CSRF protection for API endpoints

### Browser Compatibility
- Support for modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design for mobile and desktop
- Graceful degradation for older browsers

## Implementation Plan

### Phase 1: Basic Structure
- Set up Flask application structure
- Create basic frontend templates
- Implement session management

### Phase 2: Core Functionality
- Implement chat interface
- Integrate OpenAI API
- Develop award recommendation logic

### Phase 3: Enhanced Features
- Add explanation module
- Implement export functionality
- Add session saving/resuming

### Phase 4: Testing and Deployment
- Test with sample scenarios
- Validate against award manuals
- Deploy to production environment

## Deployment Strategy

### Environment Setup
- Python 3.9+ runtime
- Required Python packages:
  - Flask
  - Flask-Session
  - OpenAI
  - Gunicorn (for production)

### Deployment Process
1. Prepare application for deployment
2. Set up environment variables for API keys
3. Deploy to cloud platform
4. Verify functionality
5. Monitor for issues

### Maintenance Plan
- Regular checks of OpenAI API compatibility
- Updates to award criteria as manuals change
- Performance monitoring and optimization

## Next Steps
1. Set up development environment
2. Create basic Flask application structure
3. Implement frontend templates
4. Begin core functionality development
