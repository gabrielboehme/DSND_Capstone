#Importing Libraries
import pandas as pd
import numpy as np

import zipfile
import sys
import os
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score

#-----Loading data-----#
def load_data():
    '''
    Input:-
    Output: DataFrames for training the model
    '''

    with zipfile.ZipFile('Data/Blight_Violations.zip', 'r') as zip_ref:
        zip_ref.extractall('Data/')

    train = pd.read_csv('Data/train.csv', encoding = "ISO-8859-1")
    test = pd.read_csv('Data/test.csv')
    addresses = pd.read_csv('Data/addresses.csv')
    latlons = pd.read_csv('Data/latlons.csv')

    return train, test, addresses, latlons

#-----Pre-processing Data-----#
def pre_process_data(train, test, addresses, latlons):
    '''
    Input: DataFrames for training the model
    Output: Processed DataFrames for training the model
    '''

    
    # drop all rows with Null compliance
    train = train[np.isfinite(train['compliance'])]

    # drop all rows not in the U.S
    train = train[train.country == 'USA']
    test = test[test['country'] == 'USA']

    # merge latlons and addresses with data
    train = pd.merge(train, pd.merge(addresses, latlons, on='address'), on='ticket_id')
    test = pd.merge(test, pd.merge(addresses, latlons, on='address'), on='ticket_id')

    # drop all unnecessary columns
    train.drop(['agency_name', 'inspector_name', 'violator_name', 'non_us_str_code', 'violation_description', 
                'grafitti_status', 'state_fee', 'admin_fee', 'ticket_issued_date', 'hearing_date',
                # columns not available in test
                'payment_amount', 'balance_due', 'payment_date', 'payment_status', 
                'collection_status', 'compliance_detail', 
                # address related columns
                'violation_zip_code', 'country', 'address', 'violation_street_number',
                'violation_street_name', 'mailing_address_str_number', 'mailing_address_str_name', 
                'city', 'state', 'zip_code', 'address'], axis=1, inplace=True)
    

    # discretizing relevant columns
    label_encoder = LabelEncoder()
    label_encoder.fit(train['disposition'].append(test['disposition'], ignore_index=True))

    train['disposition'] = label_encoder.transform(train['disposition'])
    test['disposition'] = label_encoder.transform(test['disposition'])

    label_encoder = LabelEncoder()
    label_encoder.fit(train['violation_code'].append(test['violation_code'], ignore_index=True))
    train['violation_code'] = label_encoder.transform(train['violation_code'])
    test['violation_code'] = label_encoder.transform(test['violation_code'])

    train['lat'] = train['lat'].fillna(train['lat'].mean())
    train['lon'] = train['lon'].fillna(train['lon'].mean())
    
    test['lat'] = test['lat'].fillna(test['lat'].mean())
    test['lon'] = test['lon'].fillna(test['lon'].mean())

    train_columns = list(train.columns.values)
    train_columns.remove('compliance')
    test = test[train_columns]

    #test.to_csv('Data/teste1.csv')

    return train, test

#-----Training the model-----#
def blight_model(train, test):
    '''
    Input: Processed DataFrames for training the model
    Output: Machine Learning model
    '''

    X_train, X_test, y_train, y_test = train_test_split(train.ix[:, train.columns != 'compliance'], train['compliance'])
    regr_rf = RandomForestRegressor()

    grid_values = {'n_estimators': [10, 100], 'max_depth': [None, 30]}
    model = GridSearchCV(regr_rf, param_grid=grid_values, scoring='roc_auc')
    
    return X_train, y_train, model

#-----Saving the model in pickle format-----#
def save_model(model):
    '''
    Input: Trained Machine Learning Model
    Output: Binary file (pickle) with ML Models
    '''

    #create output directory
    try:
        os.makedirs('Model')

    except OSError:
        None 


    # save model binary 
    pickle.dump(model, open('Model/Classifier.pkl', 'wb'))

    return None


#-----Executing code------#
def main():

    print('\nLoading data...')
    train, test, addresses, latlons = load_data()
    
    train, test = pre_process_data(train, test, addresses, latlons)
    print('\nProcessing data...')
    
    print('\nBuilding model...')
    X_train, y_train, model = blight_model(train, test)
    
    print('Training model...')
    model.fit(X_train, y_train)

    print('\nGrid best parameter (max. AUC): ', model.best_params_)
    print('\nGrid best score (AUC): ', model.best_score_)

    print('\nSaving model...')
    save_model(model)

    print('Trained model saved!')

    return None


#-----Execute------
if __name__ == '__main__':
    main()
