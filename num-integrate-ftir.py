import numpy as np
import scipy.integrate
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd

def process_single_file(test, wavenumber_range):
    """
    Args:
        test: path object to .CSV
        wavenumber_range (tuple): (start, end)
    """
    data = np.loadtxt(test, delimiter=",")
    x = data[:, 0]
    y = data[:, 1]

    total_auc = scipy.integrate.simpson(y, x)

    # wavenumbers not integers, get closest ones to desired start/end
    start = np.searchsorted(x, wavenumber_range[0])
    end = np.searchsorted(x, wavenumber_range[1])

    sucrose_auc = scipy.integrate.simpson(y[start:end], x[start:end])
    ratio = sucrose_auc / total_auc

    return total_auc, sucrose_auc, ratio


def sensitivity_single_file(file, wavenumber_range, split_size):
    '''
    Returns DF with total auc and auc/ratios of "slices" within the wavenumber_range ratio.
    Elementary sensitivity analysis - find which of the slices are most sensitive to sample changes

    Args:
        file: path object to .csv
        wavenumber_range (tuple): (start, end)
        split_size (int): size of each slice
    '''
    # assert (wavenumber_range[1] - wavenumber_range[0]) % split_size == 0
    total_auc, sucrose_auc, ratio = process_single_file(file, wavenumber_range)
    data = {'name': file.name, 'total_auc': total_auc}

    for start_slice in range(wavenumber_range[0], wavenumber_range[1], split_size):
        _, slice_auc, slice_ratio = process_single_file(file, (start_slice, start_slice + split_size))

        # data.update({f"auc_{start_slice}_{start_slice + split_size}" :
        #              slice_auc}) 
        data.update({f"ratio_{start_slice}_{start_slice + split_size}" :
                     slice_ratio}) 

    return data, list(data.keys())

def sensitivity_all_files(wavenumber_range, split_size):
    # just to get headers for dataframe this is so bad ack
    path = Path("data\\Ethiopia Genet 1.CSV")
    _, headers = sensitivity_single_file(Path("data\\Ethiopia Genet 1.CSV"), wavenumber_range, split_size)
    df = pd.DataFrame(columns=headers)

    # real code now
    data = Path("data")
    
    for file in data.iterdir():
        if not file.name.endswith(".CSV"):
            continue
        
        print(str(file))

        results, _ = sensitivity_single_file(file, wavenumber_range, split_size)

        df.loc[len(df)] = results

    df.to_csv(f'sensitvity_{wavenumber_range[0]}_{wavenumber_range[1]}_split_{split_size}.csv', ',', header=True)


def main():
    data = Path("data")
    # initialize np array to hold results
    df = pd.DataFrame(columns=['name', 'total1', 'suc1', 'ratio1', 'suc2', 'ratio2'])
    # - col 1: sample number
    # - col 2: full AUC (A) 'total1'
    # - col 3: AUC B 'suc1'
    # - col 4: AUC C 'ratio1'
    # - col 5: ratio B/A 'suc2'
    # - col 6: ratio C/A 'ratio2'
    # see README

    for file in data.iterdir():
        if not file.name.endswith(".CSV"):
            continue

        print(str(file))
        total_auc, sucrose_auc, ratio = process_single_file(file, (750, 1500))
        _, sucrose_auc_2, ratio_2 = process_single_file(file, (3000, 3500))

        df.loc[len(df)] = {
            'name': file.name,
            'total1': total_auc,
            'suc1': sucrose_auc,
            'ratio1': ratio,
            'suc2': sucrose_auc_2,
            'ratio2': ratio_2,
        }

    df.to_csv('results.csv', ',', header=True)



if __name__ == "__main__":
    result, _ = sensitivity_single_file(Path("data\\Ethiopia Genet 1.CSV"), (750, 1500), split_size=10)

    print(result)

    sensitivity_all_files((750, 1500), split_size=10)
    # main() 