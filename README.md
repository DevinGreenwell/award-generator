# Coast Guard Award Generator

An AI-powered web application that helps generate Coast Guard award recommendations and citations based on achievements and accomplishments.

## Features

- 🎖️ **Intelligent Award Recommendation**: Analyzes achievements against Coast Guard award criteria
- 💬 **Interactive Chat Interface**: Natural language input for describing accomplishments
- 📊 **Comprehensive Scoring**: Evaluates leadership, impact, innovation, and more
- 📄 **Multiple Export Formats**: Word documents, JSON, and text formats
- 🔒 **Secure Design**: Input validation and error handling throughout
- 📈 **Detailed Analytics**: Shows scoring breakdown and improvement suggestions

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/award-generator.git
cd award-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. Run the application:
```bash
python src/app.py
```

6. Open your browser to `http://localhost:5000`

## Usage

1. **Enter Awardee Information**: Fill in name, rank, unit, and date range
2. **Describe Achievements**: Use the chat interface to enter accomplishments
3. **Generate Recommendation**: Click to analyze and receive award recommendation
4. **Review & Improve**: Review suggestions and add more details if needed
5. **Finalize Citation**: Generate the formal award citation
6. **Export**: Download in your preferred format

## Project Structure

```
Award Generator/
├── src/                    # Source code
│   ├── app.py             # Main Flask application
│   ├── award_engine/      # Award scoring logic
│   ├── static/            # Frontend assets
│   └── templates/         # HTML templates
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── .env.example          # Environment template
```

## Documentation

- [User Guide](docs/USER_GUIDE.md) - Complete usage instructions
- [Technical Guide](docs/TECHNICAL_GUIDE.md) - Architecture and development details

## Award Levels

The system can recommend the following awards (from lowest to highest):

1. Coast Guard Letter of Commendation
2. Coast Guard Achievement Medal
3. Coast Guard Commendation Medal
4. Meritorious Service Medal
5. Legion of Merit
6. Distinguished Service Medal
7. Medal of Honor

## Technologies Used

- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-4
- **Frontend**: HTML, CSS, JavaScript
- **Export**: python-docx for Word documents
- **Deployment**: Compatible with Railway, Heroku, Docker

## Security

- API keys stored in environment variables
- Input validation on all user inputs
- Error handling with no sensitive data exposure
- Session-based data storage

## Contributing

Contributions are welcome! Please read the [Technical Guide](docs/TECHNICAL_GUIDE.md) for development setup and guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions, please open an issue on GitHub or consult the documentation.