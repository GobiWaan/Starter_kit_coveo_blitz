from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions
import math, random
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
    return math.sqrt((abs(first[0] - second[0]))**2 + (abs(first[1] - second[1]))**2)


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        # for now, the bot starts at any port location
        self.position = random.choice(Tick.map.port)
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

    def static_low_tide_map(tick: Tick):
        hard_map = tick.map.topology.copy()
        low = tick.map.tideLevels.min
        for rows in hard_map:
            for tile in rows:
                if tile < low:
                    tile = 0
                else:
                    tile = 1
        return hard_map
        
    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            return Spawn(tick.map.ports[0])
        elif (tick.currentLocation in tick.map.ports) and (tick.map.port.index(tick.currentLocation) not in tick.visitedPortIndices):
            return Dock()
        return Sail(directions[tick.currentTick % len(directions)])
