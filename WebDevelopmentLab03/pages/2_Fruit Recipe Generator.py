import google.generativeai as genai
import os
import streamlit as st
import requests as r

st.title("Fruit Recipe Generator")
st.write("Choose 2 fruits and a style. We will generate a fun recipe for you!")

fruit1 = st.text_input("Enter your first fruit:")
fruit2 = st.text_input("Enter your second fruit:")

cuisine = st.selectbox("Choose a style:", ['Tropical', 'Italian', 'Dessert', 'Smoothie','Salad', 'Snack'])

if st.button("**Reveal Your Recipe**"):
    fruit_data = []
    if fruit1 and fruit2:
        fruits = [fruit1, fruit2]
        for fruit in fruits:
            response = r.get(f"https://www.fruityvice.com/api/fruit/{fruit.lower().strip()}")
            if response.status_code == 200:
                data = response.json()
                fruit_data.append({"name": fruit, "nutritions": data["nutritions"]})
            else:
               st.error(f"Could not find a fruit with the name: {fruit}. Check the spelling or enter a different fruit.")
        
    genai.configure(api_key="AIzaSyDwEXKHLchXS9S67hi6lTy9O0btpD4Qf4I")
    model = genai.GenerativeModel("gemini-2.0-flash")

    fruit_names = ""
    if len(fruit_data) == 2 :
        for fruit in fruit_data:
         fruit_names += fruit['name'] + ' '
        prompt = f"""
            Create a {cuisine.lower()} style recipe using {fruit_names}.
            Include a fun recipe name, ingredients list, and short instructions.
            Highlight nutritional benefits based on: {fruit_data}.
            """
        response = model.generate_content(prompt)

        st.subheader("🍴Recipe Suggestion🍴")
        st.write(response.text)


