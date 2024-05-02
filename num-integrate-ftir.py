import numpy as np
import scipy.integrate
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd

def process_single_file(test, wavenumber_range):
    """
    Args:
        test: path to .CSV
        wavenumber_range (tuple): (start, end)
    """
    with test.open("r") as f:
        lines = [x.split(",") for x in f.readlines()]
        x = np.array([float(x[0].strip()) for x in lines])
        y = np.array([float(x[1].strip()) for x in lines])

    total_auc = scipy.integrate.simpson(y, x)

    # wavenumbers not integers, get closest ones to desired start/end
    start = np.searchsorted(x, wavenumber_range[0])
    end = np.searchsorted(x, wavenumber_range[1])

    sucrose_auc = scipy.integrate.simpson(y[start:end], x[start:end])
    ratio = sucrose_auc / total_auc

    return total_auc, sucrose_auc, ratio


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
    main()