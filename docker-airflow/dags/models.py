import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import aws_s3 as s3

bucket_name = 'immoeliza'
s3_key = f'{bucket_name}/pickles/' # path of file in s3
cleaned = 'cleaned.csv'

def preprocess():

    ohe_pickle_path = "ohe.pickle"
    minmax_pickle_path = "minmax_scaler.pickle"

    read_cleaned = s3.read_file_from_s3(bucket_name, s3_key + cleaned)
    df = pd.read_csv( read_cleaned)

    column=[ 'type_of_property', 'building_condition', 'kitchen_type', 'energy_class', 'heating_type',] # catagorical

    # using onehot encoder
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
    one_hot_encoded_array = ohe.fit_transform(df[column]).toarray()
    pickle.dump(ohe, open(s3_key + ohe_pickle_path, 'wb'))

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
    pickle.dump(minmax_scaler, open(s3_key + minmax_pickle_path, 'wb'))

    x_test[[ 'surface_of_the_plot', 'living_room_surface']]= minmax_scaler.transform(x_test[[ 'surface_of_the_plot', 'living_room_surface']])
    return x_train,y_train,x_test,y_test

def RandomForestReg(train_x,train_y, test_x,test_y):

    forest_pickle_path =  "forest.pickle"

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
    pickle.dump(forest, open(s3_key + forest_pickle_path, "wb"))
    return test_score

def training_model():
    x_train,y_train,x_test,y_test = preprocess()
    RandomForestReg(x_train,y_train,x_test,y_test)
    return

