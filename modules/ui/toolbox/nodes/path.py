import arcade
import math

from modules.ui.toolbox.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.mouse import mouse
from modules.data import data


class Path(Node):

    def __init__(self, id):
        super().__init__(id)

        self.current_point = None
        self.paths = []      # (start, end, branch_id)
        self.hitboxs = []
        self.inputs = []
        self.outputs = []
        self.grid_size = data.UI_EDITOR_GRID_SIZE
        
        self.current_branch_count = 0

        # NEW: smoothing skip value
        self.LINE_WIDTH = 5      # 0 = no skip, higher = smoother
        self.RADIUS = self.LINE_WIDTH * 2

    # ==========================
    #  Add orthogonal path parts
    # ==========================
    def add_path(self):

        if self.current_point is None:
            self.current_point = mouse.cursor
            return

        if mouse.previous_direction in ["RIGHT", "LEFT"]:
            next_point = (mouse.cursor[0], self.current_point[1])
            segment = (self.current_point, next_point, self.current_branch_count)

            hb = HitBox()
            hb.x = min(self.current_point[0], mouse.cursor[0])
            hb.y = self.current_point[1]
            hb.width = abs(mouse.cursor[0] - self.current_point[0])
            hb.height = 1

            self.paths.append(segment)
            self.hitboxs.append(hb)
            self.current_point = next_point

        else:
            next_point = (self.current_point[0], mouse.cursor[1])
            segment = (self.current_point, next_point, self.current_branch_count)

            hb = HitBox()
            hb.x = self.current_point[0]
            hb.y = min(self.current_point[1], mouse.cursor[1])
            hb.width = 1
            hb.height = abs(mouse.cursor[1] - self.current_point[1])

            self.paths.append(segment)
            self.hitboxs.append(hb)
            self.current_point = next_point


    def move(self):
        if mouse.previous_direction != mouse.direction:
            self.add_path()


    def finish(self):
        self.add_path()
        self.current_branch_count += 1
        self.current_point = None


    def draw(self):
        self.draw_smooth_path(self.paths, arcade.color.RED)
        
        if self.current_point != None:
            # Draw current segment smoothly too
            if len(self.paths) > 0:
                # Connect from last point to current mouse position
                last_point = self.paths[-1][1] if self.paths else self.current_point
                self.draw_smooth_line(last_point, mouse.cursor, arcade.color.RED, self.LINE_WIDTH)
            else:
                self.draw_smooth_line(self.current_point, mouse.cursor, arcade.color.RED, self.LINE_WIDTH)

        for a in self.hitboxs:
            a.draw()

    def draw_smooth_path(self, paths, color):
        """Draw smooth connected path using line strips"""
        if not paths:
            return
            
        # Extract all points from the path segments
        points = []
        for i, segment in enumerate(paths):
            if i == 0:
                points.append(segment[0])  # Start of first segment
            points.append(segment[1])  # End of each segment
        
        # Draw the main smooth line
        if len(points) > 1:
            arcade.draw_line_strip(points, color, self.LINE_WIDTH)
            
            # Add rounded joints for smoother appearance
            self.draw_rounded_joints(points, color)

    def draw_smooth_line(self, start, end, color, line_width):
        """Draw a single smooth line using polygon method"""
        # Calculate angle of the line
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        angle = math.atan2(dy, dx) if dx != 0 or dy != 0 else 0
        
        half_width = line_width / 2
        
        # Calculate perpendicular offsets
        perp_dx = -math.sin(angle) * half_width
        perp_dy = math.cos(angle) * half_width
        
        # Create polygon points for smooth line
        point_list = [
            (start[0] - perp_dx, start[1] - perp_dy),  # Bottom left
            (start[0] + perp_dx, start[1] + perp_dy),  # Top left  
            (end[0] + perp_dx, end[1] + perp_dy),      # Top right
            (end[0] - perp_dx, end[1] - perp_dy)       # Bottom right
        ]
        
        arcade.draw_polygon_filled(point_list, color)
        
        # Draw rounded caps
        self.draw_rounded_cap(start, angle + math.pi, color, line_width)  # Start cap
        self.draw_rounded_cap(end, angle, color, line_width)  # End cap

    def draw_rounded_cap(self, center, angle, color, line_width):
        """Draw rounded line cap"""
        radius = line_width / 2
        # Draw a circle at the line end for rounded cap
        arcade.draw_circle_filled(center[0], center[1], radius, color)

    def draw_rounded_joints(self, points, color):
        """Draw rounded joints between line segments"""
        radius = self.LINE_WIDTH / 2
        
        for i in range(1, len(points) - 1):
            # Draw circle at each joint point for rounded corners
            arcade.draw_circle_filled(points[i][0], points[i][1], radius, color)

    # ============================
    # TOUCH DETECTION
    # ============================
    @property
    def touched(self):
        return any(hb.touched for hb in self.hitboxs)
