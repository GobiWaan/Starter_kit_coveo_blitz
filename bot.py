from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions

# Tick has form :
# {
#   currentTick: number;
#   totalTicks: number;
#   currentLocation: Position | null;
#   spawnLocation: Position | null;
#   map: {
#     topology: [ // Matrix of tiles, representing terrain height
    #   [8,8,7,6,5,5,5],
    #   [8,8,6,5,4,4,3]
    #   // ...;
    #  ], 
    # tideLevels: {min: int, max: int} 
#
#       max: number;
#       min: number;
#     },
#   ports: [
#      { row: 15, column: 7 },
#      { row: 8, column: 8 },
#     ],;
#   };
#   visitedPortIndices: number[];
#   tideSchedule: number[];
#   isOver: boolean;
# }



class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        
    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            return Spawn(tick.map.ports[0])
        
        return Sail(directions[tick.currentTick % len(directions)])
