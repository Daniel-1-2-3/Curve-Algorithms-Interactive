import os, math, pygame, time, json

class CurvePolygon:
    def __init__ (self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 50)
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.all_coords = []
        self.leading_seg = []
        self.origin_seg = []
        self.click_coords = [0]
        self.control_points_display = []
        self.shape_closed = False
        self.LINE_COLOR = (10, 80, 124)
    
    def generate_arc_points(self, points_temp):
        """Catmull-rom spline: x = 0.5*(2*x1 + (-x0 + x2)*t + (2*x0 - 5*x1 + 4*x2 -x3)*t**2 + (-x0 + 3*x1 -3*x2 + x3)*t**3), same for y, where t ranges from 0-1
        This spline should generate a curve that passes through the 2 center points, with the left and right points acting as contorls"""
        result_coords = []
        
        points = points_temp[:]
        if not self.shape_closed:
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
        if not self.shape_closed:
            self.control_points_display = points[len(points)-5:]
        return result_coords
    
    def new_click_point(self, mouse_x, mouse_y):
        self.click_coords.append((mouse_x, mouse_y))
    
    def modify_last_segment(self, mouse_x, mouse_y):
        self.click_coords[-1] = (mouse_x, mouse_y)
        try:
            self.all_coords = self.generate_arc_points(self.click_coords)
        except:
            pass
        
    def draw(self, color):
        try:
            pygame.draw.lines(self.screen, color, False, self.all_coords, 7)
            try:
                pygame.draw.circle(self.screen, (180, 100, 0), self.control_points_display[-1], 5)
                self.control_points_display.pop()
                pygame.draw.lines(self.screen, (200, 0, 0), False, self.control_points_display, 3)
                for point in self.control_points_display:
                    pygame.draw.circle(self.screen, (250, 0, 0), point, 5)
            except:
                pass
        except:
            pass

    def export_coords(self):
        with open("Curved_Polygon_Coords", "w") as file:
            json.dump(self.all_coords, file)
        with open("Click_Coords", "w") as file:
            json.dump(self.click_coords, file)
            
    def close_shape(self):
        """Catmull-rom spline: x = 0.5*(2*x1 + (-x0 + x2)*t + (2*x0 - 5*x1 + 4*x2 -x3)*t**2 + (-x0 + 3*x1 -3*x2 + x3)*t**3), same for y, where t ranges from 0-1
        This spline should generate a curve that passes through the 2 center points, with the left and right points acting as contorls"""
        if self.shape_closed:
            return
        
        self.shape_closed = True
        self.all_coords = []
        self.control_points_display = []
        
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
        self.screen.fill((200, 200, 200))
        self.draw(self.LINE_COLOR)
        pygame.display.flip()
    
    def shift_horizontal(self, dirn): #dirn -1 for left, 1 for right
        try:
            sorted_x = sorted([x for x, _ in self.click_coords])
            if not (sorted_x[0] < 1 and dirn == -1) and not (sorted_x[-1] > 999 and dirn == 1):
                for i in range(len(self.click_coords)):
                    self.click_coords[i] = (self.click_coords[i][0]+dirn*0.25, self.click_coords[i][1])
                self.control_points_display = []
                self.all_coords = self.generate_arc_points(self.click_coords)
        except:
            pass
    
    def shift_vertical(self, dirn): #dirn -1 for up, 1 for down
        try:
            sorted_y = sorted([y for _, y in self.click_coords])
            if not (sorted_y[0] < 1 and dirn == -1) and not (sorted_y[-1] > 699 and dirn == 1):
                for i in range(len(self.click_coords)):
                    self.click_coords[i] = (self.click_coords[i][0], self.click_coords[i][1]+dirn*0.25)
                self.control_points_display = []
                self.all_coords = self.generate_arc_points(self.click_coords)
        except:
            pass

    def resize(self, dirn): #dirn -1 for down, 1 for up
        try:
            center_point = (sum([x for x, _ in self.click_coords])/len(self.click_coords), sum([y for _, y in self.click_coords])/len(self.click_coords))
            for i in range(len(self.click_coords)):
                if (self.click_coords[i][0] - center_point[0]) != 0:
                    slope = (self.click_coords[i][1] - center_point[1])/(self.click_coords[i][0] - center_point[0])
                    new_x = self.click_coords[i][0] + dirn*(self.click_coords[i][0] - center_point[0])*0.001
                    new_y = slope*(new_x - self.click_coords[i][0]) + self.click_coords[i][1]
                else:
                    new_x = self.click_coords[i][0]
                    new_y = self.click_coords[i][1] + dirn*(self.click_coords[i][1] - center_point[1])*0.001
                self.click_coords[i] = (new_x, new_y)
            self.all_coords = self.generate_arc_points(self.click_coords)
        except:
            pass
                
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
                    if e.key == pygame.K_SPACE:
                        isClicked = True
                    if e.key == pygame.K_c:
                        stopped_editing = True
                        self.close_shape()
                    if e.key == pygame.K_s:
                        self.export_coords()
                    
            self.screen.fill((200, 200, 200))
            
            if not stopped_editing:
                if isClicked:
                    self.new_click_point(mouse_x, mouse_y)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.modify_last_segment(mouse_x, mouse_y)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.shift_horizontal(-1)
            if keys[pygame.K_RIGHT]:
                self.shift_horizontal(1)
            if keys[pygame.K_UP]:
                self.shift_vertical(-1)
            if keys[pygame.K_DOWN]:
                self.shift_vertical(1)
            if keys[pygame.K_a]:
                self.resize(1)
            if keys[pygame.K_d]:
                self.resize(-1)
                                
            self.draw(self.LINE_COLOR)
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
            pygame.draw.polygon(self.screen, self.LINE_COLOR, coords)
            pygame.display.flip()
        pygame.quit()
        
if __name__ == "__main__":
    polyCurve = CurvePolygon()
    polyCurve.interact()
    polyCurve.display_saved()
        