import arcade
import arcade.geometry
from modules.ui.mouse import mouse

class PolyHitbox():
    
    def __init__(self,points = []):

        self.points = points

    def draw(self):
        if len(self.points) > 1:
            arcade.draw_polygon_outline(self.points, arcade.color.ALLOY_ORANGE)

    @property
    def touched(self):

        mouse_x, mouse_y = mouse.position
        return arcade.geometry.is_point_in_polygon(x=mouse_x,y=mouse_y,polygon=self.points)

    def __repr__(self):
        return (f"PolyHitBox (points={self.points})")

    def __str__(self):
        return (f"PolyHitBox (points={self.points})")
