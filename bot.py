from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions
import math, random
from christofides import tsp
from pathfinding import AStar
# Tick has form :
# {
#   currentTick: number;
#   totalTicks: number;
#   currentLocation: Position | null;
#   spawnLocation: Position | null;
#   map: {
#       topology: 
#         [ // Matrix of tiles, representing terrain height
#           [8,8,7,6,5,5,5],
#           [8,8,6,5,4,4,3]
#           // ...;
#         ], 
#       tideLevels: {min: int, max: int} 
#       }
#       tideSchedule: [5,4,3,3,4,5,6], // List of numbers representing the tide schedule
#       // ...
#       }
#       ports: 
#         [
#           { row: 15, column: 7 },
#           { row: 8, column: 8 },
#         ],;
#   };
#   visitedPortIndices: number[];
#   tideSchedule: number[];
#   isOver: boolean;
# }
def dist(first: tuple, second: tuple) -> float:
    # pythagorea's theorem
    return math.sqrt((first[0] - second[0])**2 + (first[1] - second[1])**2)


class Bot:
    def __init__(self, tick : Tick):
        print("Initializing your super mega duper bot")
        self.tsp_ports_order = tsp(tick.map.ports)
        
        # for now, the bot starts at any port location
        # find nearest dock - > choose fastest route {predict tide movement -> }-> start moving 

    def find_nearest_dock(self, tick: Tick) -> int:
        # returns the index of the closest dock in tick.map.ports
        ports = tick.map.ports.copy()
        visited = tick.visitedPortIndices.copy()
        dico = {}
        for i, port in enumerate(ports):
            dico[f"{dist(port)}"] = (i,port)
        minimum = min(dist(port) for port in ports if port not in visited)
        for key, values in dico.items:
            if values[1] not in visited and minimum == float(key):
                return values[0]

    def get_direction(self, tick: Tick) -> str:
        index = self.find_nearest_dock(tick)
        current_position = tick.currentLocation
        nearest = tick.map.ports[index]
        diff = tick.currentLocation - nearest

    def port_direction(self, vec_of_port) -> str:
        # uses scalar product to find most appropriate direction
        const = 1/math.sqrt(2)
        dic = {"N":(0,1), "NE":(1/const,1/const), "E":(1,0), "SE":(1/const,-1/const), "S":(0,-1), "SW":(-1/const,-1/const), "W":(-1, 0), "NW":(-1/const, 1/const)}
        biggest = 0

        for key, vec in dic.items():
            dot_prod = sum([i*j for (i, j) in zip(vec, vec_of_port)])
            if dot_prod > biggest:
                biggest = dot_prod
                res = key
        return res

    def static_low_tide_map(self, tick: Tick):
        low = tick.map.tideLevels.min
        return [[int(j < low) for j in i] for i in tick.map.topology]
    
    def dynamic_sailable_map(self, tick: Tick, turn_in_future): 
        # Return Binary Map of Sailable Water from Tide Schedule for set turn
        #(1 : sailable) (0 : ground)

        tide = tick.tideSchedule[turn_in_future % len(tick.tideSchedule)]
        return [[int(j < tide) for j in i] for i in tick.map.topology]
    

    def next_position(self, current_position, direction):

        cap = {"N":(0,1), "NE":(1,1), "E":(1,0), "SE":(1,-1), "S":(0,-1), "SW":(-1,-1), "W":(-1, 0), "NW":(-1, 1)}
        new_row = current_position["row"] + cap[direction][1]
        new_column = current_position["column"] + cap[direction][0]
        return {"row": new_row, "column": new_column}

    def is_sailable(self, tick: Tick, position, tide) -> bool:
        return tick.map.topology[position['row']][position['column']] < tide

    def get_path_to_port(self, grid, position, port_position):
        path = AStar.find_shortest_path(grid, position, port_position)
        return path

    def get_paths_for_all_ports(self, tick: Tick):
        grid = self.dynamic_sailable_map(tick, 0)
        paths = [self.get_path_to_port(grid, (tick.currentLocation.row, tick.currentLocation.column), (p.row, p.column)) for p in tick.map.ports]

        return paths
        
    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            return Spawn(self.tsp_ports_order[0])
        elif (tick.currentLocation in tick.map.ports) and (tick.map.ports.index(tick.currentLocation) not in tick.visitedPortIndices):
            return Dock()
        return Sail(directions[tick.currentTick % len(directions)])
