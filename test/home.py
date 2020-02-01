import random
import arcade
import os

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1600
SCREEN_TITLE = "Sprite Collect Coins with Background Example"

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.texture = None
        self.scale = 0.6
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.texture  = arcade.load_texture("images/real.jpg")
        print('Original Dimensions : ',self.scale * self.texture.width, self.scale * self.texture.height)
        self.scale = 0.3

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(700, 500, self.scale * self.texture.width, self.scale * self.texture.height, self.texture, 0)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.finish_render()
    arcade.run()

if __name__ == "__main__":
    main()