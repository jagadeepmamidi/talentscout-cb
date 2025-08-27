import streamlit as st
import time

def call_llm_mock(prompt_template, user_data):
    """
    Simulates a call to a Large Language Model.
    In a real application, this function would interact with an API (e.g., OpenAI, Cohere).
    It uses the prompt_template and injects user_data to generate a response.
    """
    if "generate technical questions" in prompt_template:
        tech_stack = user_data.get("tech_stack", "general")
        experience = user_data.get("experience", "an unspecified number of")
        position = user_data.get("position", "a role")

        st.session_state.messages.append({"role": "assistant", "content": f"Understood. Generating relevant technical questions for a candidate with {experience} years of experience applying for {position} with skills in {tech_stack}. Please wait a moment..."})
        time.sleep(2)

        questions = {
            "python": [
                "1. Can you explain the difference between a list and a tuple in Python?",
                "2. What are decorators and how have you used them?",
                "3. Describe the Global Interpreter Lock (GIL) and its implications for multi-threaded programming in Python."
            ],
            "django": [
                "1. What is the Django ORM and what are its main advantages?",
                "2. Explain the MVT (Model-View-Template) architecture in Django.",
                "3. How do you handle database migrations in a Django project?"
            ],
            "javascript": [
                "1. What is the difference between `==` and `===` in JavaScript?",
                "2. Can you explain what a closure is and provide a simple example?",
                "3. Describe event bubbling and capturing in the context of the DOM."
            ],
            "react": [
                "1. What is the Virtual DOM and how does it improve performance?",
                "2. Explain the difference between state and props in React.",
                "3. Describe the component lifecycle in a class-based React component."
            ],
            "sql": [
                "1. What is the difference between an `INNER JOIN` and a `LEFT JOIN`?",
                "2. What are database indexes and why are they important for performance?",
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
             response = "Thank you for sharing your tech stack. It seems quite specialized. We will have a technical specialist review your profile and reach out with tailored questions. For now, we can proceed."

        return response
    else:
        # Fallback for other simulated calls, though not used in this specific flow
        return "I'm sorry, I'm not sure how to respond to that."


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
        "GATHERING_LOCATION": "And finally, what is your tech stack? Please list the programming languages, frameworks, and databases you are proficient in (e.g., Python, Django, React, SQL)."
    }
    return question_map.get(current_state, "")

def handle_user_input(prompt):
    """Processes user input, updates state, and generates chatbot responses."""
    st.session_state.messages.append({"role": "user", "content": prompt})

    current_state = st.session_state.state
    response = ""

    if current_state == "GREETING":
        st.session_state.candidate_info["full_name"] = prompt
        st.session_state.state = "GATHERING_NAME"
        response = get_next_question(st.session_state.state)

    elif current_state == "GATHERING_NAME":
        st.session_state.candidate_info["email"] = prompt
        st.session_state.state = "GATHERING_EMAIL"
        response = get_next_question(st.session_state.state)

    elif current_state == "GATHERING_EMAIL":
        st.session_state.candidate_info["phone"] = prompt
        st.session_state.state = "GATHERING_PHONE"
        response = get_next_question(st.session_state.state)

    elif current_state == "GATHERING_PHONE":
        st.session_state.candidate_info["experience"] = prompt
        st.session_state.state = "GATHERING_EXPERIENCE"
        response = get_next_question(st.session_state.state)

    elif current_state == "GATHERING_EXPERIENCE":
        st.session_state.candidate_info["position"] = prompt
        st.session_state.state = "GATHERING_POSITION"
        response = get_next_question(st.session_state.state)

    elif current_state == "GATHERING_POSITION":
        st.session_state.candidate_info["location"] = prompt
        st.session_state.state = "GATHERING_LOCATION"
        response = get_next_question(st.session_state.state)

    elif current_state == "GATHERING_LOCATION":
        st.session_state.candidate_info["tech_stack"] = prompt
        st.session_state.state = "GENERATING_QUESTIONS"
        prompt_template = "You are a technical interviewer. A candidate with {experience} years of experience, applying for {position}, has declared the following tech stack: {tech_stack}. Please generate technical questions."
        response = call_llm_mock(prompt_template, st.session_state.candidate_info)
        st.session_state.state = "CONCLUDED"

    if st.session_state.state == "CONCLUDED":
        final_message = "Thank you for your time and for answering these initial questions. Your profile has been recorded. Our recruitment team will review your information and get back to you with the next steps. Have a great day!"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.messages.append({"role": "assistant", "content": final_message})
        st.session_state.conversation_ended = True

    else:
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    """Main function to run the Streamlit application."""
    st.title("TalentScout Hiring Assistant")

    initialize_session_state()

    if not st.session_state.messages:
        greeting = "Hello! I am the intelligent Hiring Assistant from TalentScout. I'm here to help with the initial screening process by gathering some essential information. Let's get started. You can type 'exit' or 'bye' at any time to end our conversation."
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        first_question = get_next_question(st.session_state.state)
        st.session_state.messages.append({"role": "assistant", "content": first_question})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.conversation_ended:
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
