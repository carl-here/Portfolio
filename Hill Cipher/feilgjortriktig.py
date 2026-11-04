import numpy as np


a = np.array([[2, 4, 0, 8],
               [0, 3, 2, 5], 
               [0, 0, 9, 8],
               [0, 0, 6, 3],
               ])

b = np.array([15, 20, 18, 19])


print("matrise a ganger b mod 29 er:", a @ b.T % 29 )

b1 = np.array([15, 20])
b2 = np.array([18, 19])

a1 = np.array([[2, 4],
               [0, 3]])

a2 = np.array([[9, 8],
               [6, 3]])

print("kryptert med to små matriser:", a1 @ b1.T % 29, a2 @ b2.T % 29)uu



