
from testing.tests import preprocess_data_test
from testing.tests import form_similarity_ratings_test
from testing.tests import form_popularity_ratings_test
from testing.tests import shuffle_bounds_test
from testing.tests import get_top_recommendations_test
from testing.tests import tutors_latent_features_test
from testing.tests import Tutor_Recommendation_Engine_test

if __name__ == "__main__":
    preprocess_data_test()
    form_similarity_ratings_test()
    form_popularity_ratings_test()
    shuffle_bounds_test()
    get_top_recommendations_test()
    tutors_latent_features_test()
    Tutor_Recommendation_Engine_test()
