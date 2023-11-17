import pickle
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import aws_s3 as s3

def preprocess():

    df = s3.read_data_from_csv('cleaned.csv')
    
    column=[ 'type_of_property', 'building_condition', 'kitchen_type', 'energy_class', 'heating_type',] # catagorical

    # using onehot encoder
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
    one_hot_encoded_array = ohe.fit_transform(df[column]).toarray()
    ohe_pickle = pickle.dump(ohe)
    s3.pickling(ohe_pickle,'ohe_pickle.pkl')

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
    minmax_pickle = pickle.dump(minmax_scaler)
    s3.pickling(minmax_pickle, 'minmax_pickle.pkl')

    x_test[[ 'surface_of_the_plot', 'living_room_surface']]= minmax_scaler.transform(x_test[[ 'surface_of_the_plot', 'living_room_surface']])
    return x_train,y_train,x_test,y_test

def RandomForestReg(train_x,train_y, test_x,test_y):

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
    forest_pickle = pickle.dump(forest)
    s3.pickling(forest_pickle, 'forest_pickle.pkl')
    return test_score

def training_model():
    
    logging.info('start train model')
    x_train,y_train,x_test,y_test = preprocess()
    RandomForestReg(x_train,y_train,x_test,y_test)
    logging.info('end train model')

    return

