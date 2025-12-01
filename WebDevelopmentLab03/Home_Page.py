import streamlit as st

# Title of App
st.title("Web Development Lab03")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 44, Web Development - Section C")
st.subheader("Biana Akpokabayen, Tringa Ibrahimi")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

-  **Fruits Nutrition Analysis** - In this page you can get the nutritional value of choosen fruits. You can also get information about fruit families. In addition, you cans see which fruit are better for you based on your health condition (if applicable).
-  **Fruit Recipe Generator** - In this page you can choose your two favorite fruits and a style and we will generate a fun recipe for you
-  **Fruitbot** - In this page you will be able to communicate with a chatbot and answer all of your food related questions


""")


st.image('https://raw.githubusercontent.com/TringaI/lab-partnering/main/WebDevelopmentLab03/Images/avocado.avif')
