# A graph that shows the amount of fruits per family
# The user can choose the families to display 
import requests as r
import streamlit as st
from pprint import pprint
data = r.get("https://www.fruityvice.com/api/fruit/all")
fruits_list = data.json()
family_dict = {}
family_names = [] # names for the multiselect 
for fruit in fruits_list:
    if fruit['family'].strip() not in family_dict:
        family_dict[fruit['family'].strip()] = 1
        family_names.append(fruit['family'].strip())
    else:
        family_dict[fruit['family'].strip()] += 1
    
# Select a fruit from a drop-down list
# Adjust a slider for the serving size in grams

fruit_names = []
for i in range(len(fruits_list)):
    fruit_names.append(fruits_list[i]['name'])
    
user_fruit = st.selectbox('Choose a fruit',sorted(fruit_names))
serving_size = st.slider('Serving size (in grams)', 0, 500)

fruit_dict = r.get(f"https://www.fruityvice.com/api/fruit/{user_fruit}").json()
nutrients_dict = fruit_dict['nutritions']

calories = round(serving_size/100 * nutrients_dict['calories'],2)
fat = round(serving_size/100 * nutrients_dict['fat'],2)
sugar = round(serving_size/100 * nutrients_dict['sugar'],2)
carbohydrates = round(serving_size/100 * nutrients_dict['carbohydrates'],2)
protein = round(serving_size/100 * nutrients_dict['protein'],2)

# Use these to display a table or pie chart? with a picture of the fruit
# and maybe some sort of 'results' comment that analyses the nutrients 
