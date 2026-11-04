import numpy as np

alfabetet = "abcdefghijklmnopqrstuvwxyzæøå"


d = np.matrix([25, 3, 22, 24])



a_invers = np.matrix([[15, 9, 33, 10],
                      [44, 12, 1, 0], 
                      [10, 0, 14, 8], 
                      [22, 91, 0, 12]])




print("cipher text matrise av kristes ord ganger invers av nøkkelmatrise blir:", d @ a_invers % 29)
#print(result.append(int((alfabetet.index))))
