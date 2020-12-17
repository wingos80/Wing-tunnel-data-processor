import os.path, timeit
from Functions import main

nik = timeit.default_timer()

# Some really shit file reading code.
windtunnel_folder = 'C:/Users/wing/Desktop/wing\'s stuff/TUD/yr 1/q4/python/coding/wind tunnel thermal data code'

# folder is where your csv files that you want to read are stored
folder = windtunnel_folder + '/thermal 3d csv files/'
aoa_folders = os.listdir(folder)
aoa_folders.sort()
dir2 = []

# Creating a list for all the directory paths
for q in range(len(aoa_folders)):
    dir2.append(folder + aoa_folders[q] + "/")

# running the main function over every folder under /thermal/
for i in range(len(dir2)):
    main(i, aoa_folders[i], dir2, windtunnel_folder)
    bak = timeit.default_timer()
    elapsed_time = bak - nik
    print("Elapsed time: ", elapsed_time, "seconds (" + str(round(elapsed_time/60, 2)) + " mins) \n\n")

nak = timeit.default_timer()
time = nak - nik
print("Total Processing time:", time, "seconds (" + str(round(time/60, 2)) + " mins) \n\n")



# Examples for plotting data from the text files

# Plotting example of a pressure distribution (cp file)
# Reynolds number can be accessed with data[0, y_dataset - 1]
# Angle of Attack can be accessed with data[1, y_dataset - 1]
#y_dataset = 2 # Column number of desired data set in cp file
#data = read_data("D:/courses/Windtunnel test/AE2130-II G25/2D/experimental/cp_test.txt").T
#plt.xlabel(data[0][1])
#plt.ylabel("C_p")
#plt.plot(data[0, 2:].astype(numpy.float, casting = "unsafe"), data[y_dataset - 1, 2:].astype(numpy.float, casting = "unsafe"))
#plt.show()

# Plotting example of data in the press file
#x_dataset = 2 # Column number of the desired data set in the press file, for example 2 when x-axis is Angle of Attack
#y_dataset = 4 # Column number of the desired data set in the press file, for example 4 when y-axis is lift coefficient
#data = read_data("D:/courses/Windtunnel test/AE2130-II G25/2D/experimental/press_test.txt").T
#plt.xlabel(data[x_dataset - 1][0])
#plt.ylabel(data[y_dataset - 1][0])
#plt.plot(data[x_dataset - 1, 2:].astype(numpy.float, casting = "unsafe"), data[y_dataset - 1, 2:].astype(numpy.float, casting = "unsafe"))
#plt.show()