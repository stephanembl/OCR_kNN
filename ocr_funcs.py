import os
import sys
import numpy as np
import cv2
import json
from math import floor
from flask import jsonify
from matplotlib import pyplot as plt

# Fonction appelée par l'API
def scan_letter_from_api(filename):
    print("OCR - Machine Learning")
    print("bartho_c - crouze_t - mombul_s - wriszt_j")

    if os.path.isfile(filename) == False:
        print("Bad test file.")
        json = {
            'result': '',
            'error': 'Bad file'
        }
        return json

    cells = build_samples(filename)
    ret,result,neighbours,dist = train_knn(filename, cells)
    json = handle_results(ret, result, neighbours, dist)
    return json

# Cette fonction génère toutes les cases de notre tableau d'échantillons
def build_samples(filename):
    dn = os.path.dirname(os.path.realpath(__file__))
    j = 1
    cells = []
    tmp_arr = []
    sample_dir = dn + '/samples/55x_dataset/'
    os.chdir(sample_dir)
    samples = filter(os.path.isfile, os.listdir(sample_dir))
    samples = [os.path.join(sample_dir, s) for s in samples] # On récupère le chemin complet de chaque image
    samples.sort(key=os.path.getmtime) # On tri par date

    print("Cleaning and building samples...")
    for i in samples: # On traite chaque échantillon
        img = cv2.imread(i) # Ouverture avec OpenCV
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Passage en nuance de gris pour plus de précision
        tmp_arr.append(gray) # on rempli notre ligne 
        j = j + 1
        if j > 54:
            # on passe à la ligne suivante (chaque ligne représente
            # une lettre et contient autant de cases que d'échantillons de la lettre)
            cells.append(tmp_arr)
            tmp_arr = []
            j = 1

    return cells

def train_knn(filename, cells):
    # On ouvre l'image
    try:
        img_test = cv2.imread(filename)
    except cv2.error:
        print("Bad file.")
        exit()

    width = 100
    height = 75
    area = width * height
    
    gray_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY) # Passage en nuance de gris pour plus de précision
    cells_test = [[gray_test]]

    # On crée nos np arrays
    x = np.array(cells)
    x_test = np.array(cells_test)

    # On applati notre tableau pour que chaque case ne soit représentée
    # que sur une ligne (une img 20x20 produira une case de 1*400 (400=20*20))
    train = x[:,:54].reshape(-1,area).astype(np.float32)
    test = x_test[0].reshape(-1,area).astype(np.float32)

    # On crée un tableau contenant les décimaux ASCII de chacun des caractères de nos échantillons
    # le tableau est de la même taille que "train", il contient donc 54 cases pour chaque décimale ASCII
    # knn pourra ainsi lier chaque image à son index ASCII et nous la retourner
    k = [48,49,50,51,52,53,54,55,56,57,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122]
    train_labels = np.repeat(k,54)[:,np.newaxis]
    
    print("Training in progress...")
    knn = cv2.KNearest() # On crée notre instance de KNN, l'algo du voisin le plus proche
    knn.train(train,train_labels) # On entraine notre programme avec nos échantillons

    # On demande ensuite de comparer l'image de test avec ce qu'il a appris pour
    # nous sortir les voisins s'en rapprochant le plus (5 voisins max)
    return knn.find_nearest(test,k=5)

def handle_results(ret, result, neighbours, dist):
    padding = 0
    accuracy_outer = 0

    # On set le padding selon si le résultat est une minuscule ou une majuscule
    # Le padding nous permettra de vérifier si la lettre opposée n'est pas également dans les voisins. Exemple :
    # - Si le résultat est un "c" minuscule à 60% et qu'il y a le "C" majuscule dans les voisins proches à 20%
    #   on considère qu'on a trouvé "c" avec 80% de précision
    if result[0][0] >= 65 and result[0][0] <= 90:
        padding = 32
    elif result[0][0] >= 97 and result[0][0] <= 122:
        padding = -32

    accuracy = float((neighbours == result[0][0]).sum())
    if padding != 0:
        accuracy_outer = float((neighbours == (result[0][0] + padding)).sum())

    # Format du pourcentage
    accuracy_print = '{:.0%}'.format(float((float(accuracy) + float(accuracy_outer)) / neighbours.size))

    # On affiche le résultat
    print("Result(s):")
    print("Character found: " + chr(int(result[0][0]))) + " (" + accuracy_print +" accurate)"

    # Et on affiche les voisins que kNN nous a également retourné
    print("Other possibilities:")
    others = []
    for character in set(neighbours[0]):
        if character != result[0][0] and character != (result[0][0] + padding):
            accuracy = '{:.0%}'.format(float((neighbours == character).sum()) / neighbours.size)
            print("Character found: " + chr(int(character))) + " (" + accuracy +" accurate)"
            other = {
                'char': chr(int(character)),
                'accuracy': accuracy
            }
            others.append(other)
    
    list = {
        'result': {
            'char': chr(int(result[0][0])),
            'accuracy': accuracy_print
        },
        'others': others
    }

    return list

def main():
    if len(sys.argv) != 4:
        print("Usage: ocr.py x y fullpath_to_image")
        exit()

    if os.path.isfile(sys.argv[3]) == False:
        print("Bad test image.")
        exit()

    scan_letter_from_api(sys.argv[3])

if __name__ == "__main__":
    main()
