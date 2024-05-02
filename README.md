DATA: 
- csv 
- x: wavenumbers (col 1)
- y: spectra peak? idk y axis on the graph (col 2)

functions
- get everything into numpy array

actual integration:
- params: lower x bound, upper x bound

main:
- initialize np array to hold all processed data
    - col 1: sample number
    - col 2: full AUC (A)
    - col 3: AUC B
    - col 4: AUC C
    - col 5: ratio B/A
    - col 6: ratio C/A

- BIG LOOP
    - load csv of individual spectra
    - integrate full spectra (A)
    - integrate from 750-1500 wavenumbers (B)
    - integrate from 3000-3500 wavenumbers (C)
    - calculate rations B/A and C/A
    - add results to results np array

- dump results array into csv