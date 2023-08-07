import numpy as np
import pandas as pd

from normalizations import *
from mcdm_method import MCDM_method
from rank_preferences import *


class ARAS(MCDM_method):
    def __init__(self):
        pass

    def __call__(self, matrix, weights, types):
        ARAS._verify_input_data(matrix, weights, types)
        return ARAS._aras(matrix, weights, types)

    @staticmethod
    def _aras(matrix, weights, types):
        # Create optimal alternative
        A0 = np.zeros(matrix.shape[1])
        A0[types == 1] = np.max(matrix[:, types == 1], axis = 0)
        A0[types == -1] = np.min(matrix[:, types == -1], axis = 0)
        matrix = np.vstack((A0, matrix))
        # Normalize matrix using the sum normalization method
        norm_matrix = sum_normalization(matrix, types)
        # Calculate the weighted normalized decision matrix
        d = norm_matrix * weights
        S = np.sum(d, axis = 1)
        print(S)
        U = S / S[0]
        return U[1:]


def main():
    file_name = 'mobilki.csv'
    data = pd.read_csv(file_name, index_col = 'Ai')

    df_data = data.iloc[:len(data) - 1, :]
    df_types = data.iloc[len(data) - 1, :]
    types = df_types.to_numpy()
    matrix = df_data.to_numpy()

    list_alt_names = [r'$A_{' + str(i + 1) + '}$' for i in range(0, len(df_data))]

    results = pd.DataFrame(index = list_alt_names)

    weights = np.array([0.60338, 0.13639, 0.19567, 0.06456])

    aras = ARAS()
    pref = aras(matrix, weights, types)
    rank = rank_preferences(pref, reverse = True)
    results['Utility'] = pref
    results['Rank'] = rank
    print(results)


if __name__ == '__main__':
    main()