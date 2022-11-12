from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class CellData:
    g: float
    h: float

    parent: Tuple[int, int]

    @property
    def f(self):
        return self.g + self.h

class AStar:
    ROWS = 40
    COLS = 40

    @classmethod
    def init_closed_list(cls):
        return [[False for _ in range(cls.COLS)] for _ in range(cls.ROWS)]

    @classmethod
    def init_cell_data_and_parents(cls):
        cell_data = []
        for i in range(cls.ROWS):
            row = []
            for j in range(cls.COLS):
                row.append(CellData(
                    g=float('inf'),
                    h=float('inf'),
                    parent=(-1, -1)
                ))
            cell_data.append(row)
        
        return cell_data

    @classmethod
    def compute_h(cls, src, dst):
        # Diagonal distance
        di = abs(src[0] - dst[0])
        dj = abs(src[1] - dst[1])

        return (di + dj) + (2**0.5 - 2) * min(di, dj)

    @classmethod
    def get_path_from_cell_data(cls, cell_data, src, dst):
        path = [dst]
        while path[-1] != src:
            i, j = path[-1]
            path.append(cell_data[i][j].parent)

        return path[::-1]

    @classmethod
    def find_shortest_path(cls, grid: List[List[bool]], starting_point: Tuple[int, int], destination: Tuple[int, int]) -> List[Tuple[int, int]]:
        closed_list = cls.init_closed_list()
        cell_data_and_parents = cls.init_cell_data_and_parents()
        open_list = []

        # La destination est dans un 'mur'
        if not grid[destination[0]][destination[1]]:
            return []

        # Init starting point node
        cell_data_and_parents[starting_point[0]][starting_point[1]] = CellData(g=0.0, h=0.0, parent=starting_point)

        open_list.append(starting_point)

        found_destination = False
        while open_list and not found_destination:

            i, j = open_list.pop()
            closed_list[i][j] = True

            for di in range(-1, 2):
                for dj in range(-1, 2):
                    # On regarde les 8 autour
                    if di == 0 and dj == 0:
                        continue
                    
                    # On s'assure d'être dans à l'intérieur de la carte
                    if not (0 <= (i+di) < cls.ROWS) or not (0 <= (j+dj) < cls.COLS):
                        continue

                    if (di+i, dj+j) == destination:
                        cell_data_and_parents[di+i][dj+j].parent = (i, j)
                        found_destination = True

                    elif not closed_list[di+i][j+dj] and grid[di+i][dj+j]:
                        new_g = cell_data_and_parents[i][j].g + (di**2 + dj**2)**0.5
                        new_h = cls.compute_h((i, j), destination)
                        
                        if cell_data_and_parents[di+i][dj+j].f > (new_g + new_h):
                            cell_data_and_parents[di+i][dj+j] = CellData(
                                g=new_g,
                                h=new_h,
                                parent=(i, j)
                            )

                            open_list.append((di+i, dj+j))
        
        return cls.get_path_from_cell_data(cell_data_and_parents, starting_point, destination) 
