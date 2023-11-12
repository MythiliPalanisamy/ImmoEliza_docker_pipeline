import pandas as pd
import tkinter as tk
import pickle
import numpy as np

AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"
ohe_pickle_path = AIRFLOW_HOME + "/dags/pickles/ohe.pickle"
minmax_pickle_path = AIRFLOW_HOME + "/dags/pickles/minmax_scaler.pickle"
forest_pickle_path = AIRFLOW_HOME + "/dags/pickles/forest.pickle"

def preprocess(raw_dataframe):
    
    """ For reference :
    'one_hot_encoded_array' = encoding given column's with one hot encoder.
    'ohe.categories_' = list of category in each column as separate array.
    'categories' = coverting list of (names of) arrays as single array
    'encoded_dataframe' = converting encoded array and names of array as single dataframe
    'final' = concatenating encoded dataframe and original dataframe
    """

    # catagorical columns
    column=[ 'type_of_property', 'building_condition', 'kitchen_type',  'energy_class', 'heating_type',]
    
    # loading one hot encoding trained data and minmax scaler
    ohe = pickle.load(open(ohe_pickle_path, 'rb'))
    minmax_scaler = pickle.load(open(minmax_pickle_path, 'rb'))



# using onehot encoder
    one_hot_encoded_array = ohe.transform(raw_dataframe[column]).toarray()
    categories = np.concatenate(ohe.categories_)
    encoded_dataframe = pd.DataFrame(one_hot_encoded_array, columns=categories)

    # droping encoded columns from original dataframe
    raw_dataframe = raw_dataframe.drop(columns=[ 'type_of_property', 'building_condition', 'kitchen_type','energy_class', 'heating_type','postal_code'])
    raw_dataframe = raw_dataframe.astype(int) 
    final = pd.concat([raw_dataframe,encoded_dataframe], axis=1)

# using minmax scaler
    final[['surface_of_the_plot', 'living_room_surface']] = minmax_scaler.transform(final[[ 'surface_of_the_plot', 'living_room_surface']])
    processed=final

    return processed

def predict(property):

    #property = json.loads(property.json())
    df = pd.DataFrame(property, index=[0])
    
    processed = preprocess(df)
    price = predict_forest_price(processed)

    return {'predicted_price' : price[0]}

def predict_forest_price(processed):

    # loading forest module
    forest = pickle.load(open(forest_pickle_path, 'rb'))
    predicted_price = forest.predict(processed)

    return predicted_price

def form(type_of_property_entry, bedrooms_entry, energy_class_entry, surface_of_the_plot_entry,
         living_room_surface_entry, building_condition_entry, bathrooms_entry, kitchen_type_entry,
         heating_type_entry, postal_code_entry, result_label):
    # Collect input values from the Tkinter widgets
    property_details = {
        "type_of_property": type_of_property_entry.get(),
        "bedrooms": bedrooms_entry.get(),
        "energy_class": energy_class_entry.get(),
        "surface_of_the_plot": surface_of_the_plot_entry.get(),
        "living_room_surface": living_room_surface_entry.get(),
        "number_of_frontages": 0,
        "building_condition": building_condition_entry.get(),
        "bathrooms": bathrooms_entry.get(),
        "toilets": 0,
        "kitchen_type": kitchen_type_entry.get(),
        "heating_type": heating_type_entry.get(),
        "postal_code": postal_code_entry.get(),
    }

    # Call the predict function and update the result_label
    prediction_result = predict(property_details)
    result_label.config(text=f'Predicted Price: {prediction_result["predicted_price"]}')

def open_prediction_dialog():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Property Price Prediction")

    # Create input fields for some of the properties
    type_of_property_label = tk.Label(root, text="Type of Property:")
    type_of_property_label.pack()
    type_of_property_entry = tk.Entry(root)
    type_of_property_entry.pack()

    postal_code_label = tk.Label(root, text="Postal Code:")
    postal_code_label.pack()
    postal_code_entry = tk.Entry(root)
    postal_code_entry.pack()

    energy_class_label = tk.Label(root, text="Energy Class:")
    energy_class_label.pack()
    energy_class_entry = tk.Entry(root)
    energy_class_entry.pack()

    bedrooms_label = tk.Label(root, text="Bedrooms:")
    bedrooms_label.pack()
    bedrooms_entry = tk.Entry(root)
    bedrooms_entry.pack()

    bathrooms_label = tk.Label(root, text="Bathroom:")
    bathrooms_label.pack()
    bathrooms_entry = tk.Entry(root)
    bathrooms_entry.pack()

    building_condition_label = tk.Label(root, text="Building Condition:")
    building_condition_label.pack()
    building_condition_entry = tk.Entry(root)
    building_condition_entry.pack()

    kitchen_type_label = tk.Label(root, text="Kitchen Type:")
    kitchen_type_label.pack()
    kitchen_type_entry = tk.Entry(root)
    kitchen_type_entry.pack()

    heating_type_label = tk.Label(root, text="Heating Type:")
    heating_type_label.pack()
    heating_type_entry = tk.Entry(root)
    heating_type_entry.pack()

    surface_of_the_plot_label = tk.Label(root, text="Surface of the Plot:")
    surface_of_the_plot_label.pack()
    surface_of_the_plot_entry = tk.Entry(root)
    surface_of_the_plot_entry.pack()

    living_room_surface_label = tk.Label(root, text="Living Room Surface:")
    living_room_surface_label.pack()
    living_room_surface_entry = tk.Entry(root)
    living_room_surface_entry.pack()

    # Create a button to submit the form
    submit_button = tk.Button(root, text="Submit", command=lambda: form(
        type_of_property_entry, bedrooms_entry, energy_class_entry, surface_of_the_plot_entry,
        living_room_surface_entry, building_condition_entry, bathrooms_entry, kitchen_type_entry,
        heating_type_entry, postal_code_entry, result_label))
    submit_button.pack()
    # Create a label to display the predicted price
    result_label = tk.Label(root, text="Prediction:     ")
    result_label.pack()

    # Start the Tkinter event loop
    root.mainloop()

# Determine if the script is triggered by the "prediction" tag
if __name__ == "__main__":
    open_prediction_dialog()
