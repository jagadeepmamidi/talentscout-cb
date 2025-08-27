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
