
import pandas as pd
import copy

def read_data():
    """
    Reads data 'input_data/Preply_tutor_views_datasaet.csv'

    Returns
    -------
    data : pandas.DataFrame
        Read data.

    """
    data = pd.read_csv('input_data/Preply_tutor_views_datasaet.csv')
    return data

def preprocess_data(data_input):
    """
    Preprocesses data

    Parameters
    ----------
    data_input : pandas.DataFrame
        Data to preprocess.

    Returns
    -------
    data : pandas.DataFrame
        Preprocessed data.

    """
    data = copy.deepcopy(data_input)
    
    data = data.drop('id', axis=1)
    
    # exclude tutors that visited their own page
    data = data[data['user_id'] != data['tutor_id']]
    
    # exclude duplicates
    data = data.drop_duplicates()
    
    # make user-tutor matrix
    data['visit'] = 1
    data = data.pivot(index='user_id', 
                      columns='tutor_id', 
                      values='visit')
    data = data.fillna(0)
    
    return data