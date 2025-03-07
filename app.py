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
        "Authorization": f"Bearer {APPLICATION_TOKEN}"
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

# Streamlit UI
st.title("🤖 ChatFlow AI")
st.write("A conversational chatbot designed to keep the conversation flowing effortlessly!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
