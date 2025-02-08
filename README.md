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

### Configuration

1. Create `.env` file in project root with your API key:
   ```ini
   DEEPSEEK_API_KEY=your_api_key_here

   
Prepare q.csv with questions in first column:

question,status
"What is the capital of France?",
"Explain the theory of relativity?",
"How does photosynthesis work?",ERROR


🧠 Usage
bash
python dset_generator.py

Copy
| question                | status |
|-------------------------|--------|
| How do black holes form?|        |
| What is CRISPR?         | ERROR  |  ← Bookmark
Output Directory (dset_generator/)

File structure
project-root/
├── dset_generator/    # Auto-created output folder
│   ├── output.csv     # Main dataset (UTC timestamps)
│   ├── output.json    # Machine-readable JSON lines
│   └── output.txt     # Human-friendly transcript
├── q.csv              # Input questions with status tracking
└── .env               # API credentials


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

Temporary API Outage

text
Copy
[14:30:45] Processing question 15/100: What is... 
Error: API connection failed
Retrying in 1 minutes...
[14:31:45] Retry attempt 1/3...
Successfully processed question 15/100

Persistent Failure

text
Copy
[15:00:00] Processing question 42/100: How... 
Error: API unavailable
Retrying in 4 minutes...
[15:04:00] Final retry failed!
Updating q.csv bookmark at row 44
Execution paused. Resume with same command later.


Output smaples

CSV Format

csv
Copy
timestamp,question,thoughts,final_answer
2024-03-15 14:30:45,"What is...","The capital...","Paris"

Json lines

{
  "metadata": {
    "timestamp": "2024-03-15 14:30:45",
    "question": "What is..."
  },
  "response": {
    "reasoning": "The capital...",
    "answer": "Paris"
  }
}

Important Notes
Maintain question CSV encoding as UTF-8

API costs accrue on each attempt - monitor usage

Never modify q.csv while script is running

Bookmarked questions retain previous columns

Output files append data - delete old files for fresh runs

📜 License
MIT License - Free for academic/commercial use with attribution

Note: Monitor API usage carefully - failed retries may still incur charges
