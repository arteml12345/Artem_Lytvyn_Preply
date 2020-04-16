
import numpy as np

from functions.matrix_factorization import tutors_latent_features
from functions.recommendations import get_top_recommendations
from functions.recommendations import form_popularity_ratings
from functions.recommendations import form_similarity_ratings

class Tutor_Recommendation_Engine:
    
    def __init__(self, random_state=None):
        """
        Tutor_Recommendation_Engine is an object that makes recomendations

        Parameters
        ----------
        random_state : numpy.random.RandomState, optional
            random state used for random operations. The default is None.

        Returns
        -------
        None.

        """
        self.data = None
        self.tutors_latent_factors = None
        if random_state is None:
            self.random_state = np.random.RandomState(seed=12345)
        else:
            self.random_state = random_state
    
    def train(self, input_data):
        """
        Trains recommendation engine

        Parameters
        ----------
        input_data : pandas.DataFrame
            user-tutor relation dataframe. Index is expected to be user ids.
            Columns are expected to be tutor ids.

        Returns
        -------
        None.

        """
        
        self.data = input_data
        
        self.tutors_latent_factors = tutors_latent_features(input_data=self.data, 
                                                            random_state=self.random_state)
        
    def get_popularity_recommendations(self, tutor_id, recommendation_length):
        """
        Returns the most popular tutors that users that viewed tutor_id also
        viewed

        Parameters
        ----------
        tutor_id : str
            tutor id.
        recommendation_length : int
            recommendation length.

        Returns
        -------
        recommendations : list
            list of tutors to recommend.

        """
        
        recommendations = None
        
        try:
            popularity_tutors_rating = form_popularity_ratings(tutor_id, self.data)
            recommendations = get_top_recommendations(popularity_tutors_rating,
                                                      recommendation_length,
                                                      self.random_state) 
        except:
            print('Popularity recommendations for tutor {0} has not been found'.format(tutor_id))
        
        return recommendations

    def get_similarity_recommendations(self, 
                                       tutor_id, 
                                       recommendation_length, 
                                       totors_to_ignore=[]):
        """
        Returns the most similar tutors to tutor_id 
        
        Parameters
        ----------
        tutor_id : str
            tutor id.
        recommendation_length : int
            recommendation length.
        totors_to_ignore : list of strings, optional
            List of tutors' ids to exlude from recommendation. 
            The default is [].

        Returns
        -------
        recommendations : list
            list of tutors to recommend.

        """
        
        recommendations = None
        
        try:
            tutors_latent_factors = self.tutors_latent_factors.drop(totors_to_ignore,
                                                                    axis=1)
            similarity_tutors_rating = form_similarity_ratings(tutor_id, 
                                                               tutors_latent_factors)
            recommendations = get_top_recommendations(similarity_tutors_rating,
                                                      recommendation_length,
                                                      self.random_state) 
        except:
            print('Similarity recommendations for tutor {0} has not been found'.format(tutor_id))
        
        return recommendations
            
    def get_recommendations(self, tutor_id, recommendation_length):       
        """
        Recommendation that combines popularity and similarity recommendation

        Parameters
        ----------
        tutor_id : str
            tutor id.
        recommendation_length : int
            recommendation length.

        Returns
        -------
        recommendations : list
            list of tutors to recommend.

        """
        
        recommendations = None
        
        popularity_recommendations = self.get_popularity_recommendations(tutor_id, recommendation_length)
        
        if popularity_recommendations is None:
            similarity_recommendations = self.get_similarity_recommendations(tutor_id, recommendation_length)
            recommendations = similarity_recommendations
            
        elif len(popularity_recommendations) == recommendation_length:
            recommendations = popularity_recommendations
            
        elif len(popularity_recommendations) < recommendation_length:
            missing_positions = recommendation_length - len(popularity_recommendations)
            similarity_recommendations = self.get_similarity_recommendations(tutor_id,
                                                                             missing_positions,
                                                                             popularity_recommendations)
            recommendations = popularity_recommendations + similarity_recommendations
        
        return recommendations
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            