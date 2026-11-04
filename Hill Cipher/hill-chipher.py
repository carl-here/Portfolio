import numpy as np


a = np.matrix([[2, 4, 0, 8],
               [0, 3, 2, 5], 
               [0, 0, 9, 8],
               [0, 0, 6, 3]])

b = np.matrix([[15], 
               [20], 
               [18],
               [19]])


print("matrise a ganger b er:", a @ b)
print("matrise a ganger b mod 29 er:",a @ b % 29)

a_invers = np.matrix([[15, 9, 1, 10],
                      [0, 10, 1, 0], 
                      [0, 0, 4, 28], 
                      [0, 0, 21, 12]])

print("matrise a ganger a invers er:", a @ a_invers % 29)

c = np.matrix([[1],
               [17],
               [24],
               [20]])

d = np.matrix([14, 11, 28, 23])

kristerHemmeligOrd = np.matrix([[2],
                                [2],
                                [13],
                                [12]])

print("cipher text matrise av kryptert ord ganger invers av nøkkelmatrise blir:", a_invers @ c % 29)
print("cipher text matrise av kristes ord ganger invers av nøkkelmatrise blir:", a_invers @ kristerHemmeligOrd % 29)
print("cipher text matrise av kristes ord ganger invers av nøkkelmatrise blir:", d @ a_invers % 29)
