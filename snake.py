import pygame
import math
import os
import time 

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 50)
pygame.init()
screen = pygame.display.set_mode((1000, 700))

BUSHY_GREEN = (106, 198, 92)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
def generate_arc_points(p0, p1, p2, new_points):
    #Bezier's curve: x(t) = ((1-t)^2)*x0 + 2*(1-t)*t*x1 + (t^2)*x2, same for y, where t ranges from 0-1
    #points along curve, in tuple, are appended
    x0, x1, x2, y0, y1, y2 = p0[0], p1[0], p2[0], p0[1], p1[1], p2[1]
    for t in range(100):
        t /= 100
        x = ((1-t)**2)*x0 + 2*(1-t)*t*x1 + (t**2)*x2
        y = ((1-t)**2)*y0 + 2*(1-t)*t*y1 + (t**2)*y2
        if distance(x, y, x0, y0) < distance(x, y, x2, y2):#the arc is 2 segments, only record the first segment
            new_points.append((x, y))

def draw_bush(coords, color):
    new_points = []
    if len(coords) >= 4:
        for i in range(2, len(coords)):
            if i >= 2:
                generate_arc_points(coords[i-2], coords[i-1], coords[i], new_points)
                coords[i-1] = new_points[len(new_points)-1]
            pygame.draw.lines(screen, color, False, new_points, 7)
            time.sleep(0.001)
    for coord in coords:
        pygame.draw.circle(screen, (0, 0, 0), coord, 3)

coords = [0]
running = True
while running:
    isClicked = False
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            isClicked = True

    mouse_x, mouse_y = pygame.mouse.get_pos()
    coords[len(coords)-1] = (mouse_x, mouse_y)
    
    if isClicked:
        coords.append((mouse_x, mouse_y))
    screen.fill((255, 255, 255))

    draw_bush(coords, BUSHY_GREEN)
    pygame.display.flip()

pygame.quit()
