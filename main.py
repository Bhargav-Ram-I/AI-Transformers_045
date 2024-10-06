import streamlit as st
import pandas as pd
import preprocessor
import matplotlib.pyplot as plt
import pydeck as pdk
# changing the layout of streamlit
st.set_page_config(layout = "wide")
# reading the data
df = pd.read_csv("Crime_Data_from_2020_to_Present.csv")

# cleaning the data
# droping all the values with lots of null values
df = df.drop(columns = ["crime_code_2","victim_descent","crime_code_3","crime_code_4","modus_operandi","weapon_code","weapon_description","cross_street"], axis = 1)
# filling the rest data with forward fill 
df = df.ffill()

# creating feature
df = preprocessor.fetching_year(df)

#Creating new age category 
df['Age Category'] = df['victim_age'].apply(preprocessor.categorize_age)
# sidebar
st.sidebar.title("Filters")
# year filter
selected_year = preprocessor.multiselect("Select Year", df["year"].unique())
selected_crime_area = preprocessor.multiselect("Select Crime Area", df["area_name"].unique())
selected_victim_sex = preprocessor.multiselect("Select Victim Sex", df["victim_sex"].unique())
selected_crime_descriptionar = preprocessor.multiselect("Select Crime Descriptionar", df["crime_description"].unique())
selected_victim_age_category = preprocessor.multiselect("Select Age Category",["Child", "Teenager", "Adult", "Senior Citizen"])


# global filter
filtered_df = df[(df["year"].isin(selected_year)) & (df["area_name"].isin(selected_crime_area)) & (df["victim_sex"].isin(selected_victim_sex)) & (df["crime_description"].isin(selected_crime_descriptionar)) & (df["Age Category"].isin(selected_victim_age_category))]
# title
st.title("Crime Analytics Dashboard")
# creating columns for Indicators or KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label = "Total Crime", value = len(filtered_df["area"]))
with col2:
    st.metric(label = "Number of Types of crimes", value = len(filtered_df["crime_description"].unique()))
with col3:
    st.metric(label = "Number of Crime Areas", value = len(filtered_df["area_name"].unique()))
    

# Making colums of months and year to fetch the according data
filtered_df['date'] = pd.to_datetime(filtered_df['date_occurred'])
filtered_df['year'] = filtered_df['date'].dt.year
filtered_df['month'] = filtered_df['date'].dt.month



# Making a table for monthly crimes in the state
yearly_crimes = filtered_df.groupby(['year'])[['month']].value_counts().reset_index().sort_values(by = 'month')
monthly_crimes = yearly_crimes.pivot(index = 'month', columns = 'year', values = 'count')

# PLoting a line chart showing the crimes
st.line_chart(monthly_crimes, x_label = "Months", y_label = "Crimes Counts")




# Grouping age_cotegory and counting the values
age = filtered_df.groupby('Age Category')[["victim_age"]].count()

# fetching crime discription of top 10 crimes in locality
crimes = filtered_df['crime_description'].value_counts().reset_index().head(10)



# making columns for pie chart
col4, col5 = st.columns(2)
# ploting pie chart in column 1
with col4:
    st.title("Affected Victims")
    fig, ax = plt.subplots()
    plt.figure(figsize= (3,2))
    labels1 = age.index
    ax.pie(age['victim_age'], labels=labels1, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# Creating a table fetching top 10 areas affected by crimes
area1 = filtered_df[['area_name']].value_counts().reset_index().head(10)
with col5:
    st.title("Crime Counts by Area")

    # Create a bar chart using matplotlib
    fig, ax = plt.subplots()
    ax.bar(area1['area_name'], area1['count'], color='grey')

    # Add labels and title
    ax.set_xlabel("Area Name")
    ax.set_ylabel("Count")
    ax.set_title("10 most Crimes affected Area ")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Display the plot using Streamlit
    st.pyplot(fig)

st.title("Top 10 Crimes")
fig, ax = plt.subplots()
l = crimes.crime_description
ax.pie(crimes['count'], autopct='%1.1f%%', startangle=90,)
ax.legend(l,loc='upper right', bbox_to_anchor=(2, 1)) 
ax.axis('equal')
st.pyplot(fig)


