import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


df = pd.read_csv("Crime_Data_from_2020_to_Present.csv")
# fetching year
def fetching_year(df):
    df["date"] = pd.to_datetime(df["date_occurred"])
    df["year"] = df["date"].dt.year
    return df
# multiselect feature
def multiselect(title,option_list):
    selected = st.sidebar.multiselect(title,option_list)
    select_all = st.sidebar.checkbox("Select all", value = True, key = title)
    if select_all:
        selected_options = option_list
    else:
        selected_options = selected
    return selected_options

# creating a new columns of age_category
def categorize_age(victim_age):
    if victim_age <= 12:
        return "Child"
    elif 13 <= victim_age <= 19:
        return "Teenager"
    elif 20 <= victim_age <= 64:
        return "Adult"
    elif victim_age >= 65:
        return "Senior Citizen"
    return "Unknow"


