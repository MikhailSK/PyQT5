# PyQT5 project
# Created by Mikhail Skoptsov
# This file is needed to generate a GIF
# image with fire images that are also generated

from PIL import Image, ImageDraw
import numpy as np
import random
import imageio
import os


class Fire:
    def __init__(self, name, count, height,
                 width, drops, drops_count):

        # dict with rgd colors
        self.colors = {-5: (7, 7, 7),
                       -4: (7, 7, 7),
                       -3: (150, 165, 150),
                       -2: (200, 165, 150),
                       -1: (200, 190, 170),
                       0: (150, 165, 200),
                       1: (7, 7, 7),
                       2: (31, 7, 7),
                       3: (40, 10, 7),
                       4: (47, 15, 7),
                       5: (60, 15, 7),
                       6: (87, 23, 7),
                       7: (103, 31, 7),
                       8: (119, 17, 7),
                       9: (143, 39, 7),
                       10: (150, 42, 7),
                       11: (159, 47, 7),
                       12: (175, 63, 7),
                       13: (191, 71, 7),
                       14: (199, 71, 7),
                       15: (233, 79, 7),
                       16: (223, 87, 7),
                       17: (223, 87, 7),
                       18: (215, 103, 15),
                       19: (210, 103, 14),
                       20: (207, 111, 15),
                       21: (207, 119, 15),
                       22: (203, 123, 15),
                       23: (207, 127, 15),
                       24: (207, 135, 23),
                       25: (199, 135, 23),
                       26: (199, 143, 23),
                       27: (199, 151, 23),
                       28: (191, 159, 31),
                       29: (191, 159, 31),
                       30: (191, 167, 39),
                       31: (191, 167, 39),
                       32: (191, 175, 47),
                       33: (183, 175, 47),
                       34: (183, 183, 47),
                       35: (183, 183, 55),
                       36: (207, 207, 111),
                       37: (223, 223, 159),
                       38: (239, 239, 199),
                       39: (255, 255, 255)}

        # parameters
        self.img_arr = []
        self.count = count
        self.name = name
        self.height = height
        self.width = width
        self.drops = drops
        self.drops_count = drops_count

    # main function of generating
    def generate_images(self):
        # This cycle is needed to generate <count> images
        for number in range(self.count):

            # Array of statuses of the pixels
            # The color depends on the status
            arr_stat = np.ones((self.width, self.height))

            for i in range(self.width):
                for j in range(self.height):
                    arr_stat[i, j - 1] = 34

            image = Image.new("RGB", (self.width, self.height))

            # image.save("img.png")

            draw = ImageDraw.Draw(image)

            arr_bool = np.ones(self.width)

            # Fill the array of statuses
            # Each status depends on the one above it
            for i in range(self.width):
                for j in range(1, self.height):
                    # if there are drops
                    if self.drops == 1:
                        # Strange condition
                        if random.randint(0, self.drops_count) \
                                not in range(0, 5):
                            # first 5 lines of pixels
                            if arr_stat[i, j - 2] < 34 and\
                                    j < int(self.height * 0.02):
                                stat = arr_stat[i, j - 2] - \
                                       random.randint(-1, 1)
                            # 5-30 lines of pixels
                            elif arr_stat[i, j - 2] < 34 and\
                                    j < int(self.height * 0.08):
                                stat = arr_stat[i, j - 2] - \
                                       random.randint(0, 1)
                                if stat < 17:
                                    stat = random.randint(18, 27)
                            # other
                            else:
                                stat = arr_stat[i, j - 2] -\
                                       random.randint(0, 1)
                            if stat <= 1:
                                stat = 1
                                arr_bool[i] = j
                            arr_stat[i, j - 1] = stat
                    # if no drops
                    else:
                        # first 5 lines of pixels
                        if arr_stat[i, j - 2] < 34 and\
                                j < int(self.height * 0.02):
                            stat = arr_stat[i, j - 2]\
                                   - random.randint(-1, 1)
                        # 5-30 lines of pixels
                        elif arr_stat[i, j - 2] < 34 and\
                                j < int(self.height * 0.08):
                            stat = arr_stat[i, j - 2]\
                                   - random.randint(0, 1)
                            if stat < 17:
                                stat = random.randint(18, 27)
                        # other
                        else:
                            stat = arr_stat[i, j - 2]\
                                   - random.randint(0, 1)
                        if stat <= 1:
                            stat = 1
                            arr_bool[i] = j
                        arr_stat[i, j - 1] = stat

            # remove sharp changes in colors
            for i in range(1, self.width - 1):
                for j in range(1, self.height - 1):
                    stat = (arr_stat[i, j - 1] +
                            arr_stat[i - 1, j]
                            + arr_stat[i + 1, j] +
                            arr_stat[i, j + 1]) // 4
                    arr_stat[i, j] = stat

            # draw a image
            for i in range(self.width):
                for j in range(self.height):
                    draw.point((i - 1, j - 1),
                               self.colors[
                                   int(arr_stat[i - 1, j - 1])])
                    # print(
                    #     str(self.colors[
                    #     arr_stat[i, j]]) +
                    #     (80 - len(str(self.colors[arr_stat[
                    #     i, j]])))* "-" + str(number))

            # add blur
            for i in range(1, self.width - 1):
                for j in range(1, self.height - 1):
                    draw.point((i, j),
                               ((self.colors[
                                     int(arr_stat[i - 1, j])][0]
                                 + self.colors[
                                     int(arr_stat[i, j - 1])][0]
                                 + self.colors[
                                     int(arr_stat[i + 1, j])][0]
                                 + self.colors[
                                     int(arr_stat[i, j + 1])][0]
                                 + self.colors[
                                     int(arr_stat[i - 1, j - 1])][0]
                                 + self.colors[
                                     int(arr_stat[i + 1, j - 1])][0]
                                 + self.colors[
                                     int(arr_stat[i + 1, j + 1])][0]
                                 + self.colors[
                                     int(arr_stat[i - 1, j + 1])][0])
                                // 8,
                                (self.colors[
                                     int(arr_stat[i - 1, j])][1]
                                 + self.colors[
                                     int(arr_stat[i, j - 1])][1]
                                 + self.colors[
                                     int(arr_stat[i + 1, j])][1]
                                 + self.colors[
                                     int(arr_stat[i, j + 1])][1]
                                 + self.colors[
                                     int(arr_stat[i - 1, j - 1])][1]
                                 + self.colors[
                                     int(arr_stat[i + 1, j - 1])][1]
                                 + self.colors[
                                     int(arr_stat[i + 1, j + 1])][1]
                                 + self.colors[
                                     int(arr_stat[i - 1, j + 1])][1])
                                // 8,
                                (self.colors[
                                     int(arr_stat[i - 1, j])][2]
                                 + self.colors[
                                     int(arr_stat[i, j - 1])][2]
                                 + self.colors[
                                     int(arr_stat[i + 1, j])][2]
                                 + self.colors[
                                     int(arr_stat[i, j + 1])][2]
                                 + self.colors[
                                     int(arr_stat[i - 1, j - 1])][2]
                                 + self.colors[
                                     int(arr_stat[i + 1, j - 1])][2]
                                 + self.colors[
                                     int(arr_stat[i + 1, j + 1])][2]
                                 + self.colors[
                                     int(arr_stat[i - 1, j + 1])][2])
                                // 8))

            if not os.path.exists("image"):
                os.mkdir("image")
            # flip and save the image
            image.transpose(Image.ROTATE_180).save(
                "image/img{}.png".format(number))
            self.img_arr.append("image/img{}.png".format(number))
        self.save_gif()
        return "success"

    # function of creating and saving GIF images
    def save_gif(self):
        images = []
        if not os.path.exists("gif"):
            os.mkdir("gif")
        # print("fire", self.name)
        for filename in self.img_arr:
            images.append(imageio.imread(filename))
            os.remove(filename)
        # files = os.listdir("gif\\")
        # print(files)
        imageio.mimsave("gif\\" + self.name + '.gif', images)
        # print("SAVED")
        # files = os.listdir("gif\\")
        # print(files)
        os.rmdir('image')

# fire = Fire("mov", 1, 400, 400, 1, 400)
# fire.generate_images()
