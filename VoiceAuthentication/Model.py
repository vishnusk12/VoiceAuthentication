# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:34:20 2018

@author: Vishnu
"""

from VoiceAuthentication.Features import mfcc
from sklearn.mixture import GaussianMixture 
from sklearn.externals import joblib
import os

path = os.getcwd() + '/VoiceAuthentication/VoiceAuthentication'

def model(login, file):
    if file == '':
        feature = mfcc(login, '')
        gmm = GaussianMixture(n_components = 8, max_iter = 200, 
                              covariance_type='diag', n_init = 3)
        gmm.fit(feature)
        joblib.dump(gmm, path + '/speaker_models/' + login + '.pkl')
        array = [j for i in feature for j in i]
        joblib.dump(array, path + '/speaker_models/' + login + 'Model.pkl')
    response = {}
    response['message'] = 'Model successfully built'
    return response
