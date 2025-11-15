import requests as r
import streamlit as st
import pandas as pd
import plotly.express as px

data = r.get("https://www.fruityvice.com/api/fruit/all")
fruits_list = data.json()
family_dict = {}
family_names = []
for fruit in fruits_list:
    if fruit['family'].strip() not in family_dict:
        family_dict[fruit['family'].strip()] = 1
        family_names.append(fruit['family'].strip())
    else:
        family_dict[fruit['family'].strip()] += 1

fruit_names = [fruit['name'] for fruit in fruits_list]


st.header("Fruit Nutrition Analysis")

with st.container():
    
    st.subheader(f"Nutritional values for fruits per serving (g)")
    with st.expander("Read description", expanded=False):
        st.write("Select a fruit and adjust the serving size. The outputs show the nutritional values "
                 "(Calories, Fat, Sugar, Carbohydrates, Protein) for the chosen serving size.")
    col1, col2 = st.columns(2)
    with col1:
        user_fruit = st.selectbox('Choose a fruit', sorted(fruit_names))
    with col2:
        serving_size = st.slider('Serving size (in grams)', 0, 500)

    fruit_dict = r.get(f"https://www.fruityvice.com/api/fruit/{user_fruit}").json()
    nutrients_dict = fruit_dict['nutritions']

    calories = round(serving_size/100 * nutrients_dict['calories'], 2)
    fat = round(serving_size/100 * nutrients_dict['fat'], 2)
    sugar = round(serving_size/100 * nutrients_dict['sugar'], 2)
    carbohydrates = round(serving_size/100 * nutrients_dict['carbohydrates'], 2)
    protein = round(serving_size/100 * nutrients_dict['protein'], 2)

    colA, colB = st.columns(2)
    with colA:
        st.write(f'**Calories**: {calories}')
        st.write(f'**Fat**: {fat} g')
    with colB:
        st.write(f'**Sugar:** {sugar} g')
        st.write(f'**Carbohydrates:** {carbohydrates} g')
        st.write(f'**Protein:** {protein} g')
st.divider()

with st.container():
    st.subheader("Number of Fruits per Family")
    
    with st.expander("Read description", expanded=False):
        st.write("Select fruit families to display. The chart shows the number of fruits in each selected family.")
    selected_families = st.multiselect("Choose fruit families to display", sorted(family_names))
    selected_family_counts = {}
    for fam in selected_families:
        selected_family_counts[fam] = family_dict[fam]
    if selected_family_counts:
        st.bar_chart(selected_family_counts)
    else:
        st.write("Please select at least one family to display the chart.")

st.divider()

with st.container():
    st.header("Filter fruits by nutrient ranges")
    
    with st.expander("Read description", expanded=False):
        st.write("Adjust the sliders to filter fruits by maximum calories, minimum protein, and maximum sugar. "
                 "The table or bar chart shows fruits matching your criteria.")
    colN1, colN2, colN3 = st.columns(3)
    with colN1:
        max_calories = st.slider("Max Calories", 0, 200, 100)
    with colN2:
        min_protein = st.slider("Min Protein (g)", 0, 10, 1)
    with colN3:
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
        st.subheader(f"({len(filtered_fruits)} fruits found)")
        tab1, tab2 = st.tabs(["Table View", "Bar Chart"])
        with tab1:
            st.dataframe(df)
        with tab2:
            st.bar_chart(df.set_index("Name")[["Calories", "Sugar"]])
    else:
        st.write("No fruits match the selected criteria. Adjust your sliders.")

st.divider()


with st.container():
    st.header("Fruits Suitable for Health Conditions")
    
    with st.expander("Read description", expanded=False):
        st.write("Select health conditions to filter fruits. The chart shows recommended fruits suitable "
                 "for the selected condition(s).")
    colC1, colC2, colC3 = st.columns(3)
    with colC1:
        c_diabetes = st.checkbox("Diabetes")
    with colC2:
        c_hypertension = st.checkbox("Hypertension (High Blood Pressure)")
    with colC3:
        c_kidney = st.checkbox("Kidney Disease")

    conditions = {
        "Diabetes": lambda f: f['nutritions']['sugar'] <= 15,
        "Hypertension (High Blood Pressure)": lambda f: f['nutritions']['carbohydrates'] <= 20,
        "Kidney Disease": lambda f: f['nutritions']['protein'] <= 1
    }

    selected_conditions = []
    if c_diabetes:
        selected_conditions.append("Diabetes")
    if c_hypertension:
        selected_conditions.append("Hypertension (High Blood Pressure)")
    if c_kidney:
        selected_conditions.append("Kidney Disease")

    filtered_fruits = fruits_list
    for cond in selected_conditions:
        filtered_fruits = [f for f in filtered_fruits if conditions[cond](f)]

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
