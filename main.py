import streamlit as st
import requests

# ✅ Your actual Perplexity API key
API_KEY = "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"
API_URL = "https://api.perplexity.ai/chat/completions"

# ✅ Valid models: sonar, sonar-pro, sonar-reasoning, sonar-deep-research
MODEL = "sonar-pro"
USE_ONLINE = False  # Set True if your key supports real-time search

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
st.markdown("Ask me anything powered by **Perplexity API**.")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Your question:", key="user_input")

if user_input:
    reply = ask_perplexity(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", reply))
    st.experimental_rerun()

# Display chat
for role, message in reversed(st.session_state.history):
    if role == "You":
        st.markdown(f"**🧑 {role}:** {message}")
    else:
        st.markdown(f"**🤖 {role}:** {message}")
