
import copy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def form_similarity_ratings(tutor_id, tutors_latent_factors):
    """
    Form sorted in dexcending order tutors' similarity ratings relevant 
    for tutor_id. 

    Parameters
    ----------
    tutor_id :  str
        tutor id.
    tutors_latent_factors : pandas.DataFrame
        Tutors latent features. Each column is avector of latemt features of
        corresponding tutor.

    Returns
    -------
    tutors_similarity : pandas.Series
        Sorted in dexcending order tutors' ratings.
        
    """
    
    data = copy.deepcopy(tutors_latent_factors)
    tutor_data = data[tutor_id]
    other_tutors_data = data.drop(tutor_id, axis=1)
    similarity = []
    X = np.array(tutor_data.values.tolist()).reshape(1, -1)
    for i in other_tutors_data:
        Y = np.array(other_tutors_data[i].values.tolist()).reshape(1, -1)
        similarity.append(cosine_similarity(X, Y)[0][0])
    tutors_similarity = pd.Series(data=similarity, 
                                  index=other_tutors_data.columns.tolist())
    tutors_similarity = tutors_similarity.sort_values(ascending=False)
    
    return tutors_similarity

def form_popularity_ratings(tutor_id, input_data):
    """
    Form sorted in dexcending order tutors' ratings relevant for tutor_id.

    Parameters
    ----------
    tutor_id : str
        tutor id.
    input_data : pandas.DataFrame
        DataFrame with user-tutor interactions. Index of DataFrame should be
        ids of users and columns of DataFrame should be ids of tutors.

    Returns
    -------
    related_tutors_rating : pandas.Series
        Sorted in dexcending order tutors' ratings.

    """
    data = copy.deepcopy(input_data)
    
    tutor_data = data[tutor_id]
    users = tutor_data[tutor_data > 0].index.values.tolist()
    users_data = data[data.index.isin(users)]
    related_tutors = users_data.max()
    related_tutors = related_tutors[related_tutors.index != tutor_id]
    related_tutors = related_tutors[related_tutors > 0].index.values.tolist()
    related_tutors_rating = data[related_tutors].sum()
    related_tutors_rating = related_tutors_rating.sort_values(ascending=False)
    
    return related_tutors_rating

def shuffle_bounds(ratings, recommendation_length):
    """
    Looks for bounds of subarray that needs to be shuffles

    Parameters
    ----------
    ratings : list of ints
        ratings list to analyse.
    recommendation_length : int
        length of a recommendation.

    Returns
    -------
    left_bound : int
        left bound of sub array of rating to shuffle.
    right_bound : TYPE
        right bound of sub array of rating to shuffle.

    """
    ratings_len = len(ratings)
    counter = recommendation_length
    while True:
        if ratings[counter] == ratings[counter-1]:
            counter = counter + 1
        else:
            right_bound = counter - 1
            break
        if counter >= ratings_len - 1:
            right_bound = ratings_len - 1
            break
    counter = recommendation_length-1
    while True:
        if ratings[counter] == ratings[counter-1]:
            counter = counter - 1
        else:
            left_bound = counter
            break
        if counter <= 0 :
            left_bound = 0
            break
    return left_bound, right_bound

def get_top_recommendations(related_tutors_rating,
                            recommendation_length,
                            random_state=None):
    """
    Returns recommendation for "tutor_id" with length equal to 
    "recommendation_length" based on "input_data" 

    Parameters
    ----------
    related_tutors_rating : pandas.Series
        Sorted in dexcending order tutors' ratings.
    recommendation_length : int
        length of a recommendation
    random_state : np.random.RandomState, optional
        random state under which shuffling of tutors for recommendation will be
        performed if needed. 
        The default is None.

    Returns
    -------
    recommendation : list
        Recommendation for "tutor_id".

    """
    if random_state is None:
        random_state = np.random.RandomState(seed=12345)
    
    # if some tutors have same ratings shuffle them before giving recommendation
    ratings = related_tutors_rating.values.tolist()
    if len(ratings) <= recommendation_length:
        recommendation = related_tutors_rating.index.tolist()
    else:
        needs_to_shuffle = False
        if ratings[recommendation_length] == ratings[recommendation_length-1]:
            needs_to_shuffle = True
        if needs_to_shuffle:
            left_bound, right_bound = shuffle_bounds(ratings, 
                                                     recommendation_length)
        
        recommendation = related_tutors_rating.index.tolist()
        if not needs_to_shuffle:
            recommendation = recommendation[:recommendation_length]
        else:
            recommendation_left = recommendation[:left_bound]
            shuffle_list = recommendation[left_bound:right_bound]
            random_state.shuffle(shuffle_list)
            recommendation_right = shuffle_list[:recommendation_length-left_bound]
            recommendation = recommendation_left + recommendation_right
    
    return recommendation