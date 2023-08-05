# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:56:48 2022

@author: BMU085
"""

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
    flag = False
    for vb in Vowel[::-1]:
        if vb in temp_name:
            n_vowels= temp_name.count(vb) # COunt how many times you see Vowels            
            temp_name = temp_name.replace(vb, "")
            Vclusters.append(vb)
            features[vb]=n_vowels
    return features

def gender(name):
    import unidecode
    from nltk.corpus import names
    name = unidecode.unidecode(name)
    name = name.capitalize()
    
    if name in names.words('male.txt'):
        gender = 'male'
    elif name in names.words('female.txt'):
        gender = 'female'
    else:
        import pickle

        classifier = open(r"dame_sexo.pickle", 'wb')
        pickle.load(classifier)
        classifier = classifier.classify(gender_features_luis(name))
        
    return gender