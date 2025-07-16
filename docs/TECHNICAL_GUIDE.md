# Coast Guard Award Generator - Technical Documentation

## Architecture Overview

The Coast Guard Award Generator is a Flask-based web application with the following architecture:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Flask Backend  │────▶│   OpenAI API    │
│  (HTML/JS/CSS)  │     │   (Python)       │     │   (GPT-4)       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Award Engine    │
                        │  (Scoring Logic) │
                        └──────────────────┘
```

## Project Structure

```
Award Generator/
├── src/
│   ├── app.py                 # Main Flask application
│   ├── openai_client.py       # OpenAI API client with retry logic
│   ├── config.py              # Configuration management
│   ├── validation.py          # Input validation schemas
│   ├── award_engine/          # Award scoring module
│   │   ├── __init__.py
│   │   ├── base.py           # Main AwardEngine class
│   │   ├── scorers.py        # Scoring methods
│   │   ├── criteria.py       # Award criteria definitions
│   │   ├── keywords.py       # Keyword definitions
│   │   ├── utils.py          # Utility functions
│   │   └── exceptions.py     # Custom exceptions
│   ├── static/               # Frontend assets
│   │   ├── css/             # Stylesheets
│   │   ├── js/              # JavaScript files
│   │   └── img/             # Images
│   └── templates/           # HTML templates
├── docs/                    # Documentation
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration template
└── Procfile               # Deployment configuration
```

## Key Components

### 1. Award Engine (`src/award_engine/`)
The award scoring system evaluates achievements across multiple criteria:

- **Leadership**: Team size, management responsibilities, command roles
- **Impact**: Quantifiable results, operational improvements, lives saved
- **Innovation**: New processes, creative solutions, first-time achievements
- **Scope**: Individual, unit, district, national, or international reach
- **Challenges**: Obstacles overcome, resource constraints, complexity
- **Quantifiable Results**: Specific metrics, percentages, dollar amounts
- **Valor**: Life-saving actions, dangerous conditions, heroic acts
- **Collaboration**: Inter-agency work, partnerships, joint operations
- **Training Provided**: Knowledge transfer, mentoring, instruction
- **Above & Beyond**: Voluntary overtime, exceptional effort
- **Emergency Response**: Crisis management, urgent missions

### 2. OpenAI Client (`src/openai_client.py`)
Handles all AI interactions with:
- Retry logic for rate limits
- Comprehensive error handling
- Structured data extraction
- Citation generation

### 3. Validation (`src/validation.py`)
Input validation for:
- Awardee information
- Achievement data
- Message content
- Export requests
- Session data

### 4. Configuration (`src/config.py`)
Centralized configuration management:
- Environment-based settings
- Security configurations
- Logging setup
- API credentials

## API Endpoints

### Core Endpoints

#### POST `/api/chat`
Handles chat messages and stores conversation history.
```json
Request: {
    "message": "Led team of 25 personnel..."
}
Response: {
    "success": true,
    "response": "AI response text",
    "message_count": 5
}
```

#### POST `/api/recommend`
Generates award recommendation based on achievements.
```json
Request: {
    "awardee_info": {
        "name": "John Doe",
        "rank": "LCDR",
        "unit": "Sector Boston"
    }
}
Response: {
    "success": true,
    "award": "Coast Guard Commendation Medal",
    "explanation": "HTML formatted explanation",
    "scores": {...},
    "suggestions": [...]
}
```

#### POST `/api/finalize`
Generates formal award citation.
```json
Request: {
    "award": "Coast Guard Commendation Medal"
}
Response: {
    "success": true,
    "award": "Coast Guard Commendation Medal",
    "citation": "Formal citation text..."
}
```

#### POST `/api/export`
Exports award package in various formats.
```json
Request: {
    "format": "docx",
    "awardee_info": {...}
}
Response: {
    "success": true,
    "filename": "award_package_20240115_143022.docx",
    "download_url": "/api/export/download/docx"
}
```

### Session Management

#### POST `/api/session/clear`
Clears current session data.

#### GET `/api/session`
Retrieves current session data.

#### POST `/api/session`
Saves session data.

## Scoring Algorithm

The award recommendation system uses a weighted scoring algorithm:

1. **Individual Criteria Scoring** (0-5 scale)
   - Each criterion is scored based on keywords, counts, and patterns
   - Multiple scoring methods for comprehensive evaluation

2. **Weighted Aggregation**
   ```python
   weights = {
       "impact": 5,
       "scope": 5,
       "leadership": 5,
       "above_beyond": 4,
       "innovation": 4,
       "quantifiable_results": 4,
       "challenges": 3,
       "valor": 5,
       "collaboration": 4,
       "training_provided": 3,
       "emergency_response": 3
   }
   ```

3. **Dynamic Scoring**
   - Zero scores are excluded from calculation
   - Prevents irrelevant criteria from lowering total

4. **Award Matching**
   - Total score compared against thresholds
   - Minimum requirements checked for each award
   - "Big Three" criteria (leadership, impact, scope) must meet minimums

## Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run application
python src/app.py
```

### Production Deployment

#### Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway login
railway init
railway up
```

#### Heroku
```bash
# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here

# Deploy
git push heroku main
```

#### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:5000"]
```

## Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `FLASK_ENV`: development/production
- `SECRET_KEY`: Flask secret key
- `LOG_LEVEL`: DEBUG/INFO/WARNING/ERROR
- `OPENAI_MODEL`: GPT model to use
- `SESSION_LIFETIME`: Session duration in seconds

## Security Considerations

1. **API Key Management**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **Input Validation**
   - All user inputs are validated
   - SQL injection prevention (no direct DB queries)
   - XSS protection through proper escaping

3. **Session Security**
   - Secure session cookies in production
   - Session timeout configuration
   - HTTPS enforcement recommended

4. **Error Handling**
   - No sensitive information in error messages
   - Comprehensive logging for debugging
   - Graceful degradation on API failures

## Monitoring and Logging

Logs are written to:
- Console (stdout)
- File: `logs/app.log`

Log levels:
- DEBUG: Detailed information for debugging
- INFO: General operational information
- WARNING: Warning messages
- ERROR: Error messages with stack traces

## Performance Optimization

1. **Caching Considerations**
   - Session-based caching of analysis results
   - Potential for Redis integration

2. **API Rate Limiting**
   - Exponential backoff for OpenAI API
   - Maximum retry configuration

3. **Frontend Optimization**
   - Debounced API calls
   - Loading states for better UX
   - Efficient DOM updates

## Extending the Application

### Adding New Award Criteria
1. Update `src/award_engine/criteria.py`
2. Add scoring method in `src/award_engine/scorers.py`
3. Update weights in configuration

### Adding New Export Formats
1. Create export method in `src/app.py`
2. Update validation in `src/validation.py`
3. Add frontend option

### Integrating with External Systems
1. Add API client in new module
2. Update validation schemas
3. Add error handling
4. Update documentation

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Check API key validity
   - Verify API credits
   - Check rate limits

2. **Session Issues**
   - Clear browser cookies
   - Check session configuration
   - Verify filesystem permissions

3. **Export Failures**
   - Check python-docx installation
   - Verify temp directory permissions
   - Check file size limits

### Debug Mode
Enable debug mode for detailed error information:
```bash
export FLASK_DEBUG=True
python src/app.py
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

## License

This project is licensed under the terms specified in the LICENSE file.