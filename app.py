import streamlit as st
import openai
import pandas as pd
from dotenv import load_dotenv
import os
import datetime

# --- Environment and API Key Setup ---
# It is recommended to use environment variables for API keys for security.
# Create a .env file in your project directory and add your OpenAI API key:
# OPENAI_API_KEY="your_actual_api_key_here"
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_response(prompt, model="gpt-3.5-turbo"):
    """
    Sends a prompt to the OpenAI API and retrieves the model's response.
    """
    try:
        response = openai.chat.completions.create( # Updated OpenAI SDK call
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error communicating with the language model: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now."

def initialize_session_state():
    """
    Initializes the session state variables required for the chatbot's operation.
    """
    if 'stage' not in st.session_state:
        st.session_state.stage = 'greeting'
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Welcome to TalentScout! I'm your intelligent hiring assistant. I'll start by asking a few questions to get to know you better. To end our conversation at any time, just type 'exit'."}]
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}
    if 'questions_asked' not in st.session_state:
        st.session_state.questions_asked = 0
    if 'tech_stack' not in st.session_state:
        st.session_state.tech_stack = []

def save_to_csv():
    """
    Saves the collected candidate information to a pandas DataFrame and returns it as a CSV string.
    """
    if st.session_state.candidate_info:
        # Flatten the chat history for CSV readability
        st.session_state.candidate_info['chat_history'] = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history])
        df = pd.DataFrame([st.session_state.candidate_info])
        return df.to_csv(index=False).encode('utf-8')
    return b"" # Return empty bytes if no data

def handle_user_input(user_input):
    """
    Manages the conversation flow based on the current stage and user input.
    """
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = "" # Initialize response
    # --- Conversation Stages ---
    if st.session_state.stage == 'greeting':
        st.session_state.stage = 'gather_name'
        response = "To begin, could you please tell me your full name?"

    elif st.session_state.stage == 'gather_name':
        st.session_state.candidate_info['Full Name'] = user_input
        st.session_state.stage = 'gather_email'
        response = f"Thank you, {user_input.split()[0]}. What is your email address?"

    elif st.session_state.stage == 'gather_email':
        st.session_state.candidate_info['Email Address'] = user_input
        st.session_state.stage = 'gather_experience'
        response = "Great. How many years of professional experience do you have?"

    elif st.session_state.stage == 'gather_experience':
        st.session_state.candidate_info['Years of Experience'] = user_input
        st.session_state.stage = 'gather_position'
        response = "What specific position or type of role are you looking for?"

    elif st.session_state.stage == 'gather_position':
        st.session_state.candidate_info['Desired Position(s)'] = user_input
        st.session_state.stage = 'gather_tech_stack'
        response = "Understood. Please list the programming languages, frameworks, and tools that make up your primary tech stack. (e.g., Python, Django, Docker)"

    elif st.session_state.stage == 'gather_tech_stack':
        st.session_state.candidate_info['Tech Stack'] = user_input
        st.session_state.tech_stack = [tech.strip() for tech in user_input.split(',')]
        st.session_state.stage = 'technical_questions'
        st.session_state.questions_asked = 0
        response = "Thanks for sharing your tech stack. I will now ask you a few technical questions based on what you've listed."
        # Generate and ask the first question
        if st.session_state.tech_stack:
            prompt = f"Generate one concise technical interview question for a candidate proficient in {st.session_state.tech_stack[0]}."
            tech_question = get_llm_response(prompt)
            response += f"\n\nLet's start with {st.session_state.tech_stack[0]}: {tech_question}"
            st.session_state.candidate_info[f"Question 1 ({st.session_state.tech_stack[0]})"] = tech_question
        else:
            st.session_state.stage = 'conclusion' # Skip to conclusion if no tech stack provided
            response = "It seems you haven't listed a tech stack. We will proceed with the information we have."


    elif st.session_state.stage == 'technical_questions':
        current_tech_index = st.session_state.questions_asked
        current_tech = st.session_state.tech_stack[current_tech_index]
        st.session_state.candidate_info[f"Answer {st.session_state.questions_asked + 1} ({current_tech})"] = user_input
        st.session_state.questions_asked += 1

        if st.session_state.questions_asked < len(st.session_state.tech_stack) and st.session_state.questions_asked < 4: # Limit to 4 questions max
            next_tech = st.session_state.tech_stack[st.session_state.questions_asked]
            prompt = f"Generate a concise technical interview question about {next_tech}."
            tech_question = get_llm_response(prompt)
            response = f"Great, thank you. Now for {next_tech}: {tech_question}"
            st.session_state.candidate_info[f"Question {st.session_state.questions_asked + 1} ({next_tech})"] = tech_question
        else:
            st.session_state.stage = 'conclusion'
            response = "Thank you for your answers. That's all the technical questions for now."

    if st.session_state.stage == 'conclusion' and not response: # Ensure conclusion message is set once
        st.session_state.candidate_info['Application Date'] = datetime.date.today().isoformat()
        response = "Thank you for your time and for completing the initial screening. Your information has been recorded. Our recruitment team will review your profile and get in touch if your skills and experience are a match for any open roles. Have a great day!"
        st.session_state.stage = 'finished'

    # --- Append assistant response to chat history ---
    if response:
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")

# --- Main Application UI ---
st.title("PG-AGI TalentScout Chatbot 🤖")
st.markdown("This is an intelligent hiring assistant designed to conduct initial candidate screenings.")

# Initialize session state
initialize_session_state()

# --- Sidebar for Data Download ---
st.sidebar.title("Candidate Data")
st.sidebar.markdown("Once the interview is complete, you can download the collected data.")
csv_data = save_to_csv()
if csv_data:
    st.sidebar.download_button(
        label="Download Interview Data (CSV)",
        data=csv_data,
        file_name=f"candidate_data_{st.session_state.candidate_info.get('Full Name', 'export').replace(' ', '_')}.csv",
        mime='text/csv',
    )
else:
    st.sidebar.info("No candidate data to download yet.")


# --- Chat Interface ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input Handling ---
if st.session_state.stage != 'finished':
    prompt = st.chat_input("Your response...")
    if prompt:
        if prompt.lower().strip() in ['exit', 'quit', 'goodbye']:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": "Thank you for your time. The conversation has now ended. Have a great day!"})
            st.session_state.stage = 'finished'
            st.rerun() # <<< CORRECTED LINE
        else:
            handle_user_input(prompt)
            st.rerun() # <<< CORRECTED LINE
else:
    st.success("The conversation has concluded. Thank you for using TalentScout!")
