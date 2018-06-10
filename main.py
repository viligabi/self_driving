import os
import numpy as np
import pandas as pd


def create_dataset():
    """
    creates dataset using objects.txt file coming from xml parser
    returns:
        data: pd.DataFrame with columns: file, xs, ys, xe, ye, cat
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

    return data


dataset = create_dataset()