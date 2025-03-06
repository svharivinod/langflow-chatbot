import streamlit as st
import requests
import speech_recognition as sr
from fpdf import FPDF

# Load API Token from Streamlit Secrets
APPLICATION_TOKEN = st.secrets["APPLICATION_TOKEN"]

# Langflow API URL
LANGFLOW_API_URL = "https://api.langflow.astra.datastax.com/lf/fd0b889e-09f8-4a5d-ba96-7f9476c8a80f/api/v1/run/1e2a1826-1112-4ff3-b261-a8bbb45e5a1c"

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to send request to Langflow API and extract response
def get_response(user_input):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {APPLICATION_TOKEN}"
    }
    payload = {
        "input_value": user_input,
        "output_type": "chat",
        "input_type": "chat",
        "system_message": "You are ChatFlow AI, a friendly and engaging chatbot that provides insightful and clear responses to users."
    }

    response = requests.post(LANGFLOW_API_URL, headers=headers, json=payload)

    try:
        response_json = response.json()
        return response_json["outputs"][0]["outputs"][0]["results"]["message"]["text"]

    except (KeyError, IndexError, TypeError):
        return "⚠️ Error: API response not in expected format."

# Function for voice input
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak now!")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Could not request results, check your internet connection."

# Function to save chat as PDF
def save_chat_as_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Chat Conversation", ln=True, align="C")
    pdf.ln(10)

    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "ChatFlow AI"
        pdf.multi_cell(0, 10, f"{role}: {msg['content']}")
        pdf.ln(5)

    pdf.output("chat_history.pdf")
    with open("chat_history.pdf", "rb") as file:
        st.download_button("📥 Download Chat as PDF", file, file_name="chat_history.pdf")

# Streamlit UI
st.title("🤖 ChatFlow AI")
st.write("A conversational chatbot designed to keep the conversation flowing effortlessly!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input (Text)
user_input = st.text_input("You:", "")

# Voice Input Button
if st.button("🎤 Speak"):
    user_input = record_voice()
    st.text_input("You:", user_input)

# Send Button
if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": f"🗣️ {user_input}"})

    # Get chatbot response
    response = get_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": f"🤖 {response}"})

    with st.chat_message("assistant"):
        st.markdown(f"🤖 {response}")

# Save Chat as PDF Button
save_chat_as_pdf()