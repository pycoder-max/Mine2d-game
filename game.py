import tkinter as tk
from time import time as t

# main init
root = tk.Tk()

# constants
from setting import *
WS = root.winfo_screenwidth(), root.winfo_screenheight() # window_size
SO = [WS[0] // 2, WS[1] // 2] # SCREEN_ORGIN


# main loop with tkloop
def loop(time, tick = 0, t2 = t(), l_of_fps : list[float] = []):

	delay = t() - time
	fps = 1 / delay
	tick += 1

	delta = TARGET_FPS / fps
	range  = 1 / delta

	if tick % range if range != 0 else 1 == 0:
		delay2 = t() - t2
		canvas.delete("all")

		tm.tick(canvas, player.x - SO[0], player.y - SO[1])
		if tm.started_drawing:
			canvas.config(bg = BG)

			player.tick(canvas, tm.camera_x, tm.camera_y, delta, tm.level)
			tm.level = lev_e.update(canvas, tm.level, tm.camera_x, tm.camera_y)


		else:
			canvas.create_text(SO[0] - 350, SO[1], text = f"Loading new world |{"🟩" * (int(tick // 28) % 30)}|",
					  		  fill= "white", font= ("bold", 19), anchor= "nw")
			

		fps2 = float(f"{1 / delay2:.2f}")
		l_of_fps.insert(0, fps2),

		while l_of_fps.__len__() > 10:
			l_of_fps.pop()

		sumed = 0
		for i in l_of_fps:
			sumed += i

		afps = sumed / l_of_fps.__len__()

		if tm.started_drawing:
			canvas.create_text(SO[0], SO[1] - 200, text = f"geting {afps / (TARGET_FPS + 14) * 100:.2f}% of expected speed")

		t2 = t()

	time = t()
	root.after(1, loop, time, tick, t2, l_of_fps)

def distribute_event(event, etype):
	player.event(event, etype)
	lev_e.event(event, etype)
	if event.keysym.lower() == "escape":
		root.destroy()

# set window attributes
root.wm_title("Game")
root.wm_geometry(f"{WS[0]}x{WS[1]}")
root.attributes("-fullscreen", True)
root.wm_resizable(False, False)

#maximization
try:
	# windows only supports this
	# others may maximize normally
	root.wm_state("zoomed")
except:
	...

# canvas init
canvas = tk.Canvas(root, width = WS[0], height = WS[1], bg = "black")
canvas.pack()

# import tiles and player after init of root window
from tiles import TileManager
from player import Player
from ui import EditorUi

tm = TileManager() # init tilemanager as tm
player = Player(tm.px + 1, tm.py) # init player
lev_e = EditorUi(*SO) # init of level editor

# loop init
loop(t())

# keyboard events
root.bind("<KeyPress>", lambda event: distribute_event(event, "P"))
root.bind("<KeyRelease>", lambda event: distribute_event(event, "R"))

# mouse events
root.bind("<ButtonPress>", lambda event: distribute_event(event, "BP"))
root.bind("<ButtonRelease>", lambda event: distribute_event(event, "BR"))
root.bind("<Motion>", lambda event: distribute_event(event, "M"))

# window events
root.bind("<FocusOut>", lambda event: distribute_event(event, "FO"))

# tkloop init
root.mainloop() 
