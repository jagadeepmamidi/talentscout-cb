# TalentScout - AI-Powered Hiring Assistant Chatbot

## Project Overview

TalentScout is an intelligent hiring assistant chatbot developed for a fictional recruitment agency specializing in technology placements. This project serves as a demonstration of using Large Language Models (LLMs) to automate the initial screening process for job candidates. The chatbot interacts with candidates to gather essential information and assesses their technical proficiency by asking relevant questions based on their declared tech stack.

The application is built in Python using the Streamlit framework for the user interface and integrates with OpenAI's GPT models to power the conversation and question generation.

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
*   **Large Language Model**: OpenAI GPT-3.5-Turbo (or GPT-4)
*   **Core Libraries**:
    *   `streamlit`: For building the interactive web application.
    *   `openai`: The official Python client for the OpenAI API.
    *   `pandas`: For data manipulation and saving information to a CSV file.
    *   `python-dotenv`: To manage environment variables securely.

---

## Installation and Setup

Follow these steps to set up and run the application locally.

### Prerequisites
- Python 3.9 or higher installed on your system.
- An API key from OpenAI.

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
Create a file named `.env` in the root directory of the project. Add your OpenAI API key to this file.
```
OPENAI_API_KEY="your_openai_api_key_here"
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

## Prompt Design

Effective prompt engineering is crucial for guiding the LLM to perform its tasks accurately. The core logic for this is within the `get_llm_response` and `handle_user_input` functions in `app.py`.

**1. Information Gathering**: The conversation flow is managed by a state machine (`st.session_state.stage`). The prompts are simple, direct questions designed to elicit specific pieces of information (e.g., "What is your full name?").

**2. Technical Question Generation**: To generate relevant technical questions, a dynamic prompt is crafted and sent to the LLM. The prompt explicitly asks the model to generate a question for a specific technology from the candidate's declared stack. For example:
```python
prompt = f"Generate one concise technical interview question for a candidate proficient in {technology_name}."
```
This approach ensures that the questions are directly related to the candidate's skills. The prompt is designed to be "concise" to keep the questions focused and suitable for a chat-based screening.

---

## Challenges and Solutions

### Challenge 1: Maintaining Conversation Context
Maintaining the flow of a multi-turn conversation can be complex. The chatbot needs to remember what has been said to ask the right follow-up questions.

**Solution**: This was addressed by implementing a simple state machine using `streamlit.session_state`. A `stage` variable tracks the current point in the conversation (e.g., `greeting`, `gather_name`, `technical_questions`). The application logic checks the current stage to determine what question to ask next and how to process the user's input. The entire chat history is also stored in `st.session_state.chat_history` to be displayed in the UI.

### Challenge 2: Handling Sensitive Information
Collecting personal data like names and email addresses requires careful handling to comply with privacy best practices.

**Solution**: For this demo, the data is stored in session and then made available for download as a CSV file, which simulates passing the information to a secure backend system. The use of the `python-dotenv` library ensures that the OpenAI API key is not hardcoded into the source code, which is a critical security measure. In a production environment, this data would be sent over HTTPS to a secure database with encryption and access controls, adhering to standards like GDPR.

### Challenge 3: Ensuring Relevant Technical Questions
The quality and relevance of the technical questions are paramount. The LLM could potentially generate overly simple, complex, or irrelevant questions.

**Solution**: The prompt was carefully engineered to be specific. By including phrases like "concise technical interview question" and specifying the exact technology (e.g., "Python," "Django"), we guide the model to produce appropriate outputs. The temperature parameter in the API call is set to `0.5` to encourage factual and focused responses rather than highly creative ones. The application also iterates through the provided tech stack, asking one question per technology, which diversifies the assessment.
