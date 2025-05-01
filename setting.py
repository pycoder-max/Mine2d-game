from tkinter import PhotoImage
from PIL import Image, ImageTk

BG = "lightblue"
TILE_IMAGES = [PhotoImage(file = f"assets/tiles/{i}.png") for i in range(18)]
TILE_IMAGES_SCALED = [ImageTk.PhotoImage(Image.open(f"assets/tiles/{i}.png").resize((60, 60))) for i in range(18)]

STEVE_IMAGES = [[PhotoImage(file = f"assets/steve/{p}{i + 1}.png").zoom(3, 3) for i in range(4)]
		 		for p in ["h", "b", "a", "l"] ]

TARGET_FPS = 45

MX = 20 # max_x_tiles
MY = 11 # max_y_tiles
TILE_SIZE = TILE_IMAGES[0].height() # side of squared tile

MLX = 20000 # maximum tiles in level towards x
MLY = 256 # maximum tiles in level towards y
