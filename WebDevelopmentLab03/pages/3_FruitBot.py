import streamlit as st
import requests as r
import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# load_dotenv()
key = st.secrets['key']

genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("Fruit Chatbot 🤖")
st.write("Ask about fruits, recipes, or nutrition!")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    fruit_data = []
    fruits_list = r.get("https://www.fruityvice.com/api/fruit/all").json()
    fruit_names_list = [f['name'].lower() for f in fruits_list]
    for fruit_name in fruit_names_list:
        if fruit_name in user_input.lower():
            response = r.get(f"https://www.fruityvice.com/api/fruit/{fruit_name}")
            if response.status_code == 200:
                data = response.json()
                fruit_data.append({"name": fruit_name, "nutritions": data["nutritions"]})

    prompt = f"""
You are a helpful fruit expert chatbot.
Answer the user's question: {user_input}.
Use the following fruit data if relevant: {fruit_data}.
Keep your answer short and informative.
"""

    try:
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
