import tkinter as tk
if __name__ != "__main__":
	from setting import *

class Player:
	"""inits player this class can also be used for drawing,
		holding positions, handling collisions and handling events 
		by just passing tk.Event class"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.sx = 0
		self.sy = 0

		self.px = 0 
		self.py = 0 

		self.falling = 9
		self.dir = 1

	def event(self, event : tk.Event, etype):
		"""update player class's asumption on events and update it
		as soon as event had got from root.bind() over any needed event"""
		if etype == "P":
			match event.keysym.lower():
				case "up":
					self.py = -1
				case "down":
					self.py = 1
				case "right":
					self.px = 1
				case "left":
					self.px = -1

		if etype == "R":
			match event.keysym.lower():
				case "up":
					if self.py == -1:
						self.py = 0
				case "down":
					if self.py == 1:
						self.py = 0
				case "right":
					if self.px == 1:
						self.px = 0
				case "left":
					if self.px == -1:
						self.px = 0 

	def tick(self, canvas: tk.Canvas, cx : int, cy : int, delta: float, level: list[list[int]]):
		"""draw on every iteration and keep track of posiotion, gravity and collision handling"""
		px = self.x - cx # projection x
		py = self.y - cy # projection y

		self.x += self.sx * delta
		if self.check_collision(level): 
			self.x -= self.sx * delta 
			self.sx = 0  

		self.falling += 1

		self.y += self.sy * delta
		if self.check_collision(level):
			self.y -= self.sy * delta 
			if self.sy > 0.1:
				self.falling = 0
			self.sy = 0

		self.sx += self.px * 3
		self.sy += self.py * 12.25 if self.falling < 3 else 0

		self.sx *= 0.85 

		self.sy += 3 * delta
		self.draw(px, py, canvas)

	def check_collision(self, level) -> bool:

		player_size = 48

		if self.col_at_point(self.x, self.y, level):
			return 1
		if self.col_at_point(self.x + player_size, self.y + player_size, level):
			return 1
		if self.col_at_point(self.x, self.y + player_size, level):
			return 1
		if self.col_at_point(self.x + player_size, self.y, level):
			return 1

		return 0

	def col_at_point(self, x, y, level):
		try:
			tile =level[int(y / TILE_SIZE)] [int(x / TILE_SIZE)]
			hollow_blocks = [0, 8,9,10]
			return not tile in hollow_blocks
		except:
			pass

	def draw(self, x, y, canvas : tk.Canvas):
		canvas.create_image(x, y, image = STEVE_IMAGES[0][0], anchor = "nw")
