# Created by Mikhail Skoptsov
# This file contains the GIF animation
# output function in a separate window
import pyglet
import os
from pyglet.window import Platform


def gen_result(name, width, height):
    try:
        pyglet.resource.path = ['gif']
        pyglet.resource.reindex()

        # files = os.listdir("gif\\")
        # print(files)
        animation = pyglet.resource.animation(name + '.gif')
        sprite = pyglet.sprite.Sprite(animation)

        w = width
        h = height

        # screen = Platform().get_default_display().get_default_screen()
        window = pyglet.window.Window(width=w, height=h)

        # window.set_fullscreen(True)

        @window.event
        def on_draw():
            window.clear()
            sprite.draw()

        pyglet.app.run()

    except Exception as ex:
        print(ex)
        print("error")
        for i in os.listdir('gif\\'):
            os.remove("gif\\" + i)
