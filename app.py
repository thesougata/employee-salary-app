import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("salary_prediction_model.joblib")

st.set_page_config(page_title="Employee Salary Class Predictor")
st.title("💼 Employee Salary Class Predictor")
st.write("Predict whether a person earns **>50K** or **<=50K** based on their profile.")

# Manual encoders (must match original training order)
def encode_input(value, options):
    return options.index(value) if value in options else 0

# Input fields
age = st.number_input("Age", 17, 90, step=1)

workclass_opts = ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov',
                  'Local-gov', 'State-gov', 'Without-pay', 'Never-worked']
workclass = st.selectbox("Workclass", workclass_opts)

education_opts = ['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school',
                  'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters',
                  '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool']
education = st.selectbox("Education", education_opts)

education_num = st.slider("Education Number", 1, 16, 9)

marital_opts = ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated',
                'Widowed', 'Married-spouse-absent']
marital_status = st.selectbox("Marital Status", marital_opts)

occupation_opts = ['Tech-support', 'Craft-repair', 'Other-service', 'Sales',
                   'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners',
                   'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing',
                   'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces']
occupation = st.selectbox("Occupation", occupation_opts)

relationship_opts = ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried']
relationship = st.selectbox("Relationship", relationship_opts)

race_opts = ['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black']
race = st.selectbox("Race", race_opts)

sex_opts = ['Male', 'Female']
sex = st.selectbox("Sex", sex_opts)

capital_gain = st.number_input("Capital Gain", 0, 99999, step=1)
capital_loss = st.number_input("Capital Loss", 0, 4356, step=1)
hours_per_week = st.slider("Hours per Week", 1, 100, 40)

country_opts = ['United-States', 'India', 'Mexico', 'Philippines', 'Germany',
                'Canada', 'England', 'China', 'Cuba', 'Other']
native_country = st.selectbox("Native Country", country_opts)

# Prepare input for model (in exact training order)
input_data = pd.DataFrame([[
    age,
    encode_input(workclass, workclass_opts),
    encode_input(education, education_opts),
    education_num,
    encode_input(marital_status, marital_opts),
    encode_input(occupation, occupation_opts),
    encode_input(relationship, relationship_opts),
    encode_input(race, race_opts),
    encode_input(sex, sex_opts),
    capital_gain,
    capital_loss,
    hours_per_week,
    encode_input(native_country, country_opts)
]], columns=['age', 'workclass', 'education', 'education-num', 'marital-status',
             'occupation', 'relationship', 'race', 'sex',
             'capital-gain', 'capital-loss', 'hours-per-week', 'native-country'])

# Predict and display result
if st.button("Predict Salary Class"):
    prediction = model.predict(input_data)[0]
    result = ">50K" if prediction == 1 else "<=50K"
    st.success(f"💰 Predicted Salary Class: **{result}**")