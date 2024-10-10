# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 13:19:20 2023

@author: GFEEU

Pka's learning Quizz 
"""

import random

pka = {
        "Triethylamine" : 11,
        "Morpholine" : 8,
        "pyridine" : 5,
        "acide sulfuriqu" : -3,
        "NH4Cl" : 9,
        "OH-" : 14,
        "H3O+" : 0,
        "acide phosphorique" : 2,
        "Acide nitritique" : -2,
        "acide acetique" : 5,
        "Acide formique": 4,
        "Ammoniaque" : 9,
        "NaNH2" : 38,
        "DBU" : 12,
        "Phtalimide" : 8,
        "Succinimide" : 9.5,
        "DMAP" : 9,
        "guanidine" : 20,
        "imidazolium" : 7,
        "Aniline" : 4,
        "Trifluoroacetic acid" : 0,
        "potassium carbonate" : 10,
        "Phénol" : 10,
        "LDA" : 35, 
        "Malonate" : 11,
        "ROH" : 15, 
        "Tert-butoxide" : 18,
        "nBuLi" : 45,
        "Thiophenol" : 6,
        "LiHMDS" : 26,
       }  
 

def quizz_points():
    global pka
    counter = 0    
    points = 0

    if counter == 0:
        print("This is a pka game. You'll have 20 questions to answer")
        print("To stop the game, please enter ''stop''")
        print("")

    while counter < 20:
        reagent = random.choice(list(pka))
        print(f"{counter+1 }) Quel est le pKa de : {reagent}?")
        ask = input()
        if ask == str(pka[reagent]):
            print("This is a good answer !")
            print("------------------------------------------------")
            points += 1
            counter += 1
        elif ask == "stop" :
            return
        else:
            print(f"Wrong answer, the correct pKa is : {pka[reagent]}")
            print("------------------------------------------------")
            counter += 1
            
    if counter == 20:
        print("Game Over ! Your score is :")
        print(f" {points} / 20 !")
        print("Try again ?")
        ask = input()
        if ask in ["Yes", "Y", "yes", "y", "o"]:
            quizz_points()
        else :
            return
            

quizz_points()



           
        
