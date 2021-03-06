import numpy as np
import csv, os, os.path, timeit, math
from PIL import Image
import matplotlib.pyplot as plt

def read_data(filepath):
    f = open(filepath,"r")

    reader = csv.reader(f, delimiter="\t", skipinitialspace = True)
    data = list(reader)

    return np.array(data)

def summer(i, z):
    # This function produces the sum of the input arrays, with z being the input list of arrays,
    # and i being length of file.

    # Opening the files
    with open(z[i - 1], 'r') as dest_f:
        data_iter = csv.reader(dest_f,
                               delimiter=';',
                               quotechar='"')
        data = [data for data in data_iter]

    a = np.asarray(data)

    # steps to create a new numpy array because the files have slight abnormalities that need to be smoothed out
    temp_img = np.zeros((len(a), len(a[0]) - 1))

    for k in range(len(a)):
        for j in range(len(a[0]) - 1):
            temp_img[k][j] = float(a[k][j])

    # recursive step
    if i != 1:
        i -= 1
        return summer(i, z) + temp_img
    elif i == 1:
        return temp_img
    # return temp_img


def colour(temp, denoise, T_min, T_max, T_max_denoise):
    # This is the function that returns the rgb value for each pixel
    if denoise:
        range_fraction = (temp - T_min) / (T_max_denoise - T_min)
    else:
        range_fraction = (temp - T_min) / (T_max - T_min)

    # Clamp it to value between 0 and 1
    range_fraction = max(0, min(1, range_fraction))

    # Returning the rgb values of temp
    r = max(0, 255 * (1 - math.cos(math.pi * range_fraction)))
    g = 255 * math.sin(math.pi * range_fraction)
    b = max(0, 255 * math.cos(math.pi * range_fraction))

    return r, g, b


def main(index, aoa, dir2, windtunnel_folder):
    # this is the main function, creates the thermal bitmap for each aoa
    dir_files = os.listdir(dir2[index])

    z = []
    for i in range(len(dir_files)):
        z.append(dir2[index] + dir_files[i])

    print("Processing alpha: " + str(aoa) + " (" + str(len(z)) + " files)")

    tic = timeit.default_timer()

    my_data = summer(len(z), z)/len(z)

    tac = timeit.default_timer()

    print("time to average temperature readings: ", tac - tic, " seconds")

    # Finding the max and min temperature in the picture
    temp_max = []
    for i in range(int(len(my_data)/3), int(2*len(my_data)/3)):
        temp_max.append(max(my_data[i]))

    # T_min = my_data[200][155] # for the 2d ones
    T_min = my_data[267][155]  # for the 3d ones
    T_max = max(temp_max) - 0.12
    T_max_smoothed = max(temp_max) - 0.25
    tonc = timeit.default_timer()

    print("time to find max temperature: ", tonc - tac, " seconds")

    # Creating rgb arrays
    picture_array_smoothed = np.zeros((len(my_data), len(my_data[0])-1, 3), dtype=np.uint8)
    picture_array_noisey = np.zeros((len(my_data), len(my_data[0])-1, 3), dtype=np.uint8)

    # Creating array for temperature graph
    temp_array_smoothed = np.zeros((len(my_data), len(my_data[0])), dtype=float)

    # Generating the final bitmap
    for i in range(1, len(my_data) - 3):
        for j in range(140, len(my_data[0]) - 100):
            # # # Smoothing algorithms
            # # temp2 = (float(my_data[i-1][j+1]) + float(my_data[i][j+1]) + float(my_data[i+1][j+1]) + float(my_data[i+2][j+1]) +
            # #         float(my_data[i-1][j]) + float(my_data[i][j]) + float(my_data[i+1][j]) + float(my_data[i+2][j+1]) +
            # #         float(my_data[i-1][j-1]) + float(my_data[i][j-1]) + float(my_data[i+1][j-1]) + float(my_data[i+2][j+1]) +
            # #         float(my_data[i-1][j-2]) + float(my_data[i][j-2]) + float(my_data[i+1][j-2]) + float(my_data[i+2][j-2]))\
            # #         /16
            #
            # temp2 = (float(my_data[i - 1][j + 1]) + float(my_data[i][j + 1]) + float(my_data[i + 1][j + 1]) +
            #
            #          float(my_data[i - 1][j]) + float(my_data[i][j]) + float(my_data[i + 1][j]) +
            #
            #          float(my_data[i - 1][j - 1]) + float(my_data[i][j - 1]) + float(my_data[i + 1][j - 1]) +
            #
            #          float(my_data[i - 1][j - 2]) + float(my_data[i][j - 2]) + float(my_data[i + 1][j - 2]) +
            #
            #          float(my_data[i - 1][j - 3]) + float(my_data[i][j - 3]) + float(my_data[i + 1][j - 3])) \
            #         / 15
            #
            # # temp2 = (float(my_data[i-1][j]) + float(my_data[i][j]) + float(my_data[i][j-1])) / 3
            #
            # # temp2 = float(my_data[i][j])
            #
            # a = (T_max_smoothed + T_min) / 100
            #
            # for k in range(100):
            #     if T_min+a*k <= temp2 < T_min+a*(k+1):
            #         temp2 = float(T_min+a*k)
            # temp_array_smoothed[i][j] = temp2
            # # r2, g2, b2 = colour(temp2, 1, T_min, T_max, T_max_smoothed)
            # #
            # # picture_array_smoothed[i][j][0] = r2
            # # picture_array_smoothed[i][j][1] = g2
            # # picture_array_smoothed[i][j][2] = b2

            # No smoothing bitmap creation
            temp1 = float(my_data[i][j])

            r1, g1, b1 = colour(temp1, 0, T_min, T_max, T_max_smoothed)

            picture_array_noisey[i][j][0] = r1
            picture_array_noisey[i][j][1] = g1
            picture_array_noisey[i][j][2] = b1

    graph_array = np.zeros(len(temp_array_smoothed[0]) - 240, dtype=float)

    # for i in range(140, len(my_data[0]) - 100):
    #     temp3 = 0
    #     for j in range(25):
    #         temp3 += temp_array_smoothed[int(j+len(temp_array_smoothed)/2)][i]
    #     temp3 = temp3 / 25
    #     graph_array[i-140] = temp3

    for i in range(140, len(my_data[0]) - 100):
        temp3 = 0
        for j in range(25):
            temp3 += my_data[int(j+len(my_data)/2)][i]
        temp3 = temp3 / 25
        graph_array[i-140] = temp3

    plt.ylabel('Celsius')
    plt.xlabel('Position along the width of the thermal scan section')
    plt.plot(range(len(graph_array)), graph_array)
    # plt.show()
    graph_name = str(aoa) + " temperature graph.tiff"
    plt.savefig(windtunnel_folder + '/thermal 3d tiff files/' + graph_name)
    plt.clf()

    # File saving codes
    noisey_pic = Image.fromarray(picture_array_noisey)
    # noisey_pic.show(title = "Noisey", command = None)
    name_noise = str(aoa) + " alpha, noisey.tiff"
    noisey_pic.save(windtunnel_folder + '/thermal 3d tiff files/' + name_noise)

    # smoothed_pic = Image.fromarray(picture_array_smoothed)
    # # smoothed_pic.show(title = "Denoised", command = None)
    # name_smoothed = str(aoa) + " degrees alpha, smoothed.tiff"
    # smoothed_pic.save(windtunnel_folder + '/thermal 3d tiff files/smoothed/' + name_smoothed)

    toc = timeit.default_timer()

    print("time to generate image and graphs: ", toc - tonc, " seconds")
    print("Processing time for this batch: ", toc - tic, " seconds \n")

