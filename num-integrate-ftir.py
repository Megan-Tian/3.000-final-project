import numpy as np
import scipy.integrate
from pathlib import Path

# PARAMETERS
def process_single_file(test, wavenumber_range):
    '''
    Args: 
        test: path to .csv
        wavenumber_range (tuple): (start, end)
    '''
    with test.open('r') as f:
        lines = [x.split(',') for x in f.readlines()]
        x = np.array([float(x[0].strip()) for x in lines])
        y = np.array([float(x[1].strip()) for x in lines])

    total_auc = scipy.integrate.simpson(x, y)
    
    # wavenumbers not integers, get closest ones to desired start/end
    start = np.searchsorted(x, wavenumber_range[0]) 
    end = np.searchsorted(x, wavenumber_range[1])
    
    sucrose_auc = scipy.integate.simpson(x[start:end], y[start:end])
    ratio = sucrose_auc / total_auc

    return total_auc, sucrose_auc, ratio


def main():
    data = Path('data')
    # initialize np array to hold results
    results = np.empty((1, 6), float)
    # - col 1: sample number
    # - col 2: full AUC (A)
    # - col 3: AUC B
    # - col 4: AUC C
    # - col 5: ratio B/A
    # - col 6: ratio C/A

    for file in data.iterdir():
        if not file.endswith('.csv'):
            continue
        total_auc, sucrose_auc, ratio = process_single_file(file, (750, 1500))
        total_auc_2, sucrose_auc_2, ratio_2 = process_single_file(file, (3000, 3500))

        np.append(results, [file, total_auc, sucrose_auc, sucrose_auc_2, ratio, ratio_2])
    
    results.tofile('results.csv', sep = ',')


if __name__ == "__main__":
    main()
