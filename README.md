
# TalentScout - AI-Powered Hiring Assistant Chatbot

## Project Overview

TalentScout is an intelligent hiring assistant chatbot developed for a fictional recruitment agency specializing in technology placements. This project serves as a demonstration of using Large Language Models (LLMs) to automate the initial screening process for job candidates. The chatbot interacts with candidates to gather essential information and assesses their technical proficiency by asking relevant questions based on their declared tech stack.

The application is built in Python using the Streamlit framework for the user interface and integrates with **Google's Gemini Pro model** to power the conversation and question generation.

### Key Capabilities:
- **Greets Candidates**: Initiates the conversation with a warm welcome.
- **Gathers Information**: Collects essential details like name, email, experience, and desired position.
- **Tech Stack Declaration**: Prompts candidates to specify their technical skills.
- **Dynamic Question Generation**: Uses an LLM to generate 3-5 technical questions tailored to the candidate's tech stack.
- **Context Handling**: Maintains a coherent conversational flow throughout the interaction.
- **Data Storage**: Saves the conversation and candidate details into a CSV file for recruiter review.

---

## Technical Details

*   **Programming Language**: Python 3.9+
*   **Frontend UI**: Streamlit
*   **Large Language Model**: Google Gemini Pro
*   **Core Libraries**:
    *   `streamlit`: For building the interactive web application.
    *   `google-generativeai`: The official Python client for the Google Gemini API.
    *   `pandas`: For data manipulation and saving information to a CSV file.
    *   `python-dotenv`: To manage environment variables securely.

---

## Installation and Setup

Follow these steps to set up and run the application locally.

### Prerequisites
- Python 3.9 or higher installed on your system.
- An API key from **Google AI Studio**.

### 1. Clone the Repository
Clone this project to your local machine:
```bash
git clone <your-repository-link>
cd <repository-directory>
```

### 2. Create a Virtual Environment
It's a best practice to use a virtual environment to manage project dependencies.
```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all the required Python libraries using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory of the project. Add your Google API key to this file. You can obtain a key from [Google AI Studio](https://aistudio.google.com/app/apikey).
```
GOOGLE_API_KEY="your_google_api_key_here"
```
**Note:** Never commit your `.env` file or expose your API key in public repositories.

---

## Usage Guide

To run the application, execute the following command in your terminal from the project's root directory:

```bash
streamlit run app.py
```

Your web browser should automatically open a new tab with the chatbot interface. If it doesn't, the terminal will provide a local URL (usually `http://localhost:8501`) that you can navigate to.

Interact with the chatbot by typing your responses in the input box at the bottom of the screen. Once the conversation is complete, a download button will appear in the sidebar, allowing you to save the collected data as a CSV file.

---

## Challenges and Solutions

### Challenge 1: Maintaining Conversation Context
Maintaining the flow of a multi-turn conversation can be complex. The chatbot needs to remember what has been said to ask the right follow-up questions.

**Solution**: This was addressed by implementing a simple state machine using `streamlit.session_state`. A `stage` variable tracks the current point in the conversation (e.g., `greeting`, `gather_name`, `technical_questions`). The application logic checks the current stage to determine what question to ask next and how to process the user's input. The entire chat history is also stored in `st.session_state.chat_history` to be displayed in the UI.

### Challenge 2: Handling API and Key Errors
An invalid or missing API key would cause the application to crash. The connection to the LLM could also fail for other reasons.

**Solution**: The application now includes robust error handling. It checks for the `GOOGLE_API_KEY` upon startup and displays a clear error message if it's not found, preventing a crash. The `get_llm_response` function is wrapped in a `try...except` block to catch any communication errors with the Gemini API and return a user-friendly message without interrupting the entire application flow.

### Challenge 3: Ensuring Relevant Technical Questions
The quality and relevance of the technical questions are paramount. The LLM could potentially generate overly simple, complex, or irrelevant questions.

**Solution**: The prompt was carefully engineered to be specific. By including phrases like "concise technical interview question" and specifying the exact technology (e.g., "Python," "Django"), we guide the Gemini model to produce appropriate outputs. The application also iterates through the provided tech stack, asking one question per technology, which diversifies the assessment.
