# dset
# AI Dataset Generator with Resilient Bookmarking

**A robust pipeline for generating structured datasets using AI (Deepseek API) with fault-tolerant processing and resume capabilities**

## 📖 Overview

This Python script automates dataset creation by processing questions through an AI API, featuring smart error recovery and multi-format output. Designed for reliability in unstable API environments, it maintains processing continuity through network interruptions and service outages.

### Key Features

🛡 **Fault-Tolerant Architecture**
- Exponential backoff retry logic (1m → 2m → 4m)
- Automatic bookmarking of failed questions
- Resume-from-error capability
- Atomic writes to prevent data corruption

📊 **Multi-Format Output**
- Simultaneous CSV/JSON/TXT generation
- Organized output directory structure
- Human-readable and machine-parsable formats
- Comprehensive metadata tracking

⚙ **Smart Processing**
- Progress tracking with question counters
- API response validation
- Environment-based configuration
- CSV header auto-detection
- Empty question filtering

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Deepseek API access
- `dotenv` for configuration

```bash
pip install python-dotenv openai
```

###Configuration
Create .env with your API key:

ini

DEEPSEEK_API_KEY=your_api_key_here
Prepare q.csv with questions in first column:

csv
Copy
question,status
"What causes aurora borealis?",
"Explain quantum entanglement?",
🧠 Usage
bash
Copy
python dset_generator.py
Input Structure (q.csv)

Copy
| question                | status |
|-------------------------|--------|
| How do black holes form?|        |
| What is CRISPR?         | ERROR  |  ← Bookmark
Output Directory (dset_generator/)

Copy
📁 dset_generator/
├── 📄 output.csv     # Structured dataset
├── 📄 output.json    # JSON Lines format
└── 📄 output.txt     # Human-readable log
🔄 Recovery Workflow
Initial Failure: Marks question with ERROR status

Auto-Retry: 3 attempts with increasing delays

Continuation:

csv
Copy
question,status
"Completed question", 
"Failed question",ERROR  # Resume point
Resume: Re-run script to continue from bookmark

📜 License
MIT License - Free for academic/commercial use with attribution

Note: Monitor API usage carefully - failed retries may still incur charges
