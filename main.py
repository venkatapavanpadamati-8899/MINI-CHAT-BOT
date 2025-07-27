import streamlit as st
import requests

# ✅ Your actual Perplexity API key
API_KEY = "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"
API_URL = "https://api.perplexity.ai/chat/completions"

# ✅ Choose a valid model
MODEL = "sonar-pro"
USE_ONLINE = False  # Set True if your key supports "sonar-pro-online"

def ask_perplexity(question):
    model_name = f"{MODEL}-online" if USE_ONLINE else MODEL

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.HTTPError as http_err:
        try:
            error_message = response.json().get("error", {}).get("message", response.text)
        except:
            error_message = response.text
        return f"❌ HTTP {response.status_code} Error: {error_message}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

# 🚀 Streamlit UI
st.set_page_config(page_title="Perplexity Chatbot", page_icon="🤖")
st.title("🤖 Perplexity AI Chatbot")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box and submit button
with st.form("chat_form"):
    user_input = st.text_input("Your question:", key="input")
    submitted = st.form_submit_button("Ask")

# If submitted, process the input
if submitted and user_input:
    response = ask_perplexity(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

# Display chat history
for role, message in reversed(st.session_state.history):
    if role == "You":
        st.markdown(f"**🧑 {role}:** {message}")
    else:
        st.markdown(f"**🤖 {role}:** {message}")
