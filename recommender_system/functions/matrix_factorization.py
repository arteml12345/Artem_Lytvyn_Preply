
import copy
import numpy as np
from sklearn.decomposition import NMF
import pandas as pd

def tutors_latent_features(input_data,
                           step=None,
                           start=None,
                           stop=None,
                           stopping_criteria=0.2,
                           random_state=None):
    """
    Calculates tutors latent features based on user-tutor interaction matrix.

    Parameters
    ----------
    input_data : pandas.DataFrame
        DataFrame with user-tutor interactions. Index of DataFrame should be
        ids of users and columns of DataFrame should be ids of tutors.
    step : int, optional
        step for search of optimal number of latent features. 
        The default is None.
    start : int, optional
        start for search of optimal number of latent features. 
        The default is None.
    stop : int, optional
        stop for search of optimal number of latent features. 
        The default is None.
    stopping_criteria : float, optional
        Error theshold that when reached will break seach for optimal number
        of latent features. If Error theshold is not reached process will
        continue until "stop" parameter is reached.
        The default is 0.2.
    random_state : np.random.RandomState, optional
        Random state used for search of optimal number of latent features. 
        The default is None.

    Returns
    -------
    tutors_latent_factors : pandas.DataFrame
        Tutors latent features. Each column is avector of latemt features of
        corresponding tutor.

    """
    data = copy.deepcopy(input_data)
    
    X = data.values
    
    if step is None:
        step = max(1, round(X.shape[1]/10))
    if start is None:
        start = step
    if stop is None:
        stop = round(X.shape[1]/2) + step
    if random_state is None:
        random_state = np.random.RandomState(seed=12345)

    for i in range(start, stop, step):
        random_state = random_state
        model = NMF(n_components=i, init='random', random_state=random_state)
        model = model.fit(X)
        err = model.reconstruction_err_
        if err <= stopping_criteria:
            break
    tutors_latent_factors = model.components_
    
    tutors_latent_factors = pd.DataFrame(data=tutors_latent_factors, 
                                         columns=data.columns)

    return tutors_latent_factors