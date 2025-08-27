```
# TalentScout - Intelligent Hiring Assistant

## Project Overview
The TalentScout Hiring Assistant is an intelligent chatbot designed to streamline the initial candidate screening process for a fictional recruitment agency specializing in technology placements. Developed using Python and Streamlit, this chatbot interacts with candidates to gather essential information (name, contact details, experience, etc.) and poses relevant technical questions based on their self-declared tech stack. This project demonstrates core concepts in conversational AI, prompt engineering, and user interface development.

## Installation Instructions
To set up and run the application locally, please follow these steps.

**Prerequisites:**
*   Python 3.8 or higher
*   pip (Python package installer)

**Steps:**
1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install the required Python libraries using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    Start the Streamlit server.
    ```bash
    streamlit run app.py
    ```
    The application will open in a new tab in your default web browser.

## Usage Guide
Upon launching the application, you will be greeted by the chatbot.
1.  The chatbot will sequentially ask for the following information:
    *   Full Name
    *   Email Address
    *   Phone Number
    *   Years of Experience
    *   Desired Position
    *   Current Location
    *   Tech Stack
2.  Provide your answers in the input box at the bottom of the screen and press Enter.
3.  Based on your declared tech stack, the chatbot will generate a set of 3-5 technical questions.
4.  After presenting the questions, the chatbot will conclude the conversation.
5.  You can type `exit`, `bye`, or `quit` at any point to gracefully end the conversation.

## Technical Details
*   **Programming Language:** Python
*   **Frontend Interface:** Streamlit
*   **Large Language Models (LLM):** The application is designed to be model-agnostic. The core logic is built around a function `call_llm_mock()` which **simulates** the behavior of a powerful LLM like GPT-4 or Llama. This approach focuses on demonstrating the prompt engineering and conversation flow logic without requiring a live API key for this assignment submission. This mock function can be easily swapped with a real API call in a production environment.
*   **Architecture:** The application uses a state machine pattern to manage the conversation flow. The current state is stored in Streamlit's `session_state`, allowing the chatbot to know which piece of information to ask for next and ensuring a coherent interaction despite Streamlit's script re-run model.

## Prompt Design
Effective prompt design is crucial for guiding the LLM to produce the desired outputs.

**1. Information Gathering:**
For information gathering, the prompts are implicit in the chatbot's conversational logic. The system moves through a predefined set of states, asking a specific question at each stage (e.g., "What is your full name?").

**2. Technical Question Generation:**
The core of the prompt engineering is demonstrated in the generation of technical questions. The simulated LLM call is based on the following prompt template:

```
"You are an expert technical interviewer for 'TalentScout'. A candidate has listed the following technologies in their tech stack: {tech_stack}.
Generate a set of 3-5 technical questions tailored to assess the candidate’s proficiency in each specified technology.
Format the output clearly, grouping questions by technology.
The questions should be relevant for a candidate with {years_of_experience} years of experience applying for a {desired_position} role.
Do not ask for code implementations, just conceptual questions."
```

**Explanation of Prompt Design:**
*   **Role-Playing:** The prompt begins with "You are an expert technical interviewer..." to set the context and tone for the LLM.
*   **Context Injection:** Critical candidate details like `{tech_stack}`, `{years_of_experience}`, and `{desired_position}` are dynamically inserted. This ensures the generated questions are relevant and appropriately challenging.
*   **Clear Instructions:** The prompt gives explicit instructions on the task ("Generate a set of 3-5 technical questions"), the format ("grouping questions by technology"), and the constraints ("Do not ask for code implementations...").

## Challenges & Solutions

*   **Challenge: Maintaining Conversation State**
    *   **Problem:** Streamlit re-runs the entire script on every user interaction, making it inherently stateless.
    *   **Solution:** I utilized Streamlit's `st.session_state` object to persist the conversation history, the current conversation state (e.g., `GATHERING_NAME`), and all collected candidate information. This creates a stable and context-aware user experience.

*   **Challenge: Integrating a Live LLM without API Keys**
    *   **Problem:** Using a real LLM requires an API key, which should not be hardcoded or exposed in a public submission.
    *   **Solution:** I developed a mock function, `call_llm_mock()`, that simulates the output of a real LLM based on the prompt's intent. For technical question generation, it uses a predefined dictionary of questions for common technologies. This approach effectively demonstrates my understanding of how to structure the logic and engineer the prompts, which is the core of the assignment, while keeping the application self-contained and secure.

*   **Challenge: Handling Unexpected User Input**
    *   **Problem:** Users might provide input that doesn't directly answer the question or is irrelevant.
    *   **Solution:** The chatbot employs a strict state-based flow. It interprets any input received in a particular state as the answer to the question associated with that state. While a more advanced implementation could use an LLM for intent recognition, this direct approach serves as a robust fallback mechanism, preventing the conversation from deviating from its primary purpose of information gathering.
```
