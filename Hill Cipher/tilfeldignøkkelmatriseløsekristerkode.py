import numpy as np
import random
from math import gcd
from numpy.linalg import det

# Funksjon for å sjekke om en 2x2-matrise er invertibel modulo 29
def er_invertibel(matrise, mod=29):
    det_verdi = int(round(det(matrise)))
    return gcd(det_verdi, mod) == 1


hemmeligOrd = np.matrix([25, 3, 22, 24])


#kode som gjør matrise tallene om til bokstaver
alfabetet = "abcdefghijklmnopqrstuvwxyzæøå"

def cipherTilPlainText(matrise):
    # Gjør matrisen om til en flat liste med tall
    tall = np.asarray(matrise).flatten()
    
    return ''.join(alfabetet[int(i)] for i in tall)

for i in range(100):   
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    c = random.randint(0, 100)
    d = random.randint(0, 100)
    e = random.randint(0, 100)
    f = random.randint(0, 100)
    g = random.randint(0, 100)
    h = random.randint(0, 100)
    i = random.randint(0, 100)
    j = random.randint(0, 100)
    k = random.randint(0, 100)
    l = random.randint(0, 100)
    
    a_invers = np.array([[a, b, c, d],
                         [e, f, g, h],
                         [i, j, k, l]])
    
    if not er_invertibel(a_invers):
        continue  # Hopp over hvis ikke invertibel
    
    dekryptert = hemmeligOrd.T @ a_invers % 29


    ordet = cipherTilPlainText(dekryptert)
    
    forbudte_bokstaver = {"z", "x", "c", "q", "w"}

    ordet = cipherTilPlainText(dekryptert)
    
    if (not any(bokstav in ordet for bokstav in forbudte_bokstaver)
        and len(set(ordet)) == len(ordet)):
            
            print(ordet)

    print(f"{cipherTilPlainText(dekryptert)}")
    


