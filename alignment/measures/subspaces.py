import time

import scipy
import numpy as np
from sklearn.decomposition import PCA

from alignment.utils import find_repeat

def distance(X, A, Y, k_X, k_A, k_Y):

    subspace_X = subspace_pca(X, k_X)
    subspace_A = subspace_eigendecomposition(A, k_A)
    subspace_Y = subspace_pca(Y, k_Y)

    angles_X_A = prinAngles(subspace_X, subspace_A)
    angles_X_Y = prinAngles(subspace_X, subspace_Y)
    angles_A_Y = prinAngles(subspace_A, subspace_Y)

    d_X_A = chordal(angles_X_A)
    d_X_Y = chordal(angles_X_Y)
    d_A_Y = chordal(angles_A_Y)

    d_X_A_Y = np.sqrt(2 * (np.power(d_X_A,2) + np.power(d_X_Y,2) + np.power(d_A_Y,2)))

    return d_X_A_Y


def chordal(angles):
    return np.linalg.norm(np.sin(angles))
    
# subspace of a matrix by PCA where k is the dimension of subspace
def subspace_pca(X, k):
    pca = PCA(n_components=k)
    pca.fit(X)
    return pca.transform(X)

# subspace of graph
def subspace_eigendecomposition(A, k):
    vals, vecs = scipy.linalg.eigh(A, eigvals=(A.shape[0]-k, A.shape[0]-1))
    vals_unique_sorted = sorted(list(set(vals)), reverse=True)

    vecs_ordered = []
    for i in vals_unique_sorted:
        index_temp = find_repeat(list(vals), i)
        for j in index_temp:
            vec = vecs[:,j]
            vecs_ordered.append(vec)

    return np.array(vecs_ordered).transpose().reshape(A.shape[0], k)

# principal angles
def prinAngles(A, B):
    Q_A, R_A = scipy.linalg.qr(A, mode='economic')
    Q_B, R_B = scipy.linalg.qr(B, mode='economic')

    U, C, Vh = scipy.linalg.svd(np.dot(Q_A.transpose(),Q_B), full_matrices=False)

    angles = np.arccos(np.clip(C, -1., 1.))
    angles.sort()

    return angles