
import numpy as np

from functions.data_functions import read_data
from functions.data_functions import preprocess_data
from functions.matrix_factorization import tutors_latent_features
from functions.recommendations import form_popularity_ratings
from functions.recommendations import get_top_recommendations
from functions.recommendations import form_similarity_ratings
from engine.recommendation_engine import Tutor_Recommendation_Engine

# =============================================================================
# state tutor_id for the problem
# =============================================================================
tutor_id = "ff0d3fb21c00bc33f71187a2beec389e9eff5332"

# =============================================================================
# state length of expected recommendation
# =============================================================================
recommendation_length = 10

# =============================================================================
# read data
# =============================================================================
data = read_data()

# =============================================================================
# preprcess data
# =============================================================================
data = preprocess_data(data)

# =============================================================================
# Making Populatity Rating 
# =============================================================================
popularity_tutors_rating = form_popularity_ratings(tutor_id, data)

# =============================================================================
# Initiate and train Tutor_Recommendation_Engine
# =============================================================================
random_state = np.random.RandomState(seed=12345)
engine = Tutor_Recommendation_Engine(random_state)
engine.train(data)

# =============================================================================
#1. Which tutors will your recommendation engine return given the tutor_id “ff0d3fb21c00bc33f71187a2beec389e9eff5332”? Will it work for any tutor_id of the dataset?
# =============================================================================
recommendation = engine.get_recommendations(tutor_id, recommendation_length)
print('Recommendations for {0} are'.format(tutor_id))
print(recommendation)

print('Top 15 popularity recommendations for tutor {0} :'.format(tutor_id))
print(popularity_tutors_rating.head(15))

for i in data.columns:
    try:
        recommendation = engine.get_recommendations(tutor_id, recommendation_length)
        if len(recommendation) < recommendation_length:
            print(i, 'Fail')
    except:
        print(i, 'Fail')
        



