import numpy as np

# Oppgavedel (a) #########################################
x0 = 0          # Startverdi
tol = 1e-5      # Toleranse for avvik

def fikspunkt():
    x = x0
    na = 0  # Antall iterasjoner
    while True:
        gx = (np.cos(x)) / 2  # Fikspunktfunksjonen
        avvik = abs(gx - x)
        na += 1  # Øk antall iterasjoner FØR vi sjekker avviket

        if avvik <= tol:
            xa = gx
            return xa, na

        x = gx

# Kjør funksjonen og lagre resultatene
xa, na = fikspunkt()

# Lagre resultatene i variablene du ønsker
na = na
xa = xa

# Oppgavedel (b) #########################################

tolb = 1e-3

def gb(x): # Fikspunkt funksjonen
    x = x0
    na = x0
    while True:
        gbx = (2*x*(np.sin(x)+1)+np.cos(x))/(4+2*np.sin(x))
        avvik = abs(gbx-x)
        na +=1
        
        if avvik <= tolb:
            xb = gbx
            return xb, nb
        
xb, nb = fikspunkt()

xb = xb
nb = nb
print(fikspunkt())

#oppgave 9 newtons metode 
#orker ikke hilsen charlie kl. 14:45 på en lørdag
