import tkinter as tk
from setting import *

class EditorUi:
    def __init__(self, sox, soy):
        """
        Initializes the EditorUi object.
        """
        self.mx : int = 0 # Mouse X
        self.my : int = 0 # Mouse Y 
        self.mp : bool = 0 # Whether RightMouseButton is pressed

        self.mgx : int = 0 # mouse x on global grid
        self.mgy : int = 0 # mouse y on global grid
        self.selected = 0 
        self.state = 0 # 0:idle, 1:placing, -1:destroying
        self.mb = 0 # 1: left button 3 : right button

        self.sox = sox
        self.soy = soy

        self.cmx = 0 # clipped mouse x from orgin of nw cordinate system
        self.cmy = 0 # clipped mouse y from orgin of nw cordinate system

        self.holding = [2, 3, 4, 11, 12, 8, 0, 0, 0]

    def event(self, event: tk.Event, etype: str):
        """
        Handles mouse events.
        """
        self.mx = event.x_root
        self.my = event.y_root
        keys = "123456789"
        match etype:
            case "BP":
                self.mp = 1
                self.mb = event.num
            case "BR":
                self.mp = 0
            case "P":
                for i in range(keys.__len__()):
                    if event.keysym.lower() == keys[i]:
                        self.selected = i
    
    def is_tile_surounded(self, level , x, y) -> bool:
        return level[y + 1] [x] or level[y - 1] [x]\
            or level[y] [x + 1] or level[y] [x - 1]\
            or level[y + 1] [x + 1] or level[y + 1] [x - 1]\
            or level[y - 1] [x - 1] or level[y - 1] [x - 1]
    
    def is_tile_reachable_from_player(self, level : list[list[int]], playerx : float, playery : float, type = 0) -> bool:
        targetX = self.mgx
        targetY = self.mgy

        x_dif = targetX - int(playerx // TILE_SIZE) # x difference
        y_dif = targetY - int(playery // TILE_SIZE) # y difference

        x_dif = int(x_dif)
        y_dif = int(y_dif)

        rx = 0 # relative x
        ry = 0 # relative y

        sx, sy = 0, 0


        if x_dif == 0 and y_dif == 0:
            return False, [int(playerx // TILE_SIZE) + int(rx), int(playery // TILE_SIZE) + int(ry)]
        
        if x_dif != 0:
            sx = abs(x_dif) / x_dif
        if y_dif != 0:
           sy = abs(y_dif) / y_dif

        if type:
            rx -= sx
            ry -= sy

        while (x_dif != 0  or y_dif != 0):
            if x_dif != 0:
                rx += sx
                x_dif -= sx
            if y_dif != 0:
                ry += sy
                y_dif -= sy
            
            if level[int(playery // TILE_SIZE) + int(ry)] [int(playerx // TILE_SIZE) + int(rx)] != 0:
                return False, [int(playerx // TILE_SIZE) + int(rx), int(playery // TILE_SIZE) + int(ry)]
        
        return True, [int(playerx // TILE_SIZE) + int(rx),
                     int(playery // TILE_SIZE) + int(ry)]
        
    def update(self, canvas: tk.Canvas, level: list[list[int]], cx: float, cy: float, playerx : float, playery : float) -> list[list[int]]:
        """
        Updates the editor UI.
        """
        self.mgx, self.mgy = self.is_tile_reachable_from_player(level, playerx, playery)[1]

        self.draw_placeholder(canvas, cx, cy)
        self.draw_ui(canvas)

        self.mgx = int((cx + self.mx) // TILE_SIZE)
        self.mgy = int((cy + self.my + TILE_SIZE // 1.30) // TILE_SIZE) - 1

        self.mgx, self.mgy = self.is_tile_reachable_from_player(level, playerx, playery)[1]

        brush = self.holding[self.selected]

        if self.mp:
            if self.state == 0:
                if self.mb == 1:
                    self.state = -1
                elif self.mb == 3:
                    self.state = 1
                    
            if self.state == 1:
                if level[self.mgy] [self.mgx] == 0:
                    if self.is_tile_surounded(level, self.mgx, self.mgy):
                            if self.is_tile_reachable_from_player(level, playerx, playery)[0]:
                                level[self.mgy] [self.mgx] = brush 

            if self.state == -1:
                if level[self.mgy] [self.mgx] != 1:
                        if self.is_tile_reachable_from_player(level, playerx, playery, 1)[0]:
                            level[self.mgy] [self.mgx] = 0
        else:
            self.state = 0

        return level

    def draw_placeholder(self, canvas: tk.Canvas, cx: float, cy: float):
        """
        Draws a tile placeholder.
        """
        x = self.mgx - int(cx // TILE_SIZE)
        y = self.mgy - int(cy // TILE_SIZE)

        x *= TILE_SIZE
        y *= TILE_SIZE

        x -= cx % TILE_SIZE
        y -= cy % TILE_SIZE

        self.cmx = x
        self.cmy = y

        canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, width = 4, dash= "50")

    def draw_ui(self, canvas: tk.Canvas):
        uihight = 80
        uiwidth = 720
        bwidth = uiwidth / 9

        uix = self.sox - uiwidth // 2
        uiy = self.soy + uihight * 3 + 60

        canvas.create_rectangle(uix, uiy, uix + uiwidth, uiy + uihight, fill= "#6f6f6f", outline= "")
        for i in range(9):
            canvas.create_rectangle(uix + i * bwidth, uiy, uix + bwidth * (i + 1), uiy + uihight, 
                                    width = 4, outline= "#afafaf")
        
        s = self.selected
        for i in range(12):
            step = 20
            fade = i * step
            hexed = format(fade, "x")
            hexed = ( ("0" + hexed) if hexed.__len__() == 1 else hexed)
            canvas.create_rectangle(uix + s * bwidth, uiy, uix + bwidth * (s + 1), uiy + uihight, 
                                    width = 13 - i, outline= "#cccc" + hexed)

        for i in range(9):
            canvas.create_image(uix + i * bwidth + 11, uiy + 11, image = \
                                TILE_IMAGES_SCALED[ self.holding[i] - 1], anchor = "nw") if self.holding[i] > 1 else ...

