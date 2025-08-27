import streamlit as st
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

try:
 
    api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    if not api_key:
        st.error("Google API Key not found. Please set it in your Streamlit secrets or a local .env file.")
        st.stop()
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API Key configuration error: {e}")
    st.stop()

# --- 3. Core Functions ---

def get_llm_response(prompt):
    """
    Sends a prompt to the Google Gemini model and returns the text response.
    Includes error handling for API calls and content generation issues.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        # Handle cases where the model's response might be blocked or empty
        if response.text:
            return response.text.strip()
        else:
            return "I'm sorry, I couldn't generate a question for that topic. Let's move to the next one."
    except Exception as e:
        # Provide a user-friendly error message
        st.error(f"An error occurred while connecting to the AI model: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now. Please check the API key and configuration."

def initialize_session_state():
    """
    Sets up the initial session state variables if they don't already exist.
    This is crucial for maintaining the conversation's state across user interactions.
    """
    # 'stage' tracks the current point in the conversation (e.g., greeting, gathering name).
    if 'stage' not in st.session_state:
        st.session_state.stage = 'greeting'

    # 'chat_history' stores the entire conversation log.
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": "Welcome to TalentScout! I'm your intelligent hiring assistant. To start, I'll ask a few questions to get to know you. You can type 'exit' at any time to end our conversation."
        }]

    # 'candidate_info' is a dictionary to store all collected data.
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}

def save_to_csv():
    """
    Converts the collected candidate information into a CSV format for download.
    Returns the data as a UTF-8 encoded string.
    """
    if st.session_state.candidate_info:
        # Create a deep copy to avoid modifying the session state directly
        display_info = st.session_state.candidate_info.copy()
        # For readability, join the chat history into a single string for the CSV.
        display_info['chat_history'] = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history])
        df = pd.DataFrame([display_info])
        return df.to_csv(index=False).encode('utf-8')
    return b"" # Return empty bytes if there's no data

# --- 4. Main Conversation Handler ---

def handle_user_input(user_input):
    """
    The main logic for the chatbot. It directs the conversation based on the current 'stage'.
    """
    # Append the user's message to the chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    stage = st.session_state.stage
    response = ""

    # This state machine controls the flow of the conversation
    if stage == 'greeting':
        st.session_state.stage = 'gather_name'
        response = "To begin, could you please tell me your full name?"

    elif stage == 'gather_name':
        st.session_state.candidate_info['Full Name'] = user_input
        st.session_state.stage = 'gather_email'
        response = f"Thank you, {user_input.split()[0]}. What is your email address?"

    elif stage == 'gather_email':
        st.session_state.candidate_info['Email Address'] = user_input
        st.session_state.stage = 'gather_experience'
        response = "Perfect. And how many years of professional experience do you have?"

    elif stage == 'gather_experience':
        st.session_state.candidate_info['Years of Experience'] = user_input
        st.session_state.stage = 'gather_position'
        response = "Great. What specific position or type of role are you looking for?"

    elif stage == 'gather_position':
        st.session_state.candidate_info['Desired Position(s)'] = user_input
        st.session_state.stage = 'gather_tech_stack'
        response = "Understood. Please list the programming languages, frameworks, and tools in your primary tech stack. (e.g., Python, Django, React, Docker)"

    elif stage == 'gather_tech_stack':
        st.session_state.candidate_info['Tech Stack'] = user_input
        st.session_state.tech_stack = [tech.strip() for tech in user_input.split(',') if tech.strip()]
        st.session_state.questions_asked = 0
        st.session_state.stage = 'technical_questions'
        response = "Thanks for sharing your tech stack. I will now ask a few technical questions based on what you've listed."
        # If the tech stack isn't empty, generate the first question
        if st.session_state.tech_stack:
            first_tech = st.session_state.tech_stack[0]
            prompt = f"Generate one concise technical interview question for a candidate proficient in {first_tech}."
            tech_question = get_llm_response(prompt)
            response += f"\n\nLet's start with {first_tech}: {tech_question}"
            st.session_state.candidate_info[f"Question 1 ({first_tech})"] = tech_question
        else:
            # If no tech stack is provided, skip to the conclusion.
            st.session_state.stage = 'conclusion'
            response += "\n\nIt seems no tech stack was provided. We'll proceed with the information we have."

    elif stage == 'technical_questions':
        # Record the answer to the previous question
        q_num = st.session_state.questions_asked
        tech = st.session_state.tech_stack[q_num]
        st.session_state.candidate_info[f"Answer {q_num + 1} ({tech})"] = user_input
        st.session_state.questions_asked += 1
        
        # Ask the next question if there are more technologies, up to a limit of 4
        if st.session_state.questions_asked < len(st.session_state.tech_stack) and st.session_state.questions_asked < 4:
            next_tech = st.session_state.tech_stack[st.session_state.questions_asked]
            prompt = f"Generate a concise technical interview question about {next_tech}."
            tech_question = get_llm_response(prompt)
            response = f"Great, thank you. Now for {next_tech}: {tech_question}"
            st.session_state.candidate_info[f"Question {st.session_state.questions_asked + 1} ({next_tech})"] = tech_question
        else:
            # If all questions have been asked, move to the conclusion
            st.session_state.stage = 'conclusion'
            response = "Thank you for your answers. That's all the technical questions for now."

    # If the conversation has reached the conclusion stage, generate the final message
    if st.session_state.stage == 'conclusion' and 'Application Date' not in st.session_state.candidate_info:
        st.session_state.candidate_info['Application Date'] = datetime.date.today().isoformat()
        response = "Thank you for your time and for completing this initial screening. Your information has been recorded. Our recruitment team will review your profile and get in touch if your skills are a match. Have a great day!"
        st.session_state.stage = 'finished'

    # Add the assistant's response to the chat history
    if response:
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- 5. Streamlit User Interface ---

# Page configuration
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")

# Header
st.title("PG-AGI TalentScout Chatbot 🤖")
st.markdown("Welcome! This is an intelligent hiring assistant for initial candidate screenings.")

# Initialize the session state on the first run
initialize_session_state()

# Sidebar for downloading candidate data
st.sidebar.title("Candidate Data")
st.sidebar.markdown("Once the interview is complete, you can download the collected data as a CSV file.")
csv_data = save_to_csv()
if csv_data:
    st.sidebar.download_button(
        label="Download Interview Data",
        data=csv_data,
        file_name=f"candidate_{st.session_state.candidate_info.get('Full Name', 'export').replace(' ', '_')}.csv",
        mime='text/csv',
    )
else:
    st.sidebar.info("Candidate data will be available for download here upon completion.")

# Display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input at the bottom of the page
if st.session_state.stage != 'finished':
    user_prompt = st.chat_input("Your response...")
    if user_prompt:
        # Allow user to exit the conversation
        if user_prompt.lower().strip() in ['exit', 'quit', 'goodbye']:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": "Thank you for your time. The conversation has now ended."})
            st.session_state.stage = 'finished'
            st.rerun()
        else:
            handle_user_input(user_prompt)
            st.rerun()
else:
    st.success("The conversation has concluded. Thank you for using TalentScout!")
    st.balloons()
