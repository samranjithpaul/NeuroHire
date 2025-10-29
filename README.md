# NeuroHire – AI Resume Screening Platform

NeuroHire is an AI-powered recruitment assistant that automatically analyzes resumes, extracts key skills, and evaluates candidate suitability for a given job description.  
It uses local large language models (via Ollama) instead of external APIs — meaning it's private, fast, and doesn't rely on paid OpenAI keys.

## Features

- Upload one or multiple resumes (PDF)
- Analyze resumes using local AI (LLaMA 3.1 through Ollama)
- Detect relevant skills and job fit automatically
- Export results as CSV (with suitability labels)
- Web-based interface built with Flask

## Tech Stack

| Layer | Tools |
|-------|-------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| AI/ML | Ollama (LLaMA 3.1), NLP |
| Data Handling | pdfplumber, CSV |
| Deployment | Localhost / ngrok / Docker |

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/NeuroHire.git
cd NeuroHire
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Install Ollama
```bash
# macOS
brew install --cask ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# Download model
ollama pull llama3.1
```

4. Run the app
```bash
python app.py
```
Access at `http://localhost:5000`

## Project Structure
```
NeuroHire/
├── app.py               # Main Flask backend
├── templates/          
│   └── upload.html      # Frontend UI
├── static/              # CSS, JS, assets
├── requirements.txt     # Python dependencies
├── results.csv          # Generated output
└── README.md           
```

## Usage
1. Upload resumes (PDF format)
2. Enter job description and requirements
3. System analyzes and categorizes as:
    - Suitable
    - Maybe Suitable
    - Not Suitable
4. Export results to CSV

## Roadmap
- React frontend with animations
- Custom scoring system
- Authentication system
- Docker deployment

## Author
Sam Ranjith Paul

## License
MIT License
