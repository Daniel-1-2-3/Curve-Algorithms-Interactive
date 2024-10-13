import os, math, pygame, time, json
import numpy as np

class CurvePolygon:
    def __init__ (self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 50)
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.segments = []
        self.leading_segment = []
        self.all_coords = []
        self.click_coords = [0]
        self.BUSHY_GREEN = (106, 198, 92)
    
    def export_coords(self):
        with open("Curved_Polygon_Coords", "w") as file:
            json.dump(self.all_coords, file)
    
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def generate_arc_points(self, points):
        #Bezier's curve: x(t) = ((1-t)^2)*x0 + 2*(1-t)*t*x1 + (t^2)*x2, same for y, where t ranges from 0-1
        #points along curve, in tuple, are appended
        result_coords = []
        self.leading_segment = []
        x_points, y_points = [x for x, _ in points], [y for _, y in points]
        x0, x1, x2 = x_points
        y0, y1, y2 = y_points
       
        for t in range(100):
            t /= 100
            x = ((1-t)**2)*x0 + 2*(1-t)*t *x1 + (t**2)*x2
            y = ((1-t)**2)*y0 + 2*(1-t)*t*y1 + (t**2)*y2
            if self.distance(x, y, x0, y0) < self.distance(x, y, x2, y2):#the arc is 2 segments, only record the first segment
                result_coords.append((x, y))
            else:
                self.leading_segment.append((x, y))
        return result_coords
    
    def new_click_point(self, mouse_x, mouse_y):
        self.click_coords.append((mouse_x, mouse_y))
        if len(self.segments) > 0 and len(self.segments[-1]) > 0:
            self.click_coords[-3] = self.segments[-1][-1]
        self.segments.append([])
    
    def modify_last_segment(self, mouse_x, mouse_y):
        self.click_coords[-1] = (mouse_x, mouse_y)
        if len(self.click_coords) >= 3:
            last_seg_coords = self.generate_arc_points(self.click_coords[len(self.click_coords)-3:])
            self.segments[-1] = last_seg_coords
        
    def draw(self, color):
        if len(self.segments) > 0:
            self.all_coords = [] #concatenate lists to make the overall polygon
            for segment in self.segments[1:]:
                self.all_coords.extend(segment)
                pygame.draw.lines(self.screen, color, False, segment, 7)
            if len(self.leading_segment) > 0:
                pygame.draw.lines(self.screen, color, False, self.leading_segment, 7)
                self.all_coords.extend(self.leading_segment)
            if len(self.all_coords) > 0:
                pygame.draw.polygon(self.screen, color, self.all_coords)
            for coord in self.click_coords:
                pygame.draw.circle(self.screen, (0, 0, 0), coord, 3)

    def close_shape(self):
        self.click_coords[-1] = self.click_coords[0]

    def interact(self):
        isRunning = True
        stopped_editing = False
        while isRunning:
            isClicked = False
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    isRunning = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    isClicked = True
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_a:
                        isClicked = True
                    if e.key == pygame.K_s:
                        stopped_editing = not stopped_editing
                        self.screen.fill((200, 200, 200))
                        self.close_shape()
                        self.modify_last_segment(self.click_coords[-1][0], self.click_coords[-1][1])
                        self.draw(self.BUSHY_GREEN)
                        pygame.display.flip()
                        self.export_coords()
                    
            if stopped_editing:
                continue
            self.screen.fill((200, 200, 200))
            
            if isClicked:
                self.new_click_point(mouse_x, mouse_y)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.modify_last_segment(mouse_x, mouse_y)

            self.draw(self.BUSHY_GREEN)
            pygame.display.flip()

        pygame.quit()
if __name__ == "__main__":
    polyCurve = CurvePolygon()
    polyCurve.interact()
        