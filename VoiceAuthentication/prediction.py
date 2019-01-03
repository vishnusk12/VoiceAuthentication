'''
Created on 16-Oct-2018

@author: Vishnu
'''

from VoiceAuthentication.Features import mfcc
from sklearn.externals import joblib
import os
from sklearn.neighbors import LSHForest
from sklearn.metrics import pairwise_distances_argmin_min

path = os.getcwd() + '/VoiceAuthentication/VoiceAuthentication'

def predict(login, file):
    login_features = mfcc(login, file)
    lshf = LSHForest(random_state=42)
    gmm = joblib.load(path + '/speaker_models/' + login + '.pkl')
    ubm = joblib.load(path + '/speaker_models/' + 'ubm.pkl')
    model = joblib.load(path + '/speaker_models/' + login + 'Model.pkl')
    gmm_likelihood_score = gmm.score(login_features)
    ubm_likelihood_score = ubm.score(login_features)
    likelihood_score = gmm_likelihood_score - ubm_likelihood_score
    login_features = [j for i in login_features for j in i]
    if len(model) > len(login_features):
        array = model[:len(login_features)]
        lshf.fit([array])
        distances, indices = lshf.kneighbors([login_features], n_neighbors=2)
        dist = pairwise_distances_argmin_min([array], [login_features])
    else:
        array = login_features[:len(model)]
        lshf.fit([array])
        distances, indices = lshf.kneighbors([model], n_neighbors=2)
        dist = pairwise_distances_argmin_min([array], [model])
    result = {}
    result['score'] = [likelihood_score, distances]
    result['distance'] = dist
    if likelihood_score > 0:
        result['Message'] = 'Authenticated'
    else:
        result['Message'] = 'Not Authenticated'   
    return result
