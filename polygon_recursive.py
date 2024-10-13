import os, math, pygame, time, json
import numpy as np

class RecursivePolygon:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (20, 50)
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.coords = []
        self.curve_coords = []

    def load_coords(self):
        with open('Click_Coords', 'r') as file:
            coords = json.load(file)
            self.coords = coords
        print(self.coords)

    def catmull_rom_spline(self, x0, x1, x2, x3, y0, y1, y2, y3, t=0, steps=100):
        if t > 1:
            return
        x = 0.5 * (2 * x1 + (-x0 + x2) * t + (2 * x0 - 5 * x1 + 4 * x2 - x3) * t**2 + (-x0 + 3 * x1 - 3 * x2 + x3) * t**3)
        y = 0.5 * (2 * y1 + (-y0 + y2) * t + (2 * y0 - 5 * y1 + 4 * y2 - y3) * t**2 + (-y0 + 3 * y1 - 3 * y2 + y3) * t**3)
        self.curve_coords.append((x, y))
        
        self.catmull_rom_spline(x0, x1, x2, x3, y0, y1, y2, y3, t + (1 / steps))

    def recursive_generate_arcs(self, i=3):
        if i >= len(self.coords):
            return

        x_points, y_points = [x for x, _ in self.coords[i-3:i+1]], [y for _, y in self.coords[i-3:i+1]]
        x0, x1, x2, x3 = x_points
        y0, y1, y2, y3 = y_points
        self.catmull_rom_spline(x0, x1, x2, x3, y0, y1, y2, y3)
        
        self.recursive_generate_arcs(i + 1)

    def draw(self):
        isRunning = True
        while isRunning:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    isRunning = False
            self.screen.fill((200, 200, 200))
            pygame.draw.lines(self.screen, (0, 0, 0), True, self.curve_coords, 10)
            pygame.display.flip()

recursivePolygon = RecursivePolygon()
recursivePolygon.load_coords()
recursivePolygon.recursive_generate_arcs()
recursivePolygon.draw()
