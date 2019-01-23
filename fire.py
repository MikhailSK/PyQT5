from PIL import Image, ImageDraw
import numpy as np
import random
import imageio
import os


class Fire:
    def __init__(self, name, count, height, width, drops, drops_count):

        self.colors = {-5: (7, 7, 7), -4: (7, 7, 7), -3: (150, 165, 150), -2: (200, 165, 150),
                       -1: (200, 190, 170), 0: (150, 165, 200), 1: (7, 7, 7), 2: (31, 7, 7),
                       3: (47, 15, 7), 4: (87, 23, 7), 5: (103, 31, 7), 6: (119, 17, 7),
                       7: (143, 39, 7), 8: (159, 47, 7), 9: (175, 63, 7), 10: (191, 71, 7),
                       11: (199, 71, 7), 12: (233, 79, 7), 13: (223, 87, 7), 14: (223, 87, 7),
                       15: (215, 103, 15), 16: (207, 111, 15), 17: (207, 119, 15),
                       18: (207, 127, 15), 19: (207, 135, 23), 20: (199, 135, 23),
                       21: (199, 143, 23), 22: (199, 151, 23), 23: (191, 159, 31),
                       24: (191, 159, 31), 25: (191, 167, 39), 26: (191, 167, 39),
                       27: (191, 175, 47), 28: (183, 175, 47), 29: (183, 183, 47),
                       30: (183, 183, 55), 31: (207, 207, 111), 32: (223, 223, 159),
                       33: (239, 239, 199), 34: (255, 255, 255)}

        self.img_arr = []
        self.count = count
        self.name = name
        self.height = height
        self.width = width
        self.drops = drops
        self.drops_count = drops_count

    def generate_images(self):
        for number in range(self.count):
            arr_stat = np.ones((self.width, self.height))
            for i in range(self.width):
                for j in range(self.height):
                    arr_stat[i, j - 1] = 34

            image = Image.new("RGB", (self.width, self.height))
            # image.save("img.png")
            draw = ImageDraw.Draw(image)

            arr_bool = np.ones(self.width)

            for i in range(self.width):
                for j in range(1, self.height):
                    if self.drops == 1:
                        if random.randint(0, self.drops_count) not in range(0, 5):
                            if arr_stat[i, j - 2] < 34 and j < 5:
                                stat = arr_stat[i, j - 2] - random.randint(-1, 1)
                            elif arr_stat[i, j - 2] < 34 and j < 30:
                                stat = arr_stat[i, j - 2] - random.randint(0, 1)
                                if stat < 17:
                                    stat = random.randint(18, 27)
                            else:
                                stat = arr_stat[i, j - 2] - random.randint(0, 1)
                            if stat <= 1:
                                stat = 1
                                arr_bool[i] = j
                            arr_stat[i, j - 1] = stat
                    else:
                        if arr_stat[i, j - 2] < 34 and j < 5:
                            stat = arr_stat[i, j - 2] - random.randint(-1, 1)
                        elif arr_stat[i, j - 2] < 34 and j < 30:
                            stat = arr_stat[i, j - 2] - random.randint(0, 1)
                            if stat < 17:
                                stat = random.randint(18, 27)
                        else:
                            stat = arr_stat[i, j - 2] - random.randint(0, 1)
                        if stat <= 1:
                            stat = 1
                            arr_bool[i] = j
                        arr_stat[i, j - 1] = stat

            for i in range(1, self.width - 1):
                for j in range(1, self.height - 1):
                    stat = (arr_stat[i, j - 1] + arr_stat[i - 1, j]
                            + arr_stat[i + 1, j] + arr_stat[i, j + 1]) // 4
                    arr_stat[i, j] = stat

            for i in range(self.width):
                for j in range(self.height):
                    draw.point((i - 1, j - 1), self.colors[int(arr_stat[i - 1, j - 1])])
                    # print(
                    #     str(self.colors[arr_stat[i, j]]) +
                    #     (80 - len(str(self.colors[arr_stat[i, j]]))) * "-" + str(number))

            for i in range(1, self.width - 1):
                for j in range(1, self.height - 1):
                    draw.point((i, j),
                               ((self.colors[int(arr_stat[i - 1, j])][0]
                                 + self.colors[int(arr_stat[i, j - 1])][0]
                                 + self.colors[int(arr_stat[i + 1, j])][0]
                                 + self.colors[int(arr_stat[i, j + 1])][0]
                                 + self.colors[int(arr_stat[i - 1, j - 1])][0]
                                 + self.colors[int(arr_stat[i + 1, j - 1])][0]
                                 + self.colors[int(arr_stat[i + 1, j + 1])][0]
                                 + self.colors[int(arr_stat[i - 1, j + 1])][0]) // 8,
                                (self.colors[int(arr_stat[i - 1, j])][1]
                                 + self.colors[int(arr_stat[i, j - 1])][1]
                                 + self.colors[int(arr_stat[i + 1, j])][1]
                                 + self.colors[int(arr_stat[i, j + 1])][1]
                                 + self.colors[int(arr_stat[i - 1, j - 1])][1]
                                 + self.colors[int(arr_stat[i + 1, j - 1])][1]
                                 + self.colors[int(arr_stat[i + 1, j + 1])][1]
                                 + self.colors[int(arr_stat[i - 1, j + 1])][1]) // 8,
                                (self.colors[int(arr_stat[i - 1, j])][2]
                                 + self.colors[int(arr_stat[i, j - 1])][2]
                                 + self.colors[int(arr_stat[i + 1, j])][2]
                                 + self.colors[int(arr_stat[i, j + 1])][2]
                                 + self.colors[int(arr_stat[i - 1, j - 1])][2]
                                 + self.colors[int(arr_stat[i + 1, j - 1])][2]
                                 + self.colors[int(arr_stat[i + 1, j + 1])][2]
                                 + self.colors[int(arr_stat[i - 1, j + 1])][2]) // 8))

            if not os.path.exists("image"):
                os.mkdir("image")
            image.transpose(Image.ROTATE_180).save("image/img{}.png".format(number))
            self.img_arr.append("image/img{}.png".format(number))
        self.save_gif()
        return "success"

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

# fire = Fire("movo", 1, 400, 400, 1, 400)
# fire.generate_images()
