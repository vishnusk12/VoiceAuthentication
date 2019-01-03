# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:06:13 2018

@author: Vishnu
"""

import os
import uuid
from pydub import AudioSegment
import io
from pydub.utils import which

path = os.getcwd() + '/VoiceAuthentication/VoiceAuthentication'

#signing up using voice
def folder(login):
    response = {}
    if login != '':
        current_path = path + '/' + 'speaker_models'
        file_list = os.listdir(current_path)
        if login + '.pkl' in file_list:
            response['message'] = 'Login ID already exists.'
            return response   
        else:
            try:
                os.mkdir(path + '/' + login)
                response['message'] = 'Sign Up successful.'
                return response
            except:
                response['message'] = 'Login ID already exists.'
                return response
                
    else:
        response['message'] = 'Please enter login id'
        return response 
      
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

#saving 5 training samples to the folder with login name
def save(login, file):
    if login != '':
        try:
            current_path = path + '/' + login
            for chunk in file.chunks():
                AudioSegment.converter = which("ffmpeg")
                Audio = AudioSegment.from_file(io.BytesIO(chunk), format="wav")
                normalized_audio = match_target_amplitude(Audio, -20.0)
                file_path = os.path.join(current_path, login + uuid.uuid4().hex) 
#                 ubmfile_path = os.path.join(path + '/' + 'UBM', login + uuid.uuid4().hex)
                normalized_audio.export(file_path + '.wav', format="wav")
#                 normalized_audio.export(ubmfile_path + '.wav', format='wav')
        except:
            pass
