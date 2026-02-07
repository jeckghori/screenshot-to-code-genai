# Screenshot to Code

A Streamlit application that converts screenshots into code using AI models (OpenAI GPT-4o, Anthropic Claude 3.5, or Google Gemini).

## Prerequisites

- Python 3.8 or higher
- API keys for at least one of the following:
  - OpenAI API key (for GPT-4o)
  - Anthropic API key (for Claude 3.5)
  - Google Gemini API key (for Gemini 1.5 Pro)

## Setup Instructions

### 1. Navigate to the project directory

```bash
cd "/Users/jenilghori/screenshot to code"
```

### 2. Activate the virtual environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit
- openai
- anthropic
- google-generativeai
- python-dotenv

### 4. Run the application

```bash
streamlit run app.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`

## Usage

1. **Select AI Provider**: In the sidebar, choose one of:
   - OpenAI (GPT-4o)
   - Anthropic (Claude 3.5)
   - Google (Gemini)

2. **Enter API Key**: Enter your API key for the selected provider

3. **Select Stack**: Choose your preferred code stack:
   - html_tailwind
   - react_tailwind
   - bootstrap
   - html_css
   - ionic_tailwind
   - vue_tailwind
   - svg

4. **Upload Screenshot**: Upload a PNG, JPG, or JPEG image

5. **Generate Code**: Click the "Generate Code" button

6. **View Results**: The generated code will appear on the right side with a live preview

## Troubleshooting

### If you get "File does not exist: app.py"
Make sure you're in the project root directory:
```bash
cd "/Users/jenilghori/screenshot to code"
streamlit run app.py
```

### If dependencies are missing
Activate your virtual environment and install requirements:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### If the app doesn't start
Check if Streamlit is installed:
```bash
pip install streamlit
```

## Project Structure

```
screenshot to code/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── backend/
│   ├── config.py         # Configuration settings
│   ├── llm.py            # LLM model definitions
│   ├── prompts/          # Prompt templates
│   └── codegen/          # Code generation utilities
└── README.md             # This file
```

