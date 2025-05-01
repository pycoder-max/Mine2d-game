from tkinter import Canvas

if __name__ != "__main__":
	from setting import *
	from level import Level

# Building main class for every single tile
class Tile:
	def __init__(self, x, y, idx, idy):
		self.x = x
		self.y = y 
		self.idx = idx
		self.idy = idy
		self.tile = 0
		self.started_drawing = False

	def tick(self, canvas, level : list[list[int]], cx, cy):
		x, y = self.x - cx, self.y - cy

		if x < -TILE_SIZE:
			self.x += MX * TILE_SIZE
			self.idx += MX
		if y < -TILE_SIZE:
			self.y += MY * TILE_SIZE
			self.idy += MY

		if x > (MX - 1) * TILE_SIZE:
			self.x -= MX * TILE_SIZE
			self.idx -= MX 
		if y > (MY - 1) * TILE_SIZE:
			self.y -= MY * TILE_SIZE
			self.idy -= MY 

		x, y = self.x - cx, self.y - cy

		self.tile = level[self.idy][self.idx]

		self.draw(canvas, self.tile, x, y)

	def draw(self, canvas : Canvas, tile, x, y):
		if tile:
			canvas.create_image(x, y, image = TILE_IMAGES[tile - 1], anchor = "nw")

			if x > -1 and y > -1:
				self.started_drawing = True


class TileManager:
	def __init__(self):
		"""Tile manager to create initialise , controll and cordinate 
			all of level and tiles"""
		self.tiles : list[Tile] = []
		self.levelmng = Level()

		self.level : list[list[int]]= self.levelmng.init(MLX, MLY)

		self.px = self.levelmng.px
		self.py =  self.levelmng.py

		self.camera_x = 0
		self.camera_y = 0
		self.started_drawing = False

		tile_idx = 0
		tile_idy = 0
		tile_x = 0
		tile_y = 0

		for _ in range(MY):
			tile_x = 0
			tile_idx = 0
			for _ in range(MX):
				self.tiles.append(Tile(tile_x, tile_y, tile_idx, tile_idy))
				tile_idx += 1
				tile_x += TILE_SIZE
			tile_idy += 1
			tile_y += TILE_SIZE

	def clip_camera(self):
		if self.camera_x < 0:
			self.camera_x = 0

		if self.camera_x > (MLX - MX) * TILE_SIZE - TILE_SIZE:
			self.camera_x = (MLX - MX) * TILE_SIZE - TILE_SIZE

		if self.camera_y < 0:
			self.camera_y = 0

		if self.camera_y > (MLY - MY + 1.5) * TILE_SIZE:
			self.camera_y = (MLY - MY + 1.5) * TILE_SIZE


	def tick(self, canvas, player_x, player_y):
		"""ticks over all the tiles which fits under screen \
			which could draw tiles and clips camera in range"""

		self.camera_x += (player_x - self.camera_x) / 9
		self.camera_y += (player_y - self.camera_y) / 9

		self.clip_camera()


		for i in range(self.tiles.__len__()):
			try:
				self.tiles[i].tick(canvas, self.level, self.camera_x, self.camera_y)
				if not self.started_drawing:
					if self.tiles[i].started_drawing:
						self.started_drawing =True
			except:
				pass
		
