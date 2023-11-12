import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

def preprocess():

    AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"
    ohe_pickle_path = AIRFLOW_HOME + "/dags/pickles/ohe.pickle"
    minmax_pickle_path = AIRFLOW_HOME + "/dags/pickles/minmax_scaler.pickle"
    df = pd.read_csv(AIRFLOW_HOME + '/dags/data/cleaned.csv')
    column=[ 'type_of_property', 'building_condition', 'kitchen_type', 'energy_class', 'heating_type',] # catagorical

    # using onehot encoder
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
    one_hot_encoded_array = ohe.fit_transform(df[column]).toarray()
    pickle.dump(ohe, open(ohe_pickle_path, 'wb'))

    categories = np.concatenate(ohe.categories_)
    encoded_dataframe = pd.DataFrame(one_hot_encoded_array, columns=categories)
    df = df.drop(columns=[ 'type_of_property', 'building_condition', 'kitchen_type',   'energy_class', 'heating_type',]).reset_index(drop=True)
    new = pd.concat([df,encoded_dataframe], axis=1)

    #initialising 
    x = new.drop(['price'], axis=1)
    y = new['price']
    x_train,x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # normalisation or scaling - train and test
    minmax_scaler = MinMaxScaler()
    x_train[['surface_of_the_plot', 'living_room_surface']] = minmax_scaler.fit_transform(x_train[[ 'surface_of_the_plot', 'living_room_surface']])
    pickle.dump(minmax_scaler, open(minmax_pickle_path, 'wb'))

    x_test[[ 'surface_of_the_plot', 'living_room_surface']]= minmax_scaler.transform(x_test[[ 'surface_of_the_plot', 'living_room_surface']])
    return x_train,y_train,x_test,y_test

def RandomForestReg(train_x,train_y, test_x,test_y):

    AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"
    forest_pickle_path = AIRFLOW_HOME + "/dags/pickles/forest.pickle"

    y_train = np.ravel(train_y)
    y_test = np.ravel(test_y)
    forest = RandomForestRegressor()
    forest.fit(train_x,train_y)

    # score of train
    train_score = forest.score(train_x,train_y)
    print("Train Score:", train_score)

    # score of test
    test_score = forest.score(test_x,test_y)
    print("Test Score:", test_score)

    # saving the model
    pickle.dump(forest, open(forest_pickle_path, "wb"))
    return test_score

def training_model():
    x_train,y_train,x_test,y_test = preprocess()
    RandomForestReg(x_train,y_train,x_test,y_test)
    return

"""def predict_forest_price(processed_data):

    # loading forest module
    forest = pickle.load(open('forest_pickle.pickle', 'rb'))
    predicted_price = forest.predict(processed_data)

    return predicted_price"""