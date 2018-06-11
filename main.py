import os
import numpy as np
import pandas as pd

image_size_x = 1920
image_size_y = 1088


def create_dataset(cell_side=16, max_predictions_in_cell=5):
    """
    creates dataset using objects.txt file coming from xml parser
    returns:
        images:     list of strings     path to images in dataset
        labels:     np.ndarray          contains first max_predictions_in_cell predictions for each cell
    """
    main_dir = os.path.abspath('./')
    objects_file = os.path.join(main_dir, "data", "objects.txt")
    file = open(objects_file, "r")
    all_objects = [row.split(" ") for row in file]
    # formatting all_objects parameters inplace
    for objects in all_objects:
        # removing newline character
        objects[-1] = objects[-1].replace("\n", "")
        # convert positions and classes from str to int
        objects[1:] = list(map(int, objects[1:]))

    # creating dataset
    data = []
    for objects in all_objects:
        while len(objects) > 6:
            data.append(objects[:6])
            del objects[1:6]
    data = pd.DataFrame(data)
    data = data.rename(columns={0: "img_file", 1: "xmin", 2: "ymin", 3: "xmax", 4: "ymax", 5: "cat"})

    images = data.img_file.unique()
    n_datapoints_cell_x = int(image_size_x / cell_side)
    n_datapoints_cell_y = int(image_size_y / cell_side)
    labels = np.zeros([len(images), n_datapoints_cell_y, n_datapoints_cell_x, max_predictions_in_cell, 6])

    data[["xmin", "ymin", "xmax", "ymax"]] = data[["xmin", "ymin", "xmax", "ymax"]] / cell_side   # resizing
    data[["xmin", "ymin", "xmax", "ymax"]] = data[["xmin", "ymin", "xmax", "ymax"]].astype(int)   # rounding down

    for image_i, image_path in enumerate(images):
        print(image_i)
        n_predictions_in_cell = np.zeros([n_datapoints_cell_y, n_datapoints_cell_x], dtype=int)
        for item in range(len(data[data.img_file == images[image_i]])):
            bb = data[data.img_file == images[image_i]].values[item]
            x_min = bb[1]
            x_max = bb[2]
            y_min = bb[3]
            y_max = bb[4]
            cat = bb[5]
            confidence = 1
            n_predictions_in_cell[y_min:y_max, x_min:x_max] += 1
            for cell_x in np.arange(x_min, x_max):
                for cell_y in np.arange(y_min, y_max):
                    n_i = n_predictions_in_cell[cell_y, cell_x]-1
                    if n_i < max_predictions_in_cell:
                        labels[image_i][cell_y, cell_x][n_i] = [x_min, x_max, y_min, y_max, cat, confidence]

    return images, labels


imgs, labels = create_dataset()
