
import pandas as pd
import numpy as np
from sklearn.decomposition import NMF

from functions.matrix_factorization import tutors_latent_features
from functions.data_functions import preprocess_data
from functions.recommendations import form_similarity_ratings
from functions.recommendations import form_popularity_ratings
from functions.recommendations import shuffle_bounds
from functions.recommendations import get_top_recommendations
from engine.recommendation_engine import Tutor_Recommendation_Engine

def preprocess_data_test():
    data = [[1, 'tutor1', 'user1'],
            [2, 'tutor2', 'user2'],
            [3, 'tutor3', 'user3'],
            [4, 'tutor4', 'user4'],
            [5, 'tutor5', 'user5'],
            [6, 'tutor5', 'tutor5'],
            [7, 'tutor4', 'tutor4']]
    columns = ['id', 'tutor_id', 'user_id']
    data = pd.DataFrame(data=data, columns=columns)
    data = preprocess_data(data_input=data)
    etalon = pd.DataFrame(data=[[1.0, 0.0, 0.0, 0.0, 0.0], 
                                [0.0, 1.0, 0.0, 0.0, 0.0], 
                                [0.0, 0.0, 1.0, 0.0, 0.0], 
                                [0.0, 0.0, 0.0, 1.0, 0.0], 
                                [0.0, 0.0, 0.0, 0.0, 1.0]],
                          columns=['tutor1', 
                                   'tutor2', 
                                   'tutor3', 
                                   'tutor4', 
                                   'tutor5'],
                          index=['user1', 
                                 'user2', 
                                 'user3', 
                                 'user4', 
                                 'user5'])
    etalon.index = etalon.index.set_names('user_id')
    etalon.columns = etalon.columns.set_names('tutor_id')
    no_errors = True
    if not data.equals(etalon):
        no_errors = False
        raise Warning("preprocess_data_test FAILED")
    if no_errors:
        print('preprocess_data_test PASSED')
    else:
        print('preprocess_data_test FAILED')
        
def form_similarity_ratings_test():
    data = [[1, 0, 1, -1, 1],
            [0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0]]
    columns = ['tutor1', 'tutor2', 'tutor3', 'tutor4', 'tutor5',]
    data = pd.DataFrame(data=data, columns=columns)
    ratings = form_similarity_ratings(tutor_id='tutor1', 
                                      tutors_latent_factors=data)
    ratings = ratings.round(4)
    no_errors = True
    if not ratings.equals(pd.Series(data=[1.0,
                                          0.7071,
                                          0.0,
                                          -1.0], 
                                    index=['tutor3', 
                                           'tutor5',
                                           'tutor2',
                                           'tutor4'])):
        no_errors = False
        raise Warning("shuffle_bounds_test FAILED")
    if no_errors:
        print('form_similarity_ratings_test PASSED')
    else:
        print('form_similarity_ratings_test FAILED')

def form_popularity_ratings_test():
    data = [[1, 0, 1, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 1, 1, 0, 1]]
    columns = ['tutor1', 'tutor2', 'tutor3', 'tutor4', 'tutor5']
    index = ['user1', 'user2', 'user3']
    data = pd.DataFrame(data=data, columns=columns, index=index)
    ratings = form_popularity_ratings(tutor_id='tutor2', input_data=data)
    no_errors = True
    if not ratings.equals(pd.Series(data=[3,2], index=['tutor3', 'tutor5'])):
        no_errors = False
        raise Warning("shuffle_bounds_test FAILED")
    if no_errors:
        print('shuffle_bounds_test PASSED')
    else:
        print('shuffle_bounds_test FAILED')
        
def shuffle_bounds_test():
    no_errors = True
    ratings = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    recommendation_length = 5
    left_bound, right_bound = shuffle_bounds(ratings, recommendation_length)
    if (left_bound != 0) or (right_bound != 9):
        no_errors = False
        raise Warning("shuffle_bounds_test FAILED on 'ratings = {0}, recommendation_length = {1}'".format(ratings, recommendation_length))
    ratings = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
    recommendation_length = 5
    left_bound, right_bound = shuffle_bounds(ratings, recommendation_length)
    if (left_bound != 0) or (right_bound != 6):
        no_errors = False
        raise Warning("shuffle_bounds_test FAILED on 'ratings = {0}, recommendation_length = {1}'".format(ratings, recommendation_length))
    ratings = [1, 1, 1, 3, 3, 3, 3, 2, 2, 2]
    recommendation_length = 5
    left_bound, right_bound = shuffle_bounds(ratings, recommendation_length)
    if (left_bound != 3) or (right_bound != 6):
        no_errors = False
        raise Warning("shuffle_bounds_test FAILED on 'ratings = {0}, recommendation_length = {1}'".format(ratings, recommendation_length))
    ratings = [1, 1, 1, 1, 3, 3, 3, 2, 2, 2]
    recommendation_length = 5
    left_bound, right_bound = shuffle_bounds(ratings, recommendation_length)
    if (left_bound != 4) or (right_bound != 6):
        no_errors = False
        raise Warning("shuffle_bounds_test FAILED on 'ratings = {0}, recommendation_length = {1}'".format(ratings, recommendation_length))
    ratings = [1, 1, 1, 1, 3, 3, 3, 3, 3, 3]
    recommendation_length = 5
    left_bound, right_bound = shuffle_bounds(ratings, recommendation_length)
    if (left_bound != 4) or (right_bound != 9):
        no_errors = False
        raise Warning("shuffle_bounds_test FAILED on 'ratings = {0}, recommendation_length = {1}'".format(ratings, recommendation_length))
    if no_errors:
        print('shuffle_bounds_test PASSED')
    else:
        print('shuffle_bounds_test FAILED')

def get_top_recommendations_test():
    no_errors = True
    related_tutors_rating = pd.Series(data=[5, 4, 3, 2, 1], 
                                      index=['tutor5', 
                                             'tutor4',
                                             'tutor3',
                                             'tutor2',
                                             'tutor1'])
    recommendation_length = 3
    random_state = np.random.RandomState(seed=12345)
    recommendations = get_top_recommendations(related_tutors_rating,
                                              recommendation_length,
                                              random_state)   
    if recommendations != ['tutor5', 'tutor4', 'tutor3']:
        no_errors = False
        raise Warning("get_top_recommendations_test FAILED on test with unique ratings")

    related_tutors_rating = pd.Series(data=[5, 3, 3, 3, 1], 
                                      index=['tutor5', 
                                             'tutor4',
                                             'tutor3',
                                             'tutor2',
                                             'tutor1'])
    recommendation_length = 3
    random_state = np.random.RandomState(seed=1234567)
    recommendations = get_top_recommendations(related_tutors_rating,
                                              recommendation_length,
                                              random_state)   
    if recommendations != ['tutor5', 'tutor3', 'tutor2']:
        no_errors = False
        raise Warning("get_top_recommendations_test FAILED on test with duplicate ratings")

    related_tutors_rating = pd.Series(data=[5, 4, 3, 2, 1], 
                                      index=['tutor5', 
                                             'tutor4',
                                             'tutor3',
                                             'tutor2',
                                             'tutor1'])
    recommendation_length = 10
    random_state = np.random.RandomState(seed=1234567)
    recommendations = get_top_recommendations(related_tutors_rating,
                                              recommendation_length,
                                              random_state)   
    if recommendations != ['tutor5', 'tutor4', 'tutor3', 'tutor2', 'tutor1']:
        no_errors = False
        raise Warning("get_top_recommendations_test FAILED on test with short related ratings")


    if no_errors:
        print('get_top_recommendations_test PASSED')
    else:
        print('get_top_recommendations_test FAILED')

def tutors_latent_features_test():
    W = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
    H = np.array([[1, 2, 3], [4, 5, 6]])
    X = W.dot(H)
    random_state = np.random.RandomState(seed=12345)
    stopping_criteria = 0.2
    for i in range(1, 3, 1):
        random_state = random_state
        model = NMF(n_components=i, init='random', random_state=random_state)
        model = model.fit(X)
        err = model.reconstruction_err_
        if err <= stopping_criteria:
            break
    etalon = pd.DataFrame(data=model.components_, 
                          columns=['tutor1', 'tutor2', 'tutor3'])
    
    random_state = np.random.RandomState(seed=12345)
    data = pd.DataFrame(data=X, columns=['tutor1', 'tutor2', 'tutor3'])
    latent_features = tutors_latent_features(data, random_state=random_state)
    
    no_errors = True
    if not latent_features.equals(etalon):
        no_errors = False
        raise Warning("tutors_latent_features_test FAILED")
    if no_errors:
        print('tutors_latent_features_test PASSED')
    else:
        print('tutors_latent_features_test FAILED')

def Tutor_Recommendation_Engine_test():
    data = [[1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 1, 1]]
    index = ['user1', 
             'user2', 
             'user3', 
             'user4', 
             'user5']
    columns = ['tutor1', 
               'tutor2', 
               'tutor3', 
               'tutor4', 
               'tutor5', 
               'tutor6', 
               'tutor7']
    data = pd.DataFrame(data=data, index=index, columns=columns)
    
    tutor_id = 'tutor2'
    recommendation_length = 5
    
    popularity_tutors_rating = form_popularity_ratings(tutor_id, data)
    
    random_state = np.random.RandomState(seed=12345)
    tutors_latent_factors = tutors_latent_features(input_data=data, 
                                                   random_state=random_state)
    random_state = np.random.RandomState(seed=12345)
    popularity_recommendations = get_top_recommendations(popularity_tutors_rating,
                                                         recommendation_length,
                                                         random_state)
    similarity_tutors_rating = form_similarity_ratings(tutor_id, 
                                                       tutors_latent_factors)
    random_state = np.random.RandomState(seed=12345)
    similarity_recommendations = get_top_recommendations(similarity_tutors_rating,
                                                         recommendation_length,
                                                         random_state)
    s_recommendations = get_top_recommendations(similarity_tutors_rating,
                                                len(columns),
                                                random_state)
    s_recommendations = [i for i in s_recommendations if not i in popularity_recommendations]
    missing_positions = recommendation_length - len(popularity_recommendations)
    recommendations = popularity_recommendations + s_recommendations[:missing_positions]
    
    random_state = np.random.RandomState(seed=12345)
    engine = Tutor_Recommendation_Engine(random_state=np.random.RandomState(seed=12345))
    engine.train(input_data=data)
    engine_popularity_recommendations = engine.get_popularity_recommendations(tutor_id, 
                                                                              recommendation_length)
    engine_similarity_recommendations = engine.get_similarity_recommendations(tutor_id, 
                                                                              recommendation_length)
    engine_recommendations = engine.get_recommendations(tutor_id, 
                                                        recommendation_length)
    no_errors = True
    if not engine_popularity_recommendations == popularity_recommendations:
        no_errors = False
        raise Warning("Tutor_Recommendation_Engine_test FAILED on comparing popularity recommendations")
    elif not engine_similarity_recommendations == similarity_recommendations:
        no_errors = False
        raise Warning("Tutor_Recommendation_Engine_test FAILED on comparing similarity recommendations")
    elif not engine_recommendations == recommendations:
        no_errors = False
        raise Warning("Tutor_Recommendation_Engine_test FAILED on comparing total recommendations")
    if no_errors:
        print('Tutor_Recommendation_Engine_test PASSED')
    else:
        print('Tutor_Recommendation_Engine_test FAILED')