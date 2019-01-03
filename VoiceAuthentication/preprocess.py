# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 12:15:06 2018

@author: Vishnu
"""
#I/ps for building GMM model
import librosa
import os
from scipy import signal
import random

path = os.getcwd() + '/VoiceAuthentication/VoiceAuthentication'

def load_data(login, file):
    if file == '':
        current_path = path + '/' + login
        file_list = os.listdir(current_path)
        file_list = random.sample(file_list, 2)
        data_list = [librosa.load(current_path + '/' + i) for i in file_list]#signup #iterating through 5 training files in folder
        data_array = [i[0] for i in data_list]
        sr = list(set([i[1] for i in data_list]))
        return data_array, sr[0]#numpy array
    else:
        data_array, sr = librosa.load(file)# login# single file case while claiming
        return data_array, sr
       
def trim_silence(login, file):
    if file == '':
        y, sr = load_data(login, '')
        silenced_list = [librosa.effects.trim(i, top_db=12) for i in y]
        silenced_array = [i[0] for i in silenced_list]
        return silenced_array, sr
    else:
        y, sr = load_data(login, file)
        silenced_array, x = librosa.effects.trim(y, top_db=12)
        return silenced_array, sr

def denoise(login, file):
    if file == '':
        y, sr = trim_silence(login, '')
        medfilt_list =  [signal.medfilt(i).astype(dtype="float32") for i in y]
        return medfilt_list, sr#1D array
    else:
        y, sr = trim_silence(login, file)
        medfilt_list = signal.medfilt(y).astype(dtype="float32")
        return medfilt_list, sr
