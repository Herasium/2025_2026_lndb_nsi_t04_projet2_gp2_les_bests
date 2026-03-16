import arcade
import math
from typing import Any, Dict, List, Optional, Tuple

from modules.data.node import Node
from modules.ui.toolbox.poly_hitbox import PolyHitbox
from modules.ui.mouse import mouse
from modules.data import data

from line_profiler import profile


class Path(Node):
    """
    Represents a path node in the UI editor, consisting of branched line segments.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Path object.

        Parameters:
        - id: Unique identifier for the node.
        """
        super().__init__(id)

        self.current_point: Optional[Tuple[float, float]] = None
        self.points: List[Tuple[float, float]] = []

        self.branch_points: Dict[int, List[Tuple[float, float]]] = {}
        self.branch_hitboxes: Dict[int, List[PolyHitbox]] = {}

        self.inputs: List[List[Any]] = []
        self.outputs: List[List[Any]] = []
        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        self.current_branch_count: int = 0
        self.color: arcade.types.Color = arcade.color.RED

        self.thickness: int = 12

        self.branch_points[0] = []
        self.branch_hitboxes[0] = []

        self.input_off_color: arcade.types.Color = arcade.types.Color.from_hex_string(
            data.COLORS.VALUE_OFF
        )
        self.input_on_color: arcade.types.Color = arcade.types.Color.from_hex_string(
            data.COLORS.VALUE_ON
        )

        self.current_value: int = 0
        self.current_size: int = 0
        self.draw_hitboxes: bool = False

        self.do_points: bool = True
        self._camera: Tuple[float, float] = (0.0, 0.0)

    def project_point_onto_segments(self, x: float, y: float) -> Dict[str, Any]:
        """
        Finds the closest point on any segment to the given (x, y) coordinates.

        Parameters:
        - x: Target x-coordinate
        - y: Target y-coordinate

        Returns:
        - dict: Containing 'point', 'branch', 'index', and 'dist' of the closest segment.
        """
        closest: Dict[str, Any] = {
            "point": None,
            "branch": None,
            "index": None,
            "dist": float("inf"),
        }

        for bid, pts in self.branch_points.items():
            if len(pts) < 2:
                continue

            # Iterate through line segments within the branch
            for i in range(len(pts) - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]

                dx = x2 - x1
                dy = y2 - y1
                seg_len_sq = dx * dx + dy * dy

                if seg_len_sq == 0:
                    continue

                # Project point onto segment and clamp to segment bounds
                t = ((x - x1) * dx + (y - y1) * dy) / seg_len_sq
                t = max(0.0, min(1.0, t))

                px = x1 + t * dx
                py = y1 + t * dy

                dist_sq = (px - x) ** 2 + (py - y) ** 2

                # Update if a closer point is found
                if dist_sq < closest["dist"]:
                    closest = {
                        "point": (px, py),
                        "branch": bid,
                        "index": i,
                        "dist": dist_sq,
                    }

        return closest

    def recalculate_hitbox(self) -> None:
        """
        Regenerates hitboxes for all path segments based on current camera position.
        """
        for current in range(len(self.branch_hitboxes.keys())):
            if len(self.branch_points[current]) > 1:
                self.branch_hitboxes[current] = []
                for point in range(len(self.branch_points[current]) - 1):
                    # Adjust points by camera offset
                    current_point = self.branch_points[current][point]
                    current_point = (
                        current_point[0] + self._camera[0],
                        current_point[1] + self._camera[1],
                    )
                    next_point = self.branch_points[current][point + 1]
                    next_point = (
                        next_point[0] + self._camera[0],
                        next_point[1] + self._camera[1],
                    )

                    # Generate polygon representing the thick line
                    left, right = self.generate_thick_line_polygon(
                        [current_point, next_point], thickness=self.thickness
                    )
                    polygon = left + list(reversed(right))

                    self.branch_hitboxes[current].append(PolyHitbox(polygon))

    def clean_out_single_branch(self, depth: int = 0) -> None:
        """
        Removes branches that have insufficient connections.

        Parameters:
        - depth: Recursive depth tracker to prevent infinite loops.
        """
        if depth > 100:
            print("Max depth on branch clean out.")
            return

        # Count how many connections exist for each branch
        branch_counts = [0 for _ in range(len(self.branch_points.keys()))]
        for i in self.inputs + self.outputs:
            branch_counts[i[4]] += 1

        to_delete = []
        for index in range(len(branch_counts)):
            if branch_counts[index] <= 1:
                to_delete.append(index)

        to_delete.sort(reverse=True)

        for i in to_delete:
            self.remove_branch(i)

        # Recursively clean if branches were deleted
        if len(to_delete) > 1 or (
            len(to_delete) > 0 and to_delete[0] != len(self.branch_points) - 1
        ):
            self.clean_out_single_branch(depth=depth + 1)

    @property
    def camera(self) -> Tuple[float, float]:
        return self._camera

    @camera.setter
    def camera(self, value: Tuple[float, float]) -> None:
        self._camera = value
        self.recalculate_hitbox()

    @property
    def empty(self) -> bool:
        """Checks if the path is essentially empty."""
        value = len(self.branch_points.keys())
        if 0 in self.branch_points:
            value += len(self.branch_points[0])
        return value <= 1

    def remove_branch(self, branch: int) -> None:
        """
        Removes a branch and updates input/output indices.

        Parameters:
        - branch: The branch index to remove.
        """
        for index in range(branch, len(self.branch_points) - 1):
            self.branch_points[index] = self.branch_points[index + 1]
            self.branch_hitboxes[index] = self.branch_hitboxes[index + 1]

        del self.branch_hitboxes[len(self.branch_hitboxes) - 1]
        del self.branch_points[len(self.branch_points) - 1]

        self.current_branch_count = len(self.branch_hitboxes.keys())

        # Ensure at least one empty branch remains
        if len(self.branch_points) > 0:
            if len(self.branch_points[len(self.branch_points) - 1]) != 0:
                self.branch_points[len(self.branch_points)] = []
                self.branch_hitboxes[len(self.branch_hitboxes)] = []
        else:
            self.branch_points[len(self.branch_points)] = []
            self.branch_hitboxes[len(self.branch_hitboxes)] = []

        # Update input indices
        for entry in self.inputs:
            if entry[4] > branch:
                entry[4] -= 1
        self.inputs = [i for i in self.inputs if i[4] != branch]

        # Update output indices
        for entry in self.outputs:
            if entry[4] > branch:
                entry[4] -= 1
        self.outputs = [i for i in self.outputs if i[4] != branch]

    def add_path(self) -> None:
        """Adds a new segment to the current path branch."""
        pt = None

        # Try snapping to existing segments
        if self.current_point is None and self.current_branch_count > 0:
            snapped = self.project_point_onto_segments(
                mouse.cursor[0] - self._camera[0], mouse.cursor[1] - self._camera[1]
            )
            pt = snapped["point"]
            if pt:
                pt = (pt[0], pt[1])
                self.branch_points[snapped["branch"]].insert(snapped["index"] + 1, pt)

        if pt is None:
            pt = (mouse.cursor[0] - self._camera[0], mouse.cursor[1] - self._camera[1])

        self.points.append(pt)
        self.branch_points[self.current_branch_count].append(pt)
        self.recalculate_hitbox()
        self.current_point = (
            mouse.cursor[0] - self._camera[0],
            mouse.cursor[1] - self._camera[1],
        )

    def finish(self) -> None:
        """Finalizes the current path branch."""
        self.add_path()
        self.current_branch_count += 1
        self.current_point = None
        self.points = []
        self.branch_points[self.current_branch_count] = []
        self.branch_hitboxes[self.current_branch_count] = []
        self.recalculate_hitbox()

    def abort(self) -> None:
        """Resets the current drawing operation."""
        self.current_point = None
        self.points = []
        self.branch_points[self.current_branch_count] = []
        self.branch_hitboxes[self.current_branch_count] = []
        self.recalculate_hitbox()

    @profile
    def draw(self) -> None:
        """Renders the paths and hitboxes."""
        self.color = (
            self.input_on_color if self.current_value == 1 else self.input_off_color
        )

        for bid, pts in self.branch_points.items():
            if len(pts) > 1:
                new_pts = [
                    (i[0] + self._camera[0], i[1] + self._camera[1]) for i in pts
                ]

                if self.do_points and bid > 0:
                    arcade.draw_circle_filled(
                        center_x=pts[0][0] + self._camera[0],
                        center_y=pts[0][1] + self._camera[1],
                        radius=self.thickness,
                        color=self.color,
                    )

                arcade.draw_line_strip(
                    point_list=new_pts, color=self.color, line_width=self.thickness
                )

        # Draw the line being currently dragged
        if self.current_point:
            arcade.draw_line(
                self.current_point[0] + self._camera[0],
                self.current_point[1] + self._camera[1],
                mouse.cursor[0],
                mouse.cursor[1],
                color=self.color,
                line_width=self.thickness,
            )

        if self.draw_hitboxes:
            for i in self.branch_hitboxes:
                for a in self.branch_hitboxes[i]:
                    a.draw()

    def merge(self, path: "Path") -> None:
        """
        Merges another path into this one.

        Parameters:
        - path: The Path object to merge.
        """
        branch_offset = self.current_branch_count
        last_point = path.branch_points[path.current_branch_count][-1]
        snapped = self.project_point_onto_segments(last_point[0], last_point[1])

        pt = snapped["point"]
        self.branch_points[snapped["branch"]].insert(snapped["index"] + 1, pt)
        path.branch_points[path.current_branch_count][-1] = pt

        for i in path.branch_points:
            self.branch_points[self.current_branch_count] = path.branch_points[i]
            self.current_branch_count += 1

        for i in path.inputs:
            self.inputs.append([i[0], i[1], i[2], i[3], i[4] + branch_offset])

        for i in path.outputs:
            self.outputs.append([i[0], i[1], i[2], i[3], i[4] + branch_offset])

        self.current_branch_count -= 1
        self.finish()

    def get_connected_points(
        self, target_id: Any
    ) -> Tuple[List[List[Any]], List[List[Any]]]:
        """
        Returns inputs and outputs connected to a specific target.

        Parameters:
        - target_id: The ID to look for.

        Returns:
        - Tuple of (inputs, outputs) lists.
        """
        connected_inputs = [inp for inp in self.inputs if inp[1] == target_id]
        connected_outputs = [outp for outp in self.outputs if outp[1] == target_id]
        return connected_inputs, connected_outputs

    @property
    def touched(self) -> bool:
        """Returns True if any hitbox is currently touched."""
        return any(
            hb.touched for group in self.branch_hitboxes.values() for hb in group
        )

    @property
    def get_touched_branch(self) -> Optional[int]:
        """Returns the index of the branch currently being touched, if any."""
        for index in self.branch_hitboxes:
            group = self.branch_hitboxes[index]
            if any(hb.touched for hb in group):
                return index
        return None

    def generate_thick_line_polygon(
        self, points: List[Tuple[float, float]], thickness: float
    ) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
        """
        Calculates the polygon vertices for a thick line.

        Parameters:
        - points: List of coordinates.
        - thickness: Line thickness.

        Returns:
        - Tuple of (left_points, right_points) lists.
        """
        if len(points) < 2:
            return [], []

        half = thickness / 2
        left_points = []
        right_points = []

        def normalize(vx: float, vy: float) -> Tuple[float, float]:
            length = math.sqrt(vx * vx + vy * vy)
            return (vx / length, vy / length) if length != 0 else (0.0, 0.0)

        for i in range(len(points)):
            p = points[i]
            # Calculate normal vector at each point
            if i == 0:
                dx, dy = points[i + 1][0] - p[0], points[i + 1][1] - p[1]
            elif i == len(points) - 1:
                dx, dy = p[0] - points[i - 1][0], p[1] - points[i - 1][1]
            else:
                dx = (points[i + 1][0] - p[0]) + (p[0] - points[i - 1][0])
                dy = (points[i + 1][1] - p[1]) + (p[1] - points[i - 1][1])

            nx, ny = normalize(dx, dy)
            px, py = -ny, nx  # Perpendicular vector

            left_points.append((p[0] + px * half, p[1] + py * half))
            right_points.append((p[0] - px * half, p[1] - py * half))

        return left_points, right_points

    def __str__(self) -> str:
        return f"Path {self.id}"

    def save_hitboxes(self) -> Dict[int, List[Dict[str, Any]]]:
        """Serializes hitboxes."""
        result = {}
        for bid in self.branch_hitboxes:
            result[bid] = [i.save() for i in self.branch_hitboxes[bid]]
        return result

    def save(self) -> Dict[str, Any]:
        """Serializes the Path node for saving."""
        return {
            "type": "path",
            "inputs": self.inputs,
            "outputs": self.outputs,
            "id": self.id,
            "branch_points": self.branch_points,
            "branch_hitboxes": self.save_hitboxes(),
            "current_branch_count": self.current_branch_count,
        }

    def load_hitboxes(
        self, hitboxes: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[int, List[PolyHitbox]]:
        """Deserializes hitboxes."""
        result = {}
        for index in hitboxes:
            count = len(result.keys())
            result[count] = [PolyHitbox(hit["points"]) for hit in hitboxes[index]]
        return result

    def load(self, data: Dict[str, Any]) -> None:
        """
        Loads path data from a dictionary.

        Parameters:
        - data: Dictionary containing saved path state.
        """
        self.inputs = data["inputs"]
        self.outputs = data["outputs"]
        self.id = data["id"]
        self.branch_points = {int(k): v for k, v in data["branch_points"].items()}
        self.branch_hitboxes = self.load_hitboxes(data["branch_hitboxes"])
        self.current_branch_count = data["current_branch_count"]
