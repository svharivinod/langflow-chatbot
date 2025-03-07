import streamlit as st
import requests

# Load API Token from Streamlit Secrets
APPLICATION_TOKEN = st.secrets["APPLICATION_TOKEN"]

# Langflow API URL
LANGFLOW_API_URL = "https://api.langflow.astra.datastax.com/lf/fd0b889e-09f8-4a5d-ba96-7f9476c8a80f/api/v1/run/1e2a1826-1112-4ff3-b261-a8bbb45e5a1c"

# Function to send request to Langflow API and extract response
def get_response(user_input):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer " + APPLICATION_TOKEN
    }
    payload = {
        "input_value": user_input,
        "output_type": "chat",
        "input_type": "chat"
    }

    response = requests.post(LANGFLOW_API_URL, headers=headers, json=payload)

    try:
        response_json = response.json()
        return response_json["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except (KeyError, IndexError, TypeError, requests.exceptions.JSONDecodeError):
        return "⚠️ Error: Unable to process the response. Please try again."

# Set up Streamlit page
st.set_page_config(page_title="ChatFlow AI", layout="wide")

st.title("🤖 ChatFlow AI")
st.write("A conversational chatbot designed to keep the conversation flowing effortlessly!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Ensure the text input box remains at the bottom
st.markdown("---")
query_container = st.container()
with query_container:
    user_input = st.text_input("You:", "", key="user_input", help="Type your query below.", label_visibility="hidden")
    send_button = st.button("Send", use_container_width=True)

# If the user enters a query or clicks "Send", process it
if send_button and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear the input field after sending the message
    st.query_params()["user_input"] = ""

    # Rerun the app to reflect the new chat
    st.rerun()
