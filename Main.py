import os.path, timeit
from Functions import main

nik = timeit.default_timer()

# Some really shit file reading code.
windtunnel_folder = 'C:/Users/wing/Desktop/wing\'s stuff/TUD/yr 1/q4/python/coding/wind tunnel thermal data code'
folder = windtunnel_folder + '/thermal 3d csv files/'
aoa_folders = os.listdir(folder)
aoa_folders.sort()
dir2 = []

# Creating a list for all the directory paths
for q in range(len(aoa_folders)):
    dir2.append(folder + aoa_folders[q] + "/")

# running the main function over every folder under /thermal/
for i in range(len(dir2)):
    main(i, aoa_folders[i], dir2)
    bak = timeit.default_timer()
    elapsed_time = bak - nik
    print("Elapsed time: ", elapsed_time, "seconds (" + str(round(elapsed_time/60, 2)) + " mins) \n\n")

nak = timeit.default_timer()
time = nak - nik
print("Total Processing time:", time, "seconds (" + str(round(time/60, 2)) + " mins) \n\n")
