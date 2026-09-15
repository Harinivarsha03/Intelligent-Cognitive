#  Intelligent Cognitive and Interaction Assistant System

An AI-powered intelligent assistant that understands natural language, detects user intent, uses external tools when required, maintains conversation context, and generates responses using a locally running Large Language Model.

##  Project Overview

The Intelligent Cognitive and Interaction Assistant System is designed to demonstrate an **AI Agentic Workflow**.

Instead of responding to every request in the same way, the system analyzes the user's request and decides how it should be handled.

For example:

- General questions → Llama 3.2
- Weather requests → Weather API
- Mathematical calculations → Calculator
- Follow-up questions → Conversation Memory

##  System Architecture

```text
                    👤 User
                      │
                      ▼
              🌐 Web Interface
                      │
                      ▼
               ⚡ FastAPI Backend
                      │
                      ▼
              🤖 Cognitive Agent
                      │
             ┌────────┼────────┐
             ▼        ▼        ▼
          Weather   Math    General
             │        │        │
             ▼        ▼        ▼
        Weather API Calculator Llama 3.2
             │        │        │
             └────────┼────────┘
                      ▼
              🧠 Conversation Memory
                      │
                      ▼
                💬 Final Response
**** Technologies Used**
Python	Core programming language
Llama 3.2	Local Large Language Model
Ollama	Local LLM runtime
FastAPI	Backend API
Open-Meteo	Weather data
HTML/CSS/JavaScript	Frontend
Git	Version control
GitHub	Project repository

****PROJECT STRUCTURE****
Intelligent-Cognitive-system/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── api.py
│   ├── memory.py
│   └── tools.py
│
├── frontend/
│   └── index.html
│
├── data/
│
├── tests/
│
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
└── test_llm.py

**** How to Run****
1. Clone the repository
git clone https://github.com/Harinivarsha03/Intelligent-Cognitive.git
cd Intelligent-Cognitive
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows PowerShell:
venv\Scripts\Activate.ps1
  If PowerShell blocks activation:
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
Then:
venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Install Ollama
Install Ollama and download the Llama 3.2 model:
ollama pull llama3.2
6. Start the FastAPI server
uvicorn app.api:app --reload
The application will run at:
http://127.0.0.1:8000

💬 Example Requests
General Question
What is machine learning?
The request is handled by Llama 3.2.
Weather
What is the weather in Coimbatore?
The system uses the weather API.
Calculation
Calculate 125 * 48
The system routes the request to the calculator tool.
Conversation Context
What is machine learning?
Then:
Why is it important?

**** Agentic Workflow****
User Request
     ↓
Intent Detection
     ↓
Decision Making
     ↓
Tool Selection
     ↓
Tool/API Execution
     ↓
Context + Memory
     ↓
LLM Response
     ↓
   User
**** Privacy****
The language model runs locally through Ollama.

Sensitive configuration files such as .env and the Python virtual environment are excluded from Git using .gitignore.

**** Future Improvements****
Voice interaction
Long-term memory
Multiple AI agents
More external APIs
Authentication
User-specific sessions
Database integration
Advanced tool calling
Production deployment
Mobile-friendly interface
Improved security and validation

**** Project Goal****
The goal of this project is to demonstrate how Python, LLMs, APIs, memory, and agentic workflows can be combined to create an intelligent interactive assistant.
