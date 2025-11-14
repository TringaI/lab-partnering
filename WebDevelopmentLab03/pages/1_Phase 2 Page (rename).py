# A graph that shows the amount of fruits per family
# The user can choose the families to display 
import requests as r
import streamlit as st
from pprint import pprint
import pandas as pd
import plotly.express as px

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


st.subheader(f"Nutritional values for {user_fruit} ({serving_size}g serving)")
st.write(f'**Calories**: {calories}')
st.write(f'**Fat** {fat} g')
st.write(f'**Sugar:** {sugar} g')
st.write(f'**Carbohydrates:** {carbohydrates} g')
st.write(f'**Protein:** {protein}g')



st.subheader("Number of Fruits per Family")

selected_families = st.multiselect(
    "Choose fruit families to display",
    sorted(family_names)
)

selected_family_counts = {}

for fam in selected_families:
    selected_family_counts[fam] = family_dict[fam]
    

if selected_family_counts:  
    st.bar_chart(selected_family_counts)
else:
    st.write("Please select at least one family to display the chart.")





st.header("Filter fruits by nutrient ranges")
max_calories = st.slider("Max Calories", 0, 200, 100)
min_protein = st.slider("Min Protein (g)", 0, 10, 1)
max_sugar = st.slider("Max Sugar (g)", 0, 50, 20)

filtered_fruits = []
for fruit in fruits_list:
    nutrients = fruit['nutritions']
    if (
        nutrients['calories'] <= max_calories
        and nutrients['protein'] >= min_protein
        and nutrients['sugar'] <= max_sugar
    ):
        filtered_fruits.append({
            "Name": fruit['name'],
            "Calories": nutrients['calories'],
            "Protein": nutrients['protein'],
            "Sugar": nutrients['sugar'],
            "Carbs": nutrients['carbohydrates'],
            "Fat": nutrients['fat']
        })

if filtered_fruits:
    df = pd.DataFrame(filtered_fruits)
    st.subheader(f"Fruits matching your nutrient criteria ({len(filtered_fruits)} found)")
    st.dataframe(df)

    st.subheader("Calories vs Sugar of filtered fruits")
    st.bar_chart(df.set_index("Name")[["Calories", "Sugar"]])
else:
    st.write("No fruits match the selected criteria. Adjust your sliders.")
    

st.header("Fruits Suitable for Health Conditions")

conditions = {
    "Diabetes": lambda f: f['nutritions']['sugar'] <= 15,
    "Hypertension (High Blood Pressure)": lambda f: f['nutritions']['carbohydrates'] <= 20,  # approximate proxy
    "Kidney Disease": lambda f: f['nutritions']['protein'] <= 1
}

st.write("Select all health conditions that apply to you:")
selected_conditions = [cond for cond in conditions if st.checkbox(cond)]

filtered_fruits = fruits_list
for cond in selected_conditions:
    filtered_fruits = [f for f in filtered_fruits if conditions[cond](f)]

import pandas as pd
import plotly.express as px

df = pd.DataFrame([{
    "Name": f['name'],
    "Family": f['family'],
    "Sugar": f['nutritions']['sugar'],
    "Protein": f['nutritions']['protein'],
    "Carbs": f['nutritions']['carbohydrates']
} for f in filtered_fruits])

st.subheader("Fruits suitable for your selected conditions")

if df.empty:
    st.write("No fruits match the selected condition(s).")
else:
    fig = px.bar(
        df,
        x="Name",
        y="Sugar",
        color="Family",
        hover_data=["Sugar", "Protein", "Carbs"],
        title="Recommended Fruits for Your Conditions"
    )
    st.plotly_chart(fig)

