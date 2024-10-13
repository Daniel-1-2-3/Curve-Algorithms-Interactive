import os, math, pygame, time, json
import numpy as np

class CurvePolygon:
    def __init__ (self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 50)
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.all_coords = []
        self.leading_seg = []
        self.origin_seg = []
        self.click_coords = [0]
        self.BUSHY_GREEN = (106, 198, 92)
    
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def generate_arc_points(self, points_temp):
        """Catmull-rom spline: x = 0.5*(2*x1 + (-x0 + x2)*t + (2*x0 - 5*x1 + 4*x2 -x3)*t**2 + (-x0 + 3*x1 -3*x2 + x3)*t**3), same for y, where t ranges from 0-1
        This spline should generate a curve that passes through the 2 center points, with the left and right points acting as contorls"""
        result_coords = []
        
        points = points_temp[:]
        #add extra control points to beggining and end of the click_coords list
        control_x1 = 2*points[0][0] - points[1][0]
        control_y1 = 2*points[0][1] - points[1][1]
        control_x2 = 2*points[-1][0] - points[-2][0]
        control_y2 = 2*points[-1][1] - points[-2][1]
        points.insert(0, (control_x1, control_y1))
        points.append((control_x2, control_y2))

        for i in range(3, len(points)):
            x_points, y_points = [x for x, _ in points[i-3:i+1]], [y for _, y in points[i-3:i+1]]
            x0, x1, x2, x3 = x_points
            y0, y1, y2, y3 = y_points
          
            for t in range(100):
                t = t/100
                x = 0.5*(2*x1 + (-x0 + x2)*t + (2*x0 - 5*x1 + 4*x2 -x3)*t**2 + (-x0 + 3*x1 -3*x2 + x3)*t**3)
                y = 0.5*(2*y1 + (-y0 + y2)*t + (2*y0 - 5*y1 + 4*y2 -y3)*t**2 + (-y0 + 3*y1 -3*y2 + y3)*t**3)
                result_coords.append((x, y))
        return result_coords
    
    def new_click_point(self, mouse_x, mouse_y):
        self.click_coords.append((mouse_x, mouse_y))
    
    def modify_last_segment(self, mouse_x, mouse_y):
        self.click_coords[-1] = (mouse_x, mouse_y)
        try:
            self.all_coords = self.generate_arc_points(self.click_coords)
        except Exception as e:
            pass
        
    def draw(self, color):
        try:
            pygame.draw.lines(self.screen, color, False, self.all_coords, 10)
        except Exception as e:
            pass

    def export_coords(self):
        with open("Curved_Polygon_Coords", "w") as file:
            json.dump(self.all_coords, file)
        with open("Click_Coords", "w") as file:
            json.dump(self.click_coords, file)
            
    def close_shape(self):
        """Catmull-rom spline: x = 0.5*(2*x1 + (-x0 + x2)*t + (2*x0 - 5*x1 + 4*x2 -x3)*t**2 + (-x0 + 3*x1 -3*x2 + x3)*t**3), same for y, where t ranges from 0-1
        This spline should generate a curve that passes through the 2 center points, with the left and right points acting as contorls"""
        self.all_coords = []
        
        #add extra control points to beggining and end of the click_coords list
        self.click_coords.insert(0, self.click_coords[-1])
        self.click_coords.pop()
        self.click_coords.append(self.click_coords[1])
        self.click_coords.append(self.click_coords[2])

        for i in range(3, len(self.click_coords)):
            x_points, y_points = [x for x, _ in self.click_coords[i-3:i+1]], [y for _, y in self.click_coords[i-3:i+1]]
            x0, x1, x2, x3 = x_points
            y0, y1, y2, y3 = y_points
          
            for t in range(100):
                t = t/100
                x = 0.5*(2*x1 + (-x0 + x2)*t + (2*x0 - 5*x1 + 4*x2 -x3)*t**2 + (-x0 + 3*x1 -3*x2 + x3)*t**3)
                y = 0.5*(2*y1 + (-y0 + y2)*t + (2*y0 - 5*y1 + 4*y2 -y3)*t**2 + (-y0 + 3*y1 -3*y2 + y3)*t**3)
                self.all_coords.append((x, y))
        self.export_coords()
        self.screen.fill((50, 50, 50))
        self.draw(self.BUSHY_GREEN)
        pygame.display.flip()

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
                        self.close_shape()
                    
            if stopped_editing:
                continue
            self.screen.fill((50, 50, 50))
            
            if isClicked:
                self.new_click_point(mouse_x, mouse_y)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.modify_last_segment(mouse_x, mouse_y)
            self.draw(self.BUSHY_GREEN)
            pygame.display.flip()
    
    def display_saved(self):
        coords = []
        with open('Curved_Polygon_Coords', 'r') as file:
            coords = json.load(file)
        isRunning = True
        while isRunning:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    isRunning = False
            self.screen.fill((200, 200, 200))
            pygame.draw.lines(self.screen, (0, 0, 0), True, coords, 10)
            pygame.draw.polygon(self.screen, self.BUSHY_GREEN, coords)
            pygame.display.flip()
        pygame.quit()
        
if __name__ == "__main__":
    polyCurve = CurvePolygon()
    polyCurve.interact()
    polyCurve.display_saved()
        