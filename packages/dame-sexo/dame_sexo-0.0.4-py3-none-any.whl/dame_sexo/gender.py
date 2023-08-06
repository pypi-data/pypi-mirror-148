# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:56:48 2022

@author: BMU085
"""
from importlib import resources
import io
import unidecode
#from nltk.corpus import names
import pickle
import os
import numpy as np

male_path = "male.txt"
female_path = "female.txt"
model_path = 'dame_sexo.pickle'

def gender_features_luis(name):
    features = {}
    temp_name = name
    cons_clusters = ["bl", "br", "ch", "cl", "cr", "dr", "fl", "fr", 
                     "gl", "gr", "pl", "pr", "sc", "sh", "sk", "sl", 
                     "sm", "sn", "sp", "st", "sw", "th", "tr", "tw", 
                     "wh", "wr", "sch", "scr", "shr", "sph", "spl", 
                     "spr", "squ", "str", "thr"]
    features["firstletter"] = name[0].lower() 
    features["lastletter"] = name[-1].lower()
    features["first2"] = name[:2].lower() if len(name) > 3 else name[:1].lower() 
    features["last2"] = name[-2:].lower() if len(name) > 3 else name[-1:].lower()
    
    features["prefix"] = name[:3].lower() if len(name) > 4 else name[:2].lower() 
    features["suffix"] = name[-3:].lower() if len(name) > 4 else name[-2:].lower()
    clusters = []
    for cluster in cons_clusters[::-1]:
        if cluster in temp_name:
            temp_name = temp_name.replace(cluster, "")
            clusters.append(cluster)
    features["consonant_clusters_1"] = clusters[0] if len(clusters) > 0 else None
    features["consonant_clusters_2"] = clusters[1] if len(clusters) > 1 else None
    features["consonant_clusters_3"] = clusters[2] if len(clusters) > 2 else None
    Vowel = ['a','e','i','o','u']
    Vclusters = []
    #flag = False
    for vb in Vowel[::-1]:
        if vb in temp_name:
            n_vowels= temp_name.count(vb) # COunt how many times you see Vowels            
            temp_name = temp_name.replace(vb, "")
            Vclusters.append(vb)
            features[vb]=n_vowels
    return features


class Gender:

    def __init__(self):
        return

    def generate(self):
        
        with resources.open_text('dame_sexo', male_path) as fp:
            male_txt = fp.read()
        with resources.open_text('dame_sexo', female_path) as fp:
            female_txt = fp.read()
            
        this_dir, this_filename = os.path.split(__file__)  # Get path of data.pkl
        data_path = os.path.join(this_dir, 'dame_sexo.pickle')
        model = pickle.load(open(data_path, 'rb'))
        self = unidecode.unidecode(self)
        self = self.capitalize()
        if self in male_txt.split():
            gen = 'male'
        elif self in female_txt.split():
            gen = 'female'
        else:
            
            gen = model.classify(gender_features_luis(self))
            
        return gen
    
    def gencolumn(self):
        
        def columnas(name):
            gender = Gender.generate(name)
            return gender
        
        vfunct = np.vectorize(columnas)
        
        gender = vfunct(self)
        
        return gender
        
            