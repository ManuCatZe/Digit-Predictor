class CanvasProcessor:
    def __init__(self, canvas_size, grid_size):
        self.canvas_size = canvas_size
        self.grid_size = grid_size
        self.cell_size = canvas_size / grid_size
        self.points = []

    def add_point(self, x, y):
        self.points.append((x, y))

    def clear_points(self):
        self.points.clear()

    def _empty_grid(self):
        grid = []

        for _ in range(self.grid_size):
            grid.append([0] * self.grid_size)

        return grid

    def _points_to_counts(self):
        grid = self._empty_grid()

        for x, y in self.points:
            col = int(x / self.cell_size)
            row = int(y / self.cell_size)

            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                grid[row][col] += 1

        return grid

    def _max_value(self, grid):
        max_value = 0

        for row in grid:
            row_max = max(row)
            if row_max > max_value:
                max_value = row_max

        return max_value

    def _normalize_grid(self, grid):
        max_value = self._max_value(grid)

        if max_value == 0:
            return grid

        normalized = self._empty_grid()

        for row_index in range(self.grid_size):
            for col_index in range(self.grid_size):
                value = grid[row_index][col_index]
                scaled = int((value / max_value) * 16)

                if scaled < 2:
                    scaled = 0
                elif scaled > 16:
                    scaled = 16

                normalized[row_index][col_index] = scaled

        return normalized

    def _find_bounds(self, grid):
        min_row = None
        max_row = None
        min_col = None
        max_col = None

        for row_index in range(self.grid_size):
            for col_index in range(self.grid_size):
                if grid[row_index][col_index] == 0:
                    continue

                if min_row is None or row_index < min_row:
                    min_row = row_index
                if max_row is None or row_index > max_row:
                    max_row = row_index
                if min_col is None or col_index < min_col:
                    min_col = col_index
                if max_col is None or col_index > max_col:
                    max_col = col_index

        if min_row is None:
            return None

        return min_row, max_row, min_col, max_col

    def _center_grid(self, grid):
        bounds = self._find_bounds(grid)

        if bounds is None:
            return grid

        min_row, max_row, min_col, max_col = bounds
        height = max_row - min_row + 1
        width = max_col - min_col + 1

        start_row = (self.grid_size - height) // 2
        start_col = (self.grid_size - width) // 2

        centered = self._empty_grid()

        # тут просто переносим цифру в центр, без изменения ее формы
        for row_index in range(min_row, max_row + 1):
            for col_index in range(min_col, max_col + 1):
                value = grid[row_index][col_index]
                if value == 0:
                    continue

                new_row = start_row + (row_index - min_row)
                new_col = start_col + (col_index - min_col)
                centered[new_row][new_col] = value

        return centered

    def get_grid(self):
        grid = self._points_to_counts()
        grid = self._normalize_grid(grid)
        grid = self._center_grid(grid)
        return grid

    def get_flattened_input(self):
        flat = []

        for row in self.get_grid():
            for value in row:
                flat.append(value)

        return flat
