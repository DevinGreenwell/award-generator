# Coast Guard Award Generator - User Guide

## Overview
The Coast Guard Award Generator is an AI-powered tool that helps create award recommendations and citations based on achievements and accomplishments. It analyzes your input against Coast Guard award criteria to recommend the most appropriate award level.

## Accessing the Tool
- **Local Development**: Run `python src/app.py` and access at `http://localhost:5000`
- **Production**: Deploy to your preferred hosting service (Railway, Heroku, etc.)

## Features

### 1. Awardee Information
At the top of the page, enter:
- **Name**: Full name of the awardee
- **Rank/Rate**: Current rank or rate
- **Unit**: Current unit assignment (optional)
- **Date Range**: Period of performance

### 2. Chat Interface
The chat interface collects achievement information:
- Enter accomplishments in natural language
- Include specific details, numbers, and impacts
- The AI assistant will acknowledge your input
- Continue adding information until complete

### 3. Award Recommendation Workflow

#### Step 1: Enter Achievements
1. Fill in awardee information
2. Use the chat to describe accomplishments
3. Include:
   - Leadership roles and responsibilities
   - Quantifiable impacts (percentages, dollar amounts, etc.)
   - Scope of impact (unit/district/national level)
   - Challenges overcome
   - Innovations or process improvements

#### Step 2: Generate Recommendation
1. Click **"Generate Recommendation"**
2. The system will analyze your input and:
   - Score achievements across multiple criteria
   - Recommend an appropriate award level
   - Provide detailed justification
   - Show improvement suggestions

#### Step 3: Review and Improve (Optional)
1. Review the recommendation and suggestions
2. Click **"Improve"** to get specific enhancement ideas
3. Add more details via chat if needed
4. Click **"Refresh Recommendation"** to regenerate

#### Step 4: Finalize Award
1. Click **"Finalize Award"** to generate the formal citation
2. The system creates a properly formatted award citation
3. Ready for export or printing

### 4. Export Options
Export your award package in multiple formats:
- **Word Document (.docx)**: Professional format for official submission
- **JSON**: Complete data package for archival
- **Text**: Human-readable format

### 5. Session Management
- **Clear Session**: Reset all data and start fresh
- **Auto-save**: Your work is automatically saved during the session
- **Persistent Sessions**: Return to your work later (if configured)

## Tips for Best Results

### Include Quantifiable Impacts
- "Reduced processing time by 40%"
- "Saved $250,000 in operational costs"
- "Trained 15 personnel in new procedures"
- "Managed team of 25 members"

### Specify Scope and Duration
- "District-wide implementation"
- "National impact across all sectors"
- "Over 18-month period"
- "During 6-month deployment"

### Highlight Leadership
- Direct supervision numbers
- Decision-making authority
- Project management roles
- Mentoring and training provided

### Document Challenges
- Resource constraints overcome
- Complex problems solved
- Emergency situations handled
- Time-critical operations

## Award Levels (Lowest to Highest)
1. **Coast Guard Letter of Commendation**: Outstanding achievement at unit level
2. **Coast Guard Achievement Medal**: Sustained superior performance
3. **Coast Guard Commendation Medal**: Heroic or meritorious achievement
4. **Meritorious Service Medal**: Outstanding meritorious achievement
5. **Legion of Merit**: Exceptionally meritorious service (officers)
6. **Distinguished Service Medal**: Exceptionally meritorious service in position of great responsibility
7. **Medal of Honor**: Gallantry and intrepidity at risk of life above and beyond call of duty

## Troubleshooting

### "No achievements found" error
- Ensure you've entered accomplishments in the chat before generating
- Check that your descriptions include specific details

### Low award recommendation
- Review improvement suggestions
- Add more quantifiable impacts
- Clarify scope of responsibility
- Include leadership details

### OpenAI API errors
- Check your API key in the .env file
- Ensure you have API credits available
- Try again if rate limited

## Security Notes
- Never share your OpenAI API key
- Sessions are stored locally by default
- Sensitive information should be handled per your organization's policies

## Support
For issues or feature requests, please contact your system administrator or refer to the project documentation.