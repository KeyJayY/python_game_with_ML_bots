import json

from config import MapConfig


class Map:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
            self.width = data["width"]
            self.height = data["height"]
            self.obstacles = data["obstacles"]
            
    
    def create_grid(self,cell_size: int) -> list[list[int]]: # For static map (no moving obstacles)
        rows = MapConfig().height // cell_size
        cols = MapConfig().width // cell_size
        grid = [[0 for _ in range(cols)] for _ in range(rows)]

        for obstacle in self.obstacles:
            x_start = obstacle["x"] // cell_size
            y_start = obstacle["y"] // cell_size
            x_end = (obstacle["x"] + obstacle["width"]) // cell_size
            y_end = (obstacle["y"] + obstacle["height"]) // cell_size

            for y in range(y_start, y_end + 1):
                for x in range(x_start, x_end + 1):
                    if 0 <= x < cols and 0 <= y < rows:
                        grid[y][x] = 1
        return grid
