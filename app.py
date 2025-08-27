import streamlit as st
import pandas as pd
import os
import time

def save_candidate_data(candidate_info):
    """
    Saves the collected candidate information to a CSV file.
    In a real-world application, this would be a secure database call.
    """
    df = pd.DataFrame([candidate_info])
    file_path = 'candidates.csv'

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

def call_llm_mock(prompt_template, user_data):
    """
    Simulates a call to a Large Language Model for generating technical questions.
    """
    tech_stack = user_data.get("tech_stack", "general")
    experience = user_data.get("experience", "an unspecified number of")
    position = user_data.get("position", "a role")

    # Simulate a thinking process
    st.session_state.messages.append({"role": "assistant", "content": f"Understood. Generating relevant technical questions for a candidate with {experience} years of experience applying for {position} with skills in {tech_stack}. Please wait a moment..."})
    time.sleep(2)

    questions = {
        "python": [
            "1. Can you explain the difference between a list and a tuple in Python?",
            "2. What are decorators and how have you used them?",
            "3. Describe the Global Interpreter Lock (GIL) and its implications."
        ],
        "django": [
            "1. What is the Django ORM and what are its main advantages?",
            "2. Explain the MVT (Model-View-Template) architecture.",
            "3. How do you handle database migrations in a Django project?"
        ],
        "javascript": [
            "1. What is the difference between `==` and `===` in JavaScript?",
            "2. Can you explain what a closure is and provide a simple example?",
            "3. Describe event bubbling and capturing."
        ],
        "react": [
            "1. What is the Virtual DOM and how does it improve performance?",
            "2. Explain the difference between state and props in React.",
            "3. Describe the component lifecycle in a class-based component."
        ],
        "sql": [
            "1. What is the difference between an `INNER JOIN` and a `LEFT JOIN`?",
            "2. What are database indexes and why are they important?",
            "3. Explain the concept of a transaction and the ACID properties."
        ]
    }

    response = "Great, based on your tech stack, here are a few questions for you:\n\n"
    tech_stack_lower = [tech.lower() for tech in tech_stack.split(',')]
    found_questions = False
    for tech in tech_stack_lower:
        tech = tech.strip()
        if tech in questions:
            found_questions = True
            response += f"**For {tech.capitalize()}:**\n"
            response += "\n".join(questions[tech]) + "\n\n"

    if not found_questions:
         response = "Thank you for sharing your tech stack. It seems quite specialized. We will have a technical specialist review your profile and reach out with tailored questions."

    return response

def initialize_session_state():
    """Initializes the session state variables for the chatbot."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "state" not in st.session_state:
        st.session_state.state = "GREETING"
    if "candidate_info" not in st.session_state:
        st.session_state.candidate_info = {}
    if "conversation_ended" not in st.session_state:
        st.session_state.conversation_ended = False

def get_next_question(current_state):
    """Determines the next question to ask the candidate based on the conversation state."""
    question_map = {
        "GREETING": "To start, could you please provide your full name?",
        "GATHERING_NAME": "Thank you. What is your email address?",
        "GATHERING_EMAIL": "Great. What is your phone number?",
        "GATHERING_PHONE": "Thanks. How many years of professional experience do you have?",
        "GATHERING_EXPERIENCE": "Understood. What is the desired position you are applying for?",
        "GATHERING_POSITION": "What is your current location (City, Country)?",
        "GATHERING_LOCATION": "And finally, what is your tech stack? Please list the programming languages, frameworks, and tools you are proficient in (e.g., Python, Django, React, SQL)."
    }
    return question_map.get(current_state, "")

def handle_user_input(prompt):
    """Processes user input, updates state, and generates chatbot responses."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    current_state = st.session_state.state
    response = ""
    state_machine = {
        "GREETING": ("full_name", "GATHERING_NAME"),
        "GATHERING_NAME": ("email", "GATHERING_EMAIL"),
        "GATHERING_EMAIL": ("phone", "GATHERING_PHONE"),
        "GATHERING_PHONE": ("experience", "GATHERING_EXPERIENCE"),
        "GATHERING_EXPERIENCE": ("position", "GATHERING_POSITION"),
        "GATHERING_POSITION": ("location", "GATHERING_LOCATION"),
    }

    if current_state in state_machine:
        key, next_state = state_machine[current_state]
        st.session_state.candidate_info[key] = prompt
        st.session_state.state = next_state
        response = get_next_question(st.session_state.state)
        st.session_state.messages.append({"role": "assistant", "content": response})

    elif current_state == "GATHERING_LOCATION":
        st.session_state.candidate_info["tech_stack"] = prompt
        st.session_state.state = "GENERATING_QUESTIONS"
        prompt_template = "Generate technical questions based on user's tech stack."
        response = call_llm_mock(prompt_template, st.session_state.candidate_info)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.state = "CONCLUDED"

    if st.session_state.state == "CONCLUDED":
        final_message = "This concludes our initial automated screening. Thank you for your time and for answering these questions. Our recruitment team will review your profile and get back to you with the next steps. You may now close this window."
        st.session_state.messages.append({"role": "assistant", "content": final_message})
        save_candidate_data(st.session_state.candidate_info)
        st.session_state.conversation_ended = True

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="TalentScout Assistant", page_icon="🤖", layout="centered")

    with st.sidebar:
        st.header("TalentScout Inc.")
        st.markdown("Welcome to the initial screening process. Our AI assistant will guide you through the first steps.")
        st.markdown("Please answer all questions to the best of your ability. Good luck!")

    st.title("🤖 TalentScout Hiring Assistant")
    st.markdown("---")

    initialize_session_state()

    if not st.session_state.messages:
        greeting = "Hello! I am the intelligent Hiring Assistant from TalentScout. I'm here to gather some essential information to begin the screening process. You can type 'exit' or 'bye' to end our conversation at any time."
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        first_question = get_next_question(st.session_state.state)
        st.session_state.messages.append({"role": "assistant", "content": first_question})

    for message in st.session_state.messages:
        avatar = '👤' if message["role"] == "user" else '🤖'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if st.session_state.conversation_ended:
        st.chat_input("The conversation has ended.", disabled=True)
        st.stop()

    prompt = st.chat_input("Your answer...")

    if prompt:
        exit_keywords = ["exit", "bye", "quit"]
        if any(keyword in prompt.lower() for keyword in exit_keywords):
            farewell_message = "Thank you for your time. The conversation has now ended. Have a great day!"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": farewell_message})
            st.session_state.conversation_ended = True
            st.rerun()
        else:
            handle_user_input(prompt)
            st.rerun()

if __name__ == "__main__":
    main()
