import numpy as np

# 鲜明
def identity_kernel(iden=1.0):
    return np.array([[0, 0,    0],
                     [0, iden, 0],
                     [0, 0,    0]])
