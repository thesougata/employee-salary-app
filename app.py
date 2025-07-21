import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load("salary_prediction_model.joblib")

# Page Title
st.set_page_config(page_title="Employee Salary Class Predictor", layout="centered")
st.title("💼 Salary Prediction App")
st.markdown("Predict whether an employee earns more or less than 50K.")

# Collect user input
st.header("🔍 Enter Employee Details")

age = st.number_input("Age", min_value=18, max_value=90, step=1)
education_num = st.slider("Education Level (numerical)", 1, 16, 10)
hours_per_week = st.slider("Working Hours per Week", 1, 100, 40)

# Other categorical features
workclass = st.selectbox("Workclass", ['Private', 'Self-emp-not-inc', 'Self-emp-inc',
                                       'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'])
marital_status = st.selectbox("Marital Status", ['Married-civ-spouse', 'Divorced', 'Never-married',
                                                  'Separated', 'Widowed', 'Married-spouse-absent'])
occupation = st.selectbox("Occupation", ['Tech-support', 'Craft-repair', 'Other-service',
                                         'Sales', 'Exec-managerial', 'Prof-specialty',
                                         'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical',
                                         'Farming-fishing', 'Transport-moving', 'Priv-house-serv',
                                         'Protective-serv', 'Armed-Forces'])
relationship = st.selectbox("Relationship", ['Wife', 'Own-child', 'Husband', 'Not-in-family',
                                             'Other-relative', 'Unmarried'])
race = st.selectbox("Race", ['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'])
sex = st.radio("Gender", ['Male', 'Female'])
native_country = st.selectbox("Native Country", ['United-States', 'Other'])

# Convert categorical to numbers (manual encoding based on training)
def encode_input():
    workclass_dict = {'Private': 4, 'Self-emp-not-inc': 6, 'Self-emp-inc': 5,
                      'Federal-gov': 1, 'Local-gov': 2, 'State-gov': 7,
                      'Without-pay': 8, 'Never-worked': 3}
    marital_dict = {'Married-civ-spouse': 2, 'Divorced': 0, 'Never-married': 3,
                    'Separated': 4, 'Widowed': 6, 'Married-spouse-absent': 1}
    occupation_dict = {'Tech-support': 12, 'Craft-repair': 2, 'Other-service': 8,
                       'Sales': 10, 'Exec-managerial': 4, 'Prof-specialty': 9,
                       'Handlers-cleaners': 5, 'Machine-op-inspct': 6, 'Adm-clerical': 0,
                       'Farming-fishing': 3, 'Transport-moving': 13, 'Priv-house-serv': 7,
                       'Protective-serv': 11, 'Armed-Forces': 1}
    relationship_dict = {'Wife': 5, 'Own-child': 2, 'Husband': 1, 'Not-in-family': 3,
                         'Other-relative': 4, 'Unmarried': 0}
    race_dict = {'White': 4, 'Asian-Pac-Islander': 1, 'Amer-Indian-Eskimo': 0, 'Other': 2, 'Black': 3}
    sex_dict = {'Male': 1, 'Female': 0}
    native_dict = {'United-States': 39, 'Other': 0}

    return [age,
            workclass_dict[workclass],
            education_num,
            marital_dict[marital_status],
            occupation_dict[occupation],
            relationship_dict[relationship],
            race_dict[race],
            sex_dict[sex],
            hours_per_week,
            native_dict[native_country]]

# Predict
if st.button("🔮 Predict Salary Class"):
    user_data = np.array(encode_input()).reshape(1, -1)
    prediction = model.predict(user_data)
    result = ">50K" if prediction[0] == 1 else "<=50K"
    st.success(f"Predicted Salary Class: **{result}**")
