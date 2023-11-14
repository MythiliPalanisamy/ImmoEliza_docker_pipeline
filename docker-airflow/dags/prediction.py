import streamlit as st
import pickle
import pandas as pd
import numpy as np
import aws_s3 as s3

    # For reference :
    #'one_hot_encoded_array' = encoding given column's with one hot encoder.
    #'ohe.categories_' = list of category in each column as separate array.
    #'categories' = coverting list of (names of) arrays as single array
    #'encoded_dataframe' = converting encoded array and names of array as single dataframe
    #'final' = concatenating encoded dataframe and original dataframe

# Load the pickled models

ohe = s3.read_pickled_data_from_s3('ohe_pickle.pkl')
minmax_scaler = s3.read_pickled_data_from_s3('minmax_pickle.pkl')
forest = s3.read_pickled_data_from_s3('forest_pickle.pkl')

# Function to preprocess input data
def preprocess(raw_dataframe):
    column = ['type_of_property', 'building_condition', 'kitchen_type', 'energy_class', 'heating_type']
    one_hot_encoded_array = ohe.transform(raw_dataframe[column]).toarray()
    categories = np.concatenate(ohe.categories_)
    encoded_dataframe = pd.DataFrame(one_hot_encoded_array, columns=categories)
    raw_dataframe = raw_dataframe.drop(columns=['type_of_property', 'building_condition', 'kitchen_type', 'energy_class', 'heating_type', 'postal_code'])
    raw_dataframe = raw_dataframe.astype(int)
    final = pd.concat([raw_dataframe, encoded_dataframe], axis=1)
    final[['surface_of_the_plot', 'living_room_surface']] = minmax_scaler.transform(final[['surface_of_the_plot', 'living_room_surface']])
    processed = final
    return processed

# Function to make predictions
def predict_forest_price(processed):
    predicted_price = forest.predict(processed)
    return predicted_price[0]

# Streamlit app
def predict_house_or_apartment():
    st.title("Property Price Prediction")

    # Collect input values using Streamlit widgets
    type_of_property = st.text_input("Type of Property:")
    bedrooms = st.text_input("Bedrooms:")
    energy_class = st.text_input("Energy Class:")
    surface_of_the_plot = st.text_input("Surface of the Plot:")
    living_room_surface = st.text_input("Living Room Surface:")
    building_condition = st.text_input("Building Condition:")
    bathrooms = st.text_input("Bathrooms:")
    kitchen_type = st.text_input("Kitchen Type:")
    heating_type = st.text_input("Heating Type:")
    postal_code = st.text_input("Postal Code:")

    # Button to submit the form and make predictions
    if st.button("Predict"):
        # Create a dictionary with input values
        property_details = {
            "type_of_property": type_of_property,
            "bedrooms": bedrooms,
            "energy_class": energy_class,
            "surface_of_the_plot": surface_of_the_plot,
            "living_room_surface": living_room_surface,
            "number_of_frontages": 0,
            "building_condition": building_condition,
            "bathrooms": bathrooms,
            "toilets": 0,
            "kitchen_type": kitchen_type,
            "heating_type": heating_type,
            "postal_code": postal_code,
        }

        # Convert the dictionary to a DataFrame and preprocess
        df = pd.DataFrame(property_details, index=[0])
        processed = preprocess(df)

        # Make predictions and display the result
        predicted_price = predict_forest_price(processed)
        st.success(f'Predicted Price: {predicted_price}')
    return predicted_price
predict_house_or_apartment()