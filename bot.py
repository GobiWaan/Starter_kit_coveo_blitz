from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions
import math
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



class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        # find nearest dock - > choose fastest route {predict tide movement -> }-> start moving 
    def _distance_between_two_position(first: tuple, second: tuple) -> float:
        #pythagorea's theorem
        return math.sqrt((abs(first[0] - second[0]))**2 + (abs(first[1] - second[1]))**2)

    def _find_nearest_dock(tick: Tick) -> directions:
        pass
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
        
        return Sail(directions[tick.currentTick % len(directions)])
